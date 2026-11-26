# tangseng

悟空非空也的 Claude Code 自媒体创作插件，提供公众号写作、视频脚本和 HTML 幻灯片制作技能。

## 安装

在 Claude Code 中运行：

```text
/plugin marketplace add wukongnotnull/tangseng
/plugin install tangseng@tangseng
```

安装后，可以在 Claude Code 中输入 `/tangseng:wk-gzh-writer` 等命令，也可以直接说明创作需求。

## 技能

| 技能 | 用途 |
| --- | --- |
| `wk-gzh-writer` | 撰写公众号长文 |
| `wk-gzh-title` | 生成公众号标题 |
| `wk-gzh-summary` | 生成公众号文章摘要和标签 |
| `wk-gzh-cover` | 生成封面图提示词 |
| `wk-gzh-illustrations` | 生成文章配图提示词 |
| `wk-gzh-refine` | 提炼公众号文章中的事实和观点 |
| `wk-video-script` | 撰写视频脚本 |
| `wk-html-slides-amber-classified` | 制作琥珀色风格的 HTML 幻灯片 |

## 本地开发

在仓库根目录执行以下命令，分别验证插件和市场清单：

```bash
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .claude-plugin/marketplace.json
```

在 Claude Code 中试用本地版本：

```bash
claude --plugin-dir .
```

导出幻灯片 PNG 需要 Python、Playwright 和 Chromium。具体用法见[幻灯片技能说明](skills/wk-html-slides-amber-classified/SKILL.md)。
