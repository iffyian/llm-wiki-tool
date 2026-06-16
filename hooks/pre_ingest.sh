#!/usr/bin/env bash
# hooks/pre_ingest.sh
# raw/ 에 새 파일이 추가되기 전 실행됩니다.
# 용도: 파일 존재 여부 확인, 중복 감지, 로그 기록

set -euo pipefail

FILE="${1:-}"
LOGFILE="wiki/maintenance-log.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

if [ -z "$FILE" ]; then
  echo "[pre_ingest] ERROR: 파일 경로 인수가 없습니다." >&2
  exit 1
fi

# 중복 파일 감지
BASENAME=$(basename "$FILE")
if [ -f "raw/$BASENAME" ]; then
  echo "[pre_ingest] WARN: raw/$BASENAME 이미 존재합니다. 덮어쓰려면 수동으로 진행하세요." >&2
  exit 1
fi

# 지원 형식 확인
EXT="${FILE##*.}"
case "$EXT" in
  zip|pdf|txt|md) ;;
  *)
    echo "[pre_ingest] WARN: 지원하지 않는 형식($EXT)입니다. 계속 진행하려면 수동으로 추가하세요." >&2
    exit 1
    ;;
esac

# maintenance log에 기록
cat >> "$LOGFILE" <<EOF

## $TIMESTAMP — pre_ingest

- 파일: \`$BASENAME\`
- 상태: 입력 검증 통과, ingest 준비 완료
EOF

echo "[pre_ingest] OK: $BASENAME 검증 완료"
