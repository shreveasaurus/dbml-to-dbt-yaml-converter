# DBML to DBT YAML Converter

## Overview

A Python script that converts DBML (Database Markup Language) files to DBT (Data Build Tool) YAML model definition files.

## Features

- Converts DBML table definitions to dbt YAML
- Preserves table and column descriptions
- Supports primary key detection
- Interactive CLI for file and directory selection

## Requirements

- Python 3.7+
- PyYAML

## Installation

```bash
git clone https://github.com/yourusername/dbml-to-dbt-yaml-converter.git
cd dbml-to-dbt-yaml-converter
pip install -r requirements.txt
```

## Usage

```bash
python dbml_to_dbt_yaml.py
```

Follow the interactive prompts to specify:
- Path to DBML file
- Output directory for YAML files

## License

MIT License