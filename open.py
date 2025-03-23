import json
from requests import Session
from util import parse_line, parse_md, save_lines_to_file

session = Session()

session.headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
}

cvid = input("请输入cvid:")
response = session.get(f"https://api.bilibili.com/x/note/publish/info?cvid={cvid}")
assert response.ok, "抓取失败，请检查cvid是否正确"
response = response.json()
content_list = json.loads(response["data"]["content"])
md = parse_md(content_list, session)
lines = [parse_line(line) for line in md.split("\n")]
save_lines_to_file(lines)
print("done")
