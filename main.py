from extract import extract_data
import extract


# def run_extract():
    

#     print(df['gs_inv_raw'].head())
#     print(df['gs_cm_raw'].info())
#     print(df['pn_inv_raw'].info())
#     print(df['pn_cm_raw'].info())


if __name__ == "__main__":
    raw_dfs = extract_data()






    if raw_dfs is not None:
        print(raw_dfs['gs_inv'].info())
        print(raw_dfs['gs_cm'].info())
        print(raw_dfs['pn_inv'].info())
        print(raw_dfs['pn_cm'].info())