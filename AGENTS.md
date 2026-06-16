# LLM Wiki Agent Instructions

이 저장소에서 agent는 답변 생성기이자 wiki 유지보수자입니다.

## 기본 절차

1. 작업 시작 시 `README.md`, `SCHEME.md`, `wiki/index.md`를 읽습니다.
2. raw source는 수정하지 않습니다.
3. user query에는 기존 wiki pages를 먼저 사용합니다.
4. raw source가 추가되면 `PIPELINE.md` 순서로 처리합니다.
5. 재사용 가치가 있는 지식만 wiki page에 통합합니다.
6. wiki page를 변경하면 `wiki/maintenance-log.md`에 기록합니다.

## Page 작성 규칙

- `SCHEME.md`의 Topic Page Scheme을 따릅니다.
- source에서 확인된 사실과 agent의 해석을 구분합니다.
- 중복 page를 만들지 않습니다.
- 관련 page를 연결합니다.
- index에서 모든 topic page에 접근할 수 있어야 합니다.

## User Query 처리

1. 질문을 주제로 분류합니다.
2. `wiki/index.md`에서 관련 page를 찾습니다.
3. 관련 page를 읽고 답변합니다.
4. 근거가 부족하면 raw source를 확인합니다.
5. 새 지식이 생기면 maintenance 절차를 수행합니다.
