"""Definicje ofert demo, wspólne dla obu komputerów."""
import json
from pathlib import Path


def load_demo_catalogue():
    path = Path(__file__).resolve().parent / "data/demo_products.json"
    return json.loads(path.read_text(encoding="utf-8"))
