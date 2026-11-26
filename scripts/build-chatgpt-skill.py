#!/usr/bin/env python3
"""Build the ChatGPT Skill ZIP from the shared tangseng skill sources."""

import argparse
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
SUPPORT_FILES = {
    "assets": {".png"},
    "references": {".md"},
    "templates": {".html"},
    "scripts": {".py"},
}


def guide_contents(source: Path) -> str:
    opening, marker, rest = source.read_text(encoding="utf-8").partition("\n")
    _, closing, body = rest.partition("\n---\n")
    if opening != "---" or not marker or not closing or not body.strip():
        raise ValueError(f"Expected skill frontmatter and a guide in {source}")
    return body.lstrip("\n")


def build_archive(output: Path) -> None:
    manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    entry = (ROOT / "chatgpt/SKILL.md").read_bytes()
    files = {"tangseng/SKILL.md": entry}

    for skill_path in manifest["skills"]:
        skill = ROOT / skill_path
        package_path = f"tangseng/references/{skill.name}"
        guide_path = f"{package_path}/guide.md"
        if guide_path.removeprefix("tangseng/").encode() not in entry:
            raise ValueError(f"Add {skill.name} to chatgpt/SKILL.md before packaging it")
        files[guide_path] = guide_contents(skill / "SKILL.md").encode("utf-8")

        for directory, extensions in SUPPORT_FILES.items():
            for path in (skill / directory).rglob("*"):
                if path.is_file() and path.suffix in extensions:
                    files[f"{package_path}/{path.relative_to(skill).as_posix()}"] = path.read_bytes()
        for filename in ("README.md", "LICENSE.txt"):
            path = skill / filename
            if path.is_file():
                files[f"{package_path}/{filename}"] = path.read_bytes()

    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for name, content in sorted(files.items()):
            archive.writestr(name, content)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist/tangseng.zip")
    args = parser.parse_args()
    build_archive(args.output)
    print(args.output.resolve())


if __name__ == "__main__":
    main()
