import unittest
from unittest.mock import patch, mock_open
import importPlanets


class TestPlanetImporter(unittest.TestCase):

    def test_read_json_valid_json(self):
        """Test that read_json correctly parses valid JSON."""
        valid_json = '{"id": 1, "name": "Earth"}'
        result = importPlanets.read_json(valid_json)
        self.assertEqual(result['id'], 1)
        self.assertEqual(result['name'], "Earth")

    def test_read_json_invalid_json(self):
        """Test that read_json raises an error for invalid JSON."""
        invalid_json = '{"id": 1, "name": "Earth"'
        with self.assertRaises(SystemExit):
            importPlanets.read_json(invalid_json)

    def test_read_json_wrong_format(self):
        """Test that read_json handles JSON with unexpected format."""
        wrong_format_json = 'not a json string'
        with self.assertRaises(SystemExit):
            importPlanets.read_json(wrong_format_json)

    @patch("builtins.open", new_callable=mock_open)
    def test_save_file(self, mock_file):
        """Test that save_file writes the correct data to the expected file."""
        obj = '{"id": 1, "name": "Earth"}'
        data = {"id": 1, "name": "Earth"}

        with patch("importPlanets.DESTINATION_DIR", "/mock/dir/"):
            importPlanets.save_file(obj, data)

        mock_file.assert_called_once_with("/mock/dir/1.json", "w")
        handle = mock_file()
        handle.write.assert_called_once_with(obj)

    @patch("builtins.open", new_callable=mock_open, read_data='{"id": 1, "name": "Earth"}\n{"id": 2, "name": "Mars"}')
    @patch("importPlanets.save_file")
    def test_main_process(self, mock_save_file, mock_open_file):
        """Test the main process of reading and saving files."""
        with patch("importPlanets.TEXT_FILE", "/mock/textfile.txt"):
            with patch("importPlanets.DESTINATION_DIR", "/mock/dir/"):
                importPlanets.main()

        self.assertEqual(mock_save_file.call_count, 2)

    @patch("builtins.print")
    def test_fail_function(self, mock_print):
        """Test the fail function inside read_json."""
        with self.assertRaises(SystemExit):
            importPlanets.read_json("invalid")

        mock_print.assert_any_call("Loading data failed: Invalid JSON")


if __name__ == "__main__":
    unittest.main()
