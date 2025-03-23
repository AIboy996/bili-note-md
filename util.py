import os
import re
from requests import Session


def save_img(url: str, filename: str, session: Session):
    if not os.path.exists("assets"):
        os.mkdir("assets")
    if not os.path.exists(f"assets/{filename}.png"):
        with open(f"assets/{filename}.png", "wb") as f:
            f.write(session.get(url).content)
        print(f"Downloaded {filename}")


def parse_line(line: str) -> str:
    if line.endswith("<ul-0>"):
        return f"- {line[:-6]}"
    elif line.endswith("<ul-1>"):
        return f"    - {line[:-6]}"
    elif line.endswith("<ul-2>"):
        return f"        - {line[:-6]}"
    else:
        return line


def parse_md(content_list: list, session: Session) -> str:
    md = ""
    for line in content_list:
        content = line["insert"]
        if isinstance(content, dict):
            if "imageUpload" in content:
                img_url = "https:" + content["imageUpload"]["url"]
                img_id = content["imageUpload"]["id"]
                save_img(img_url, img_id, session)
                md += f"\n![{img_id}](assets/{img_id}.png)\n"
        elif isinstance(content, str):
            arrtibutes = line.get("attributes", {})
            match arrtibutes:
                case {"bold": True}:
                    content = f"**{content}**"
                case {"indent": 2, "list": "bullet"}:
                    content = f"<ul-2>{content}"
                case {"indent": 1, "list": "bullet"}:
                    content = f"<ul-1>{content}"
                case {"list": "bullet"}:
                    content = f"<ul-0>{content}"
            md += content
    return md


def save_lines_to_file(lines: list):
    f = None
    for line in lines:
        # for each h1, open a new markdown file
        if re.match(r"# \S+", line):
            if f is not None:
                f.close()
            f = open(f"./{line[2:]}.md", "w+", encoding="utf8")
        else:
            if f is None:
                f = open("./default.md", "w+", encoding="utf8")
        f.write(line + "\n")
    f.close()
