import collections
import time
from typing import Any, Optional

class TabLRU:
    def __init__(self, capacity: int = 1000):
        self.capacity = capacity
        # OrderedDict inherently uses a hash map + doubly linked list in CPython
        self.cache: collections.OrderedDict = collections.OrderedDict()

    def get(self, tab_id: str) -> Optional[Any]:
        """
        Get tab info and move it to the end (most recently used).
        O(1) time complexity.
        """
        if tab_id not in self.cache:
            return None
        self.cache.move_to_end(tab_id)
        return self.cache[tab_id]

    def put(self, tab_id: str, tab_info: Any) -> None:
        """
        Add or update tab info. If capacity is exceeded, evict the least recently used tab.
        O(1) time complexity.
        """
        # Ensure last_accessed is updated
        if "last_accessed" not in tab_info:
            tab_info["last_accessed"] = time.time()
            
        self.cache[tab_id] = tab_info
        self.cache.move_to_end(tab_id)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def touch(self, tab_id: str) -> None:
        """
        Mark a tab as recently used and update its last_accessed time.
        O(1) time complexity.
        """
        if tab_id in self.cache:
            self.cache.move_to_end(tab_id)
            self.cache[tab_id]["last_accessed"] = time.time()

    def evict_idle(self, timeout_seconds: int) -> list[tuple[str, Any]]:
        """
        Evict tabs that have been idle for longer than `timeout_seconds`.
        Returns a list of evicted (tab_id, tab_info) tuples.
        """
        current_time = time.time()
        evicted = []
        
        # Iterate from the start (least recently used)
        for tab_id, tab_info in list(self.cache.items()):
            last_accessed = tab_info.get("last_accessed", 0)
            if current_time - last_accessed > timeout_seconds:
                evicted.append((tab_id, tab_info))
                del self.cache[tab_id]
            else:
                # Since the OrderedDict is ordered by access time, 
                # if we hit a tab that hasn't timed out, subsequent tabs 
                # (which are more recently used) won't have timed out either.
                break
                
        return evicted
        
    def __len__(self):
        return len(self.cache)
