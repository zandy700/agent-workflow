"""Installer regression checks; no model calls or live settings writes."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import install


class InstallTest(unittest.TestCase):
    def test_preview_install_and_repeat_preserve_unrelated_hooks(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            settings = home / '.claude/settings.json'
            settings.parent.mkdir()
            original = {'hooks': {'Stop': [{'hooks': [{'type': 'command', 'command': 'keep-my-hook'}]}]},
                        'enabledPlugins': {'unrelated@example': True}}
            settings.write_text(json.dumps(original))
            command = [sys.executable, str(install.ROOT / 'install.py'), '--home', str(home)]
            subprocess.run(command, check=True, capture_output=True)
            self.assertEqual(json.loads(settings.read_text()), original)
            self.assertFalse((home / '.config/ponytail/config.json').exists())
            subprocess.run(command + ['--install'], check=True, capture_output=True)
            after = settings.read_bytes()
            actual = json.loads(after)
            self.assertEqual(actual['enabledPlugins'], original['enabledPlugins'])
            self.assertEqual(actual['hooks']['Stop'][0], original['hooks']['Stop'][0])
            self.assertEqual(json.loads((home / '.config/ponytail/config.json').read_text()), {'defaultMode': 'off'})
            backups = list((home / 'Scripts/agent-workflow-backups').iterdir())
            self.assertEqual(json.loads((backups[0] / '.claude/settings.json').read_text()), original)
            second = subprocess.run(command + ['--install'], check=True, capture_output=True, text=True)
            self.assertIn('Already installed', second.stdout)
            self.assertEqual(settings.read_bytes(), after)

    def test_ponytail_preserves_explicit_mode_and_other_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            cfg = home / '.config/ponytail/config.json'
            cfg.parent.mkdir(parents=True)
            cfg.write_text('{"defaultMode":"lite","hideStatus":true}')
            self.assertNotIn('.config/ponytail/config.json', install.plan(home))
            cfg.write_text('{"hideStatus":true}')
            self.assertEqual(json.loads(install.plan(home)['.config/ponytail/config.json']),
                             {'hideStatus': True, 'defaultMode': 'off'})

    def test_windows_ponytail_location(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(install, 'WINDOWS', True):
            plan = install.plan(Path(directory))
            self.assertEqual(json.loads(plan['AppData/Roaming/ponytail/config.json'])['defaultMode'], 'off')

    def test_external_xdg_config_is_not_written(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as external:
            home = Path(directory).resolve()
            with patch.object(install.Path, 'home', return_value=home), patch.dict('os.environ', {'XDG_CONFIG_HOME': external}):
                plan = install.plan(home)
            self.assertFalse(any('ponytail' in key for key in plan))
            self.assertEqual(list(Path(external).iterdir()), [])


if __name__ == '__main__':
    unittest.main()
