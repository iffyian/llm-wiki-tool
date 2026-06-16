# Agent Workflow

## Summary

Agent workflow는 user request를 분석하고 task로 분해한 뒤, plan과 review를 통해 결과를 검증하는 절차입니다.

## Key Points

- Plan mode는 구현 전에 분석과 계획을 수행하는 단계입니다.
- Sequential agent는 앞 agent의 결과를 다음 agent가 이어받습니다.
- Parallel agent는 독립적인 task를 동시에 처리할 수 있습니다.
- Agent specification은 agent의 역할, 입력, 출력, 책임을 명시합니다.
- Agent pool과 orchestrator는 여러 agent의 상태와 routing을 관리합니다.

## Related Pages

- [Agentic Coding](agentic-coding.md)
- [Harness, MCP, Automation](harness-mcp-automation.md)

## Source Basis

- `4. Plan_mode Sequential and Parallel agents.pdf`
- `5. Agent Specifications.pdf`
- `6. Agent pool and Orchestrator.pdf`

## Maintenance Notes

- 실제 agent 역할 예시를 추가할 수 있습니다.
