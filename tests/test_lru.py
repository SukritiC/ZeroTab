import unittest
import time
from zerotab.lru import TabLRU

class TestTabLRU(unittest.TestCase):
    def test_lru_capacity(self):
        lru = TabLRU(capacity=3)
        lru.put("tab1", {"url": "http://tab1"})
        lru.put("tab2", {"url": "http://tab2"})
        lru.put("tab3", {"url": "http://tab3"})
        
        self.assertEqual(len(lru), 3)
        self.assertIsNotNone(lru.get("tab1"))
        
        # Pushing a 4th tab should evict the least recently used ("tab2" since "tab1" was just accessed)
        lru.put("tab4", {"url": "http://tab4"})
        self.assertEqual(len(lru), 3)
        self.assertIsNone(lru.get("tab2"))
        self.assertIsNotNone(lru.get("tab1"))
        self.assertIsNotNone(lru.get("tab3"))
        self.assertIsNotNone(lru.get("tab4"))

    def test_evict_idle(self):
        lru = TabLRU(capacity=3)
        lru.put("tab1", {"url": "http://tab1"})
        lru.put("tab2", {"url": "http://tab2"})
        
        # Manually alter last_accessed to simulate aging
        lru.cache["tab1"]["last_accessed"] = time.time() - 400
        lru.cache["tab2"]["last_accessed"] = time.time() - 100
        
        # Evict tabs older than 300 seconds
        evicted = lru.evict_idle(300)
        
        self.assertEqual(len(evicted), 1)
        self.assertEqual(evicted[0][0], "tab1")
        self.assertIsNone(lru.get("tab1"))
        self.assertIsNotNone(lru.get("tab2"))

if __name__ == "__main__":
    unittest.main()
