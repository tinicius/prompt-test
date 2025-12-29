import pandas as pd
import yaml
import argparse
import sys
import os
import csv
import re


def clean_text(text):
    """
    Cleans text by converting HTML breaks and escaped newlines 
    into actual newlines for proper LLM evaluation.
    """
    if not isinstance(text, str):
        return str(text)

    # Replace <br>, <br/>, <br /> with actual newlines
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)

    # Replace literal string "\n" with actual newline character
    text = text.replace('\\n', '\n')

    return text.strip()


def load_data(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    try:
        if ext == '.csv':
            # Updated: engine='python' is more robust
            # quoting=csv.QUOTE_NONE tells it to treat " and ' as normal text, not container wrappers
            # sep=',' assumes your delimiter is a comma.
            df = pd.read_csv(file_path, dtype=str, engine='python',
                             quoting=csv.QUOTE_NONE, sep=',')
        elif ext == '.ods':
            df = pd.read_excel(file_path, engine='odf', dtype=str)
        elif ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path, dtype=str)
        else:
            print(f"Error: Unsupported file extension '{ext}'.")
            sys.exit(1)

        df.columns = df.columns.str.lower().str.strip()
        return df
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def create_promptfoo_config(df, output_file):
    required_cols = ['input', 'output']
    if not all(col in df.columns for col in required_cols):
        print(f"Error: Input file must contain columns: {required_cols}")
        sys.exit(1)

    tests = []

    for _, row in df.iterrows():
        if pd.isna(row['input']) or pd.isna(row['output']):
            continue

        input_clean = clean_text(row['input'])
        output_clean = clean_text(row['output'])

        filename = row['filename']

        asserts = [
            {
                "type": "llm-rubric",
                "value": f"The response must be semantically similar to this reference:\n\n{output_clean}"
            },
        ]

        if filename:
            asserts.append(
                {
                    "type": "icontains",
                    "value": filename
                }
            )

        test_case = {
            "vars": {
                "input": input_clean
            },
            "assert": asserts
        }

        tests.append(test_case)

    config = {
        "description": "Test set",
        "prompts": ["{{input}}"],
        "providers": [
            # "openai:gpt-4o",
            {"id": "file://echo_provider.py"}
        ],
        "tests": tests
    }

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, sort_keys=False,
                      default_flow_style=False, allow_unicode=True)
        print(
            f"Success! Generated {len(tests)} complex tests in '{output_file}'")
    except Exception as e:
        print(f"Error writing output file: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert CSV/Excel to Promptfoo tests")
    parser.add_argument(
        "input_file", help="Path to the input table file (csv, xlsx)")
    parser.add_argument(
        "--out", help="Path to output yaml file", default="promptfooconfig.yaml")

    args = parser.parse_args()

    df = load_data(args.input_file)
    create_promptfoo_config(df, args.out)


if __name__ == "__main__":
    main()
