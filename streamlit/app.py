import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pickle
import os

# Set page config
st.set_page_config(
    page_title="Olist Revenue Leakage Control Center",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium UI CSS injection
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Font style overriding */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Card Panel Styling */
    .dashboard-card {
        background: linear-gradient(135deg, rgba(25, 28, 41, 0.85) 0%, rgba(15, 17, 26, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        color: #ffffff;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
        margin-bottom: 20px;
        transition: all 0.3s ease-in-out;
    }
    
    .dashboard-card:hover {
        transform: translateY(-3px);
        border-color: rgba(108, 92, 231, 0.4);
        box-shadow: 0 15px 35px rgba(108, 92, 231, 0.15);
    }
    
    .card-title {
        font-size: 14px;
        color: #a4b0be;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
        font-weight: 600;
    }
    
    .card-value {
        font-size: 32px;
        font-weight: 700;
        background: linear-gradient(90deg, #ffffff 0%, #dcdde1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .card-delta {
        font-size: 14px;
        margin-top: 6px;
        font-weight: 500;
    }
    
    .delta-red {
        color: #ff6b6b;
    }
    
    .delta-green {
        color: #1dd1a1;
    }
    
    /* Custom headers */
    .main-title {
        font-size: 40px;
        font-weight: 800;
        background: linear-gradient(90deg, #6c5ce7 0%, #a29bfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    
    .subtitle {
        font-size: 16px;
        color: #a4b0be;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to load data
@st.cache_data
def load_data():
    csv_path = "data/processed_fact_orders.csv"
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path, parse_dates=["order_purchase_timestamp"])
    else:
        # Generate clean mock data if pipeline hasn't run yet so front-end does not crash
        st.warning("Processed order data not found. Please run the ETL script first. Loading simulated data for preview...")
        # Create minimal df for rendering preview
        dates = pd.date_range(start="2016-09-01", end="2018-09-01", freq="D")
        np.random.seed(42)
        mock_df = pd.DataFrame({
            "order_id": [f"order_{i}" for i in range(1000)],
            "order_purchase_timestamp": np.random.choice(dates, 1000),
            "total_price": np.random.exponential(150, 1000) + 10,
            "total_freight": np.random.exponential(25, 1000) + 5,
            "review_score": np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.05, 0.1, 0.25, 0.5], size=1000),
            "installments": np.random.randint(1, 12, 1000),
            "delay_days": np.random.choice([0, 1, 2, 5, 10], p=[0.7, 0.1, 0.08, 0.07, 0.05], size=1000),
            "payment_type": np.random.choice(["credit_card", "boleto", "voucher", "debit_card"], 1000),
            "product_category_name_english": np.random.choice(["health_beauty", "watches_gifts", "sports_leisure", "housewares", "auto"], 1000),
            "seller_id": [f"seller_{np.random.randint(1, 50)}" for _ in range(1000)],
            "order_status": np.random.choice(["delivered", "canceled", "shipped"], p=[0.96, 0.03, 0.01], size=1000)
        })
        mock_df["freight_ratio"] = mock_df["total_freight"] / mock_df["total_price"]
        # Standard rules
        mock_df["is_cancelled"] = mock_df["order_status"].isin(["canceled", "unavailable"])
        mock_df["is_late"] = mock_df["delay_days"] > 0
        mock_df["is_low_review"] = mock_df["review_score"] <= 2
        mock_df["is_high_freight_burden"] = mock_df["freight_ratio"] > 0.3
        
        conditions = [
            mock_df["is_cancelled"],
            mock_df["is_late"] & mock_df["is_low_review"],
            mock_df["is_high_freight_burden"],
            mock_df["is_low_review"],
            mock_df["is_late"]
        ]
        choices = [
            mock_df["total_price"],
            mock_df["total_price"] * 0.7,
            (mock_df["freight_ratio"] - 0.3) * mock_df["total_price"],
            mock_df["total_price"] * 0.2,
            mock_df["total_price"] * 0.1
        ]
        mock_df["leakage_amount"] = np.select(conditions, choices, default=0)
        mock_df["leakage_reason"] = np.select(
            conditions,
            ["Order Cancelled", "Late + Poor Review", "High Freight Burden", "Poor Review", "Late Delivery"],
            default="None"
        )
        mock_df["order_month"] = mock_df["order_purchase_timestamp"].dt.to_period("M").astype(str)
        return mock_df

df = load_data()

# Header Section
st.markdown("<div class='main-title'>Revenue Leakage Control Center</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Olist E-commerce Financial Audit & Predictive Risk Management</div>", unsafe_allow_html=True)

# Define Tabs
tab1, tab2, tab3 = st.tabs(["📊 CFO Executive Summary", "🔍 Deep-Dive Leakage Audit", "🔮 Predictive Risk Simulator"])

# TAB 1: EXECUTIVE SUMMARY
with tab1:
    # Calculations
    total_rev = df["total_price"].sum()
    total_leak = df["leakage_amount"].sum()
    leakage_pct = (total_leak / total_rev) * 100 if total_rev > 0 else 0
    recovery_opp = total_leak * 0.5 # 50% recovery potential assumed
    avg_score = df["review_score"].mean()
    
    # Custom HTML metrics display
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="card-title">Gross Merchant Revenue</div>
            <div class="card-value">R$ {total_rev:,.0f}</div>
            <div class="card-delta delta-green">● Total Billing Volume</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="card-title">Estimated Leakage</div>
            <div class="card-value" style="background: linear-gradient(90deg, #ff7675 0%, #d63031 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">R$ {total_leak:,.0f}</div>
            <div class="card-delta delta-red">▲ {leakage_pct:.2f}% Margin Leakage</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="card-title">Recoverable Revenue (50% target)</div>
            <div class="card-value" style="background: linear-gradient(90deg, #55efc4 0%, #00b894 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">R$ {recovery_opp:,.0f}</div>
            <div class="card-delta delta-green">▼ Actionable Recovery Pot.</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="card-title">Average Review Score</div>
            <div class="card-value">{avg_score:.2f} / 5.0</div>
            <div class="card-delta {'delta-green' if avg_score >= 4.0 else 'delta-red'}">★ Customer Satisfaction Proxy</div>
        </div>
        """, unsafe_allow_html=True)

    # Core Charts row
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Leakage by Root Cause")
        reason_df = df[df.leakage_reason != "None"].groupby("leakage_reason")["leakage_amount"].sum().reset_index()
        fig_reason = px.bar(
            reason_df.sort_values(by="leakage_amount", ascending=True),
            x="leakage_amount",
            y="leakage_reason",
            orientation="h",
            color="leakage_amount",
            color_continuous_scale="reds",
            labels={"leakage_amount": "Total Leaked (R$)", "leakage_reason": "Root Cause"},
            template="plotly_dark"
        )
        fig_reason.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            height=380,
            margin=dict(l=20, r=20, t=10, b=10)
        )
        st.plotly_chart(fig_reason, use_container_width=True)
        
    with col2:
        st.subheader("Monthly Leakage Trend")
        # Ensure correct temporal ordering for plot
        monthly = df.groupby("order_month")["leakage_amount"].sum().reset_index().sort_values("order_month")
        fig_monthly = px.area(
            monthly,
            x="order_month",
            y="leakage_amount",
            labels={"leakage_amount": "Leakage Amount (R$)", "order_month": "Month"},
            template="plotly_dark"
        )
        fig_monthly.update_traces(line_color="#6c5ce7", fillcolor="rgba(108, 92, 231, 0.2)")
        fig_monthly.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380,
            margin=dict(l=20, r=20, t=10, b=10)
        )
        st.plotly_chart(fig_monthly, use_container_width=True)

    # Key Insights Alert
    st.info("""
    💡 **CFO Financial Alert**: The analysis reveals that **Late Deliveries** and **Order Cancellations** constitute the majority of margin degradation. 
    Prioritizing logictics routing improvements in high-freight regions could recover up to **R$ {}** of lost margins.
    """.format(f"{recovery_opp:,.2f}"))

# TAB 2: DEEP-DIVE AUDIT
with tab2:
    st.subheader("Granular Margin Degradation Audit")
    
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.write("#### Top 10 Product Categories by Total Leakage")
        cat_df = df.groupby("product_category_name_english")["leakage_amount"].sum().nlargest(10).reset_index()
        fig_cat = px.bar(
            cat_df,
            x="leakage_amount",
            y="product_category_name_english",
            orientation="h",
            color="leakage_amount",
            color_continuous_scale="purples",
            template="plotly_dark"
        )
        fig_cat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            height=380,
            yaxis={'categoryorder':'total ascending'}
        )
        st.plotly_chart(fig_cat, use_container_width=True)
        
    with col_b:
        st.write("#### Top 10 High-Risk Sellers (Gross Leakage)")
        seller_df = df.groupby("seller_id").agg(
            total_leakage=("leakage_amount", "sum"),
            orders_handled=("order_id", "count"),
            avg_review_rating=("review_score", "mean")
        ).nlargest(10, "total_leakage").reset_index()
        
        # Style formatting
        seller_df["total_leakage"] = seller_df["total_leakage"].map("R$ {:,.2f}".format)
        seller_df["avg_review_rating"] = seller_df["avg_review_rating"].map("{:.2f} / 5".format)
        st.dataframe(seller_df, use_container_width=True, height=350)
        st.caption("🔍 High-risk sellers should be targeted for logistics audits or service-level agreement (SLA) reviews.")

# TAB 3: PREDICTIVE RISK SIMULATOR
with tab3:
    # Model Loading
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
            st.error(f"Failed to load trained models: {e}")
    
    if clf is None or config is None:
        st.warning("⚠️ **ML Model Not Found**: Pre-trained classifier pickles were not found in `ml/models/` directory.")
        st.info("""
        To activate the interactive XGBoost predictor, execute the model training notebook:
        `jupyter nbconvert --to notebook --execute --inplace notebooks/02_modeling.ipynb`
        
        *Using standard rule-based financial simulator logic as a backup fallback below.*
        """)
        
        # Define default categories for fallback list
        default_categories = sorted(df["product_category_name_english"].dropna().unique().tolist())
        default_payments = sorted(df["payment_type"].dropna().unique().tolist())
        if not default_payments:
            default_payments = ["credit_card", "boleto", "voucher", "debit_card"]
        if not default_categories:
            default_categories = ["health_beauty", "watches_gifts", "sports_leisure", "housewares", "telephony"]
        
        config = {
            "category_options": {
                "payment_type": default_payments,
                "product_category_name_english": default_categories
            }
        }
        
    st.subheader("Transaction Risk Profiling Sandbox")
    st.write("Simulate single order parameters to predict the risk of revenue leakage before execution.")
    
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        total_price = st.number_input("Transaction Price (R$)", min_value=1.0, max_value=20000.0, value=150.0)
        total_freight = st.number_input("Freight Charge (R$)", min_value=0.0, max_value=5000.0, value=25.0)
        installments = st.slider("Installments Count", min_value=1, max_value=24, value=3)
        delay_days = st.slider("Historical Delay Incurred (days)", min_value=0, max_value=60, value=0)
        
    with col_input2:
        payment_type = st.selectbox("Selected Payment Mode", config["category_options"]["payment_type"])
        category = st.selectbox("Product Categorization", config["category_options"]["product_category_name_english"])
        
    # Calculate ratio
    freight_ratio = total_freight / total_price if total_price > 0 else 0
    
    # Predict button
    if st.button("Audit Transaction Risk Profile", type="primary"):
        st.write("---")
        
        # DataFrame constructor
        input_data = pd.DataFrame([{
            "total_price": total_price,
            "total_freight": total_freight,
            "freight_ratio": freight_ratio,
            "installments": installments,
            "delay_days": delay_days,
            "payment_type": payment_type,
            "product_category_name_english": category
        }])
        
        # Risk assessment computation
        if clf is not None:
            # Model Predict
            proba = clf.predict_proba(input_data)[0][1]
            risk_classification = "HIGH RISK" if proba >= 0.5 else "LOW RISK"
        else:
            # Fallback simple deterministic heuristics
            # An order is high risk if delay is long, freight ratio > 0.3, or installments > 10
            proba = 0.05
            reasons_found = []
            if delay_days > 5:
                proba += 0.35
                reasons_found.append(f"Expected delay of {delay_days} days is high")
            if freight_ratio > 0.3:
                proba += 0.30
                reasons_found.append("Freight burden is above 30% threshold")
            if installments > 10:
                proba += 0.15
                reasons_found.append("Extremely high installment plan (10+ months)")
            if payment_type in ["voucher", "not_defined"]:
                proba += 0.15
                reasons_found.append("Payment mechanism prone to friction/returns")
            
            proba = min(proba, 0.99)
            risk_classification = "HIGH RISK" if proba >= 0.50 else "LOW RISK"
            
        # Display Results
        res_col1, res_col2 = st.columns([1, 2])
        
        with res_col1:
            # Gauge creation
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = proba * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Leakage Probability", 'font': {'size': 18}},
                gauge = {
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "#6c5ce7"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 50], 'color': 'rgba(29, 209, 161, 0.15)'},
                        {'range': [50, 80], 'color': 'rgba(255, 159, 67, 0.15)'},
                        {'range': [80, 100], 'color': 'rgba(255, 107, 107, 0.15)'}
                    ]
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font = {'color': "white", 'family': "Plus Jakarta Sans"},
                height=260,
                margin=dict(l=20, r=20, t=30, b=10)
            )
            st.plotly_chart(fig_gauge, use_container_width=True)
            
        with res_col2:
            st.write("### Risk Diagnosis Result")
            if risk_classification == "HIGH RISK":
                st.error(f"🔴 **HIGH LEAKAGE RISK IDENTIFIED ({proba*100:.1f}%)**")
                st.write("""
                **Recommended Mitigations**:
                1. **Delay Mitigation**: The system expects shipping delays. Check seller performance rating before routing this item.
                2. **Freight Optimization**: Freight charge constitutes **{:.1f}%** of product value. Consider subsidizing shipping or bundling items.
                3. **Credit Verification**: Verify billing information for installments exceeding 10 intervals.
                """.format(freight_ratio * 100))
            else:
                st.success(f"🟢 **LOW LEAKAGE RISK PROFILE ({proba*100:.1f}%)**")
                st.write("""
                **System Flag**: Approved for standard fulfillment pipeline. The parameters represent an order template historically correlating to positive reviews, prompt delivery timelines, and safe profit margins.
                """)
