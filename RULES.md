# LLM Wiki — Agent Rules

## 역할

이 저장소에서 agent는 **지식베이스 유지보수자**입니다.
질문에 답할 때는 wiki를 우선 읽고, raw source는 wiki가 부족할 때만 참조합니다.

## 시작 시 필수 확인 파일

작업을 시작하기 전에 반드시 아래 파일을 읽습니다.

1. `RULES.md` (이 파일)
2. `SCHEME.md` — page 작성 형식
3. `PIPELINE.md` — raw → wiki 처리 절차
4. `wiki/index.md` — 현재 wiki 구조

## 행동 원칙

| 상황 | 행동 |
|---|---|
| 사용자 질문이 들어온 경우 | wiki/index.md에서 관련 page를 먼저 찾는다 |
| wiki만으로 답변 불충분 | raw/ 안의 원본 자료를 확인한다 |
| 새 raw source가 추가된 경우 | PIPELINE.md 순서로 wiki page를 갱신한다 |
| page를 생성·수정한 경우 | wiki/index.md와 wiki/maintenance-log.md를 즉시 갱신한다 |
| MCP 도구를 사용하는 경우 | tools/ 디렉터리의 MCP 서버를 통해 접근한다 |

## 금지 사항

- raw/ 안의 파일을 수정하거나 삭제하지 않습니다.
- source에 없는 내용을 사실처럼 wiki page에 기록하지 않습니다.
- 동일 주제의 중복 page를 만들지 않습니다.
- 답변에만 쓸 정보를 wiki page로 영구 저장하지 않습니다.

## Hook 실행 규칙

- **pre-ingest**: 새 파일이 raw/에 추가되기 전에 `hooks/pre_ingest.sh`를 실행합니다.
- **post-update**: wiki page 수정 후 `hooks/post_update.sh`를 실행합니다.
- Hook 실행 결과는 wiki/maintenance-log.md에 기록합니다.

## Skill 사용

`skills/` 디렉터리의 skill 파일을 참조하여 반복 작업을 처리합니다.
새 skill이 필요하다면 `skills/` 안에 추가하고 이 파일에 목록을 업데이트합니다.

| Skill 파일 | 용도 |
|---|---|
| `skills/ingest_raw.md` | raw source → wiki page 생성 |
| `skills/update_page.md` | 기존 wiki page 갱신 |
| `skills/query_wiki.md` | wiki 검색 및 답변 생성 |
