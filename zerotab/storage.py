import gzip
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

class TabStorage:
    def __init__(self, storage_dir: str = "~/.zerotab"):
        self.storage_dir = Path(os.path.expanduser(storage_dir))
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
    def _get_file_path(self, tab_id: str) -> Path:
        # Sanitize tab_id to be a valid filename
        safe_id = "".join(c for c in tab_id if c.isalnum() or c in ('-', '_')).rstrip()
        return self.storage_dir / f"{safe_id}.json.gz"

    def save_tab(self, tab_id: str, tab_data: Dict[str, Any]) -> None:
        """
        Serialize tab state into JSON and compress it with gzip.
        """
        file_path = self._get_file_path(tab_id)
        json_data = json.dumps(tab_data).encode('utf-8')
        
        with gzip.open(file_path, 'wb') as f:
            f.write(json_data)

    def load_tab(self, tab_id: str) -> Optional[Dict[str, Any]]:
        """
        Load and decompress tab state from disk.
        """
        file_path = self._get_file_path(tab_id)
        if not file_path.exists():
            return None
            
        try:
            with gzip.open(file_path, 'rb') as f:
                json_data = f.read().decode('utf-8')
                return json.loads(json_data)
        except (gzip.BadGzipFile, json.JSONDecodeError, OSError):
            return None

    def delete_tab(self, tab_id: str) -> None:
        """
        Delete a compressed tab state from disk.
        """
        file_path = self._get_file_path(tab_id)
        if file_path.exists():
            try:
                file_path.unlink()
            except OSError:
                pass
                
    def get_total_size(self) -> int:
        """
        Get the total size (in bytes) of all compressed tab states on disk.
        """
        total_size = 0
        for f in self.storage_dir.glob("*.json.gz"):
            if f.is_file():
                total_size += f.stat().st_size
        return total_size
