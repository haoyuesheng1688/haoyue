# haoyue · SolidWorks 工程知识库与 Skills

来自 solidworks2 项目的可复用工作流、案例知识与技能依赖，整理于 2026-09-26。

## 在其他项目使用

需要 Git 和 Python 3.10+。在任意工作目录运行：

```powershell
git clone https://github.com/haoyuesheng1688/haoyue.git
python haoyue/tools/install.py --project "D:/your-project"
```

安装器将两套技能及知识库复制到目标项目 `.agents/skills/`，默认拒绝覆盖不同内容；相同内容可重复安装。不会修改目标 AGENTS.md。个人级共享可用 `--skills-dir "$env:USERPROFILE/.agents/skills"`。

在目标项目的新 Codex 任务中输入：

> 使用 $solidworks-drawing-model-loop，先只读确认当前 SolidWorks 实例及文档，再按知识库执行小案例验证。

独立零部件及面板交付可使用 `$solidworks-standalone-parametric-delivery`。

安装目录依据 [官方技能文档](https://learn.chatgpt.com/docs/build-skills)；也可通过 `--skills-dir` 指定客户端实际支持的技能目录。安装成功证明文件与依赖完整，实际技能发现取决于客户端刷新；CAD 操作仍需要 Windows、SolidWorks 与 pywin32。

## 内容入口

- [知识索引](INDEX.md)：按主题定位笔记和案例。
- `skills/`：主技能、独立交付技能、完整参考文档和只读探测脚本。
- `knowledge/`：Basic Memory Markdown 原文，可独立阅读或导入自己的知识库。
- `cases/`：五个项目案例的说明、参数、验证报告及复盘；revisions 是历史版本。
- [迁移说明](docs/migration.md)：历史路径、验证边界和内容范围。
- `manifest.json`：逐文件 SHA-256 与来源。

## 跨项目边界

历史案例中的绝对路径、PID、尺寸、材料、源模型及验收结果仅是案例记录。新项目必须重新绑定目标并执行几何回读。仓库不包含原 CAD、STEP、运行环境、凭据或完整对话日志；报告引用的原始 JSON/图片/CAD 证据仍在原项目，不能据文档声称在新项目已复现。

安装器附带知识库到每套技能的 `knowledge/` 中，可按文件名搜索。历史机器路径通过 INDEX 查找同名知识笔记；不得直接执行历史会话脚本。
