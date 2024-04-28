import json

import pandas as pd
from pandas import DataFrame


def read_csv(
    file_name: str,
    dtype: dict,
    dropna: list,
    encoding: str = 'utf-16',
    delimiter: str = '\t',
) -> DataFrame:
    '''
    Read a CSV file into a DataFrame with specific data types and drop rows with missing 'Object_ID' or 'Host_ID'.

    Parameters:
        file_name (str): The path to the CSV file to be read.

    Returns:
        DataFrame: A pandas DataFrame containing the CSV data.

    '''

    df = pd.read_csv(
        file_name,
        encoding=encoding,
        delimiter=delimiter,
        dtype=dtype,
    ).dropna(subset=dropna)

    return df


def read_json_file(file_name: str) -> dict:
    '''
    Read JSON data from a file and return it as a dictionary.

    Parameters:
        file_name (str): The path to the JSON file to be read.

    Returns:
        dict: A dictionary containing the JSON data read from the file.
    '''
    json_data = {}

    with open(file_name) as f:
        json_data = json.load(f)

    return json_data


def write_json_file(data: dict, filename: str) -> None:
    '''
    Write data to a JSON file with indentation.

    Parameters:
        data (dict): The dictionary containing the data to be written to the JSON file.
        filename (str): The path to the JSON file to be written.

    Returns:
        None
    '''
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


def add_parent_id_to_object(json_data: dict, csv_df: DataFrame) -> dict:
    '''
    Add parent IDs to objects in the JSON data based on matching object IDs in the CSV DataFrame.

    Parameters:
        json_data (dict): The JSON data containing objects.
        csv_df (DataFrame): The DataFrame containing CSV data with Image Object IDs.

    Returns:
        dict: The updated JSON data with parent IDs added to objects.
    '''
    for obj in json_data['ops_3d']:
        object_id = obj['item_id']

        for i in range(1, 4):
            parent_id = csv_df[csv_df[f'Image{i}_Object_ID'] == str(object_id)][
                'Host_ID'
            ]
            if not parent_id.empty:
                obj['parent_id'] = parent_id.to_string().split()[-1]
                break

    return json_data


def update_json_files(file_names: list, csv_data: DataFrame) -> None:
    '''
    Update multiple JSON files with parent IDs based on CSV data.

    Parameters:
        file_names (list of str): A list of paths to the JSON files to be updated.
        csv_data (Data frame): Pandas Data frame containing data used to update the JSON files.

    Returns:
        None
    '''

    # Iterate over each JSON file
    for file_name in file_names:
        # Read JSON data from the file
        data = read_json_file(file_name)

        # Add parent IDs to JSON data based on CSV data
        updated_json = add_parent_id_to_object(data, csv_data)

        # Write updated JSON data to a new file
        write_json_file(updated_json, f'updated_{file_name}')


if __name__ == '__main__':

    csv_file = 'EXP_ObjectID_HostID.csv'
    dtype = {
        'Image1_Object_ID': str,
        'Image2_Object_ID': str,
        'Image3_Object_ID': str,
        'Host_ID': str,
    }
    dropna = ['Object_ID', 'Host_ID']
    csv_data = read_csv(csv_file, dtype, dropna)

    files = [
        '3d3fde25-fc47-47ad-bda4-0b438196045b.json',
        '763fdd40-9408-45bb-b532-3f90b5c7c5d1.json',
        'b73070b3-7625-4975-872a-967b2297a458.json',
    ]
    update_json_files(files, csv_data)
