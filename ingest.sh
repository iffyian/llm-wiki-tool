#!/usr/bin/env bash
# ingest.sh
# raw/ 에 새 파일을 추가하고 에이전트에게 wiki 갱신을 요청합니다.
#
# 사용법:
#   ./ingest.sh <파일경로>
#
# 이 스크립트는 API Key를 직접 사용하지 않습니다.
# Claude Code / Claude Desktop의 MCP 세션 안에서 실행하거나,
# ANTHROPIC_API_KEY 환경변수가 설정된 셸에서 실행하세요.
#
# 에이전트 호출 방식: subprocess → claude (Claude Code CLI)

set -euo pipefail

FILE="${1:-}"
if [ -z "$FILE" ]; then
  echo "사용법: ./ingest.sh <파일경로>" >&2
  exit 1
fi

if [ ! -f "$FILE" ]; then
  echo "오류: 파일을 찾을 수 없습니다 — $FILE" >&2
  exit 1
fi

# 1. pre-ingest hook 실행
echo "[ingest] pre-ingest hook 실행..."
bash hooks/pre_ingest.sh "$FILE"

# 2. 파일을 raw/ 로 복사
BASENAME=$(basename "$FILE")
cp "$FILE" "raw/$BASENAME"
echo "[ingest] raw/$BASENAME 복사 완료"

# 3. 에이전트에게 wiki 갱신 요청 (Claude Code CLI 사용)
#    API Key는 환경변수 ANTHROPIC_API_KEY 에서 읽힙니다. 코드에 하드코딩 금지.
PROMPT="raw/$BASENAME 파일이 추가됐습니다. RULES.md와 PIPELINE.md를 따라 wiki page를 생성하거나 갱신하고, wiki/index.md와 wiki/maintenance-log.md를 업데이트하세요."

if command -v claude &>/dev/null; then
  echo "[ingest] Claude Code CLI로 에이전트 실행..."
  claude --print "$PROMPT"
else
  echo "[ingest] INFO: claude CLI를 찾을 수 없습니다."
  echo "[ingest] Claude Desktop MCP 또는 Claude Code 세션에서 아래 메시지를 직접 입력하세요:"
  echo ""
  echo "  $PROMPT"
  echo ""
fi

# 4. post-update hook 실행
echo "[ingest] post-update hook 실행..."
bash hooks/post_update.sh

echo "[ingest] 완료"
