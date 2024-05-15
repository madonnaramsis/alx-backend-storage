#!/usr/bin/env python3
"""Using mymongo"""


def list_all(mongo_collection):
    """Lists all Docs"""
    docs = mongo_collection.find()

    if docs.count() == 0:
        return []

    return docs
