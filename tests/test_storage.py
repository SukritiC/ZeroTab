import unittest
import os
import shutil
from pathlib import Path
from zerotab.storage import TabStorage

class TestTabStorage(unittest.TestCase):
    def setUp(self):
        self.test_dir = "/tmp/zerotab_test_storage"
        self.storage = TabStorage(storage_dir=self.test_dir)
        
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
            
    def test_save_and_load(self):
        tab_id = "http://example.com"
        tab_data = {"url": tab_id, "title": "Example", "last_accessed": 1234567890}
        
        self.storage.save_tab(tab_id, tab_data)
        loaded_data = self.storage.load_tab(tab_id)
        
        self.assertEqual(loaded_data, tab_data)
        
    def test_delete(self):
        tab_id = "http://delete.me"
        self.storage.save_tab(tab_id, {"url": tab_id})
        self.assertIsNotNone(self.storage.load_tab(tab_id))
        
        self.storage.delete_tab(tab_id)
        self.assertIsNone(self.storage.load_tab(tab_id))
        
    def test_total_size(self):
        self.assertEqual(self.storage.get_total_size(), 0)
        self.storage.save_tab("tab1", {"data": "A" * 1000})
        self.assertGreater(self.storage.get_total_size(), 0)

if __name__ == "__main__":
    unittest.main()
