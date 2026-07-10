"""
===========================================================
Metric Card Component
-----------------------------------------------------------
Reusable KPI Cards for Enterprise Dashboard

Author  : Gurrala Nikhil Reddy
Version : 1.0.0
===========================================================
"""

from __future__ import annotations

import streamlit as st
import textwrap


# ==========================================================
# Card Color Mapping
# ==========================================================

COLOR_MAP = {
    "primary": "#6366F1",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
}


ICON_MAP = {
    "transactions": """<svg style="width:24px;height:24px;stroke:var(--accent);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;" viewBox="0 0 24 24"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/></svg>""",
    "💳": """<svg style="width:24px;height:24px;stroke:var(--accent);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;" viewBox="0 0 24 24"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/></svg>""",
    "fraud": """<svg style="width:24px;height:24px;stroke:var(--danger);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;" viewBox="0 0 24 24"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/></svg>""",
    "🚨": """<svg style="width:24px;height:24px;stroke:var(--danger);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;" viewBox="0 0 24 24"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/></svg>""",
    "🔴": """<svg style="width:24px;height:24px;stroke:var(--danger);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;" viewBox="0 0 24 24"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/></svg>""",
    "safe": """<svg style="width:24px;height:24px;stroke:var(--success);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>""",
    "🛡️": """<svg style="width:24px;height:24px;stroke:var(--success);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>""",
    "🟢": """<svg style="width:24px;height:24px;stroke:var(--success);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>""",
    "risk": """<svg style="width:24px;height:24px;stroke:var(--warning);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;" viewBox="0 0 24 24"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>""",
    "⚠️": """<svg style="width:24px;height:24px;stroke:var(--warning);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;" viewBox="0 0 24 24"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>""",
    "🟡": """<svg style="width:24px;height:24px;stroke:var(--warning);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;" viewBox="0 0 24 24"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>""",
    "orange_circle": """<svg style="width:24px;height:24px;stroke:var(--primary);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/></svg>""",
    "🟠": """<svg style="width:24px;height:24px;stroke:var(--primary);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/></svg>""",
    "prediction": """<svg style="width:24px;height:24px;stroke:var(--accent);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;" viewBox="0 0 24 24"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M9 13h.01M15 13h.01M10 17h4"/></svg>""",
    "🤖": """<svg style="width:24px;height:24px;stroke:var(--accent);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;" viewBox="0 0 24 24"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M9 13h.01M15 13h.01M10 17h4"/></svg>""",
    "report": """<svg style="width:24px;height:24px;stroke:var(--primary);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;" viewBox="0 0 24 24"><line x1="18" x2="18" y1="20" y2="10"/><line x1="12" x2="12" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="14"/></svg>""",
    "📊": """<svg style="width:24px;height:24px;stroke:var(--primary);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;" viewBox="0 0 24 24"><line x1="18" x2="18" y1="20" y2="10"/><line x1="12" x2="12" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="14"/></svg>""",
    "model": """<svg style="width:24px;height:24px;stroke:var(--primary);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;" viewBox="0 0 24 24"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/><path d="M12 6v6l4 2"/></svg>""",
    "🧠": """<svg style="width:24px;height:24px;stroke:var(--primary);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;" viewBox="0 0 24 24"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/><path d="M12 6v6l4 2"/></svg>""",
    "performance": """<svg style="width:24px;height:24px;stroke:var(--accent);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;" viewBox="0 0 24 24"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>""",
    "📈": """<svg style="width:24px;height:24px;stroke:var(--accent);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;" viewBox="0 0 24 24"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>""",
}


# ==========================================================
# Metric Card
# ==========================================================

def metric_card(
    title: str,
    value: str | int | float,
    icon: str = "report",
    color: str = "primary",
    delta: str | None = None,
    help_text: str | None = None,
):
    """
    Display an enterprise KPI card.
    """

    border = COLOR_MAP.get(color, COLOR_MAP["primary"])

    svg_icon = ICON_MAP.get(icon, ICON_MAP.get("report", ""))
    if not svg_icon and icon.startswith("<svg"):
        svg_icon = icon
    elif not svg_icon:
        svg_icon = f'<span style="font-size:24px;">{icon}</span>'

    html = (
        f'<div class="kpi-card" style="border-left:6px solid {border}; padding: 20px; background: rgba(30, 41, 59, 0.7); border-radius: 12px; margin-bottom: 15px;">'
        f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">'
        f'<span class="kpi-title" style="font-size: 14px; color: var(--text-secondary); font-weight: 500;">{title}</span>'
        f'<div style="display:inline-flex; align-items:center;">{svg_icon}</div>'
        f'</div>'
        f'<div class="kpi-value" style="font-size: 28px; font-weight: 700; color: white;">{value}</div>'
    )

    if delta:
        html += f'<div class="kpi-change" style="font-size: 13px; color: var(--text-secondary); margin-top: 5px;">{delta}</div>'

    html += "</div>"

    clean_html = textwrap.dedent(html).strip()
    st.markdown(clean_html, unsafe_allow_html=True)

    if help_text:

        st.caption(help_text)


# ==========================================================
# KPI Grid
# ==========================================================

def metric_grid(metrics: list[dict]):
    """
    Display four metric cards in one row.

    Parameters
    ----------
    metrics : list

    Example
    -------

    [
        {
            "title":"Transactions",
            "value":"284,291",
            "icon":"💳",
            "color":"primary"
        }
    ]
    """

    cols = st.columns(len(metrics))

    for col, metric in zip(cols, metrics):

        with col:

            metric_card(
                title=metric.get("title", ""),
                value=metric.get("value", ""),
                icon=metric.get("icon", "📊"),
                color=metric.get("color", "primary"),
                delta=metric.get("delta"),
                help_text=metric.get("help"),
            )


# ==========================================================
# Placeholder Dashboard KPIs
# ==========================================================

def demo_metrics():
    """
    Placeholder cards until
    dashboard is connected
    with CSV reports.
    """

    metrics = [

        {
            "title": "Total Transactions",
            "value": "0",
            "icon": "transactions",
            "color": "primary",
            "delta": "--",
        },

        {
            "title": "Fraud Alerts",
            "value": "0",
            "icon": "fraud",
            "color": "danger",
            "delta": "--",
        },

        {
            "title": "High Risk",
            "value": "0",
            "icon": "risk",
            "color": "warning",
            "delta": "--",
        },

        {
            "title": "Safe Transactions",
            "value": "0",
            "icon": "safe",
            "color": "success",
            "delta": "--",
        },

    ]

    metric_grid(metrics)