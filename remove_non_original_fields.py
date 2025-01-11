"""
Script to preprocess the data into the format that the GSM8k reader
in lm-evaluation-harness expects, which contains only the question and answer fields.
Optionally, we also generate a subset of the data with a subset of the data instance from
each template.

Example usage: 

    python remove_non_original_fields.py --input_file data/GSM8k_p2.jsonl --output_file data/GSM8k_p2_only_q_a.jsonl --subset_file data/GSM8k_p2_subset_only_q_a_250.jsonl --limit 5

"""
import json
import argparse
from pathlib import Path

def process_jsonl(input_file: str, output_file: str, subset_file, limit: int) -> None:
    """
    Process a JSONL file to extract only question and answer fields.
    
    Args:
        input_file (str): Path to input JSONL file
        output_file (str): Path to output JSONL file
    """
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile, \
         open(subset_file, 'w', encoding='utf-8') as subsetfile:
        for line_num, line in enumerate(infile, 1):
            try:
                # Parse the JSON line
                data = json.loads(line.strip())

                # Extract only question and answer fields
                filtered_data = {
                    'question': data.get('question', ''),
                    'answer': data.get('answer', '')
                }
                if data["instance"] < limit:
                    # Write the filtered data to subset file
                    json.dump(filtered_data, subsetfile, ensure_ascii=False)
                    subsetfile.write('\n')
                
                
                # Write the filtered data to output file
                json.dump(filtered_data, outfile, ensure_ascii=False)
                outfile.write('\n')
                
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON on line {line_num}: {e}")
                continue
            except KeyError as e:
                print(f"Missing key on line {line_num}: {e}")
                continue

def main():
    # Set up command line argument parser
    parser = argparse.ArgumentParser(description='Process JSONL file to keep only question and answer fields')
    parser.add_argument('--input_file', help='Path to input JSONL file')
    parser.add_argument('--output_file', help='Path to output JSONL file')
    parser.add_argument('--subset_file', help='Path to output subset JSONL file')
    parser.add_argument('--limit', type=int)   
    
    args = parser.parse_args()
    
    # Verify input file exists
    if not Path(args.input_file).is_file():
        print(f"Error: Input file '{args.input_file}' does not exist")
        return
    
    # Process the file
    try:
        process_jsonl(args.input_file, args.output_file, args.subset_file, args.limit)
        print(f"Successfully processed {args.input_file} to {args.output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()