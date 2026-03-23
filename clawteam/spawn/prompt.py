"""Agent prompt builder — identity + task + optional role prompt.

Coordination knowledge (how to use clawteam CLI) is provided
by the ClawTeam Skill, not duplicated here.
"""

from __future__ import annotations

from pathlib import Path


def _load_role_prompt(agent_name: str) -> str:
    """Load an optional role prompt for a worker by agent name."""
    role_path = (
        Path(__file__).resolve().parent.parent
        / "agents"
        / "imported"
        / "agency_pack"
        / f"{agent_name}.md"
    )
    if role_path.exists():
        return role_path.read_text(encoding="utf-8").strip()
    return ""


def build_agent_prompt(
    agent_name: str,
    agent_id: str,
    agent_type: str,
    team_name: str,
    leader_name: str,
    task: str,
    user: str = "",
    workspace_dir: str = "",
    workspace_branch: str = "",
) -> str:
    """Build agent prompt: identity + task + optional workspace info."""
    role_prompt = _load_role_prompt(agent_name)

    lines = [
        "## Identity\n",
        f"- Name: {agent_name}",
        f"- ID: {agent_id}",
    ]
    if user:
        lines.append(f"- User: {user}")
    lines.extend([
        f"- Type: {agent_type}",
        f"- Team: {team_name}",
        f"- Leader: {leader_name}",
    ])
    if workspace_dir:
        lines.extend([
            "",
            "## Workspace",
            f"- Working directory: {workspace_dir}",
            f"- Branch: {workspace_branch}",
            "- This is an isolated git worktree. Your changes do not affect the main branch.",
        ])
    if role_prompt:
        lines.extend([
            "",
            "## Role Prompt",
            role_prompt,
        ])
    lines.extend([
        "",
        "## Task\n",
        task,
        "",
        "## Coordination Protocol\n",
        f"- Use `clawteam task list {team_name} --owner {agent_name}` to see your tasks.",
        f"- Starting a task: `clawteam task update {team_name} <task-id> --status in_progress`",
        f"- Finishing a task: `clawteam task update {team_name} <task-id> --status completed`",
        "- When you finish all tasks, send a summary to the leader:",
        f'  `clawteam inbox send {team_name} {leader_name} "All tasks completed. <brief summary>" --from {agent_name}`',
        "- If you are blocked or need help, message the leader:",
        f'  `clawteam inbox send {team_name} {leader_name} "Need help: <description>" --from {agent_name}`',
        f"- After finishing work, report your costs: `clawteam cost report {team_name} --input-tokens <N> --output-tokens <N> --cost-cents <N>`",
        f"- Before finishing, save your session: `clawteam session save {team_name} --session-id clawteam-{team_name}-{agent_name} --agent {agent_name}`",
        "",
    ])
    return "\n".join(lines)
