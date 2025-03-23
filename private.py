import json
import os
import sys
from requests import Session
from util import parse_line, parse_md, save_lines_to_file

session = Session()

if os.path.exists("./headers.json"):
    with open("./headers.json", "r") as f:
        session.headers = json.load(f)
else:
    session.headers = {
        "Cookie": input("cookie:"),
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    }

note_id = input("note_id:")
oid = input("oid:")
response = session.get(
    f"https://api.bilibili.com/x/note/info?oid={oid}&note_id={note_id}"
)
assert response.ok, "抓取失败，请检查cookie和note_id是否正确"

with open("./headers.json", "w+") as f:
    json.dump(session.headers, f, indent=4)

response = response.json()
if response["message"] == "账号未登录":
    print("登录已经失效，请使用新的cookie")
    sys.exit(1)
content_list = json.loads(response["data"]["content"])
md = parse_md(content_list, session)
lines = [parse_line(line) for line in md.split("\n")]
save_lines_to_file(lines)
print("done")
