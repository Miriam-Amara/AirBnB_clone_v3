#!/usr/bin/env python3

from dotenv import load_dotenv
import os

load_dotenv()

if os.getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()
elif os.getenv("HBNB_TYPE_STORAGE") == "file":
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()
