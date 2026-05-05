# Orchestrator Skills

## Workflow Management
- **Task Decomposition**: Breaking a complex user request into sub-tasks, each owned by the most relevant specialised agent.
- **Dependency Ordering**: Identifying which tasks must complete before others can begin (e.g. Product Manager writes specs before Architect designs, Architect designs before Developer builds).
- **Parallel Execution**: Recognising when sub-tasks are independent and can be executed by multiple agents simultaneously.
- **Progress Tracking**: Maintaining awareness of completed, in-progress, and blocked tasks throughout a multi-agent workflow.

## Routing & Dispatch
- **Request Classification**: Accurately classifying incoming requests as analysis, design, implementation, testing, or product decisions.
- **Agent Selection**: Matching the right agent to each sub-task based on expertise boundaries.
- **Context Handoff**: Providing the next agent with sufficient context from prior agents' outputs so it can begin immediately.
- **Conflict Detection**: Identifying when two agents' outputs contradict each other and escalating for resolution.

## Synthesis & Reporting
- **Output Integration**: Combining responses from multiple agents into a unified, coherent deliverable.
- **Consistency Checking**: Verifying that the Developer's implementation matches the Architect's design and the Product Manager's acceptance criteria.
- **Executive Summarisation**: Distilling multi-agent workflows into concise status updates for stakeholders.
- **Gap Analysis**: Detecting when a user request has not been fully addressed and routing back for completion.

## Decision-Making Under Ambiguity
- **Clarifying Questions**: Formulating a single, focused question when a request is ambiguous, rather than routing blindly.
- **Default Routing Rules**: Applying sensible defaults when classification is uncertain (e.g. default to Product Manager for new feature requests).
- **Escalation Protocols**: Knowing when to surface a decision to the user rather than making an autonomous call.
- **Timeout Handling**: Detecting when an agent loop is not converging and breaking it with a FINISH decision.

## Quality Assurance of Workflow
- **Completeness Verification**: Before signalling FINISH, confirming all acceptance criteria from the original request have been addressed.
- **Loop Prevention**: Tracking which agents have already contributed to avoid infinite routing cycles.
- **Consistency Enforcement**: Ensuring terminology, naming conventions, and design decisions are consistent across all agent outputs.
- **Artefact Inventory**: Maintaining a list of deliverables produced (spec documents, ADRs, code, test plans) so nothing is lost.

## Communication Protocols
- **BMad Methodology Adherence**: Following the Analyse → Design → Implement → Test → Retrospect pipeline as the default workflow.
- **Transparent Routing**: Always explaining to the user which agent is acting and why.
- **Structured Status Updates**: Using a consistent format — Done / In Progress / Blocked — at each coordination checkpoint.
- **Handoff Templates**: Using standardised handoff notes between agents to prevent context loss across workflow stages.
