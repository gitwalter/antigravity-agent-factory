import pandas as pd
import os
import json
from .database import WarehouseInventory, WarehouseBinMaster


class DataManager:
    def __init__(self, data_dir="projects/statistical_dashboards/data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def load_data(self, file_source):
        """Loads data from CSV or Excel and returns a DataFrame + metadata.

        Args:
            file_source: Either a string path OR a Streamlit UploadedFile object.
        """
        # Handle Streamlit UploadedFile objects which have a .name attribute
        file_path = getattr(file_source, "name", file_source)

        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".csv":
            df = pd.read_csv(file_source)
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(file_source)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

        metadata = {
            "columns": df.columns.tolist(),
            "types": df.dtypes.apply(lambda x: str(x)).to_dict(),
            "rows": len(df),
            "cols": len(df.columns),
        }
        return df, metadata

    def clean_data(self, df):
        """Standard cleaning: handle missing values, basic type coercion."""
        # Simple example cleaning
        df = df.dropna(how="all")
        return df

    def save_to_database(self, df, project_id, filename, db_manager):
        """Saves dataset metadata AND the actual data directly to the DB as a JSON string."""
        session = db_manager.get_session()
        from .database import Dataset

        # Log in DB
        metadata = {
            "columns": df.columns.tolist(),
            "types": df.dtypes.apply(lambda x: str(x)).to_dict(),
        }

        # We store the data as a JSON string for simplicity in SQLite
        # while keeping the app logic mostly unchanged.
        data_json = df.to_json(orient="records", date_format="iso")

        ds = Dataset(
            project_id=project_id,
            filename=filename,
            file_type="sqlite",
            row_count=len(df),
            col_count=len(df.columns),
            metadata_json=json.dumps(metadata),
            data_json=data_json,
        )
        session.add(ds)
        session.commit()
        session.close()
        return "database"

    def get_dataset_data(self, dataset_id, db_manager):
        """Retrieves actual dataset content from the database."""
        session = db_manager.get_session()
        from .database import Dataset

        ds = session.query(Dataset).filter_by(id=dataset_id).first()
        if ds and ds.data_json:
            data = pd.read_json(ds.data_json, orient="records")
            session.close()
            return data
        session.close()
        return None

    def auto_ingest_domain_data(self, df, project_id, db_manager):
        """Detects if the dataframe matches a domain model and populates specific tables."""
        cols = [c.lower() for c in df.columns]
        session = db_manager.get_session()
        ingested_tables = []

        # Inventory Signature: SKU, Location, (CurrentStock or Quantity)
        if (
            "sku" in cols
            and "location" in cols
            and any(k in cols for k in ["currentstock", "quantity"])
        ):
            stocks = []
            for _, row in df.iterrows():
                # Map columns flexibly
                sku = row.get("SKU") or row.get("sku")
                loc = row.get("Location") or row.get("location")
                qty = row.get("CurrentStock") or row.get("quantity")

                stock = WarehouseInventory(
                    project_id=project_id,
                    sku=sku,
                    bin_id=loc,
                    quantity=int(qty) if pd.notnull(qty) else 0,
                )
                stocks.append(stock)

            session.add_all(stocks)
            ingested_tables.append("WarehouseInventory")

        # Bin Master Signature: Location
        if "location" in cols:
            locations = df[
                "Location" if "Location" in df.columns else "location"
            ].unique()
            bins = []
            for loc in locations:
                # Check if it already exists in the bin master for this project
                existing = (
                    session.query(WarehouseBinMaster)
                    .filter_by(project_id=project_id, bin_id=loc)
                    .first()
                )
                if not existing:
                    bn = WarehouseBinMaster(
                        project_id=project_id,
                        bin_id=loc,
                        zone=loc[0] if len(str(loc)) > 0 else "Gen",
                        is_active=1,
                    )
                    bins.append(bn)
            if bins:
                session.add_all(bins)
                ingested_tables.append("WarehouseBinMaster")

        if ingested_tables:
            session.commit()

        session.close()
        return ingested_tables

    def get_summary_stats(self, df):
        """Returns descriptive statistics for the dataframe."""
        stats = df.describe(include="all").to_dict()
        return stats
