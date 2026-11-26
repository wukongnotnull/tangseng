---
name: wk-creating-social-covers
description: Generate finished video thumbnails, WeChat Official Account article covers, or X Articles header images for the creator's content, especially when an exact headline, creator portrait, or platform ratio matters.
---

# Creating Social Covers

Create a readable creator cover from a topic or headline, using the platform surface and ratio the user intends. Use the built-in `imagegen` tool by default.

## Workflow

1. **Resolve the surface and copy.** Preserve a supplied title or cover theme verbatim. Keep requested line breaks and emphasis (for example, highlighting “mods” or “骗局”). Condense only when the user asks for shorter copy. For X Articles requests, create only the article header; do not generate an X profile banner.
2. **Use the creator portrait.** Reference [`assets/character-reference.png`](assets/character-reference.png), relative to this guide, by default. Preserve the light comic style, visible face, short dark hair, thin silver glasses, and white crew-neck shirt. Adjust scale and placement for the cover. If the user supplies or requests a different portrait, use it instead. Avoid official logos, product icons, watermarks, extra slogans, and clutter.
3. **Choose the output set and size.** Make one cover for an article/header request unless the user asks for variants. For video-cover requests, make four independently composed versions by default. When the user specifies ratios, make only those versions.

   | Surface | Ratio and target pixels |
   |---|---|
   | Video cover | 16:9 — 1920×1080; 4:3 — 1600×1200; 3:4 — 1536×2048; 9:16 — 1080×1920 |
   | WeChat Official Account lead cover | 2.35:1 — 900×383 |
   | X Articles header | 5:2 — 1500×600 |

   Treat 5:2 as the confirmed ratio for X Articles headers. Check current authoritative guidance for unfamiliar platforms. Center the focal subject by default on article/header covers for this creator; the user has requested this layout. Follow any newer placement instruction.
4. **Compose for legibility.** Keep the focal subject and all title glyphs inside safe margins. Prefer a simple scene. Keep the title separate from the avatar’s face. Reflow each requested aspect ratio rather than squeezing text or letting a crop cut it off.
5. **Export and inspect.** The user has authorized cropping and resampling to meet requested dimensions. Use them only to reach the chosen target size, keeping the complete title and the portrait’s face visible. Inspect the final image and verify its actual pixel dimensions; do not rely on the filename.
6. **Save and report.** Save final assets in the current workspace’s `outputs/` folder and copy them to `/Users/wukong/Downloads/`, matching the creator’s repeated preference. Do not overwrite existing files; add a version suffix. Show the cover inline and link the saved file(s).

## Common mistakes

- Generating an X profile banner as part of an X Articles cover request.
- Omitting a ratio from the default video-cover set.
- Changing, abbreviating, or dropping words from the provided title.
- Claiming target dimensions without checking the exported file.
