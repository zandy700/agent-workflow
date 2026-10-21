<h1 align="center">智能体工作流</h1>

<p align="center">
  <a href="#quickstart"><img src="https://img.shields.io/badge/%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B-1_%E6%9D%A1%E5%91%BD%E4%BB%A4-blue?style=for-the-badge" alt="快速开始"></a>
  <a href="#setup"><img src="https://img.shields.io/badge/%E5%AE%89%E8%A3%85%E6%8C%87%E5%8D%97-%E5%88%86%E6%AD%A5%E8%AF%B4%E6%98%8E-7c5cff?style=for-the-badge" alt="安装指南"></a>
  <a href="#results"><img src="https://img.shields.io/badge/%E6%B5%8B%E8%AF%95%E7%BB%93%E6%9E%9C-Measured-blue?style=for-the-badge" alt="测试结果"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/English-README-red?style=for-the-badge" alt="English README"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/platform-macOS_%7C_Windows-lightgrey" alt="macOS 和 Windows">
  <img src="https://img.shields.io/badge/Claude_Code-supported-D97757" alt="Claude Code">
  <img src="https://img.shields.io/badge/Codex-supported-412991" alt="Codex">
  <img src="https://img.shields.io/badge/Cursor-supported-000000" alt="Cursor">
  <img src="https://img.shields.io/badge/notes-Obsidian-7C3AED?logo=obsidian&logoColor=white" alt="Obsidian">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-yellow" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/background_hooks-0_AI_tokens-success" alt="后台钩子不消耗 AI token">
</p>

<h3 align="center">聊天一结束，你的 AI 智能体就什么都忘了。<br>这套工作流给它一本笔记本，再加一套行为准则。</h3>

<p align="center">
  <a href="README.md">English</a> · <strong>简体中文</strong>
</p>

一套现成的 **Claude Code、Codex 和 Cursor** 配置，支持 **Mac 和 Windows**：让智能体每次加载的指令保持精简，引导它做小改动、如实汇报，并把每次聊天保存到 Obsidian，下一次聊天就能接着上次继续。

<a id="contents"></a>
## 🧭 目录

| **开始** | **使用** | **参考** |
|---|---|---|
| [一条命令安装](#quickstart) | [日常使用](#daily) | [设置选项](docs/setup-options.md) |
| [安装内容](#setup) | [内置工具](#extras) | [仓库结构](#repo) |
| [测试结果](#results) | [ICM](#icm) | [检查](#checks) |
| [解决的问题](#problems) | [问题排查](#troubleshooting) | [致谢](#credits) |

---

<a id="problems"></a>
## 🤔 解决的问题

| 没有这套工作流 | 有了这套工作流 |
|---|---|
| ❌ 每个新聊天都从零开始，你得重新解释项目。 | ✅ 智能体读一条 5 到 15 行的交接笔记，接着干。 |
| ❌ 聊天越长越慢越贵，因为整段历史都会被重新发送。 | ✅ 精简的规则和简短的回复让每条消息都很轻。 |
| ❌ 什么都没运行，智能体却说测试通过了。 | ✅ 智能体必须汇报验证过什么，并标出没验证的部分。 |
| ❌ 智能体加了你没要的层级和库。 | ✅ 核心规则要求完成任务所需的最小改动。 |
| ❌ 当初为什么这样决定，埋在某个旧聊天里。 | ✅ 每次聊天都在 Obsidian 里，直接问*“我们为什么这样做 X？”* |
| ❌ 为了找一个函数，智能体把整个文件夹都读一遍。 | ✅ 可选的代码地图（Graphify）让它直接查找。 |
| ❌ 每个应用都要单独配置、单独写规则。 | ✅ Claude Code、Codex 和 Cursor 遵守同一套规则。 |
| ❌ 手动保存聊天很容易忘。 | ✅ 每条消息后在后台自动保存聊天，不消耗任何 AI token。 |

<a id="results"></a>
## 📊 测试结果

最初的 4 步缓存测试统计的是**字符数**，不是 token：回复约短了 49%。这不能证明总 token 用量降低。

后续测试读取 Claude Code 的真实用量计数：364 行 Python 订单程序、连续 5 条编程提示、每种配置各 3 次 Haiku 会话。旧版完整工作流的**总 token 用量高了 73.8%**（每次会话 1,604,721 比 923,168），两组最终均通过 **9/9 项检查**。增加的主要是缓存输入。按标价估算的成本增加 24.4%，不等于订阅实际账单。

**新配置复测：** 总 token 平均减少 4.5%，两组最终都通过 9/9 项检查；估算的 API 成本反而增加 2.5%。每组仅测试了 3 次、任务规模较小、结果波动明显，不能推广为通用节省比例。

新默认配置精简常驻规则、按需读取详细说明、将 Ponytail 改为主动开启，并在能直接读清的小任务中跳过 Graphify 初始化。技能与聊天同步仍可使用。方法与新结果见[基准测试说明](docs/token-benchmark.md)。是否节省取决于任务，不承诺通用节省比例。

<sub>[↑ 回到顶部](#contents)</sub>

---

<a id="quickstart"></a>
## 🚀 一条命令安装

需要 **Python 3.10–3.14**、网络连接，以及至少一个已安装并登录的编程智能体应用。不用手动克隆仓库、安装 pip 包、创建技能链接，也不用往 Cursor 粘贴规则。

**Mac：粘贴到终端：**

```bash
python3 -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/zandy700/agent-workflow/main/bootstrap.py').read())"
```

**Windows：粘贴到 PowerShell：**

```powershell
py -3 -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/zandy700/agent-workflow/main/bootstrap.py').read())"
```

没有 Python 时，先从 [python.org](https://www.python.org/downloads/) 安装。Windows 没有 Python 启动器时，可以把 `py -3` 换成 `python`。

**已经下载仓库？** 运行 `python3 setup.py --install`（Windows：`py -3 setup.py --install`）。去掉 `--install` 就是预览，不修改文件、不联网。在线引导脚本也支持 `--preview`。

<a id="setup"></a>
## 这条命令会做什么

| 内容 | 自动完成的设置 |
|---|---|
| 统一规则 | 将托管规则块写入 Claude Code 和 Codex 的全局指令；Cursor 通过会话启动钩子加载同样的规则。 |
| 聊天记录 | 安装本地聊天同步钩子，并首次同步已有的 Claude Code、Codex、Cursor 记录。 |
| Python 工具 | 在独立环境中安装固定版本的聊天导出工具、Graphify 和 MarkItDown，不混入系统 Python 包。 |
| ICM | 下载并校验模板和 `icm-architect`，将技能连接到三个应用。 |
| 笔记库 | 创建 `~/Obsidian Sync/ObsidianVault` 和 Home 笔记。没有 Obsidian 也可以保存笔记；它只是查看工具。 |

再次运行同一命令即可修复或更新托管设置。保留自定义全局指令、其他钩子、笔记和插件偏好；替换的文件备份到 `~/Scripts/agent-workflow-backups/`。已有的 ICM 文件夹和 architect 技能（包括本地修改）也会保留。

<a id="app-claude"></a>
<a id="app-codex"></a>
<a id="app-cursor"></a>
### 在应用内完成

- 开始一个**新聊天**以加载规则。应用提示时批准工作流钩子；Codex 中用 `/hooks` 查看。安装器不会代替你授予信任。
- 想查看笔记时，在 Obsidian 选择 **Open folder as vault**，打开 `~/Obsidian Sync/ObsidianVault`。文件夹名称不表示需要付费的 Obsidian Sync 服务。

Cursor 通过[官方 sessionStart 钩子](https://cursor.com/docs/hooks#sessionstart)自动加载规则。如果以前粘贴过工作流规则，可以从 User Rules 中删除旧副本，避免重复。本安装面向本地应用，云端智能体需要自己的环境。

Ponytail 和夜间定时同步仍为可选功能，见[设置选项](docs/setup-options.md)。聊天钩子已经会在智能体完成回复后同步。

**Windows：** 已在 macOS 上测试生成的配置，尚未在真实 Windows 电脑上验证完整安装。

---

<a id="daily"></a>
## 💬 日常怎么用

大多数时候你只需要跟智能体对话（用中文说就行）：

| 什么时候 | 对智能体说 |
|---|---|
| 出现不需要当前聊天上下文的独立任务 | 为它开启新聊天，即使属于同一项目。 |
| 关闭一段很长的聊天之前 | *“为这个项目写交接笔记。”* |
| 在同一个项目开新聊天时 | *“读一下交接笔记，然后继续。”* |
| 需要找以前的决定 | *“查一下笔记：我们为什么这样做 X？”* |
| 你在几个可行方案中做了选择 | *“为这个决定写一份 ADR（架构决策记录）。”* |
| 学到了值得保留的经验 | *“保存这个。”* |
| 想为某个流程搭一套分步结构，或给杂乱的文件夹画张地图 | *“/icm-architect map this repo.”*（需要先装 [ICM](#extras)） |

交接笔记是 5 到 15 行的摘要：做完了什么、哪里有问题、下一步做什么。智能体只搜索你问到的内容，从不把整个仓库都加载进来。

**Ponytail 设置**（在聊天框输入）：

| 命令 | 作用 |
|---|---|
| `/ponytail lite` | 宽松一些 |
| `/ponytail full` | 在当前聊天开启完整指导 |
| `/ponytail ultra` | 最严格 |
| `stop ponytail` | 关闭 |

如需彻底卸载，请看 [Ponytail 的卸载步骤](https://github.com/DietrichGebert/ponytail#uninstall)。

<a id="extras"></a>
## 🧩 内置工具

完整安装会准备好这些工具，只在需要时运行。安装 Graphify 不会自动创建项目地图。

- **Graphify：** 需要代码地图时运行 `~/Scripts/graphify-bootstrap /path/to/project`。Windows：`& "$HOME/Scripts/graphify-bootstrap.cmd" C:\path\to\project`。每个仓库保留独立的图谱和笔记命名空间。
- **MarkItDown：** 使用 `~/Scripts/markitdown document.pdf`；Windows：`& "$HOME/Scripts/markitdown.cmd" document.pdf`。

<a id="icm"></a>
### ICM

`/icm` 提供方法和可复用工作区，`/icm-architect` 设计新结构或映射已有文件夹。新聊天中输入 *“/icm-architect map this repo”* 即可。地图仍需你批准，新工作区放在自己的项目中。

安装器下载固定版本到 `~/Scripts/icm` 和 `~/Scripts/icm-architect`，校验 SHA-256，并把 architect 技能复制到三个应用。已有文件夹和技能会保留。版本和来源见 [bundle.json](bundle.json)。

ICM 由 RinDig 创建，`/icm` 集成和工作流路由由 [zandy700](https://github.com/zandy700) 编写。

---

<a id="troubleshooting"></a>
## 🩺 问题排查

| 问题 | 怎么办 |
|---|---|
| Obsidian 里没有聊天记录 | 查看日志最后几行。Mac：`tail -20 "$HOME/Obsidian Sync/claude_obsidian_sync.log"` · Windows：`Get-Content "$HOME/Obsidian Sync/claude_obsidian_sync.log" -Tail 20` |
| 缺少 Claude Code 的聊天 | 查看 `~/Scripts/agent-workflow-setup.log`，然后重新运行安装命令。 |
| 缺少 Codex 的聊天 | 你在 `/hooks` 里批准钩子了吗？见 [Codex](#app-codex) |
| 智能体不遵守规则 | 开一个新聊天；规则只在聊天开始时加载 |
| 每晚同步没有运行 | Mac：`launchctl print "gui/$(id -u)/local.agent-workflow.obsidian-sync"` · Windows：`Get-ScheduledTask agent-workflow-obsidian-sync` |
| Windows：输入 `python` 却打开了 Microsoft Store | 从 [python.org](https://www.python.org/downloads/) 重新安装 Python 并勾选“Add python.exe to PATH”，然后重新运行安装程序 |
| 在 Windows 上移动或升级了 Python | 重新运行完整安装命令，检查运行环境并重新生成钩子 |

<sub>[↑ 回到顶部](#contents)</sub>

---

<a id="repo"></a>
## 📁 仓库里有什么

```
agent-workflow/
├── README.md            本说明（English）
├── README.zh-CN.md      本说明（简体中文）
├── LICENSE              MIT 许可证
├── bootstrap.py         下载并启动安装
├── setup.py             完整安装：工具、ICM、钩子、同步
├── bundle.json          固定工具版本和 ICM 校验值
├── install.py           核心文件安装器
├── payload/             安装程序要复制的所有文件
│   ├── claude/          Claude Code 的规则
│   ├── codex/           Codex 的规则
│   ├── cursor/          规则和自动会话启动加载器
│   ├── obsidian/        保存聊天和整理仓库的脚本
│   ├── skills/          /icm 技能
│   └── scripts/         按需读取的参考文件、文档扫描脚本
└── docs/                详细指南和本页用到的图片
```

<a id="reading"></a>
## 📚 延伸阅读

以下文档目前只有英文版：

- [How it works](docs/how-it-works.md)：用图解说明什么时候加载什么、在哪里节省 token
- [Using the Obsidian notes](docs/obsidian-notes-guide.md)：交接笔记、决策记录、经验沉淀、参考摘要

<a id="checks"></a>
## 🧪 检查（无需调用 AI）

下面的命令检查脚本有没有错误，并把安装程序装到一个临时文件夹里试运行，全程不调用任何 AI 模型：

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile bootstrap.py setup.py install.py payload/cursor/*.py payload/obsidian/*.py payload/scripts/*.py
```

测试覆盖生成的 Windows 配置、重复安装、自定义设置、下载校验和引导预览；这不等于在真实 Windows 电脑上测试过。

<a id="credits"></a>
## 🙏 致谢

本工作流从上游来源安装这些工具。ICM 快照保留上游许可证，工具版本和快照校验值记录在 bundle 清单中：

- [Ponytail](https://github.com/DietrichGebert/ponytail)，作者 DietrichGebert（MIT 许可证）
- [Obsidian](https://obsidian.md)
- [Interpretable Context Methodology](https://github.com/RinDig/Interpretable-Context-Methodology) 和 [icm-architect](https://github.com/RinDig/icm-architect)，作者 RinDig（MIT 许可证）
- [Graphify](https://pypi.org/project/graphifyy/)、[MarkItDown](https://github.com/microsoft/markitdown)、[claude-conversation-extractor](https://pypi.org/project/claude-conversation-extractor/)

<a id="license"></a>
## 📄 许可证

[MIT](LICENSE)。可以免费使用、修改和分享（包括商业用途），只需保留版权声明。按“原样”提供，不附带任何担保。

<p align="center"><sub><a href="#contents">↑ 回到顶部</a></sub></p>
