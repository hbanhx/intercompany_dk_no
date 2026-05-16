import logging
from transform import transform_data
from load import load_data

# Configure logging once at the top of the file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    logging.info("Starting ETL pipeline")

    inv_df, cm_df, vat_df, import_df = transform_data()
    logging.info("Transformation complete")

    load_data(inv_df, cm_df, vat_df, import_df)
    logging.info("ETL pipeline finished successfully")
    