import os
import pickle

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Olist Revenue Leakage Control Center",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stMarkdown, .stButton, .stMetric, .stSelectbox, .stSlider, .stForm {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 12% 10%, rgba(56, 189, 248, 0.12), transparent 22%),
            radial-gradient(circle at 88% 16%, rgba(34, 197, 94, 0.10), transparent 24%),
            linear-gradient(180deg, #07111f 0%, #0b1320 42%, #0f172a 100%);
        color: #f8fafc;
    }

    header[data-testid="stHeader"] {
        background: transparent;
        height: 0;
        border: none;
    }

    div[data-testid="stToolbar"] {
        visibility: hidden;
        height: 0;
    }

    .block-container {
        padding-top: 0.9rem;
        padding-bottom: 1.4rem;
        max-width: 92rem;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1020 0%, #0d1628 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.14);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.15rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stCaption,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: #e2e8f0;
    }

    section[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.95), rgba(34, 197, 94, 0.95));
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.10);
        box-shadow: 0 10px 24px rgba(14, 165, 233, 0.18);
        min-height: 48px;
        font-size: 0.95rem;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 12px 26px rgba(34, 197, 94, 0.18);
    }

    .sidebar-card {
        padding: 16px;
        border-radius: 18px;
        border: 1px solid rgba(148, 163, 184, 0.14);
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.96), rgba(30, 41, 59, 0.82));
        margin-bottom: 14px;
        animation: fadeUp 0.55s ease-out both;
    }

    .sidebar-title {
        color: #f8fafc;
        font-size: 15px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .sidebar-subtitle {
        color: #94a3b8;
        font-size: 12px;
        line-height: 1.55;
    }

    .sidebar-stat-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        margin-top: 12px;
    }

    .sidebar-stat {
        padding: 12px;
        border-radius: 14px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
    }

    .sidebar-stat .label {
        color: #94a3b8;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .sidebar-stat .value {
        color: #f8fafc;
        font-size: 18px;
        font-weight: 800;
        margin-top: 4px;
    }

    .sidebar-list {
        margin: 10px 0 0 18px;
        color: #cbd5e1;
        font-size: 12px;
        line-height: 1.6;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 30px 30px 24px 30px;
        margin-bottom: 18px;
        border-radius: 26px;
        border: 1px solid rgba(148, 163, 184, 0.14);
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.92), rgba(2, 6, 23, 0.88));
        box-shadow: 0 26px 70px rgba(0, 0, 0, 0.28);
        animation: fadeUp 0.55s ease-out both;
    }

    .hero::after {
        content: "";
        position: absolute;
        right: -40px;
        top: -40px;
        width: 180px;
        height: 180px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.20), transparent 65%);
        filter: blur(6px);
    }

    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 7px 12px;
        border-radius: 999px;
        background: rgba(45, 212, 191, 0.12);
        color: #5eead4;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        border: 1px solid rgba(45, 212, 191, 0.18);
    }

    .hero-title {
        margin-top: 14px;
        margin-bottom: 10px;
        color: #f8fafc;
        font-size: 42px;
        font-weight: 800;
        line-height: 1.05;
    }

    .hero-subtitle {
        max-width: 980px;
        color: #cbd5e1;
        font-size: 16px;
        line-height: 1.65;
    }

    .chip-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 18px;
    }

    .chip {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        border-radius: 999px;
        color: #e2e8f0;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
        font-size: 12px;
        font-weight: 600;
    }

    .panel {
        padding: 18px;
        border-radius: 22px;
        border: 1px solid rgba(148, 163, 184, 0.14);
        background: rgba(15, 23, 42, 0.74);
        box-shadow: 0 18px 42px rgba(0, 0, 0, 0.16);
        margin-bottom: 18px;
        animation: fadeUp 0.55s ease-out both;
    }

    .section-title {
        color: #f8fafc;
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .section-subtitle {
        color: #94a3b8;
        font-size: 13px;
        margin-bottom: 12px;
        line-height: 1.5;
    }

    .metric-card {
        display: flex;
        flex-direction: column;
        gap: 4px;
        min-height: 104px;
        padding: 14px 14px 12px 14px;
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        background: rgba(255, 255, 255, 0.04);
        transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(96, 165, 250, 0.35);
        box-shadow: 0 14px 28px rgba(0, 0, 0, 0.18);
    }

    .metric-label {
        color: #94a3b8;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .metric-value {
        color: #f8fafc;
        font-size: 23px;
        line-height: 1.15;
        font-weight: 800;
        word-break: keep-all;
    }

    .metric-sub {
        color: #cbd5e1;
        font-size: 12px;
        line-height: 1.4;
    }

    .info-card {
        padding: 16px;
        border-radius: 18px;
        border: 1px solid rgba(148, 163, 184, 0.14);
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.94), rgba(30, 41, 59, 0.82));
        margin-bottom: 14px;
    }

    .info-label {
        color: #94a3b8;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .info-value {
        color: #f8fafc;
        font-size: 24px;
        font-weight: 800;
        margin-top: 4px;
    }

    .info-text {
        color: #cbd5e1;
        font-size: 13px;
        line-height: 1.55;
        margin-top: 6px;
    }

    .callout {
        padding: 16px 18px;
        border-radius: 18px;
        border: 1px solid rgba(148, 163, 184, 0.14);
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.16), rgba(34, 197, 94, 0.10));
        color: #e2e8f0;
    }

    .stButton > button {
        width: 100%;
        border-radius: 14px;
        border: 1px solid rgba(148, 163, 184, 0.18);
        background: linear-gradient(135deg, #0ea5e9, #22c55e);
        color: white;
        font-weight: 700;
        padding: 0.72rem 1rem;
        transition: transform 180ms ease, box-shadow 180ms ease, opacity 180ms ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 22px rgba(34, 197, 94, 0.18);
        opacity: 0.95;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 999px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 10px 16px;
        font-weight: 700;
    }

    .stTabs [data-baseweb="tab"] * {
        color: #e2e8f0 !important;
        opacity: 1 !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(14,165,233,0.35), rgba(34,197,94,0.25));
    }

    .stTabs [aria-selected="true"] * {
        color: #ffffff !important;
    }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    path = "data/processed_fact_orders.csv"
    if os.path.exists(path):
        return pd.read_csv(path, parse_dates=["order_purchase_timestamp"])

    st.warning("Processed data not found. Please run the pipeline first. Showing a preview dataset instead.")
    dates = pd.date_range("2016-09-01", "2018-09-01", freq="D")
    np.random.seed(42)
    df = pd.DataFrame(
        {
            "order_id": [f"order_{i}" for i in range(1000)],
            "order_purchase_timestamp": np.random.choice(dates, 1000),
            "total_price": np.random.exponential(150, 1000) + 10,
            "total_freight": np.random.exponential(25, 1000) + 5,
            "review_score": np.random.choice([1, 2, 3, 4, 5], size=1000, p=[0.1, 0.05, 0.1, 0.25, 0.5]),
            "installments": np.random.randint(1, 12, 1000),
            "delay_days": np.random.choice([0, 1, 2, 5, 10], size=1000, p=[0.7, 0.1, 0.08, 0.07, 0.05]),
            "payment_type": np.random.choice(["credit_card", "boleto", "voucher", "debit_card"], 1000),
            "product_category_name_english": np.random.choice(
                ["health_beauty", "watches_gifts", "sports_leisure", "housewares", "auto"], 1000
            ),
            "seller_id": [f"seller_{np.random.randint(1, 50)}" for _ in range(1000)],
            "order_status": np.random.choice(["delivered", "canceled", "shipped"], 1000, p=[0.96, 0.03, 0.01]),
        }
    )
    df["freight_ratio"] = df["total_freight"] / df["total_price"]
    df["is_cancelled"] = df["order_status"].isin(["canceled", "unavailable"])
    df["is_late"] = df["delay_days"] > 0
    df["is_low_review"] = df["review_score"] <= 2
    df["is_high_freight_burden"] = df["freight_ratio"] > 0.3
    conditions = [
        df["is_cancelled"],
        df["is_late"] & df["is_low_review"],
        df["is_high_freight_burden"],
        df["is_low_review"],
        df["is_late"],
    ]
    choices = [
        df["total_price"],
        df["total_price"] * 0.7,
        (df["freight_ratio"] - 0.3) * df["total_price"],
        df["total_price"] * 0.2,
        df["total_price"] * 0.1,
    ]
    df["leakage_amount"] = np.select(conditions, choices, default=0)
    df["leakage_reason"] = np.select(
        conditions,
        ["Order Cancelled", "Late + Poor Review", "High Freight Burden", "Poor Review", "Late Delivery"],
        default="None",
    )
    df["order_month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
    return df


@st.cache_resource
def load_artifacts():
    clf_path = "ml/models/leakage_classifier_pipeline.pkl"
    cfg_path = "ml/models/feature_config.pkl"

    clf = None
    cfg = None
    if os.path.exists(clf_path) and os.path.exists(cfg_path):
        try:
            with open(clf_path, "rb") as f:
                clf = pickle.load(f)
            with open(cfg_path, "rb") as f:
                cfg = pickle.load(f)
        except Exception as exc:
            st.error(f"Model artifacts could not be loaded: {exc}")

    return clf, cfg


def currency(value):
    return f"R$ {value:,.2f}"


def top_reason(frame):
    series = frame.loc[frame["leakage_reason"] != "None", "leakage_reason"]
    return "None" if series.empty else series.value_counts().idxmax()


def top_category(frame):
    series = frame.loc[frame["product_category_name_english"].notna(), "product_category_name_english"]
    return "Unknown" if series.empty else frame.groupby("product_category_name_english")["leakage_amount"].sum().idxmax()


def build_signal_chart(signals):
    signal_df = pd.DataFrame(signals, columns=["Signal", "Score"])
    signal_df = signal_df.sort_values("Score", ascending=True)
    fig = px.bar(
        signal_df,
        x="Score",
        y="Signal",
        orientation="h",
        template="plotly_dark",
        color="Score",
        color_continuous_scale=["#0f172a", "#38bdf8", "#22c55e", "#f59e0b", "#ef4444"],
    )
    fig.update_layout(
        height=290,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        font={"family": "Inter", "color": "#e2e8f0"},
        xaxis_title="Signal strength",
        yaxis_title="",
    )
    return fig


def build_gauge(probability):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=probability * 100,
            number={"suffix": "%", "font": {"size": 42}},
            title={"text": "Leakage Risk Score", "font": {"size": 18, "color": "#e2e8f0"}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#94a3b8"},
                "bar": {"color": "#22c55e"},
                "bgcolor": "rgba(255,255,255,0.04)",
                "borderwidth": 1,
                "bordercolor": "rgba(148,163,184,0.25)",
                "steps": [
                    {"range": [0, 35], "color": "rgba(34, 197, 94, 0.18)"},
                    {"range": [35, 70], "color": "rgba(245, 158, 11, 0.18)"},
                    {"range": [70, 100], "color": "rgba(239, 68, 68, 0.18)"},
                ],
                "threshold": {"line": {"color": "#f8fafc", "width": 3}, "value": probability * 100},
            },
        )
    )
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=45, b=15),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter", "color": "#e2e8f0"},
    )
    return fig


def explain_inputs(total_price, total_freight, installments, delay_days, payment_type):
    freight_ratio = total_freight / total_price if total_price > 0 else 0
    signals = []
    signals.append(("Freight pressure", max(0.0, min((freight_ratio - 0.3) * 100, 100))))
    signals.append(("Delay pressure", min(delay_days * 2.0, 100)))
    signals.append(("Installment pressure", max(0.0, (installments - 10) * 8.0)))
    signals.append(("Payment friction", 20.0 if payment_type in ["voucher", "not_defined"] else 4.0))
    signals.append(("Price exposure", min(total_price / 500.0 * 10, 100)))
    return freight_ratio, signals


def predict_probability(clf, input_data, fallback_inputs):
    if clf is not None:
        return float(clf.predict_proba(input_data)[0][1]), "model"

    freight_ratio = fallback_inputs["freight_ratio"]
    delay_days = fallback_inputs["delay_days"]
    installments = fallback_inputs["installments"]
    payment_type = fallback_inputs["payment_type"]

    proba = 0.05
    if delay_days > 5:
        proba += 0.35
    if freight_ratio > 0.3:
        proba += 0.30
    if installments > 10:
        proba += 0.15
    if payment_type in ["voucher", "not_defined"]:
        proba += 0.15
    return min(proba, 0.99), "rules"


def apply_preset(preset):
    st.session_state.sim_total_price = preset["total_price"]
    st.session_state.sim_total_freight = preset["total_freight"]
    st.session_state.sim_installments = preset["installments"]
    st.session_state.sim_delay_days = preset["delay_days"]
    st.session_state.sim_payment_type = preset["payment_type"]
    st.session_state.sim_category = preset["category"]


df = load_data()
clf, config = load_artifacts()

if config is None:
    config = {
        "category_options": {
            "payment_type": sorted(df["payment_type"].dropna().unique().tolist()),
            "product_category_name_english": sorted(df["product_category_name_english"].dropna().unique().tolist()),
        }
    }

for key, value in {
    "sim_total_price": 150.0,
    "sim_total_freight": 25.0,
    "sim_installments": 3,
    "sim_delay_days": 0,
}.items():
    st.session_state.setdefault(key, value)

st.session_state.setdefault("sim_payment_type", config["category_options"]["payment_type"][0])
st.session_state.setdefault("sim_category", config["category_options"]["product_category_name_english"][0])


with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-title">Control Panel</div>
            <div class="sidebar-subtitle">
                Quick presets, live dataset context, and a short guide to the dashboard.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-title">What this dashboard shows</div>
            <div class="sidebar-subtitle">
                It converts Olist order, payment, review, and shipping data into a leakage score
                so finance and operations can spot margin loss faster.
            </div>
            <ul class="sidebar-list">
                <li>Executive KPI summary</li>
                <li>Leakage root-cause charts</li>
                <li>Seller and category drilldowns</li>
                <li>Risk simulator with mitigation guidance</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Simulator presets")
    st.caption("Use one-click scenarios to explore different risk profiles.")
    p1, p2 = st.columns(2)
    with p1:
        if st.button("Balanced", use_container_width=True, help="Low-risk transaction with healthy shipping balance"):
            apply_preset(
                {
                    "total_price": 150.0,
                    "total_freight": 20.0,
                    "installments": 3,
                    "delay_days": 0,
                    "payment_type": "credit_card",
                    "category": "health_beauty",
                }
            )
            st.rerun()
    with p2:
        if st.button("Risky", use_container_width=True, help="High-delay, high-freight transaction"):
            apply_preset(
                {
                    "total_price": 220.0,
                    "total_freight": 95.0,
                    "installments": 12,
                    "delay_days": 18,
                    "payment_type": "voucher",
                    "category": "watches_gifts",
                }
            )
            st.rerun()

    st.markdown("#### Dataset snapshot")
    s1, s2 = st.columns(2)
    with s1:
        st.markdown(
            f"""
            <div class="sidebar-stat">
                <div class="label">Orders</div>
                <div class="value">{len(df):,}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with s2:
        st.markdown(
            f"""
            <div class="sidebar-stat">
                <div class="label">Leakage orders</div>
                <div class="value">{int((df['leakage_amount'] > 0).sum()):,}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="sidebar-stat" style="margin-top:10px;">
            <div class="label">Top reason</div>
            <div class="value" style="font-size:16px;">{top_reason(df)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="sidebar-stat" style="margin-top:10px;">
            <div class="label">Top category</div>
            <div class="value" style="font-size:16px;">{top_category(df)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
<div class="hero">
    <div class="eyebrow">Revenue intelligence dashboard</div>
    <div class="hero-title">Olist Revenue Leakage Control Center</div>
    <div class="hero-subtitle">
        A finance and operations cockpit that turns Olist order data into leakage insights.
        Use it to see what is driving margin loss, where the biggest risks are, and how much
        value can be recovered by acting earlier.
    </div>
    <div class="chip-row">
        <div class="chip">Executive KPI overview</div>
        <div class="chip">Leakage root-cause analysis</div>
        <div class="chip">Risk simulator</div>
        <div class="chip">Business impact summary</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)


total_rev = df["total_price"].sum()
total_leak = df["leakage_amount"].sum()
leakage_pct = (total_leak / total_rev) * 100 if total_rev > 0 else 0
recovery_opp = total_leak * 0.5
avg_score = df["review_score"].mean()


st.markdown("### Executive Snapshot")
st.markdown(
    """
    <div class="info-card" style="margin-bottom:18px;">
        <div class="info-label">How to use this dashboard</div>
        <div class="info-text">
            1. Review the KPI cards to understand the overall leakage picture.<br/>
            2. Open the Drivers tab to see which categories and sellers need attention.<br/>
            3. Use the Risk Simulator to test a transaction and see the likely impact.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
m1, m2, m3, m4 = st.columns(4)
metric_data = [
    ("Gross Revenue", currency(total_rev), "Total billing volume in the processed fact table."),
    ("Estimated Leakage", currency(total_leak), f"{leakage_pct:.2f}% of revenue is exposed to loss signals."),
    ("Recovery Opportunity", currency(recovery_opp), "A conservative 50% recovery estimate."),
    ("Average Review Score", f"{avg_score:.2f}/5", "Customer sentiment proxy."),
]
for col, (label, value, note) in zip([m1, m2, m3, m4], metric_data):
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-sub">{note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


tab_overview, tab_drivers, tab_simulator, tab_impact = st.tabs(
    ["📊 Overview", "🔎 Drivers", "🧠 Risk Simulator", "💼 Impact"]
)


with tab_overview:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    left, right = st.columns([1.1, 0.9])

    with left:
        st.markdown('<div class="section-title">Leakage by root cause</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">This shows the operational issues contributing the most margin loss.</div>', unsafe_allow_html=True)
        reason_df = (
            df[df["leakage_reason"] != "None"]
            .groupby("leakage_reason")["leakage_amount"]
            .sum()
            .sort_values(ascending=True)
            .reset_index()
        )
        fig_reason = px.bar(
            reason_df,
            x="leakage_amount",
            y="leakage_reason",
            orientation="h",
            color="leakage_amount",
            color_continuous_scale=["#0f172a", "#38bdf8", "#22c55e", "#f59e0b", "#ef4444"],
            template="plotly_dark",
        )
        fig_reason.update_layout(
            height=390,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            font={"family": "Inter", "color": "#e2e8f0"},
            xaxis_title="Leakage Amount (R$)",
            yaxis_title="",
        )
        st.plotly_chart(fig_reason, use_container_width=True)

    with right:
        st.markdown('<div class="section-title">Monthly leakage trend</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Trend lines help teams see if leakage is improving or worsening over time.</div>', unsafe_allow_html=True)
        trend = df.groupby("order_month")["leakage_amount"].sum().reset_index().sort_values("order_month")
        fig_trend = px.area(trend, x="order_month", y="leakage_amount", template="plotly_dark")
        fig_trend.update_traces(line_color="#38bdf8", fillcolor="rgba(56, 189, 248, 0.22)")
        fig_trend.update_layout(
            height=240,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"family": "Inter", "color": "#e2e8f0"},
            xaxis_title="Month",
            yaxis_title="Leakage Amount (R$)",
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        mix = pd.DataFrame(
            {
                "Signal": ["Late orders", "Cancelled orders", "Freight burden"],
                "Share": [
                    (df["is_late"].sum() / len(df)) * 100,
                    (df["is_cancelled"].sum() / len(df)) * 100,
                    (df["is_high_freight_burden"].sum() / len(df)) * 100,
                ],
            }
        )
        fig_mix = px.bar(
            mix,
            x="Share",
            y="Signal",
            orientation="h",
            template="plotly_dark",
            color="Share",
            color_continuous_scale=["#0f172a", "#22c55e", "#f59e0b", "#ef4444"],
        )
        fig_mix.update_layout(
            height=185,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            font={"family": "Inter", "color": "#e2e8f0"},
            xaxis_title="% of orders",
            yaxis_title="",
        )
        st.plotly_chart(fig_mix, use_container_width=True)

    st.markdown(
        f"""
        <div class="callout">
            💡 Executive takeaway: <strong>{top_reason(df)}</strong> is the biggest leakage driver.
            The fastest recovery path is to reduce freight burden, improve delivery reliability, and
            target sellers with repeated leakage exposure.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


with tab_drivers:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    left, right = st.columns([1.05, 0.95])

    with left:
        st.markdown('<div class="section-title">Top categories by leakage</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">These categories deserve the first intervention pass.</div>', unsafe_allow_html=True)
        cat_df = (
            df.groupby("product_category_name_english")["leakage_amount"]
            .sum()
            .nlargest(10)
            .sort_values()
            .reset_index()
        )
        fig_cat = px.bar(
            cat_df,
            x="leakage_amount",
            y="product_category_name_english",
            orientation="h",
            color="leakage_amount",
            color_continuous_scale=["#0f172a", "#a78bfa", "#38bdf8", "#22c55e"],
            template="plotly_dark",
        )
        fig_cat.update_layout(
            height=410,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            font={"family": "Inter", "color": "#e2e8f0"},
            xaxis_title="Leakage Amount (R$)",
            yaxis_title="",
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with right:
        st.markdown('<div class="section-title">High-risk sellers</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Use this for operational coaching and SLA reviews.</div>', unsafe_allow_html=True)
        seller_df = df.groupby("seller_id").agg(
            total_leakage=("leakage_amount", "sum"),
            orders_handled=("order_id", "count"),
            avg_review_rating=("review_score", "mean"),
        ).nlargest(10, "total_leakage").reset_index()

        seller_view = seller_df.copy()
        seller_view["total_leakage"] = seller_view["total_leakage"].map(lambda x: f"R$ {x:,.2f}")
        seller_view["avg_review_rating"] = seller_view["avg_review_rating"].map(lambda x: f"{x:.2f} / 5")
        seller_view.columns = ["Seller ID", "Total Leakage", "Orders", "Avg Review"]
        st.dataframe(seller_view, use_container_width=True, height=350)

        st.markdown(
            """
            <div class="info-card">
                <div class="info-label">Interpretation</div>
                <div class="info-text">
                    Sellers with repeated leakage exposure should be reviewed for dispatch delays,
                    packaging inefficiency, and freight imbalance. This is the fastest path to
                    operational savings.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


with tab_simulator:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Transaction risk simulator</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Fill the form, then click Analyze Transaction to get a prediction and an explanation.</div>', unsafe_allow_html=True)

    input_col, output_col = st.columns([0.92, 1.08])

    with input_col:
        with st.form("risk_form", clear_on_submit=False):
            st.markdown("#### Input transaction")
            total_price = st.number_input(
                "Transaction price (R$)",
                min_value=1.0,
                max_value=50000.0,
                value=float(st.session_state.sim_total_price),
                step=5.0,
            )
            total_freight = st.number_input(
                "Freight charge (R$)",
                min_value=0.0,
                max_value=20000.0,
                value=float(st.session_state.sim_total_freight),
                step=1.0,
            )
            installments = st.slider("Installments", 1, 24, int(st.session_state.sim_installments))
            delay_days = st.slider("Delivery delay (days)", 0, 90, int(st.session_state.sim_delay_days))
            payment_type = st.selectbox(
                "Payment type",
                config["category_options"]["payment_type"],
                index=config["category_options"]["payment_type"].index(st.session_state.sim_payment_type)
                if st.session_state.sim_payment_type in config["category_options"]["payment_type"]
                else 0,
            )
            category = st.selectbox(
                "Product category",
                config["category_options"]["product_category_name_english"],
                index=config["category_options"]["product_category_name_english"].index(st.session_state.sim_category)
                if st.session_state.sim_category in config["category_options"]["product_category_name_english"]
                else 0,
            )
            submitted = st.form_submit_button("Analyze Transaction")

    if submitted:
        freight_ratio, signal_bars = explain_inputs(total_price, total_freight, installments, delay_days, payment_type)
        input_df = pd.DataFrame(
            [
                {
                    "total_price": total_price,
                    "total_freight": total_freight,
                    "freight_ratio": freight_ratio,
                    "installments": installments,
                    "delay_days": delay_days,
                    "payment_type": payment_type,
                    "product_category_name_english": category,
                }
            ]
        )

        probability, source = predict_probability(
            clf,
            input_df,
            {
                "freight_ratio": freight_ratio,
                "delay_days": delay_days,
                "installments": installments,
                "payment_type": payment_type,
            },
        )
        risk_label = "HIGH RISK" if probability >= 0.5 else "LOW RISK"
        impact = min(total_price * 0.7, total_price) if risk_label == "HIGH RISK" else total_price * 0.1

        st.session_state.sim_result = {
            "probability": probability,
            "risk_label": risk_label,
            "source": source,
            "freight_ratio": freight_ratio,
            "signal_bars": signal_bars,
            "impact": impact,
            "recommendations": (
                [
                    "Review fulfillment and delivery routing immediately.",
                    "Check if freight is too high relative to item value.",
                    "Validate payment and installment friction before execution.",
                ]
                if risk_label == "HIGH RISK"
                else [
                    "Proceed with standard fulfillment.",
                    "Monitor freight ratio and delivery timing.",
                    "No urgent intervention required.",
                ]
            ),
            "input_row": {
                "risk_label": risk_label,
                "probability": round(probability, 4),
                "total_price": total_price,
                "total_freight": total_freight,
                "freight_ratio": round(freight_ratio, 4),
                "installments": installments,
                "delay_days": delay_days,
                "payment_type": payment_type,
                "product_category_name_english": category,
            },
        }

    result = st.session_state.get("sim_result")

    with output_col:
        if result:
            st.plotly_chart(build_gauge(result["probability"]), use_container_width=True)
            st.markdown(
                f"""
                <div class="info-card">
                    <div class="info-label">Prediction result</div>
                    <div class="info-value">{result["risk_label"]}</div>
                    <div class="info-text">
                        Source: {"Serialized model" if result["source"] == "model" else "Rule-based fallback"}<br/>
                        Probability: {result["probability"]*100:.1f}%<br/>
                        Freight ratio: {result["freight_ratio"]:.1%}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="info-card">
                    <div class="info-label">Prediction result</div>
                    <div class="info-value">Waiting</div>
                    <div class="info-text">
                        Submit the form to generate a risk score, business explanation, and recommended actions.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.plotly_chart(build_gauge(0.0), use_container_width=True)

    if result:
        st.divider()
        st.markdown("#### Result explanation")
        signal_fig = build_signal_chart(result["signal_bars"])
        explain_left, explain_right = st.columns([1, 1])

        with explain_left:
            st.plotly_chart(signal_fig, use_container_width=True)
        with explain_right:
            if result["risk_label"] == "HIGH RISK":
                st.error(f"High leakage risk detected: {result['probability']*100:.1f}%")
            else:
                st.success(f"Low leakage risk profile: {result['probability']*100:.1f}%")

            st.markdown("#### Recommended actions")
            for idx, rec in enumerate(result["recommendations"], 1):
                st.markdown(f"- **Action {idx}:** {rec}")

            st.markdown(
                f"""
                <div class="callout">
                    💼 Estimated business impact: up to <strong>{currency(result["impact"])}</strong>
                    in avoidable or recoverable margin for this transaction profile.
                </div>
                """,
                unsafe_allow_html=True,
            )

            export_df = pd.DataFrame(
                [result["input_row"]]
            )
            st.download_button(
                "Download prediction result",
                data=export_df.to_csv(index=False).encode("utf-8"),
                file_name="leakage_prediction.csv",
                mime="text/csv",
                use_container_width=True,
            )
    else:
        st.info("Click Analyze Transaction to generate a prediction, explanation, and business impact estimate.")

    st.markdown("</div>", unsafe_allow_html=True)


with tab_impact:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    left, right = st.columns([1, 1])

    with left:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">Key insights</div>
                <div class="info-text">
                    - <strong>{top_reason(df)}</strong> is the biggest leakage driver.<br/>
                    - Late deliveries and poor reviews are strong customer-friction signals.<br/>
                    - Freight burden above 30% is a major margin pressure point.<br/>
                    - A smaller set of sellers and categories drives most of the exposure.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="info-card">
                <div class="info-label">Business impact</div>
                <div class="info-text">
                    - Helps finance quantify invisible margin loss.<br/>
                    - Helps operations focus on routing, SLA, and seller issues.<br/>
                    - Supports earlier interventions before refunds and churn happen.<br/>
                    - Makes leakage reporting repeatable and easy to share with leadership.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">Outcome summary</div>
                <div class="info-text">
                    <strong>Processed dataset:</strong> {len(df):,} orders<br/>
                    <strong>Leakage orders:</strong> {(df['leakage_amount'] > 0).sum():,}<br/>
                    <strong>Gross leakage:</strong> {currency(total_leak)}<br/>
                    <strong>Recovery opportunity:</strong> {currency(recovery_opp)}<br/>
                    <strong>Average review score:</strong> {avg_score:.2f}/5
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="info-card">
                <div class="info-label">Real-world value</div>
                <div class="info-text">
                    This project behaves like a margin-ops control tower. It transforms order,
                    payment, logistics, and review data into a practical leakage score that can
                    guide finance and operations teams toward faster recovery and better prioritization.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)
