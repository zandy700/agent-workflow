"""Behavior checks for full setup; only temporary homes and synthetic downloads."""
import contextlib
import hashlib
import io
import importlib.util
import json
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bootstrap
import install
import setup


def archive(entries):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as bundle:
        for name, content in entries.items():
            bundle.writestr(name, content)
    return buffer.getvalue()


class BundleTest(unittest.TestCase):
    def test_preview_never_downloads_or_changes_home(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(bootstrap, 'download') as fetch:
            home = Path(directory)
            with contextlib.redirect_stdout(io.StringIO()):
                setup.setup(home)
            self.assertEqual(list(home.iterdir()), [])
            fetch.assert_not_called()

    def test_rules_hooks_and_spaces_survive_install_and_repeat(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / "test user's home"
            for app in ('.claude', '.codex', '.cursor'):
                (home / app).mkdir(parents=True, exist_ok=True)
            for name in ('.claude/CLAUDE.md', '.codex/AGENTS.md'):
                (home / name).write_text('My custom instructions: preserve this.\n')
            custom = {'version': 1, 'other': True, 'hooks': {
                'stop': [{'command': 'keep-stop'}], 'sessionStart': [{'command': 'keep-start'}]}}
            (home / '.cursor/hooks.json').write_text(json.dumps(custom))
            with contextlib.redirect_stdout(io.StringIO()):
                install.apply(home, install.plan(home), write=True)
            for name in ('.claude/CLAUDE.md', '.codex/AGENTS.md'):
                text = (home / name).read_text()
                self.assertTrue(text.startswith('My custom instructions: preserve this.'))
                self.assertEqual(text.count(install.START), 1)
                self.assertIn('Give each independent project task its own session.', text)
            hooks = json.loads((home / '.cursor/hooks.json').read_text())
            self.assertTrue(hooks['other'])
            self.assertEqual(hooks['hooks']['stop'][0], custom['hooks']['stop'][0])
            self.assertEqual(hooks['hooks']['sessionStart'][0], custom['hooks']['sessionStart'][0])
            command = hooks['hooks']['sessionStart'][1]['command']
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            self.assertEqual(json.loads(result.stdout)['additional_context'],
                             (home / '.cursor/USER_RULES.md').read_text())
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(install.apply(home, install.plan(home), write=True), 0)
            backups = list((home / 'Scripts/agent-workflow-backups').iterdir())
            self.assertEqual(len(backups), 1)
            self.assertEqual((backups[0] / '.claude/CLAUDE.md').read_text(), 'My custom instructions: preserve this.\n')

    def test_managed_rule_update_keeps_surrounding_custom_text(self):
        old = 'before\n' + install.START + '\nold rules\n' + install.END + '\nafter\n'
        result = install.merge_rules(old, 'new rules\n')
        self.assertEqual(result, 'before\n' + install.START + '\nnew rules\n' + install.END + '\nafter\n')
        with self.assertRaises(ValueError):
            install.merge_rules(install.START + '\nunfinished', 'new rules')

    def test_unmodified_previous_release_migrates_without_duplicate_rules(self):
        body = (install.ROOT / 'payload/claude/CLAUDE.md').read_text()
        previous = '\n'.join(line for line in body.splitlines()
                             if not line.startswith('- Give each independent project task')) + '\n'
        self.assertEqual(hashlib.sha256(previous.strip().encode()).hexdigest(), install.LEGACY_RULE_HASH)
        merged = install.merge_rules(previous, body)
        self.assertEqual(merged.count('# Agent workflow'), 1)
        self.assertIn('Give each independent project task its own session.', merged)

    def test_existing_custom_icm_skill_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            skill = home / '.claude/skills/icm/SKILL.md'
            skill.parent.mkdir(parents=True)
            skill.write_text('my custom ICM skill')
            with contextlib.redirect_stdout(io.StringIO()):
                install.apply(home, install.plan(home), write=True)
            self.assertEqual(skill.read_text(), 'my custom ICM skill')

    def test_sync_failure_propagates_and_releases_lock(self):
        path = Path(__file__).resolve().parents[1] / 'payload/obsidian/sync_claude_obsidian.py'
        spec = importlib.util.spec_from_file_location('workflow_sync_test', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            with patch.object(module, 'LOCK', base / 'lock'), patch.object(module, 'LOG', base / 'sync.log'):
                with patch.object(module, 'run', side_effect=subprocess.CalledProcessError(7, ['synthetic-exporter'])):
                    with self.assertRaises(subprocess.CalledProcessError):
                        module.main(True)
                self.assertFalse((base / 'lock').exists())
                (base / 'lock').mkdir()
                with patch.object(module, 'run') as run:
                    self.assertFalse(module.main(True))
                    run.assert_not_called()

    def test_invalid_existing_settings_fail_before_installing_dependencies(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(setup, 'run') as run:
            home = Path(directory)
            (home / '.claude').mkdir()
            (home / '.claude/settings.json').write_text('{broken')
            with self.assertRaises(ValueError):
                setup.setup(home, write=True)
            run.assert_not_called()
            self.assertFalse((home / 'Scripts').exists())

    def test_windows_hook_commands_quote_executable_and_paths(self):
        with patch.object(install, 'WINDOWS', True):
            command = install.command(Path('C:/Users/A&B'), '.cursor/workflow_context.py')
            self.assertTrue(command.startswith('"'))
            self.assertIn('"C:/Users/A&B/.cursor/workflow_context.py"', command)
        with tempfile.TemporaryDirectory() as directory, patch.object(install, 'WINDOWS', True):
            plan = install.plan(Path(directory))
            hooks = json.loads(plan['.cursor/hooks.json'])
            self.assertEqual(len(hooks['hooks']['sessionStart']), 1)
            self.assertIn('Scripts/graphify-bootstrap.cmd', plan)
            self.assertIn('Scripts/markitdown.cmd', setup.wrappers(Path(directory)))

    def test_archives_reject_traversal_absolute_paths_symlinks_and_multiple_roots(self):
        bad = [archive({'root/../../escape': 'bad'}), archive({'/absolute': 'bad'}),
               archive({'root/\\escape': 'bad'}), archive({'root/C:escape': 'bad'}),
               archive({'one/a': 'a', 'two/b': 'b'})]
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as bundle:
            link = zipfile.ZipInfo('root/link')
            link.external_attr = (stat.S_IFLNK | 0o777) << 16
            bundle.writestr(link, '/tmp')
        bad.append(buffer.getvalue())
        for data in bad:
            with self.subTest(data=data[:20]), tempfile.TemporaryDirectory() as directory:
                with self.assertRaises(ValueError):
                    bootstrap.extract(data, Path(directory))
                self.assertEqual(list(Path(directory).iterdir()), [])

    def test_asset_integrity_and_existing_customizations(self):
        data = archive({'source/SKILL.md': 'skill', 'source/LICENSE': 'license'})
        spec = {'name': 'icm-architect', 'revision': 'a' * 40, 'url': 'https://example.invalid/source',
                'sha256': hashlib.sha256(data).hexdigest(), 'destination': 'Scripts/icm-architect',
                'required': ['SKILL.md', 'LICENSE']}
        with tempfile.TemporaryDirectory() as directory, patch.object(bootstrap, 'download', return_value=data) as fetch:
            home = Path(directory)
            with contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaisesRegex(ValueError, 'Checksum mismatch'):
                    setup.asset(home, {**spec, 'sha256': '0' * 64})
                self.assertFalse((home / spec['destination']).exists())
                path = setup.asset(home, spec)
                (path / 'SKILL.md').write_text('custom skill')
                fetch.reset_mock()
                self.assertEqual(setup.asset(home, spec), path)
            fetch.assert_not_called()
            self.assertEqual((path / 'SKILL.md').read_text(), 'custom skill')

    def test_failed_subprocess_reports_output_and_log(self):
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(RuntimeError, 'synthetic failure'):
                setup.run([sys.executable, '-c', "print('synthetic failure'); raise SystemExit(3)"],
                          Path(directory), 'Test step')
            self.assertIn('synthetic failure', (Path(directory) / 'Scripts/agent-workflow-setup.log').read_text())

    def test_distributable_archive_bootstraps_a_preview(self):
        root = Path(__file__).resolve().parents[1]
        entries = {f'workflow/{name}': (root / name).read_bytes()
                   for name in ('setup.py', 'install.py', 'bootstrap.py', 'bundle.json')}
        entries.update({f'workflow/{p.relative_to(root).as_posix()}': p.read_bytes()
                        for p in (root / 'payload').rglob('*') if p.is_file() and '__pycache__' not in p.parts})
        with tempfile.TemporaryDirectory() as directory, patch.object(bootstrap, 'download', return_value=archive(entries)):
            # Keep the real subprocess: this checks the archive can run independently of this checkout.
            with patch.object(bootstrap.subprocess, 'run', wraps=subprocess.run) as run:
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(bootstrap.main(['--preview', '--home', directory]), 0)
                self.assertNotIn('--install', run.call_args.args[0])
            self.assertEqual(list(Path(directory).iterdir()), [])


if __name__ == '__main__':
    unittest.main()
