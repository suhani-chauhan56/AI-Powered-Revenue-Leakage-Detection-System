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

    html, body, [class*="css"], .stMarkdown, .stButton, .stMetric, .stSelectbox, .stSlider {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(20, 184, 166, 0.14), transparent 30%),
            radial-gradient(circle at top right, rgba(59, 130, 246, 0.16), transparent 28%),
            linear-gradient(180deg, #07111f 0%, #0b1320 45%, #0f172a 100%);
        color: #f8fafc;
    }

    .hero {
        padding: 28px 28px 18px 28px;
        border: 1px solid rgba(255,255,255,0.08);
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.82), rgba(2, 6, 23, 0.88));
        border-radius: 24px;
        box-shadow: 0 24px 60px rgba(0, 0, 0, 0.25);
        margin-bottom: 18px;
    }

    .eyebrow {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        background: rgba(45, 212, 191, 0.12);
        color: #5eead4;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        border: 1px solid rgba(45, 212, 191, 0.20);
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        line-height: 1.05;
        margin: 12px 0 10px 0;
        color: #f8fafc;
    }

    .hero-subtitle {
        color: #cbd5e1;
        font-size: 16px;
        line-height: 1.65;
        max-width: 980px;
    }

    .pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 18px;
    }

    .pill {
        padding: 8px 12px;
        border-radius: 999px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        color: #e2e8f0;
        font-size: 12px;
        font-weight: 600;
    }

    .panel {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.16);
        border-radius: 22px;
        padding: 18px 18px 14px 18px;
        box-shadow: 0 20px 44px rgba(0, 0, 0, 0.16);
    }

    .section-title {
        font-size: 18px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 6px;
    }

    .section-subtitle {
        color: #94a3b8;
        font-size: 13px;
        margin-bottom: 14px;
    }

    .insight-card {
        padding: 16px;
        border-radius: 18px;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.94), rgba(30, 41, 59, 0.86));
        border: 1px solid rgba(148, 163, 184, 0.16);
        margin-bottom: 14px;
    }

    .insight-label {
        color: #94a3b8;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 700;
    }

    .insight-value {
        color: #f8fafc;
        font-size: 26px;
        font-weight: 800;
        margin-top: 4px;
    }

    .insight-note {
        color: #cbd5e1;
        font-size: 13px;
        margin-top: 6px;
        line-height: 1.5;
    }

    .callout {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.18), rgba(34, 197, 94, 0.12));
        border: 1px solid rgba(148, 163, 184, 0.18);
        color: #e2e8f0;
        border-radius: 18px;
        padding: 16px 18px;
    }

    .small-metric {
        display: flex;
        flex-direction: column;
        gap: 4px;
        padding: 14px 16px;
        border-radius: 16px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        min-height: 104px;
    }

    .small-metric .label {
        color: #94a3b8;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 700;
    }

    .small-metric .value {
        color: #f8fafc;
        font-size: 28px;
        font-weight: 800;
        line-height: 1.1;
    }

    .small-metric .sub {
        color: #cbd5e1;
        font-size: 13px;
    }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    csv_path = "data/processed_fact_orders.csv"
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path, parse_dates=["order_purchase_timestamp"])

    st.warning(
        "Processed order data not found. Please run the ETL pipeline first. "
        "A simulated preview dataset is being loaded so the UI remains usable."
    )
    dates = pd.date_range(start="2016-09-01", end="2018-09-01", freq="D")
    np.random.seed(42)
    mock_df = pd.DataFrame(
        {
            "order_id": [f"order_{i}" for i in range(1000)],
            "order_purchase_timestamp": np.random.choice(dates, 1000),
            "total_price": np.random.exponential(150, 1000) + 10,
            "total_freight": np.random.exponential(25, 1000) + 5,
            "review_score": np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.05, 0.1, 0.25, 0.5], size=1000),
            "installments": np.random.randint(1, 12, 1000),
            "delay_days": np.random.choice([0, 1, 2, 5, 10], p=[0.7, 0.1, 0.08, 0.07, 0.05], size=1000),
            "payment_type": np.random.choice(["credit_card", "boleto", "voucher", "debit_card"], 1000),
            "product_category_name_english": np.random.choice(
                ["health_beauty", "watches_gifts", "sports_leisure", "housewares", "auto"], 1000
            ),
            "seller_id": [f"seller_{np.random.randint(1, 50)}" for _ in range(1000)],
            "order_status": np.random.choice(["delivered", "canceled", "shipped"], p=[0.96, 0.03, 0.01], size=1000),
        }
    )
    mock_df["freight_ratio"] = mock_df["total_freight"] / mock_df["total_price"]
    mock_df["is_cancelled"] = mock_df["order_status"].isin(["canceled", "unavailable"])
    mock_df["is_late"] = mock_df["delay_days"] > 0
    mock_df["is_low_review"] = mock_df["review_score"] <= 2
    mock_df["is_high_freight_burden"] = mock_df["freight_ratio"] > 0.3
    conditions = [
        mock_df["is_cancelled"],
        mock_df["is_late"] & mock_df["is_low_review"],
        mock_df["is_high_freight_burden"],
        mock_df["is_low_review"],
        mock_df["is_late"],
    ]
    choices = [
        mock_df["total_price"],
        mock_df["total_price"] * 0.7,
        (mock_df["freight_ratio"] - 0.3) * mock_df["total_price"],
        mock_df["total_price"] * 0.2,
        mock_df["total_price"] * 0.1,
    ]
    mock_df["leakage_amount"] = np.select(conditions, choices, default=0)
    mock_df["leakage_reason"] = np.select(
        conditions,
        ["Order Cancelled", "Late + Poor Review", "High Freight Burden", "Poor Review", "Late Delivery"],
        default="None",
    )
    mock_df["order_month"] = mock_df["order_purchase_timestamp"].dt.to_period("M").astype(str)
    return mock_df


def load_artifacts():
    clf_path = "ml/models/leakage_classifier_pipeline.pkl"
    cfg_path = "ml/models/feature_config.pkl"

    clf = None
    config = None
    if os.path.exists(clf_path) and os.path.exists(cfg_path):
        try:
            with open(clf_path, "rb") as f:
                clf = pickle.load(f)
            with open(cfg_path, "rb") as f:
                config = pickle.load(f)
        except Exception as e:
            st.error(f"Failed to load model artifacts: {e}")

    return clf, config


def apply_preset(preset):
    st.session_state.total_price = preset["total_price"]
    st.session_state.total_freight = preset["total_freight"]
    st.session_state.installments = preset["installments"]
    st.session_state.delay_days = preset["delay_days"]
    st.session_state.payment_type = preset["payment_type"]
    st.session_state.category = preset["category"]


def get_prediction(clf, input_data, fallback_inputs):
    if clf is not None:
        proba = float(clf.predict_proba(input_data)[0][1])
        return proba, "model"

    total_price = fallback_inputs["total_price"]
    total_freight = fallback_inputs["total_freight"]
    installments = fallback_inputs["installments"]
    delay_days = fallback_inputs["delay_days"]
    payment_type = fallback_inputs["payment_type"]
    freight_ratio = total_freight / total_price if total_price > 0 else 0

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


def build_gauge(probability):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=probability * 100,
            number={"suffix": "%", "font": {"size": 44}},
            title={"text": "Leakage Risk Score", "font": {"size": 18, "color": "#e2e8f0"}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#94a3b8"},
                "bar": {"color": "#22c55e"},
                "bgcolor": "rgba(255,255,255,0.04)",
                "borderwidth": 1,
                "bordercolor": "rgba(148,163,184,0.30)",
                "steps": [
                    {"range": [0, 35], "color": "rgba(34, 197, 94, 0.18)"},
                    {"range": [35, 70], "color": "rgba(245, 158, 11, 0.18)"},
                    {"range": [70, 100], "color": "rgba(239, 68, 68, 0.20)"},
                ],
                "threshold": {"line": {"color": "#f8fafc", "width": 3}, "value": probability * 100},
            },
        )
    )
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=15),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter", "color": "#e2e8f0"},
    )
    return fig


def fmt_currency(value):
    return f"R$ {value:,.2f}"


def get_top_reason(frame):
    reasons = frame.loc[frame["leakage_reason"] != "None", "leakage_reason"]
    if reasons.empty:
        return "None"
    return reasons.value_counts().idxmax()


df = load_data()
clf, config = load_artifacts()

if config is None:
    config = {
        "category_options": {
            "payment_type": sorted(df["payment_type"].dropna().unique().tolist()),
            "product_category_name_english": sorted(df["product_category_name_english"].dropna().unique().tolist()),
        }
    }

if "total_price" not in st.session_state:
    st.session_state.total_price = 150.0
if "total_freight" not in st.session_state:
    st.session_state.total_freight = 25.0
if "installments" not in st.session_state:
    st.session_state.installments = 3
if "delay_days" not in st.session_state:
    st.session_state.delay_days = 0
if "payment_type" not in st.session_state:
    st.session_state.payment_type = config["category_options"]["payment_type"][0]
if "category" not in st.session_state:
    st.session_state.category = config["category_options"]["product_category_name_english"][0]


presets = {
    "Balanced order": {
        "total_price": 150.0,
        "total_freight": 20.0,
        "installments": 3,
        "delay_days": 0,
        "payment_type": "credit_card",
        "category": "health_beauty",
    },
    "Operational risk": {
        "total_price": 220.0,
        "total_freight": 95.0,
        "installments": 12,
        "delay_days": 18,
        "payment_type": "voucher",
        "category": "watches_gifts",
    },
    "High freight burden": {
        "total_price": 120.0,
        "total_freight": 60.0,
        "installments": 6,
        "delay_days": 2,
        "payment_type": "credit_card",
        "category": "housewares",
    },
}


with st.sidebar:
    st.markdown("### Control Panel")
    st.caption("Use quick presets or tune the live simulator.")

    st.markdown("#### Quick Scenario")
    cols = st.columns(3)
    with cols[0]:
        if st.button("Balanced", use_container_width=True):
            apply_preset(presets["Balanced order"])
            st.rerun()
    with cols[1]:
        if st.button("Risky", use_container_width=True):
            apply_preset(presets["Operational risk"])
            st.rerun()
    with cols[2]:
        if st.button("Freight", use_container_width=True):
            apply_preset(presets["High freight burden"])
            st.rerun()

    st.markdown("#### Data Snapshot")
    st.metric("Orders", f"{len(df):,}")
    st.metric("Leakage Orders", f"{int((df['leakage_amount'] > 0).sum()):,}")
    st.metric("Avg Review", f"{df['review_score'].mean():.2f}/5")
    st.metric("Top Reason", get_top_reason(df))


st.markdown(
    """
<div class="hero">
    <span class="eyebrow">Revenue Intelligence Dashboard</span>
    <div class="hero-title">Olist Revenue Leakage Control Center</div>
    <div class="hero-subtitle">
        A decision-ready analytics cockpit that combines ETL, leakage scoring, executive KPIs,
        and a live transaction risk simulator. Built for finance and operations teams that want
        to identify margin loss before it becomes a recurring cost.
    </div>
    <div class="pill-row">
        <div class="pill">Leakage Proxies</div>
        <div class="pill">Predictive Risk Scoring</div>
        <div class="pill">Seller and Category Drilldowns</div>
        <div class="pill">Business Impact View</div>
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
late_share = (df["is_late"].sum() / len(df)) * 100 if "is_late" in df.columns else 0
cancel_share = (df["is_cancelled"].sum() / len(df)) * 100 if "is_cancelled" in df.columns else 0
freight_burden_share = (df["is_high_freight_burden"].sum() / len(df)) * 100 if "is_high_freight_burden" in df.columns else 0


st.markdown("### Executive Snapshot")
snap1, snap2, snap3, snap4 = st.columns(4)
snapshot_data = [
    (snap1, "Gross Revenue", fmt_currency(total_rev), "Total billing volume across the fact table."),
    (snap2, "Estimated Leakage", fmt_currency(total_leak), f"{leakage_pct:.2f}% of revenue is exposed to loss signals."),
    (snap3, "Recovery Opportunity", fmt_currency(recovery_opp), "A conservative 50% recovery assumption."),
    (snap4, "Average Review Score", f"{avg_score:.2f}/5", "Customer satisfaction proxy."),
]

for col, label, value, note in snapshot_data:
    with col:
        st.markdown(
            f"""
            <div class="small-metric">
                <div class="label">{label}</div>
                <div class="value">{value}</div>
                <div class="sub">{note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Executive Summary",
        "🔎 Leakage Drivers",
        "🧠 Risk Simulator",
        "💼 Business Impact",
    ]
)


with tab1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    left, right = st.columns([1.08, 0.92])

    with left:
        st.markdown('<div class="section-title">Where the leakage is coming from</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">A clean view of operational pressure points across the order book.</div>', unsafe_allow_html=True)
        reason_df = (
            df[df.leakage_reason != "None"]
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
            color_continuous_scale=["#0f172a", "#14b8a6", "#22c55e", "#f59e0b", "#ef4444"],
            template="plotly_dark",
        )
        fig_reason.update_layout(
            height=410,
            margin=dict(l=10, r=10, t=5, b=5),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            font={"family": "Inter", "color": "#e2e8f0"},
            xaxis_title="Leakage Amount (R$)",
            yaxis_title="Root Cause",
        )
        st.plotly_chart(fig_reason, use_container_width=True)

    with right:
        st.markdown('<div class="section-title">Business health overview</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">The dashboard highlights both leakage exposure and quality signals.</div>', unsafe_allow_html=True)

        trend = df.groupby("order_month")["leakage_amount"].sum().reset_index().sort_values("order_month")
        fig_trend = px.area(
            trend,
            x="order_month",
            y="leakage_amount",
            template="plotly_dark",
        )
        fig_trend.update_traces(line_color="#38bdf8", fillcolor="rgba(56, 189, 248, 0.20)")
        fig_trend.update_layout(
            height=245,
            margin=dict(l=10, r=10, t=5, b=5),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"family": "Inter", "color": "#e2e8f0"},
            xaxis_title="Month",
            yaxis_title="Leakage Amount (R$)",
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        review_mix = pd.DataFrame(
            {
                "Signal": ["Late Orders", "Cancelled Orders", "Freight Burden"],
                "Share": [late_share, cancel_share, freight_burden_share],
            }
        )
        fig_mix = px.bar(
            review_mix,
            x="Share",
            y="Signal",
            orientation="h",
            template="plotly_dark",
            color="Share",
            color_continuous_scale=["#0f172a", "#22c55e", "#f59e0b", "#ef4444"],
        )
        fig_mix.update_layout(
            height=185,
            margin=dict(l=10, r=10, t=5, b=5),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            font={"family": "Inter", "color": "#e2e8f0"},
            xaxis_title="% of Orders",
            yaxis_title="",
        )
        st.plotly_chart(fig_mix, use_container_width=True)

    st.markdown(
        f"""
        <div class="callout">
            💡 <strong>Executive takeaway:</strong> the largest recovery levers are concentrated in
            <strong>{get_top_reason(df)}</strong>,
            late-delivery friction, and shipping cost pressure. Together they represent the most direct
            margin recovery path for operations and finance teams.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


with tab2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    left, right = st.columns([1.1, 0.9])

    with left:
        st.markdown('<div class="section-title">Top product categories by leakage</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">This helps teams decide where to focus catalog-level interventions.</div>', unsafe_allow_html=True)
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
            height=420,
            margin=dict(l=10, r=10, t=5, b=5),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            font={"family": "Inter", "color": "#e2e8f0"},
            xaxis_title="Leakage Amount (R$)",
            yaxis_title="Category",
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with right:
        st.markdown('<div class="section-title">High-risk sellers</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Seller-level view for operational coaching and SLA reviews.</div>', unsafe_allow_html=True)
        seller_df = df.groupby("seller_id").agg(
            total_leakage=("leakage_amount", "sum"),
            orders_handled=("order_id", "count"),
            avg_review_rating=("review_score", "mean"),
        ).nlargest(10, "total_leakage").reset_index()

        seller_df_display = seller_df.copy()
        seller_df_display["total_leakage"] = seller_df_display["total_leakage"].map(lambda x: f"R$ {x:,.2f}")
        seller_df_display["avg_review_rating"] = seller_df_display["avg_review_rating"].map(lambda x: f"{x:.2f} / 5")
        seller_df_display.columns = ["Seller ID", "Total Leakage", "Orders", "Avg Review"]
        st.dataframe(seller_df_display, use_container_width=True, height=350)

        st.markdown(
            """
            <div class="insight-card">
                <div class="insight-label">Operational interpretation</div>
                <div class="insight-note">
                    Sellers with repeated leakage exposure should be reviewed for dispatch SLA issues,
                    packaging delays, and freight imbalance. This is where logistics and vendor management
                    teams can act fastest.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


with tab3:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Predictive risk simulator</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Enter a transaction to see its leakage risk, likely diagnosis, and recommended action.</div>', unsafe_allow_html=True)

    input_col1, input_col2 = st.columns([0.95, 1.05])
    with input_col1:
        with st.form("risk_form"):
            total_price = st.number_input("Transaction Price (R$)", min_value=1.0, max_value=50000.0, value=float(st.session_state.total_price), step=5.0)
            total_freight = st.number_input("Freight Charge (R$)", min_value=0.0, max_value=20000.0, value=float(st.session_state.total_freight), step=1.0)
            installments = st.slider("Installments", min_value=1, max_value=24, value=int(st.session_state.installments))
            delay_days = st.slider("Delay in Days", min_value=0, max_value=90, value=int(st.session_state.delay_days))
            payment_type = st.selectbox("Payment Type", config["category_options"]["payment_type"], index=config["category_options"]["payment_type"].index(st.session_state.payment_type) if st.session_state.payment_type in config["category_options"]["payment_type"] else 0)
            category = st.selectbox("Product Category", config["category_options"]["product_category_name_english"], index=config["category_options"]["product_category_name_english"].index(st.session_state.category) if st.session_state.category in config["category_options"]["product_category_name_english"] else 0)
            submitted = st.form_submit_button("Run Risk Assessment")

    freight_ratio = total_freight / total_price if total_price > 0 else 0
    input_data = pd.DataFrame(
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

    proba, source = get_prediction(
        clf,
        input_data,
        {
            "total_price": total_price,
            "total_freight": total_freight,
            "installments": installments,
            "delay_days": delay_days,
            "payment_type": payment_type,
        },
    )
    risk_class = "HIGH RISK" if proba >= 0.5 else "LOW RISK"

    with input_col2:
        gauge_col, summary_col = st.columns([0.9, 1.1])
        with gauge_col:
            st.plotly_chart(build_gauge(proba), use_container_width=True)
        with summary_col:
            st.markdown(
                """
                <div class="insight-card">
                    <div class="insight-label">Risk diagnosis</div>
                    <div class="insight-value">{risk}</div>
                    <div class="insight-note">{source_text}</div>
                </div>
                """.format(
                    risk=risk_class,
                    source_text="Model-backed score from the serialized pipeline." if source == "model" else "Rule-based fallback score from the live heuristics.",
                ),
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="insight-card">
                    <div class="insight-label">Transaction summary</div>
                    <div class="insight-note">
                        <strong>Price:</strong> {fmt_currency(total_price)}<br/>
                        <strong>Freight:</strong> {fmt_currency(total_freight)}<br/>
                        <strong>Freight ratio:</strong> {freight_ratio:.1%}<br/>
                        <strong>Delay:</strong> {delay_days} days<br/>
                        <strong>Installments:</strong> {installments}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if submitted:
        st.divider()
        if risk_class == "HIGH RISK":
            st.error(f"High leakage risk detected: {proba*100:.1f}%")
            recommendation = [
                "Prioritize dispatch review before shipment.",
                "Check freight balance against product value.",
                "Review payment friction if installments are elevated.",
            ]
            impact = min(total_price * 0.7, total_price)
        else:
            st.success(f"Low leakage risk profile: {proba*100:.1f}%")
            recommendation = [
                "Proceed through standard fulfillment.",
                "Keep monitoring delay and freight ratio.",
                "No immediate intervention required.",
            ]
            impact = total_price * 0.1

        rec_col1, rec_col2, rec_col3 = st.columns(3)
        cards = [
            ("Suggested action 1", recommendation[0]),
            ("Suggested action 2", recommendation[1]),
            ("Suggested action 3", recommendation[2]),
        ]
        for col, (label, text) in zip([rec_col1, rec_col2, rec_col3], cards):
            with col:
                st.markdown(
                    f"""
                    <div class="small-metric">
                        <div class="label">{label}</div>
                        <div class="sub" style="font-size:14px; line-height:1.5;">{text}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown(
            f"""
            <div class="callout">
                💼 <strong>Estimated business impact:</strong> an order with this profile can expose up to
                <strong>{fmt_currency(impact)}</strong> in recoverable or avoidable margin, depending on whether
                the issue is operational, customer-service related, or freight-driven.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


with tab4:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Business impact and real-world value</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">This section turns analytics into executive language.</div>', unsafe_allow_html=True)

    left, right = st.columns([1, 1])
    with left:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-label">Key insights</div>
                <div class="insight-note">
                    • <strong>{df[df.leakage_reason != "None"]["leakage_reason"].value_counts().idxmax()}</strong> is the largest leakage driver.<br/>
                    • Late deliveries and low reviews are the strongest customer-friction signals.<br/>
                    • Freight burden above 30% is a major margin pressure point.<br/>
                    • Sellers with repeated leakage exposure should be prioritized for SLA review.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-label">Business impact</div>
                <div class="insight-note">
                    • Helps finance quantify leakage instead of treating it as an invisible cost.<br/>
                    • Helps operations identify where routing, packaging, or dispatch changes matter most.<br/>
                    • Helps leadership focus recovery efforts on categories and sellers with the highest risk.<br/>
                    • Supports proactive interventions before losses become refunds, credits, or churn.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-label">Outcome summary</div>
                <div class="insight-note">
                    <strong>Processed dataset:</strong> {len(df):,} orders<br/>
                    <strong>Leakage orders:</strong> {(df['leakage_amount'] > 0).sum():,}<br/>
                    <strong>Gross leakage:</strong> {fmt_currency(total_leak)}<br/>
                    <strong>Recovery opportunity:</strong> {fmt_currency(recovery_opp)}<br/>
                    <strong>Average review:</strong> {avg_score:.2f}/5
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="insight-card">
                <div class="insight-label">How this contributes in the real world</div>
                <div class="insight-note">
                    This project acts like a margin-ops control tower: it transforms raw order, payment,
                    review, and logistics data into a financially meaningful leakage score. In a real
                    company, that means:
                    <br/><br/>
                    • faster prioritization of problem sellers and categories<br/>
                    • better freight policy decisions<br/>
                    • stronger customer retention through fewer service failures<br/>
                    • clearer reporting for CFO and operations leadership
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)
