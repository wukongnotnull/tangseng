---
name: tangseng
description: 为公众号和视频创作内容，并审核笔记是否推广其他平台。用来撰写公众号长文、起标题、生成摘要和标签、提炼文章事实和观点、制作封面和正文配图提示词、撰写视频脚本、制作琥珀色风格的 HTML 幻灯片，以及检查错别字和辨析病句。
---

# tangseng

根据用户要求打开对应指南，并按里面的工作流程处理素材。用户同时要求多个产物时，依次使用对应的指南。用户提供了具体的功能名称时，直接使用该功能。

| 用户需求 | 功能指南 |
| --- | --- |
| 撰写、续写或扩写公众号长文 | [wk-gzh-writer](references/wk-gzh-writer/guide.md) |
| 拟定、评估或优化公众号标题 | [wk-gzh-title](references/wk-gzh-title/guide.md) |
| 写公众号摘要、引言或标签 | [wk-gzh-summary](references/wk-gzh-summary/guide.md) |
| 提取事实和数据，区分事实与作者观点 | [wk-gzh-refine](references/wk-gzh-refine/guide.md) |
| 生成公众号封面图提示词 | [wk-gzh-cover](references/wk-gzh-cover/guide.md) |
| 生成与文章段落对应的正文配图提示词 | [wk-gzh-illustrations](references/wk-gzh-illustrations/guide.md) |
| 把素材改编成视频脚本和分镜 | [wk-video-script](references/wk-video-script/guide.md) |
| 把演讲稿、PPT 文案或大纲做成 HTML 幻灯片 | [wk-html-slides-amber-classified](references/wk-html-slides-amber-classified/guide.md) |
| 校对中文、检查错别字、辨析病句或讲解中文语法 | [check-chinese-grammar](references/check-chinese-grammar/guide.md) |
| 审核笔记文案或配图中的站外推广和引流 | [wk-note-platform-review](references/wk-note-platform-review/guide.md) |

指南中的相对路径以该指南所在的目录为准。按需读取引用的资料、示例和模板。

## 在 ChatGPT 中交付

- 直接处理用户粘贴的文字或上传的附件。链接内容无法读取时，请用户粘贴相关段落或上传文件。
- 指南提到 Write 工具或要求把结果写到素材旁边时，改用当前对话的文件生成功能，保留指南约定的文件名，例如 `title.md`、`summary.md` 和 `illustrations.md`，并提供下载链接。当前对话无法生成附件时，直接给出完整内容和建议文件名。
- 封面和正文配图指南交付绘图提示词。用户明确要求出图时，可用当前对话支持的图像生成工具。
- HTML 幻灯片以 [DeepSeek 示例](references/wk-html-slides-amber-classified/templates/deepseek-demo.html) 或 [Claude Mythos 示例](references/wk-html-slides-amber-classified/templates/claude-mythos-demo.html) 为样式参考，生成完整的 `index.html`。只有用户要求 PNG 且运行环境具备 Python、Playwright 和 Chromium 时，才用[截图脚本](references/wk-html-slides-amber-classified/scripts/capture_slides.py)导出。环境缺少浏览器时先交付 HTML。
