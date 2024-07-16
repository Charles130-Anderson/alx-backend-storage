#!/usr/bin/env python3
""" MongoDB Operations with Python using pymongo """


def top_students(mongo_collection):
    """
    Returns all students sorted by average score.
    """
    # Calculate average score for each student
    students = mongo_collection.aggregate([
        {
            "$project": {
                "name": 1,
                "averageScore": { "$avg": "$topics.score" }
            }
        },
        { "$sort": { "averageScore": -1 } }
    ])

    # Convert cursor to list and return
    return list(students)
