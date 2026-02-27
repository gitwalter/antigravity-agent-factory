import argparse
import html
import json
import sys
from pathlib import Path


def generate_html(data: dict, auto_refresh: bool = False, skill_name: str = "") -> str:
    """Generate HTML visualization of run_loop history."""
    history = data.get("history", [])
    original_description = data.get("original_description", "")
    best_description = data.get("best_description", "")
    best_score = data.get("best_score", "")

    # Try to extract queries from the first iteration's results
    train_queries = []
    test_queries = []
    if history:
        h0 = history[0]
        train_results = h0.get("train_results", h0.get("results", []))
        test_results = h0.get("test_results", [])
        train_queries = [
            {"query": r["query"], "should_trigger": r.get("should_trigger", True)}
            for r in train_results
        ]
        test_queries = [
            {"query": r["query"], "should_trigger": r.get("should_trigger", True)}
            for r in test_results
        ]

    title_prefix = f"{skill_name}: " if skill_name else ""

    html_parts = [
        """<!DOCTYPE html>
<html>
<head>
    <title>"""
        + title_prefix
        + """Optimization Report</title>
    <meta charset="utf-8">
"""
        + ("<meta http-equiv='refresh' content='5'>" if auto_refresh else "")
        + """
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.5; color: #333; max-width: 1400px; margin: 0 auto; padding: 2rem; background: #f9f9f9; }
        h1 { margin-top: 0; font-weight: 700; color: #111; }
        .explainer { background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; margin-bottom: 2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        .summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
        .summary p { background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem; margin: 0; }
        .summary strong { display: block; color: #666; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem; }
        .summary .best { border-left: 4px solid #4CAF50; }
        .table-container { overflow-x: auto; background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        table { border-collapse: collapse; width: 100%; font-size: 0.9rem; }
        th, td { padding: 0.75rem 1rem; text-align: left; border-bottom: 1px solid #eee; }
        th { background: #f5f5f5; font-weight: 600; white-space: nowrap; position: sticky; top: 0; z-index: 10; }
        tr:hover { background: #fcfcfc; }
        .iter-col { width: 40px; text-align: center; }
        .score-col { width: 80px; font-weight: 600; text-align: center; }
        .description-col { min-width: 300px; max-width: 500px; }
        .query-col { text-align: center; min-width: 60px; font-size: 0.75rem; writing-mode: vertical-rl; transform: rotate(180deg); }
        .result { text-align: center; font-size: 1.2rem; }
        .pass { color: #4CAF50; }
        .fail { color: #F44336; }
        .rate { font-size: 0.7rem; color: #777; display: block; margin-top: -4px; line-height: 1; }
        .best-row { background: #f0fff0 !important; }
        .score { display: inline-block; padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: 600; }
        .score-good { background: #e8f5e9; color: #2e7d32; }
        .score-ok { background: #fff3e0; color: #ef6c00; }
        .score-bad { background: #ffebee; color: #c62828; }
        .positive-col { border-bottom: 3px solid #4CAF50; }
        .negative-col { border-bottom: 3px solid #9e9e9e; }
        .test-col { background: #f0f7ff !important; border-left: 2px solid #e0e0e0; }
        .test-result { background: #f0f7ff !important; border-left: 2px solid #e0e0e0; }
        .legend { margin-bottom: 1rem; font-size: 0.85rem; display: flex; gap: 1.5rem; flex-wrap: wrap; }
        .legend-item { display: flex; align-items: center; gap: 6px; }
        .legend-swatch { width: 16px; height: 16px; border-radius: 3px; display: inline-block; }
        .swatch-positive { background: #fff; border: 1px solid #e0e0e0; border-bottom: 3px solid #4CAF50; }
        .swatch-negative { background: #fff; border: 1px solid #e0e0e0; border-bottom: 3px solid #9e9e9e; }
        .swatch-test { background: #f0f7ff; border: 1px solid #e0e0e0; }
    </style>
</head>
<body>
    <h1>"""
        + title_prefix
        + """Skill Description Optimization</h1>
    <div class="explainer">
        <strong>Optimizing your skill's description.</strong> This page updates automatically as Claude tests different versions of your skill's description. Each row is an iteration — a new description attempt. The columns show test queries: green checkmarks mean the skill triggered correctly, red crosses mean it got it wrong.
    </div>
"""
    ]

    html_parts.append(f"""
    <div class="summary">
        <p><strong>Original:</strong> {html.escape(original_description)}</p>
        <p class="best"><strong>Best:</strong> {html.escape(best_description)}</p>
        <p><strong>Best Score:</strong> {best_score}</p>
        <p><strong>Iterations:</strong> {len(history)} | <strong>Train:</strong> {len(train_queries)} | <strong>Test:</strong> {len(test_queries)}</p>
    </div>
""")

    html_parts.append("""
    <div class="legend">
        <span style="font-weight:600">Query columns:</span>
        <span class="legend-item"><span class="legend-swatch swatch-positive"></span> Should trigger</span>
        <span class="legend-item"><span class="legend-swatch swatch-negative"></span> Should NOT trigger</span>
        <span class="legend-item"><span class="legend-swatch swatch-test"></span> Test Query</span>
    </div>
""")

    html_parts.append("""
    <div class="table-container">
    <table>
        <thead>
            <tr>
                <th>Iter</th>
                <th>Train</th>
                <th>Test</th>
                <th class="description-col">Description</th>
""")

    for qinfo in train_queries:
        polarity = "positive-col" if qinfo["should_trigger"] else "negative-col"
        html_parts.append(
            f'                <th class="query-col {polarity}">{html.escape(qinfo["query"])}</th>\n'
        )

    for qinfo in test_queries:
        polarity = "positive-col" if qinfo["should_trigger"] else "negative-col"
        html_parts.append(
            f'                <th class="query-col test-col {polarity}">{html.escape(qinfo["query"])}</th>\n'
        )

    html_parts.append("""            </tr>
        </thead>
        <tbody>
""")

    if test_queries:
        best_iter = max(history, key=lambda h: h.get("test_passed") or 0).get(
            "iteration"
        )
    else:
        best_iter = max(
            history, key=lambda h: h.get("train_passed", h.get("passed", 0))
        ).get("iteration")

    for h in history:
        iteration = h.get("iteration", "?")
        train_passed = h.get("train_passed", h.get("passed", 0))
        train_total = h.get("train_total", h.get("total", 0))
        test_passed = h.get("test_passed")
        test_total = h.get("test_total")
        description = h.get("description", "")
        train_results = h.get("train_results", h.get("results", []))
        test_results = h.get("test_results", [])

        train_by_query = {r["query"]: r for r in train_results}
        test_by_query = {r["query"]: r for r in test_results} if test_results else {}

        def score_class(passed, total):
            if not total:
                return ""
            ratio = passed / total
            if ratio >= 0.8:
                return "score-good"
            if ratio >= 0.5:
                return "score-ok"
            return "score-bad"

        train_score_class = score_class(train_passed, train_total)
        test_score_class = score_class(test_passed, test_total)
        row_class = "best-row" if iteration == best_iter else ""

        html_parts.append(f"""            <tr class="{row_class}">
                <td class="iter-col">{iteration}</td>
                <td class="score-col"><span class="score {train_score_class}">{train_passed}/{train_total}</span></td>
                <td class="score-col"><span class="score {test_score_class}">{test_passed}/{test_total} if test_total else "N/A"</span></td>
                <td class="description-col">{html.escape(description)}</td>
""")

        for qinfo in train_queries:
            r = train_by_query.get(qinfo["query"], {})
            did_pass = r.get("pass", False)
            triggers = r.get("triggers", 0)
            runs = r.get("runs", 0)
            icon = "✓" if did_pass else "✗"
            css_class = "pass" if did_pass else "fail"
            html_parts.append(
                f'                <td class="result {css_class}">{icon}<span class="rate">{triggers}/{runs}</span></td>\n'
            )

        for qinfo in test_queries:
            r = test_by_query.get(qinfo["query"], {})
            did_pass = r.get("pass", False)
            triggers = r.get("triggers", 0)
            runs = r.get("runs", 0)
            icon = "✓" if did_pass else "✗"
            css_class = "pass" if did_pass else "fail"
            html_parts.append(
                f'                <td class="result test-result {css_class}">{icon}<span class="rate">{triggers}/{runs}</span></td>\n'
            )

        html_parts.append("            </tr>\n")

    html_parts.append("""        </tbody>
    </table>
    </div>
</body>
</html>
""")

    return "".join(html_parts)


def main():
    parser = argparse.ArgumentParser(
        description="Generate HTML report from run_loop output"
    )
    parser.add_argument(
        "input", help="Path to JSON output from run_loop.py (or - for stdin)"
    )
    parser.add_argument(
        "-o", "--output", default=None, help="Output HTML file (default: stdout)"
    )
    parser.add_argument(
        "--skill-name", default="", help="Skill name to include in the report title"
    )
    args = parser.parse_args()

    if args.input == "-":
        data = json.load(sys.stdin)
    else:
        data = json.loads(Path(args.input).read_text())

    html_output = generate_html(data, skill_name=args.skill_name)

    if args.output:
        Path(args.output).write_text(html_output)
        print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(html_output)


if __name__ == "__main__":
    main()
