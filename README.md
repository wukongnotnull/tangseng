# tangseng

悟空非空也的自媒体创作工具，提供公众号写作、视频脚本和 HTML 幻灯片制作技能。支持 Codex、Claude Code 和提供 Skills 功能的 ChatGPT 账号。

## 安装

### Codex

在已下载的仓库根目录执行：

```bash
codex plugin marketplace add .
codex plugin add tangseng@tangseng
codex plugin list --marketplace tangseng
```

打开新的 Codex 会话，输入 `$` 打开技能选择器。比如，可以选择 `tangseng:wk-gzh-title`，附上文章内容，请 Codex 拟 5 个公众号标题。

### ChatGPT

在仓库根目录生成安装包：

```bash
python3 scripts/build-chatgpt-skill.py
```

打开 ChatGPT 的个人菜单，进入 **Skills**，选择上传技能，并上传生成的 `dist/tangseng.zip`。安装一次即可使用下列 10 项功能。开始新对话后，可以输入「用 tangseng 给这篇公众号文章拟 5 个标题」，并附上文章内容。

ChatGPT 会在支持文件生成的对话中提供 Markdown 或 HTML 下载链接。没有文件生成功能时，可从对话复制完整内容。PNG 导出另需 Playwright 和 Chromium，可以下载 HTML 后在本地导出。

### Claude Code

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
| `check-chinese-grammar` | 检查错别字、辨析病句和讲解现代汉语语法 |
| `wk-publish-review` | 审核笔记、短视频和广告素材的发布风险 |

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
