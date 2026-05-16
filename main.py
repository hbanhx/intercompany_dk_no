from numpy import load
from extract import extract_data 
from transform import transform_data
from load import load_data
import os



if __name__ == "__main__":
    
    # Test the transformation pipeline and save outputs to Excel files

    inv_df, cm_df, vat_df, import_df = transform_data()
    load_data(inv_df, cm_df, vat_df, import_df)
 