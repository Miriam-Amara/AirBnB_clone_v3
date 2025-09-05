#!/usr/bin/env python3

"""

"""


from api.v1.views import app_views
from models import storage


@app_views.route("/status")
def status() -> dict[str, str]:
    return {"status": "OK"}

@app_views.route("/stats")
def stats() -> dict[str, int]:
    """Returns the number of objects in storage"""
    return storage.count()
