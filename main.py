import logging
import os
from transform import transform_data
from load import load_data

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "etl.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    logging.info("Starting ETL pipeline")

    inv_df, cm_df, vat_df, import_df = transform_data()
    load_data(inv_df, cm_df, vat_df, import_df)
    
    logging.info("ETL pipeline completed successfully. VAT reconciled: {} records. Import orders: {} records"
        .format(len(vat_df[vat_df['_merge'] == 'both']), len(import_df)))
    