# 智能体工作流

[English](README.md) · **简体中文**

为 **Claude Code、Codex 和 Cursor** 提供统一编程规则、项目交接笔记和本地聊天记录。

<a id="quickstart"></a>
## 安装

需要 **Python 3.10–3.14**、网络连接，以及一个已安装并登录的编程智能体应用。没有 Python 时，先[下载安装](https://www.python.org/downloads/)。

**Mac — 终端：**

```bash
python3 -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/zandy700/agent-workflow/main/bootstrap.py').read())"
```

**Windows — PowerShell：**

```powershell
py -3 -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/zandy700/agent-workflow/main/bootstrap.py').read())"
```

Windows 没有启动器时，可把 `py -3` 换成 `python`。已克隆仓库？运行 `python3 setup.py --install`；去掉 `--install` 即可预览。

**安装完成后：**

1. 开一个新聊天。应用提示时批准工作流钩子；Codex 中用 `/hooks` 查看。Cursor 通过会话启动钩子自动加载规则。
2. 想查看笔记时，在 Obsidian 中把 `~/Obsidian Sync/ObsidianVault` 打开为笔记库。Obsidian 为可选工具，不需要付费 Sync 服务。

再次运行同一命令即可更新。保留自定义指令、其他钩子、笔记和已有的 ICM 文件夹；替换的文件会备份。见[设置与恢复说明](docs/setup-options.md)。

**Windows：** 已在 macOS 上测试生成的配置，尚未验证真实 Windows 电脑上的完整安装。本设置面向本地编程应用。

<a id="setup"></a>
<a id="extras"></a>
<a id="icm"></a>
## 包含什么

| 内容 | 作用 |
|---|---|
| 统一规则 | 保持改动聚焦、如实汇报验证结果，并为独立任务开启新会话。 |
| 聊天同步与交接笔记 | 将本地聊天记录保存到 Markdown 笔记库，在新聊天中接续项目进度。 |
| ICM + icm-architect | 提供可复用工作流、设计项目结构、映射文件夹。 |
| Graphify + MarkItDown | 分析代码结构、转换文档；工具安装在独立 Python 环境中。 |

工具按需运行，创建项目地图需先获批准。Ponytail 和夜间同步为可选功能，见[设置选项](docs/setup-options.md)。

<a id="daily"></a>
## 日常使用

| 什么时候 | 对智能体说 |
|---|---|
| 关闭聊天前 | “为这个项目写交接笔记。” |
| 在新聊天中继续 | “读一下交接笔记，然后继续。” |
| 查找以前的决定 | “查一下笔记：我们为什么这样做 X？” |
| 整理项目结构 | “/icm-architect map this repo.” |

不需要当前聊天上下文的任务，应开启独立会话，即使属于同一仓库。

<a id="results"></a>
<a id="checks"></a>
## 详细说明

- [设置选项、问题排查与检查](docs/setup-options.md)
- [工作原理](docs/how-it-works.md) · [如何使用笔记](docs/obsidian-notes-guide.md)
- [基准测试结果与局限](docs/token-benchmark.md)：不保证节省 token 或费用。
- [固定版本与下载校验值](bundle.json)

## 致谢与许可证

使用了 RinDig 的 [ICM](https://github.com/RinDig/Interpretable-Context-Methodology) 和 [icm-architect](https://github.com/RinDig/icm-architect)，以及 [Graphify](https://pypi.org/project/graphifyy/)、[MarkItDown](https://github.com/microsoft/markitdown)、[claude-conversation-extractor](https://pypi.org/project/claude-conversation-extractor/)。可选工具：[Obsidian](https://obsidian.md)、[Ponytail](https://github.com/DietrichGebert/ponytail)。

[MIT 许可证](LICENSE)。上游工具保留各自的许可证。
