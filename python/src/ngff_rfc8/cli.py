"""
Command-line script, exposed via the `ngff-rfc8-validate` entrypoint.
"""

import json
import sys
from pathlib import Path

from ngff_rfc8.validate import validate_collection


def cmd_validate() -> None:
    """
    Validate a JSON file.
    """
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file>")

    file_path = Path(sys.argv[1])

    if not file_path.is_file():
        sys.exit(f"Error: file does not exist: {file_path}")

    data = json.loads(file_path.read_text())
    validate_collection(data)
    print(f"Collection {file_path} is valid")
