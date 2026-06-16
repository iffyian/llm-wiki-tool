# LLM Wiki 조사

## 정의

LLM Wiki는 LLM을 답변 생성기가 아니라 지식베이스 유지보수자로 사용하는 패턴입니다. 새 source가 들어오면 LLM agent가 source를 읽고 핵심 정보를 추출한 뒤 기존 wiki pages에 통합합니다.

## 일반적인 질의응답과의 차이

일반적인 질의응답은 질문에 답한 뒤 지식이 사라질 수 있습니다. LLM Wiki는 반복해서 사용할 가치가 있는 정보를 Markdown page에 남깁니다. 이후 질문은 누적된 wiki를 우선 참조합니다.

## RAG와의 차이

RAG는 질문 시점에 관련 문서 조각을 검색하는 방식입니다. LLM Wiki는 source 입력 시점에 지식을 구조화하고 유지보수합니다. 둘은 경쟁 관계라기보다 함께 사용할 수 있는 방식입니다.

## 이 과제의 구현 범위

- Markdown-only 저장소
- raw source 보존
- wiki page schema
- agent 운영 지침
- user query 처리
- LLM maintenance 절차
- raw source에서 wiki page를 생성하는 pipeline

## 참고

- Week 12 Automation 강의 자료
- Andrej Karpathy, `llm-wiki`: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
