import unittest
import os
import yaml
import tempfile
from dbml_to_dbt_yaml import parse_dbml, dbml_to_dbt_yaml

class TestDbmlConverter(unittest.TestCase):
    def setUp(self):
        self.sample_dbml = '''
Table dim_address {
  note: "Represents unique addresses"
  address_key varchar [pk, unique, note: "Primary key for address"]
  city varchar [note: "City name"]
}
'''

    def test_parse_dbml(self):
        tables = parse_dbml(self.sample_dbml)

        self.assertEqual(len(tables), 1)
        self.assertEqual(tables['dim_address']['models'][0]['name'], 'dim_address')
        self.assertEqual(tables['dim_address']['models'][0]['description'], 'Represents unique addresses')

        columns = tables['dim_address']['models'][0]['columns']
        self.assertEqual(len(columns), 2)

        address_key = columns[0]
        self.assertEqual(address_key['name'], 'address_key')
        self.assertEqual(address_key['type'], 'varchar')
        self.assertEqual(address_key['description'], 'Primary key for address')
        self.assertTrue(address_key.get('primary_key', False))

    def test_dbml_to_yaml(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a temporary DBML file
            dbml_path = os.path.join(tmpdir, 'schema.dbml')
            with open(dbml_path, 'w') as f:
                f.write(self.sample_dbml)

            # Convert DBML to YAML
            dbml_to_dbt_yaml(dbml_path, tmpdir)

            # Check if YAML file was created
            yaml_path = os.path.join(tmpdir, 'dim_address.yml')
            self.assertTrue(os.path.exists(yaml_path))

            # Validate YAML content
            with open(yaml_path, 'r') as f:
                yaml_content = yaml.safe_load(f)

            self.assertEqual(yaml_content['version'], 2)
            self.assertEqual(yaml_content['models'][0]['name'], 'dim_address')

if __name__ == '__main__':
    unittest.main()