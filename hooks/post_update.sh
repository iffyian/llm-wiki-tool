#!/usr/bin/env bash
# hooks/post_update.sh
# wiki page가 수정된 후 실행됩니다.
# 용도: index 정합성 확인, orphan page 감지, 로그 기록

set -euo pipefail

LOGFILE="wiki/maintenance-log.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

echo "[post_update] wiki 정합성 검사 시작..."

# 1. wiki/pages/ 의 모든 page가 index에 링크되어 있는지 확인
MISSING=()
for PAGE in wiki/pages/*.md; do
  SLUG=$(basename "$PAGE")
  if ! grep -q "$SLUG" wiki/index.md 2>/dev/null; then
    MISSING+=("$SLUG")
  fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
  echo "[post_update] WARN: index에 누락된 page: ${MISSING[*]}" >&2
  cat >> "$LOGFILE" <<EOF

## $TIMESTAMP — post_update WARNING

- index에 누락된 page: ${MISSING[*]}
- 수동으로 wiki/index.md에 링크를 추가하세요.
EOF
else
  echo "[post_update] OK: 모든 page가 index에 연결되어 있습니다."
  cat >> "$LOGFILE" <<EOF

## $TIMESTAMP — post_update

- 정합성 검사 통과
- orphan page 없음
EOF
fi
