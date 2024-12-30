"""
Script that converts a JSONLines file to Parquet format.

"""
import argparse
import pandas as pd
import json

def convert_jsonl_to_parquet(input_path, output_path):
    """
    Convert a JSONLines file to Parquet format.
    
    Parameters:
    input_path (str): Path to input JSONLines file
    output_path (str): Path where Parquet file will be saved
    """
    # Read JSONLines file line by line to handle large files
    records = []
    with open(input_path, 'r') as file:
        for line in file:
            records.append(json.loads(line))
    
    # Convert to DataFrame
    df = pd.DataFrame(records)
    
    # Write to Parquet
    df.to_parquet(output_path, index=False)
    
    print(f"Conversion complete. File saved to: {output_path}")
    print(f"Number of records processed: {len(df)}")

# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert JSONLines file to Parquet format')
    parser.add_argument('input_file', help='Path to input JSONLines file', default = "GSM8k_p2_only_q_a.jsonl")
    parser.add_argument('output_file', help='Path to output Parquet file', default = "test-GSM8k_p2_only_q_a.parquet")
    args = parser.parse_args()

    
    convert_jsonl_to_parquet(args.input_file, args.output_file)
