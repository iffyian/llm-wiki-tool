#!/usr/bin/env python3
"""
tools/wiki_mcp_server.py
LLM Wiki MCP Server — stdio transport (Claude Desktop / Claude Code 호환)

제공 도구:
  list_pages      — wiki/pages/ 의 page 목록 반환
  read_page       — 특정 page 내용 반환
  read_index      — wiki/index.md 반환
  search_wiki     — 키워드로 page 내용 검색
  write_page      — page 생성 또는 갱신
  append_log      — maintenance-log.md에 항목 추가
  list_raw        — raw/ 파일 목록 반환
"""

import json
import sys
import os
import re
from datetime import date
from pathlib import Path

# 저장소 루트 = 이 파일의 상위 디렉터리
REPO_ROOT = Path(__file__).parent.parent
WIKI_DIR = REPO_ROOT / "wiki"
PAGES_DIR = WIKI_DIR / "pages"
RAW_DIR = REPO_ROOT / "raw"
INDEX_FILE = WIKI_DIR / "index.md"
LOG_FILE = WIKI_DIR / "maintenance-log.md"


# ── MCP 메시지 핸들러 ──────────────────────────────────────────────────────

def send(obj: dict):
    print(json.dumps(obj, ensure_ascii=False), flush=True)


def error_response(req_id, code: int, message: str):
    send({"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}})


def ok_response(req_id, result):
    send({"jsonrpc": "2.0", "id": req_id, "result": result})


# ── 도구 구현 ──────────────────────────────────────────────────────────────

def tool_list_pages(_args: dict) -> dict:
    pages = sorted(p.stem for p in PAGES_DIR.glob("*.md"))
    return {"pages": pages, "count": len(pages)}


def tool_read_page(args: dict) -> dict:
    name = args.get("name", "").strip()
    if not name:
        raise ValueError("name 파라미터가 필요합니다.")
    # slug 또는 파일명 모두 허용
    slug = name.replace(".md", "")
    path = PAGES_DIR / f"{slug}.md"
    if not path.exists():
        raise FileNotFoundError(f"page '{slug}' 를 찾을 수 없습니다.")
    return {"name": slug, "content": path.read_text(encoding="utf-8")}


def tool_read_index(_args: dict) -> dict:
    if not INDEX_FILE.exists():
        return {"content": ""}
    return {"content": INDEX_FILE.read_text(encoding="utf-8")}


def tool_search_wiki(args: dict) -> dict:
    query = args.get("query", "").strip().lower()
    if not query:
        raise ValueError("query 파라미터가 필요합니다.")
    results = []
    for path in sorted(PAGES_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if query in text.lower():
            # 첫 번째 매칭 줄 미리보기
            for line in text.splitlines():
                if query in line.lower():
                    results.append({"page": path.stem, "preview": line.strip()[:120]})
                    break
    return {"query": query, "matches": results, "count": len(results)}


def tool_write_page(args: dict) -> dict:
    name = args.get("name", "").strip()
    content = args.get("content", "")
    if not name or not content:
        raise ValueError("name 과 content 파라미터가 필요합니다.")
    slug = name.replace(".md", "")
    # 경로 순회 방지
    if "/" in slug or "\\" in slug or ".." in slug:
        raise ValueError("name에 경로 구분자를 포함할 수 없습니다.")
    path = PAGES_DIR / f"{slug}.md"
    existed = path.exists()
    path.write_text(content, encoding="utf-8")
    action = "갱신" if existed else "생성"
    # index에 링크가 없으면 추가
    index_text = INDEX_FILE.read_text(encoding="utf-8") if INDEX_FILE.exists() else ""
    if f"{slug}.md" not in index_text:
        with open(INDEX_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n- [{slug}](pages/{slug}.md)\n")
    return {"action": action, "path": str(path.relative_to(REPO_ROOT))}


def tool_append_log(args: dict) -> dict:
    entry = args.get("entry", "").strip()
    if not entry:
        raise ValueError("entry 파라미터가 필요합니다.")
    today = date.today().isoformat()
    block = f"\n## {today}\n\n{entry}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(block)
    return {"logged": True, "date": today}


def tool_list_raw(_args: dict) -> dict:
    files = sorted(p.name for p in RAW_DIR.iterdir() if not p.name.startswith("."))
    return {"files": files, "count": len(files)}


TOOLS = {
    "list_pages": tool_list_pages,
    "read_page": tool_read_page,
    "read_index": tool_read_index,
    "search_wiki": tool_search_wiki,
    "write_page": tool_write_page,
    "append_log": tool_append_log,
    "list_raw": tool_list_raw,
}

TOOL_SCHEMA = [
    {
        "name": "list_pages",
        "description": "wiki/pages/ 디렉터리의 page 목록을 반환합니다.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "read_page",
        "description": "wiki page의 내용을 반환합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {"name": {"type": "string", "description": "page slug (예: agentic-coding)"}},
            "required": ["name"],
        },
    },
    {
        "name": "read_index",
        "description": "wiki/index.md 전체 내용을 반환합니다.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "search_wiki",
        "description": "키워드로 wiki page를 검색하고 매칭된 page와 미리보기를 반환합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {"query": {"type": "string", "description": "검색 키워드"}},
            "required": ["query"],
        },
    },
    {
        "name": "write_page",
        "description": "wiki page를 생성하거나 갱신합니다. index에 없으면 자동 추가합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "page slug (예: new-topic)"},
                "content": {"type": "string", "description": "SCHEME.md 형식의 Markdown 전체 내용"},
            },
            "required": ["name", "content"],
        },
    },
    {
        "name": "append_log",
        "description": "wiki/maintenance-log.md에 날짜 헤더와 함께 항목을 추가합니다.",
        "inputSchema": {
            "type": "object",
            "properties": {"entry": {"type": "string", "description": "기록할 내용 (Markdown)"}},
            "required": ["entry"],
        },
    },
    {
        "name": "list_raw",
        "description": "raw/ 디렉터리의 파일 목록을 반환합니다.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
]


# ── MCP 메인 루프 ──────────────────────────────────────────────────────────

def handle(request: dict):
    req_id = request.get("id")
    method = request.get("method", "")
    params = request.get("params", {})

    if method == "initialize":
        ok_response(req_id, {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "llm-wiki-mcp", "version": "1.0.0"},
        })
    elif method == "tools/list":
        ok_response(req_id, {"tools": TOOL_SCHEMA})
    elif method == "tools/call":
        tool_name = params.get("name")
        tool_args = params.get("arguments", {})
        if tool_name not in TOOLS:
            error_response(req_id, -32601, f"알 수 없는 도구: {tool_name}")
            return
        try:
            result = TOOLS[tool_name](tool_args)
            ok_response(req_id, {
                "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}]
            })
        except (ValueError, FileNotFoundError) as e:
            error_response(req_id, -32602, str(e))
        except Exception as e:
            error_response(req_id, -32603, f"내부 오류: {e}")
    elif method == "notifications/initialized":
        pass  # 응답 불필요
    else:
        if req_id is not None:
            error_response(req_id, -32601, f"지원하지 않는 메서드: {method}")


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            send({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "JSON 파싱 오류"}})
            continue
        handle(request)


if __name__ == "__main__":
    main()
