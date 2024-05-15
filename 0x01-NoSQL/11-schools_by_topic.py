#!/usr/bin/env python3
"""Using mymongo"""


def schools_by_topic(mongo_collection, topic):
    """Getting matched docs with the given topic"""
    docs = mongo_collection.find({"topics": topic})
    docsList = [d for d in docs]
    return docsList
