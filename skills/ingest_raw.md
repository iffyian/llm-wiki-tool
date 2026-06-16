# Skill: ingest_raw

## 목적

`raw/` 디렉터리에 새 파일이 추가됐을 때, 내용을 읽고 wiki page를 생성하거나 갱신합니다.

## 입력

- `raw/` 안의 새 파일 경로 (ZIP, PDF, TXT, MD 등)

## 절차

1. **파일 목록 확인**
   ```
   raw/ 안의 파일을 목록으로 열거합니다.
   ```

2. **내용 읽기**
   - ZIP이면 내부 파일 목록을 먼저 확인합니다.
   - PDF면 텍스트 레이어를 추출합니다.
   - 텍스트 파일이면 전체를 읽습니다.

3. **핵심 개념 추출**
   - 반복되는 주요 개념, 정의, 절차를 목록으로 정리합니다.

4. **기존 wiki와 비교**
   - `wiki/index.md`를 읽어 기존 topic page 목록을 확인합니다.
   - 추출한 개념과 기존 주제를 매핑합니다.

5. **page 생성 또는 갱신**
   - 새 주제 → `SCHEME.md` 형식으로 `wiki/pages/<slug>.md` 생성
   - 기존 주제 → 해당 page의 Key Points·Source Basis 갱신

6. **index 갱신**
   - `wiki/index.md`의 Pages 섹션에 새 page 링크 추가

7. **maintenance log 갱신**
   - `wiki/maintenance-log.md`에 날짜, 파일명, 변경 내용 기록

## 출력

- 생성·갱신된 wiki page 경로 목록
- maintenance log 항목

## 실패 조건

- raw 파일이 읽히지 않으면 maintenance log에 실패 사유를 기록하고 중단합니다.
