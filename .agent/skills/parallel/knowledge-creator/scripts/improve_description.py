import argparse
import json
import re
import sys
from pathlib import Path


def improve_description(
    client,
    skill_name: str,
    skill_content: str,
    current_description: str,
    eval_results: dict,
    history: list,
    model: str,
    log_dir: Path | None = None,
    iteration: int | None = None,
) -> str:
    """Improve the skill description using a language model based on eval results."""

    failures = [r for r in eval_results["results"] if not r["pass"]]
    successes = [r for r in eval_results["results"] if r["pass"]]

    history_text = "\n".join(
        [
            f"- Iteration {h['iteration']}: {h['passed']}/{h['total']} passed. Description: {h['description']}"
            for h in history
        ]
    )

    prompt = f"""You are an expert at writing concise, high-performing skill descriptions for an AI agent.
The agent uses these descriptions (defined in the frontmatter of markdown files) to decide when to call a "skill" (read a file and follow its instructions).

Current Skill: {skill_name}
Skill Content:
```md
{skill_content}
```

Current Description:
"{current_description}"

Performance History:
{history_text}

Latest Eval Results ({eval_results['summary']['passed']}/{eval_results['summary']['total']} passed):
Failures:
"""
    for r in failures:
        status = (
            "TRIGGERED unnecessarily"
            if not r["should_trigger"]
            else "FAILED to trigger"
        )
        prompt += f"- Query: \"{r['query']}\" (Trigger rate: {r['trigger_rate']:.0%}). Expected tool call? {'Yes' if r['should_trigger'] else 'No'}. Outcome: {status}\n"

    prompt += "\nSuccesses:\n"
    for r in successes:
        prompt += f"- Query: \"{r['query']}\" (Correctly {'triggered' if r['should_trigger'] else 'not triggered'})\n"

    prompt += """
Your goal is to suggest an improved description that will fix the failures while maintaining the successes.
The hard limit is 1,024 characters. Keep it concise, specific, and focused on the *intent* the skill handles.
Use keywords from the failures to help Claude understand when to (or when not to) trigger this skill.

Respond with only the new description text in <new_description> tags."""

    response = client.messages.create(
        model=model,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text
    match = re.search(r"<new_description>(.*?)</new_description>", text, re.DOTALL)
    description = match.group(1).strip() if match else text.strip().strip('"')

    if log_dir:
        (log_dir / f"improve_iter_{iteration}.json").write_text(
            json.dumps(
                {"prompt": prompt, "response": text, "description": description},
                indent=2,
            )
        )

    return description


def main():
    # Placeholder main for CLI use if needed
    pass


if __name__ == "__main__":
    main()
