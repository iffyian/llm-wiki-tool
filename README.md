# 🚀 Enterprise LLM Wiki Engine

본 프로젝트는 LLM을 단순 일회성 답변 생성기가 아니라, 지속 가능한 사내 지식베이스 유지보수자 및 엔지니어링 문서 빌더로 활용하는 완전한 독립형 Markdown 위키 프레임워크입니다. 사내의 다양한 소프트웨어 설계 사양서, API 아키텍처 가이드 등의 원본 소스(`raw/`)를 투입하면 하네스 에이전트 인프라가 이를 정밀 분석하여 표준화된 구조의 위키 페이지로 자동 생성 및 점진적 갱신을 수행합니다.

---

## ⏱️ 30분 빠른 시작 — 내 자료로 첫 엔지니어링 위키 빌드하기

### 0. 환경 요구사항

| 요구 항목 | 권장 사양 / 버전 |
|---|---|
| **Python** | 3.9 이상 (별도의 파이썬 외부 종속성 패키지 설치는 필요하지 않음) |
| **에이전트 환경** | Claude Desktop GUI 또는 Claude Code CLI 최신 버전 |
| **운영체제(OS)** | macOS / Linux / Windows (WSL 환경 권장) |

### 1단계 — 저장소 클론 (Repository Clone)

git clone https://github.com/<your-username>/software-docs-wiki.git
cd software-docs-wiki


### 2단계 — 로컬 위키 뷰어 구동 (미리 확인용)

python3 tools/viewer.py

브라우저에서 http://localhost:8765 를 열면 현재 관리 중인 사내 소프트웨어 엔지니어링 위키 대시보드를 실시간으로 확인할 수 있습니다.

### 3단계 — 지식 관리 MCP 서버 등록
#### Claude Desktop 사용 시
`claude_desktop_config.json` 설정 파일을 열고 아래 구성을 주입합니다.

{
  "mcpServers": {
    "llm-wiki": {
      "command": "python3",
      "args": ["/이동한_디렉토리의_절대경로/tools/wiki_mcp_server.py"],
      "description": "사내 소프트웨어 기술 문서 통합 관리를 위한 도구 세트"
    }
  }
}

> ⚠️ **주의**: `args` 배열 내의 경로는 반드시 본인 로컬 환경의 **절대 경로**로 완벽하게 치환되어야 정상 작동합니다.

#### Claude Code CLI 사용 시
저장소 루트 디렉토리 내부 터미널에서 다음 인프라 등록 명령을 트리거합니다.

claude mcp add llm-wiki -- python3 tools/wiki_mcp_server.py


### 4단계 — 엔지니어링 원본 데이터 투입
처음 사용할 나만의 기술 소스 데이터(예: 시스템 아키텍처 문서, API 초안 텍스트 파일 등)를 불변 보존 영역인 `raw/` 폴더에 배치합니다.

cp /path/to/my_software_specification.md raw/


### 5단계 — 에이전트 자동화 위키 통합 요청
연동된 에이전트 인터페이스 세션에 진입점을 인지시키기 위해 다음 지침 프롬프트를 입력합니다.

raw/my_software_specification.md 파일이 인프라에 추가되었습니다.
RULES.md 지침과 PIPELINE.md 워크플로우 절차를 완전히 준수하여 사내 기술 위키 페이지를 새롭게 빌드하거나 기존 문서를 점진적으로 갱신하고, 중앙 index.md 및 maintenance-log.md 내역을 동적으로 최신화하세요.


### 6단계 — 변환 결과 검증 및 인터페이스 확인

python3 tools/viewer.py

브라우저에서 http://localhost:8765 페이지를 새로고침하여, 내가 투입한 데이터가 `SCHEME.md` 규격을 준수하는 깔끔한 엔지니어링 토픽 문서로 실사용 렌더링되었는지 검증합니다.

---

## 🔌 MCP Tool 목록과 동작 아키텍처

에이전트는 `tools/wiki_mcp_server.py` 엔진이 표준 입출력(stdio transport) 방식을 통해 인터페이스로 열어둔 아래 핵심 도구들을 적절히 믹스인하여 구동됩니다.

| Tool Name | Parameter Specification | 기능 및 동작 설명 |
|---|---|---|
| `list_pages` | — | 현재 생성된 `wiki/pages/` 디렉토리 내의 모든 위키 파일 슬러그 목록을 반환합니다. |
| `read_page` | `name` (string) | 요청한 특정 도메인 문서의 원본 마크다운 텍스트 컨텍스트를 스캔하여 커널에 로드합니다. |
| `read_index` | — | 중앙 게이트웨이인 `wiki/index.md` 구조 전체를 읽어와 지식 맵 상태를 확인합니다. |
| `search_wiki` | `query` (string) | 위키 저장소 내에서 특정 기술 키워드가 포함된 문서를 전수 검색하고 미리보기를 반환합니다. |
| `write_page` | `name`, `content` (string) | 에이전트가 변환한 정제 지식을 `SCHEME.md` 템플릿에 맞춰 독립 문서로 영속화하고 인덱스에 링크를 가동합니다. |
| `append_log` | `entry` (string) | 시스템 변경 추적성 보장을 위해 `wiki/maintenance-log.md`에 유지보수 로그 이력을 자동 기록합니다. |
| `list_raw` | — | 현재 분석 대기 중이거나 처리가 완료된 `raw/` 스토리지 내 원본 소스 파일들의 카탈로그를 확인합니다. |

---

## 📁 패키지 저장소 전체 구조 (Directory Blueprint)

software-docs-wiki/
├── RULES.md            ← 하네스(Harness) 에이전트 코어 운영 지침서 및 컨텍스트 규칙
├── AGENTS.md           ← 에이전트의 역할 모델링 및 내부 실행 절차 명세서
├── SCHEME.md           ← 위키 페이지 데이터 형식 표준 마크다운 스키마 레이아웃
├── PIPELINE.md         ← 원본 데이터 유입 시 파싱 및 지식 통합 제어 파이프라인 문서
├── RESEARCH.md         ← 기존 지식 관리(RAG) 대비 프레임워크 영속화 당위성 연구 기술서
├── mcp.json            ← 표준 분산 환경용 MCP 인프라 설정 명세 파일
├── ingest.sh           ← 데이터 수집 훅 트리거 및 통합 에이전트 호출 셸 스크립트
│
├── raw/                ← 변경이 불가능한 불변(Immutable) 원본 엔지니어링 소스 스토리지
│
├── wiki/               ← 정제된 사내 영구 자산 기술 지식 베이스 영역
│   ├── index.md        ← 전체 시스템 도메인을 조망하는 중앙 기술 인덱스 라우터
│   ├── maintenance-log.md ← 파이프라인 연동 변경 이력 및 영속화 히스토리 로그
│   └── pages/          ← 실제 에이전트가 가동되어 자동 생성·갱신된 기술 도메인 페이지 스토리지
│
├── tools/              ← 통합 실행 도구 및 시각화 게이트웨이 영역
│   ├── wiki_mcp_server.py   ← 외부 AI 인터페이스 연동을 지원하는 표준 Stdio MCP 엔진
│   └── viewer.py            ← 브라우저 연동 및 로컬 위키 렌더링용 빌트인 웹 뷰어 서버
│
├── hooks/              ← 전처리 및 후처리 안정성 확보를 위한 Hook 인프라
│   ├── pre_ingest.sh   ← 데이터 수집 전 포맷 무결성 및 중복성 선행 검증 훅
│   └── post_update.sh  ← 위키 자산 최신화 직후 중앙 인덱스 정합성 사후 검증 훅
│
├── skills/             ← 하네스 에이전트가 상시 재사용하는 원자적 Skill 명세 집합
│   ├── ingest_raw.md   ← 원본 자료 파싱 및 마크다운 정제 스킬 규칙
│   ├── update_page.md  ← 기존 구조화 문서 내부 컨텍스트 병합 및 점진적 갱신 스킬 규칙
│   └── query_wiki.md   ← 누적된 기술 위키 우선 참조 및 답변 아키텍처 스킬 규칙
│
├── schema/             ← 문서 무결성 자동 검증용 데이터 정의 명세 영역
│   └── page.schema.json ← 위키 메타데이터 무결성 검증을 위한 표준 JSON 스키마
│
└── demo/               ← 제품 동작 실사용 증명 자산 영역
    └── wiki_viewer_demo.png ← 실제 로컬 뷰어를 통해 활성화된 위키 화면 캡처 자산

---

## 🔍 런타임 시스템 검증 방법 (Verification)

### 1. 지식 관리 MCP 서버 단독 인터페이스 검증 (JSON-RPC over Stdio)

# 초기화 핸드셰이크 프로토콜 검증
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python3 tools/wiki_mcp_server.py

# 제공 도구 리스트 출력 스키마 검증
echo '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' | python3 tools/wiki_mcp_server.py


### 2. 빌트인 뷰어 및 레이아웃 네트워크 검증

# 백그라운드로 로컬 뷰어 가동
python3 tools/viewer.py &

# 네트워크 엔트리포인트 헬스체크 및 타이틀 렌더링 무결성 스캔
curl -s http://localhost:8765 | grep -o '<title>[^<]*</title>'


### 3. Hook 시스템 스크립트 독립 무결성 검증

bash hooks/post_update.sh


---

## 🔐 API Credentials 및 보안 운영 방침

- **하드코딩 금지**: 본 저장소에 포함된 소스코드, 마크다운 주석, 환경설정 JSON을 포함한 어떤 파일에도 OpenAI, Anthropic 등의 외부 LLM API 인증 Key를 직접 노출하거나 기록하는 행위를 철저히 배제합니다.
- **안전한 자격증명 관리**: 로컬 런타임 가동 시 클라이언트 자체 로그인 세션을 사용하거나, 시스템 터미널 환경 변수 샌드박스 영역(`export ANTHROPIC_API_KEY=sk-...`)을 통해서만 인증 메커니즘을 통과하도록 격리 설계되어 안전하게 운영됩니다.
