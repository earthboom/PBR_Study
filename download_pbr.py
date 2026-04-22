import requests, os, time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

BASE = "https://pbr-book.org/4ed/"
FOLDER = "pbr4ed"
visited = set()
session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0"


def local_path(url):
    path = urlparse(url).path.lstrip("/")
    if not path or path.endswith("/"):
        path = path + "index.html"
    local = os.path.join(FOLDER, path)
    if not os.path.splitext(local)[1]:
        local += ".html"
    return local


def download(url):
    if url in visited or not url.startswith(BASE):
        return
    visited.add(url)

    local = local_path(url)
    os.makedirs(os.path.dirname(local), exist_ok=True)

    try:
        r = session.get(url, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(f"[오류] {url} — {e}")
        return

    content_type = r.headers.get("Content-Type", "")
    if "text/html" not in content_type:
        with open(local, "wb") as f:
            f.write(r.content)
        print(f"[저장] {local}")
        return

    with open(local, "w", encoding="utf-8") as f:
        f.write(r.text)
    print(f"[저장] {local}  ({len(r.text):,}자)")

    soup = BeautifulSoup(r.text, "html.parser")
    links = [a["href"] for a in soup.find_all("a", href=True)]
    for href in links:
        next_url = urljoin(url, href).split("#")[0]
        if next_url not in visited and next_url.startswith(BASE):
            time.sleep(0.3)
            download(next_url)


# 이전에 받은 빈 파일 삭제
bad = os.path.join(FOLDER, "4ed", ".html")
if os.path.exists(bad):
    os.remove(bad)
    print(f"[삭제] 잘못된 파일 제거: {bad}")

print(f"다운로드 시작: {BASE}")
print(f"저장 폴더: {os.path.abspath(FOLDER)}\n")
download(BASE + "contents.html")
print("\n완료!")
