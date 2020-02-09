import argparse

import pandas as pd


def get_dataframe_info(dataframe):
    print("----- DATAFRAME INFORMATION -----")

    print(f"Columns: {dataframe.columns.values.tolist()}")
    print(f"Shape: {dataframe.shape}")
    print("\n")


def get_null_dataframe(dataframe):
    null_bolean_df = dataframe.isnull()
    null_entries = null_bolean_df.any(axis='columns')
    null_dataframe = dataframe[null_entries]
    null_counts = null_bolean_df.sum()

    print(f"Number of NaN entries: {null_dataframe.shape[0]}")
    print("NaN distribution:")
    print(null_counts)
    print("")
    print("Dataframe with NaN")
    print(null_dataframe)
    print("\n")

    return null_dataframe


def get_no_null_dataframe(dataframe):
    no_null_dataframe = dataframe.dropna(axis=0, how="any") 
    number_columns = no_null_dataframe.shape[0]
    number_null = int(dataframe.shape[0]) - int(number_columns)

    print("----- NaN ENTRIES -----")
    print(f"{number_null} rows with NaN entries have been deleted.")
    print("\n")

    return no_null_dataframe


def get_empty_value_dataframe(dataframe):
    string_dataframe = dataframe.applymap(str)
    no_space_df = string_dataframe.applymap(str.strip)
    empty_boolean_df = no_space_df.eq("")
    empty_entries = empty_boolean_df.any(axis='columns')
    empty_values_df = dataframe[empty_entries]
    empty_counts = empty_boolean_df.sum()

    print(f"Number of empty entries: {empty_values_df.shape[0]}")
    print("Empty entries distribution:")
    print(empty_counts)
    print("")
    print("Dataframe with empty entries")
    print(empty_values_df)
    print("\n")

    return empty_values_df


def get_no_empty_value_dataframe(dataframe):
    string_dataframe = dataframe.applymap(str)
    no_space_df = string_dataframe.applymap(str.strip)
    no_empty_boolean_df = no_space_df.ne("")
    no_empty_entries = no_empty_boolean_df.any(axis='columns')
    no_empty_values_df = dataframe[no_empty_entries]
    number_columns = no_empty_values_df.shape[0]
    number_empty = int(dataframe.shape[0]) - int(number_columns)

    print("----- EMPTY ENTRIES -----")
    print(f"{number_empty} rows with empty entries have been deleted.")
    print("\n")

    return no_empty_values_df


def get_duplicates_dataframe(data_dataframe):
    duplicates_dataframe = data_dataframe[
        data_dataframe.duplicated()
    ]
    print(f"Number of dupliciated entries: {duplicates_dataframe.shape[0]}")
    print("\n")

    return duplicates_dataframe


def get_no_duplicates_dataframe(dataframe):
    no_duplicates_df = dataframe.drop_duplicates()
    number_columns = no_duplicates_df.shape[0]
    number_duplicates = int(dataframe.shape[0]) - int(number_columns)

    print("----- DUPLICATED ENTRIES -----")
    print(f"{number_duplicates} duplicated rows have been deleted.")
    print("\n")

    return no_duplicates_df


def main():
    parser = argparse.ArgumentParser()
    # Mandatory arguments
    parser.add_argument("data", help='Data file')
    parser.add_argument("rules", help='Database rules file')
    # Optional arguments
    parser.add_argument("--all", help='Remove every anomalies', action='store_true')
    parser.add_argument("--duplicates", help='Remove duplicates', action='store_true')
    parser.add_argument("--empty", help='Remove empty entries', action='store_true')
    parser.add_argument("--NaN", help='Remove NaN entries', action='store_true')
    parser.add_argument("--sep", help='Separator', default='|')
    # parser.add_argument(
    #   "--primary_key",
    #    action='append',
    #    help="Primary key, can be called multiple times"
    # )
    args = parser.parse_args()

    data_file = args.data
    rules_file = args.rules

    data_dataframe = pd.read_csv(data_file, sep=args.sep)
    rules_dataframe = pd.read_csv(rules_file, sep=args.sep)
    rules_dataframe = rules_dataframe.set_index('FIELD')

    get_dataframe_info(data_dataframe)

    # Check optionnal arguments
    if args.duplicates or args.all:
        no_duplicates_df = get_no_duplicates_dataframe(data_dataframe)
        data_dataframe = no_duplicates_df
    else:
        get_duplicates_dataframe(data_dataframe)

    if args.NaN or args.all:
        no_null_df = get_no_null_dataframe(data_dataframe)
        data_dataframe = no_null_df
    else:
        get_null_dataframe(data_dataframe)

    if args.empty or args.all:
        no_empty_df = get_no_empty_value_dataframe(data_dataframe)
        data_dataframe = no_empty_df
    else:
        get_empty_value_dataframe(data_dataframe)

    filename = data_file.split(".")[0]
    data_dataframe.to_csv(f"{filename}_prepared.csv", index=False, sep="|")


# Define what to do if file is run as script
if __name__ == "__main__":
    main()
