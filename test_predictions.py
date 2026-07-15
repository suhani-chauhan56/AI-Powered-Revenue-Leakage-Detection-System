import pandas as pd
import numpy as np
import pickle
import os

csv_path = "data/processed_fact_orders.csv"
if not os.path.exists(csv_path):
    print("Processed CSV not found!")
    sys.exit(1)

df = pd.read_csv(csv_path)
print("Dataset size:", len(df))
print("Leakage amount description:")
print(df["leakage_amount"].describe())
print("\nLeakage amount > 0 count:", (df["leakage_amount"] > 0).sum())
print("75th percentile of leakage_amount:", df["leakage_amount"].quantile(0.75))

# Let's inspect the target
df["target_high_leakage"] = (df["leakage_amount"] > df["leakage_amount"].quantile(0.75)).astype(int)
print("Target High Leakage class counts:")
print(df["target_high_leakage"].value_counts())

# Let's see some sample records where target_high_leakage == 1
print("\nSamples of high leakage orders:")
print(df[df["target_high_leakage"] == 1][["total_price", "total_freight", "freight_ratio", "installments", "delay_days", "leakage_amount", "leakage_reason"]].head(10))

# Let's check the serialized model prediction behavior
clf_path = "ml/models/leakage_classifier_pipeline.pkl"
if os.path.exists(clf_path):
    with open(clf_path, "rb") as f:
        clf = pickle.load(f)
    
    # Test a typical low-risk order
    low_risk_test = pd.DataFrame([{
        "total_price": 50.0,
        "total_freight": 10.0,
        "freight_ratio": 0.2,
        "installments": 1,
        "delay_days": 0,
        "payment_type": "credit_card",
        "product_category_name_english": "health_beauty"
    }])
    
    # Test a typical high-risk order (very late delivery, large price)
    high_risk_test = pd.DataFrame([{
        "total_price": 500.0,
        "total_freight": 200.0,
        "freight_ratio": 0.4,
        "installments": 12,
        "delay_days": 30,
        "payment_type": "credit_card",
        "product_category_name_english": "health_beauty"
    }])
    
    print("\nLow risk test prediction probability:", clf.predict_proba(low_risk_test)[0][1])
    print("High risk test prediction probability:", clf.predict_proba(high_risk_test)[0][1])
else:
    print("\nModel pickle not found!")
