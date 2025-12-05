import json
import os
from pathlib import Path
from typing import Dict, Any

class Settings:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent.parent
        self.config_path = self.base_dir / "config" / "rules.json"
        self.rules = self._load_rules()
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model_name = os.getenv("MODEL_NAME", "claude-3-5-haiku-20241022")

    def _load_rules(self) -> Dict[str, Any]:
        with open(self.config_path, "r") as f:
            return json.load(f)

settings = Settings()
