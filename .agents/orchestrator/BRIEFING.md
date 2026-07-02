# BRIEFING — 2026-06-29T12:39:03-05:00

## Mission
Redesign the "Be The Bank" Simulator main page to establish a clear visual hierarchy.

## 🔒 My Identity
- Archetype: Teamwork Orchestrator
- Roles: orchestrator, user_liaison, human_reporter, successor
- Working directory: /Users/jaketrigg/Projects/REI/seller financing/.agents/orchestrator
- Original parent: parent
- Original parent conversation ID: 4ad7342a-a224-4823-b0fd-47ae37cd3f94

## 🔒 My Workflow
- **Pattern**: Project
- **Scope document**: /Users/jaketrigg/Projects/REI/seller financing/.agents/orchestrator/PROJECT.md
1. **Decompose**: Decompose the task into analysis/exploration, E2E test setup, implementation, and review milestones.
2. **Dispatch & Execute** (pick ONE):
   - **Direct (iteration loop)**: Run direct Explorer -> Worker -> Reviewer loop for single or compound milestones.
   - **Delegate (sub-orchestrator)**: Spawn a sub-orchestrator for individual milestones when they are too complex.
3. **On failure** (in this order):
   - Retry: nudge stuck agent or re-send task
   - Replace: spawn fresh agent with partial progress
   - Skip: proceed without (only if non-critical)
   - Redistribute: split stuck agent's remaining work
   - Redesign: re-partition decomposition
   - Escalate: report to parent (sub-orchestrators only, last resort)
4. **Succession**: Self-succeed at 16 spawns. Write handoff.md, spawn successor.
- **Work items**:
  1. Initialize Project & Explore [in-progress]
- **Current phase**: 1
- **Current focus**: Initialize Project & Explore

## 🔒 Key Constraints
- Never reuse a subagent after it has delivered its handoff — always spawn fresh
- Integrity mode: benchmark
- Must not write code directly, must delegate via invoke_subagent

## Current Parent
- Conversation ID: 4ad7342a-a224-4823-b0fd-47ae37cd3f94
- Updated: not yet

## Key Decisions Made
- Initialized briefing and project coordination files.

## Team Roster
| Agent | Type | Work Item | Status | Conv ID |
|-------|------|-----------|--------|---------|
| explorer_explore_game | teamwork_preview_explorer | Initial game.html analysis | completed | 9e663848-6b82-4400-834b-d86e66d92b53 |
| orchestrator_e2e | self | E2E Testing Track Orchestrator | completed | eb38746f-f4ed-456f-98b3-8af04c027025 |
| orchestrator_impl | self | Implementation Track Orchestrator | in-progress | 00bfb6c4-592a-4190-bf12-7460d0ba36ff |

## Succession Status
- Succession required: no
- Spawn count: 3 / 16
- Pending subagents: none
- Predecessor: none
- Successor: not yet spawned

## Active Timers
- Heartbeat cron: killed (task-13)
- Safety timer: none
- On succession: kill all timers before spawning successor
- On context truncation: run `manage_task(Action="list")` — re-create if missing

## Artifact Index
- /Users/jaketrigg/Projects/REI/seller financing/.agents/orchestrator/ORIGINAL_REQUEST.md — Verbatim user request
- /Users/jaketrigg/Projects/REI/seller financing/.agents/orchestrator/BRIEFING.md — My persistent working memory
