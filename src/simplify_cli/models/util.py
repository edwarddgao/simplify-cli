from __future__ import annotations


def format_salary(low: float | None, high: float | None, currency: str = "") -> str:
    if not low and not high:
        return ""
    sym = "$" if currency == "USD" else (currency + " " if currency else "$")
    if low and high:
        return f"{sym}{low:,.0f}–{sym}{high:,.0f}"
    if low:
        return f"{sym}{low:,.0f}+"
    return ""
