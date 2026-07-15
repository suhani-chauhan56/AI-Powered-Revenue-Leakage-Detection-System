import pandas as pd
import numpy as np

def engineer_leakage_features(df: pd.DataFrame) -> pd.DataFrame:
    """Engineers leakage indicators, leakage amounts, reasons, and temporal keys."""
    df = df.copy()

    # 1. Order Status: Cancelled or Unavailable
    df["is_cancelled"] = df["order_status"].isin(["canceled", "unavailable"])

    # 2. Delivery status (Late deliveries)
    df["is_late"] = (
        df["order_delivered_customer_date"] > df["order_estimated_delivery_date"]
    ).fillna(False)

    # Calculate exact delay days
    df["delay_days"] = (
        df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]
    ).dt.days.fillna(0).clip(lower=0).astype(int)

    # 3. Customer dissatisfaction (Return proxy: review score <= 2)
    df["is_low_review"] = (df["review_score"] <= 2).fillna(False)

    # 4. Freight burden ratio
    df["freight_ratio"] = (df["total_freight"] / df["total_price"].replace(0, np.nan)).fillna(0)
    df["is_high_freight_burden"] = df["freight_ratio"] > 0.3

    # 5. Payment friction
    df["is_payment_issue"] = (
        df["payment_type"].isin(["not_defined", "voucher"]) | 
        (df["installments"] > 10)
    ).fillna(False)

    # 6. Leakage calculations (ordered by severity to avoid overlapping double-counting)
    conditions = [
        df["is_cancelled"],
        df["is_late"] & df["is_low_review"],
        df["is_high_freight_burden"],
        df["is_low_review"],
        df["is_late"],
    ]
    
    choices = [
        df["total_price"],                                    # 100% of order price
        df["total_price"] * 0.7,                              # 70% return/resolution cost
        (df["freight_ratio"] - 0.3) * df["total_price"],       # excess freight eating margins
        df["total_price"] * 0.2,                              # 20% discount/support cost
        df["total_price"] * 0.1,                              # 10% credit/delivery penalty
    ]
    
    df["leakage_amount"] = np.select(conditions, choices, default=0)
    df["leakage_amount"] = df["leakage_amount"].clip(lower=0).fillna(0)

    # Leakage reasons
    df["leakage_reason"] = np.select(
        conditions,
        ["Order Cancelled", "Late + Poor Review", "High Freight Burden", "Poor Review", "Late Delivery"],
        default="None"
    )

    # Order Month formatting
    df["order_month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
    
    return df

if __name__ == "__main__":
    from etl import build_fact_table
    print("Testing Transform Pipeline...")
    df_raw = build_fact_table()
    df_transformed = engineer_leakage_features(df_raw)
    print(f"Transform Test Successful. Leakage calculated: {df_transformed['leakage_amount'].sum():,.2f} R$")
