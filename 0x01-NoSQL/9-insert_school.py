#!/usr/bin/env python3
"""Using mymongo"""


def insert_school(mongo_collection, **kwargs):
    """ Insert new doc """
    doc = mongo_collection.insert(kwargs)
    return doc
