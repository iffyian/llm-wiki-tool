#!/usr/bin/env python3
"""
tools/viewer.py
LLM Wiki 뷰어 — 브라우저에서 wiki page를 확인하는 로컬 HTTP 서버

사용법:
    python tools/viewer.py          # http://localhost:8765
    python tools/viewer.py 9000     # 포트 변경
"""

import sys
import os
import re
import http.server
import socketserver
from pathlib import Path
from urllib.parse import unquote

REPO_ROOT = Path(__file__).parent.parent
WIKI_DIR = REPO_ROOT / "wiki"
PAGES_DIR = WIKI_DIR / "pages"

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765


def md_to_html(text: str) -> str:
    """최소한의 Markdown → HTML 변환 (외부 의존성 없음)"""
    lines = text.splitlines()
    html_lines = []
    in_code = False
    in_table = False

    for line in lines:
        # 코드 블록
        if line.startswith("```"):
            if in_code:
                html_lines.append("</code></pre>")
                in_code = False
            else:
                lang = line[3:].strip()
                html_lines.append(f'<pre><code class="language-{lang}">')
                in_code = True
            continue
        if in_code:
            html_lines.append(line.replace("&", "&amp;").replace("<", "&lt;"))
            continue

        # 제목
        if line.startswith("### "):
            html_lines.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("# "):
            html_lines.append(f"<h1>{line[2:]}</h1>")
        # 테이블
        elif "|" in line and line.strip().startswith("|"):
            if not in_table:
                html_lines.append("<table>")
                in_table = True
            if re.match(r"^\|[-| :]+\|$", line.strip()):
                continue  # 구분선 행 스킵
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            tag = "th" if not any("<td>" in l for l in html_lines[-3:]) else "td"
            html_lines.append("<tr>" + "".join(f"<{tag}>{c}</{tag}>" for c in cells) + "</tr>")
        else:
            if in_table:
                html_lines.append("</table>")
                in_table = False
            # 목록
            if line.startswith("- "):
                content = line[2:]
                # 내부 링크 변환 [text](pages/slug.md)
                content = re.sub(
                    r"\[([^\]]+)\]\(pages/([^)]+)\.md\)",
                    lambda m: f'<a href="/pages/{m.group(2)}">{m.group(1)}</a>',
                    content,
                )
                content = re.sub(
                    r"\[([^\]]+)\]\(\.\.\/([^)]+)\)",
                    lambda m: f'<a href="/{m.group(2)}">{m.group(1)}</a>',
                    content,
                )
                html_lines.append(f"<li>{content}</li>")
            elif line.strip() == "":
                html_lines.append("<br>")
            else:
                content = re.sub(r"`([^`]+)`", r"<code>\1</code>", line)
                content = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", content)
                content = re.sub(
                    r"\[([^\]]+)\]\(pages/([^)]+)\.md\)",
                    lambda m: f'<a href="/pages/{m.group(2)}">{m.group(1)}</a>',
                    content,
                )
                html_lines.append(f"<p>{content}</p>")

    if in_table:
        html_lines.append("</table>")
    return "\n".join(html_lines)


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>{title} — LLM Wiki</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
         max-width: 860px; margin: 40px auto; padding: 0 20px; color: #222; }}
  h1 {{ border-bottom: 2px solid #3b82f6; padding-bottom: 8px; color: #1d4ed8; }}
  h2 {{ color: #374151; margin-top: 2em; }}
  h3 {{ color: #6b7280; }}
  a {{ color: #2563eb; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  code {{ background: #f3f4f6; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }}
  pre {{ background: #1e293b; color: #e2e8f0; padding: 16px; border-radius: 8px; overflow-x: auto; }}
  pre code {{ background: none; padding: 0; }}
  table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
  th, td {{ border: 1px solid #d1d5db; padding: 8px 12px; text-align: left; }}
  th {{ background: #f9fafb; font-weight: 600; }}
  nav {{ background: #f8fafc; padding: 12px 16px; border-radius: 8px;
         margin-bottom: 24px; font-size: 0.9em; }}
  nav a {{ margin-right: 12px; color: #4b5563; }}
  .badge {{ background: #dbeafe; color: #1e40af; padding: 2px 8px;
            border-radius: 12px; font-size: 0.8em; }}
</style>
</head>
<body>
<nav>
  <a href="/">🏠 Index</a>
  <a href="/maintenance-log">📋 Maintenance Log</a>
  <span class="badge">LLM Wiki</span>
</nav>
{body}
</body>
</html>"""


class WikiHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # 액세스 로그 억제

    def send_html(self, title: str, body: str, status: int = 200):
        content = HTML_TEMPLATE.format(title=title, body=body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        path = unquote(self.path.split("?")[0])

        if path == "/" or path == "/index":
            self._serve_file(WIKI_DIR / "index.md", "Index")
        elif path == "/maintenance-log":
            self._serve_file(WIKI_DIR / "maintenance-log.md", "Maintenance Log")
        elif path.startswith("/pages/"):
            slug = path[7:].strip("/")
            self._serve_file(PAGES_DIR / f"{slug}.md", slug)
        else:
            self.send_html("404", "<h1>페이지를 찾을 수 없습니다.</h1><p><a href='/'>← Index로 돌아가기</a></p>", 404)

    def _serve_file(self, filepath: Path, title: str):
        if not filepath.exists():
            self.send_html("404", f"<h1>{title}</h1><p>파일이 없습니다: {filepath.name}</p>", 404)
            return
        text = filepath.read_text(encoding="utf-8")
        body = md_to_html(text)
        self.send_html(title, body)


def main():
    os.chdir(REPO_ROOT)
    with socketserver.TCPServer(("", PORT), WikiHandler) as httpd:
        print(f"[viewer] LLM Wiki 뷰어 실행 중: http://localhost:{PORT}")
        print("[viewer] 종료하려면 Ctrl+C 를 누르세요.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[viewer] 종료")


if __name__ == "__main__":
    main()
