import os
import pandas as pd
import numpy as np

def load_raw(data_dir="data"):
    """Loads all Olist CSV datasets, parsing dates correctly."""
    orders = pd.read_csv(os.path.join(data_dir, "olist_orders_dataset.csv"), parse_dates=[
        "order_purchase_timestamp", "order_approved_at",
        "order_delivered_carrier_date", "order_delivered_customer_date",
        "order_estimated_delivery_date"])
    items = pd.read_csv(os.path.join(data_dir, "olist_order_items_dataset.csv"))
    payments = pd.read_csv(os.path.join(data_dir, "olist_order_payments_dataset.csv"))
    reviews = pd.read_csv(os.path.join(data_dir, "olist_order_reviews_dataset.csv"))
    products = pd.read_csv(os.path.join(data_dir, "olist_products_dataset.csv"))
    customers = pd.read_csv(os.path.join(data_dir, "olist_customers_dataset.csv"))
    sellers = pd.read_csv(os.path.join(data_dir, "olist_sellers_dataset.csv"))
    cat_translation = pd.read_csv(os.path.join(data_dir, "product_category_name_translation.csv"))
    return orders, items, payments, reviews, products, customers, sellers, cat_translation


def build_fact_table(data_dir="data"):
    """Aggregates and joins order, items, payments, reviews, product categories, and sellers."""
    orders, items, payments, reviews, products, customers, sellers, cat_translation = load_raw(data_dir)

    # Aggregate item-level details to order level.
    # Sort by price first so the representative product/seller reflects the highest-value line item
    # instead of the first row in the raw dataset.
    items_sorted = items.sort_values(["order_id", "price", "order_item_id"], ascending=[True, False, True])
    items_agg = items_sorted.groupby("order_id", sort=False).agg(
        n_items=("order_item_id", "count"),
        total_price=("price", "sum"),
        total_freight=("freight_value", "sum"),
        product_id=("product_id", "first"),
        seller_id=("seller_id", "first")
    ).reset_index()

    # Aggregate payments
    payments_agg = payments.groupby("order_id").agg(
        total_payment=("payment_value", "sum"),
        payment_type=("payment_type", "first"),
        installments=("payment_installments", "max")
    ).reset_index()

    # Filter out duplicate reviews, keep the latest review for each order
    reviews_agg = reviews.sort_values("review_answer_timestamp").drop_duplicates("order_id", keep="last")
    reviews_agg = reviews_agg[["order_id", "review_score"]]

    # Merge product English translations
    products = products.merge(cat_translation, on="product_category_name", how="left")

    # Master joins
    df = orders.merge(items_agg, on="order_id", how="left")
    df = df.merge(payments_agg, on="order_id", how="left")
    df = df.merge(reviews_agg, on="order_id", how="left")
    df = df.merge(customers, on="customer_id", how="left")
    df = df.merge(products[["product_id", "product_category_name_english"]], on="product_id", how="left")
    df = df.merge(sellers, on="seller_id", how="left")

    return df

if __name__ == "__main__":
    print("Testing ETL Pipeline...")
    df = build_fact_table()
    print(f"ETL Test Successful. Fact table shape: {df.shape}")
