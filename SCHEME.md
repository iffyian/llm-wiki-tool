# Wiki Page Scheme 운영 방안

## 1. Page 종류

| 종류 | 목적 | 위치 |
|---|---|---|
| Index | 전체 page 탐색 | `wiki/index.md` |
| Topic Page | 여러 source에서 반복되는 핵심 개념 정리 | `wiki/pages/` |
| Maintenance Log | LLM이 수행한 갱신 기록 | `wiki/maintenance-log.md` |
| Raw Source | 원본 자료 보존 | `raw/` |

## 2. Topic Page Scheme

각 topic page는 다음 형식을 사용합니다.

```markdown
# Topic Name

## Summary
핵심 내용을 짧게 설명합니다.

## Key Points
- 주요 사실

## Related Pages
- 관련 wiki page

## Source Basis
- 원본 source

## Maintenance Notes
- 갱신이 필요하거나 불확실한 부분
```

## 3. 운영 규칙

1. raw source는 수정하지 않습니다.
2. 새 source가 들어오면 기존 page와 먼저 비교합니다.
3. 기존 주제라면 page를 갱신하고, 새로운 주제라면 page를 생성합니다.
4. page를 추가하거나 수정하면 `wiki/index.md`와 `wiki/maintenance-log.md`를 갱신합니다.
5. 답변에만 사용하고 버릴 정보와 wiki에 남길 지식을 구분합니다.
6. source에 없는 해석은 사실처럼 기록하지 않습니다.

## 4. User Query 운영

1. `wiki/index.md`에서 관련 page를 찾습니다.
2. 관련 topic page를 우선 읽습니다.
3. wiki만으로 부족하면 raw source를 확인합니다.
4. 사용자에게 답변합니다.
5. 재사용 가치가 있는 새 지식이면 wiki page에 반영합니다.

## 5. LLM Maintenance 운영

1. 새 source, user query, 검토 요청을 trigger로 받습니다.
2. 영향을 받는 topic page를 찾습니다.
3. page를 추가하거나 수정합니다.
4. index를 갱신합니다.
5. maintenance log에 변경 이유를 기록합니다.
