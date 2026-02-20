import pandas as pd
import numpy as np
from faker import Faker
import datetime
import os

fake = Faker()


def generate_sales_data(num_records=1000):
    np.random.seed(42)
    Faker.seed(42)

    data = []
    regions = ["North", "South", "East", "West", "Central"]
    categories = [
        "Electronics",
        "Furniture",
        "Office Supplies",
        "Apparel",
        "Accessories",
    ]

    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2023, 12, 31)

    for _ in range(num_records):
        record_date = fake.date_between(start_date=start_date, end_date=end_date)
        region = np.random.choice(regions)
        category = np.random.choice(categories, p=[0.3, 0.2, 0.15, 0.25, 0.1])
        quantity = np.random.randint(1, 50)

        # Base price depends on category
        base_prices = {
            "Electronics": 500,
            "Furniture": 300,
            "Office Supplies": 20,
            "Apparel": 50,
            "Accessories": 30,
        }
        price = np.random.normal(base_prices[category], base_prices[category] * 0.2)
        price = round(max(5.0, price), 2)

        revenue = round(quantity * price, 2)
        cost = round(revenue * np.random.uniform(0.4, 0.8), 2)
        profit = round(revenue - cost, 2)

        data.append(
            {
                "TransactionID": fake.uuid4()[:8],
                "Date": record_date,
                "Region": region,
                "Category": category,
                "Quantity": quantity,
                "UnitPrice": price,
                "Revenue": revenue,
                "Cost": cost,
                "Profit": profit,
                "CustomerSegment": np.random.choice(
                    ["Consumer", "Corporate", "Home Office"]
                ),
                "Discount": round(
                    np.random.choice(
                        [0, 0.05, 0.1, 0.15, 0.2], p=[0.6, 0.15, 0.1, 0.1, 0.05]
                    ),
                    2,
                ),
            }
        )

    return pd.DataFrame(data)


def generate_warehouse_data(num_records=500):
    np.random.seed(43)
    Faker.seed(43)

    data = []
    locations = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "Bulk"]
    status_options = ["In Stock", "Low Stock", "Out of Stock", "In Transit"]

    for i in range(num_records):
        current_stock = np.random.randint(0, 1000)
        reorder_point = np.random.randint(50, 200)

        if current_stock == 0:
            status = "Out of Stock"
        elif current_stock < reorder_point:
            status = "Low Stock"
        else:
            status = np.random.choice(["In Stock", "In Transit"], p=[0.9, 0.1])

        data.append(
            {
                "SKU": f"SKU-{fake.ean(length=8)}",
                "ProductName": fake.catch_phrase(),
                "Location": np.random.choice(locations),
                "CurrentStock": current_stock,
                "ReorderPoint": reorder_point,
                "MaxCapacity": np.random.randint(current_stock, 2000),
                "Status": status,
                "UnitWeight_kg": round(np.random.uniform(0.1, 50.0), 2),
                "Supplier": fake.company(),
                "LastRestockDate": fake.date_between(
                    start_date="-60d", end_date="today"
                ),
            }
        )

    return pd.DataFrame(data)


def generate_accounting_data(num_records=800):
    np.random.seed(44)
    Faker.seed(44)

    data = []
    account_types = ["Asset", "Liability", "Equity", "Revenue", "Expense"]
    expense_categories = [
        "Payroll",
        "Rent",
        "Utilities",
        "Marketing",
        "Software",
        "Travel",
    ]
    revenue_categories = ["Product Sales", "Services", "Consulting", "Subscriptions"]

    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2023, 12, 31)

    for _ in range(num_records):
        record_date = fake.date_between(start_date=start_date, end_date=end_date)
        acct_type = np.random.choice(account_types, p=[0.1, 0.1, 0.05, 0.3, 0.45])

        if acct_type == "Expense":
            category = np.random.choice(expense_categories)
            amount = round(np.random.lognormal(mean=6, sigma=1), 2)
            debit = amount
            credit = 0.0
        elif acct_type == "Revenue":
            category = np.random.choice(revenue_categories)
            amount = round(np.random.lognormal(mean=7, sigma=1.2), 2)
            debit = 0.0
            credit = amount
        else:
            category = "General"
            amount = round(np.random.uniform(100, 50000), 2)
            if np.random.rand() > 0.5:
                debit = amount
                credit = 0.0
            else:
                debit = 0.0
                credit = amount

        data.append(
            {
                "JournalID": f"JNL-{fake.random_int(min=10000, max=99999)}",
                "Date": record_date,
                "AccountType": acct_type,
                "Category": category,
                "Description": fake.sentence(nb_words=4),
                "Debit": debit,
                "Credit": credit,
                "Department": np.random.choice(
                    ["IT", "HR", "Sales", "Marketing", "Operations", "Finance"]
                ),
                "Status": np.random.choice(
                    ["Reconciled", "Pending", "Flagged"], p=[0.8, 0.15, 0.05]
                ),
            }
        )

    return pd.DataFrame(data)


def generate_manufacturing_data(num_records=600):
    np.random.seed(45)
    Faker.seed(45)

    data = []
    machines = [f"Machine-{chr(65+i)}{j}" for i in range(5) for j in range(1, 4)]
    operators = [fake.name() for _ in range(10)]

    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2023, 12, 31)

    for _ in range(num_records):
        production_date = fake.date_between(start_date=start_date, end_date=end_date)
        machine = np.random.choice(machines)
        target_units = np.random.randint(100, 1000)

        # Simulate efficiency and defects
        efficiency = np.random.normal(loc=0.85, scale=0.1)
        efficiency = min(max(0.4, efficiency), 1.0)  # bound between 40% and 100%

        actual_units = int(target_units * efficiency)

        defect_rate = np.random.exponential(scale=0.02)
        defect_rate = min(defect_rate, 0.15)  # Max 15% defects
        defective_units = int(actual_units * defect_rate)

        uptime_hours = round(np.random.uniform(4.0, 12.0), 1)
        downtime_hours = round(12.0 - uptime_hours, 1)

        data.append(
            {
                "BatchID": f"BCH-{fake.random_int(min=1000, max=9999)}",
                "Date": production_date,
                "MachineID": machine,
                "Operator": np.random.choice(operators),
                "TargetUnits": target_units,
                "ActualUnits": actual_units,
                "DefectiveUnits": defective_units,
                "YieldPercentage": round(
                    (actual_units - defective_units) / actual_units * 100
                    if actual_units > 0
                    else 0,
                    2,
                ),
                "UptimeHours": uptime_hours,
                "DowntimeHours": downtime_hours,
                "EnergyConsumed_kWh": round(
                    uptime_hours * np.random.uniform(45.0, 60.0), 2
                ),
            }
        )

    return pd.DataFrame(data)


def main():
    os.makedirs("data", exist_ok=True)

    print("Generating Sales data...")
    sales_df = generate_sales_data()
    sales_df.to_csv("data/sales_data.csv", index=False)

    print("Generating Warehouse data...")
    warehouse_df = generate_warehouse_data()
    warehouse_df.to_csv("data/warehouse_data.csv", index=False)

    print("Generating Accounting data...")
    accounting_df = generate_accounting_data()
    accounting_df.to_csv("data/accounting_data.csv", index=False)

    print("Generating Manufacturing data...")
    manufacturing_df = generate_manufacturing_data()
    manufacturing_df.to_csv("data/manufacturing_data.csv", index=False)

    print("All mock datasets generated successfully in the 'data' directory.")


if __name__ == "__main__":
    main()
