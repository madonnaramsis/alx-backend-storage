#!/usr/bin/env python3
"""Using mymongo"""


def update_topics(mongo_collection, name, topics):
    """Update based on given name"""
    query = {"name": name}
    values = {"$set": {"topics": topics}}

    mongo_collection.update_many(query, values)
