# Skill: query_wiki

## 목적

사용자 질문에 wiki를 우선 사용하여 답변합니다.

## 절차

1. 질문을 주제 키워드로 분해합니다.
2. `wiki/index.md`에서 관련 page 링크를 찾습니다.
3. 관련 page를 읽고 답변을 구성합니다.
4. wiki만으로 충분하지 않으면 `raw/` 원본을 확인합니다.
5. 답변을 생성합니다.
6. 새로운 재사용 가능한 지식이 나왔다면 `ingest_raw` 또는 `update_page` skill을 이어 실행합니다.

## 출력 형식

- 답변 텍스트
- 사용한 wiki page 경로 (출처 명시)
