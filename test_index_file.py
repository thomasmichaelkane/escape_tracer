import unittest
from escape_tracer.utils import keep_indexed_folders
import os

class TestKeepIndexedFolders(unittest.TestCase):
    def setUp(self):
        # Setup - Create a dummy index file and data folders
        self.index_file_path = "test_index.txt"
        self.data_folders = {
            "folder1": "data1",
            "folder2": "data2",
            "folder3": "data3",
            "folder4": "data4"
        }
        with open(self.index_file_path, 'w') as f:
            f.write("folder2\nfolder3\n")

    def tearDown(self):
        # Teardown - Remove the dummy index file after tests
        os.remove(self.index_file_path)

    def test_keep_indexed_folders(self):
        # Test that the function keeps only the folders listed in the index file
        expected_result = {
            "folder2": "data2",
            "folder3": "data3"
        }
        result = keep_indexed_folders(self.data_folders, self.index_file_path)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()