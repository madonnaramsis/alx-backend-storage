#!/usr/bin/env python3
"""Using pymongo"""


def top_students(mongo_collection):
    """Get all students sorted by avg_score"""

    students = mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])

    return students
