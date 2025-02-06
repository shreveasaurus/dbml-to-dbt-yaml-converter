import re
import yaml
import os

def parse_dbml(dbml_content):
    tables = {}
    table_pattern = re.compile(r'Table\s+(\w+)\s*{(.*?)}', re.DOTALL | re.IGNORECASE)

    for table_match in table_pattern.finditer(dbml_content):
        table_name = table_match.group(1)
        table_content = table_match.group(2)

        # Extract table description
        table_desc_match = re.search(r'note:\s*"([^"]*)"', table_content)
        table_description = table_desc_match.group(1) if table_desc_match else None

        # Parse columns
        columns = []
        column_pattern = re.compile(r'^\s*(\w+)\s+([\w()]+)(\s*\[.*?\])?', re.MULTILINE)
        for col_match in column_pattern.finditer(table_content):
            col_name = col_match.group(1)
            col_type = col_match.group(2)
            col_attrs = col_match.group(3) or ''

            # Extract column description
            desc_match = re.search(r'note:\s*"([^"]*)"', col_attrs)
            col_description = desc_match.group(1) if desc_match else None

            # Prepare column entry
            column_entry = {
                'name': col_name,
                'type': col_type
            }

            # Add column description if exists
            if col_description:
                column_entry['description'] = col_description

            # Check for primary key
            if re.search(r'\[.*pk.*\]', col_attrs, re.IGNORECASE):
                column_entry['primary_key'] = True

            columns.append(column_entry)

        # Create table entry matching test expectations
        table_entry = {
            'version': 2,
            'models': [{
                'name': table_name,
                'columns': columns
            }]
        }

        # Add table description to models
        if table_description:
            table_entry['models'][0]['description'] = table_description

        tables[table_name] = table_entry

    return tables

def dbml_to_dbt_yaml(dbml_file_path=None, output_dir=None):
    # Prompt for DBML file if not provided
    if not dbml_file_path:
        dbml_file_path = input("Enter the path to your DBML file: ")

    # Read DBML file
    with open(dbml_file_path, 'r') as f:
        dbml_content = f.read()

    # Parse DBML and convert to dbt YAML
    tables = parse_dbml(dbml_content)

    if not tables:
        print("No tables found in the DBML file. Check the file format.")
        return

    # Prompt for output directory if not provided, default to current working directory
    if not output_dir:
        output_dir = input("Enter output directory (press Enter for current directory): ") or os.getcwd()

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Write individual YAML files for each table
    for table_name, dbt_yaml in tables.items():
        output_path = os.path.join(output_dir, f'{table_name}.yml')
        with open(output_path, 'w') as f:
            yaml.dump(dbt_yaml, f, default_flow_style=False, sort_keys=False)

    print(f"Generated {len(tables)} dbt YAML model files in {output_dir}")

# Allow direct script execution
if __name__ == "__main__":
    dbml_to_dbt_yaml()