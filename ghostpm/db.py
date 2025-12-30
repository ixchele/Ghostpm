import os
import json
from ghostpm.paths import make_paths


def load():
    paths = make_paths()
    db_file = paths["DB_FILE"]

    if not os.path.exists(db_file):
        return {}

    with open(db_file) as f:
        return json.load(f)


def save(db):
    paths = make_paths()
    db_file = paths["DB_FILE"]

    os.makedirs(os.path.dirname(db_file), exist_ok=True)

    with open(db_file, "w") as f:
        json.dump(db, f, indent=2)
