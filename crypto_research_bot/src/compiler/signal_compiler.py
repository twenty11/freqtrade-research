from __future__ import annotations

from domain.models.strategy_spec import SignalBlock


def _rule_expr(rule: dict) -> str:
    left = f"dataframe['{rule['left']}']"
    right = rule['right']
    right_expr = f"dataframe['{right}']" if isinstance(right, str) else repr(right)
    op = rule['op']
    if op in {">", ">=", "<", "<=", "==", "!="}:
        return f"({left} {op} {right_expr})"
    if op == "crosses_above":
        return f"(({left}.shift(1) <= {right_expr}.shift(1)) & ({left} > {right_expr}))"
    if op == "crosses_below":
        return f"(({left}.shift(1) >= {right_expr}.shift(1)) & ({left} < {right_expr}))"
    return "False"


def compile_signal(block: SignalBlock, output_col: str, tag_col: str | None = None) -> list[str]:
    rules = [{"left": r.left, "op": r.op, "right": r.right} for r in block.rules]
    exprs = [_rule_expr(r) for r in rules]
    joiner = " & " if block.logic == "all" else " | "
    combined = joiner.join(exprs) if exprs else "False"
    lines = [f"mask = {combined}", f"dataframe.loc[mask, '{output_col}'] = 1"]
    if tag_col and block.tag:
        lines.append(f"dataframe.loc[mask, '{tag_col}'] = '{block.tag}'")
    return lines
