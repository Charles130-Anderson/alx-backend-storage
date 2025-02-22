#!/usr/bin/env python3
"""
Module to update topics of a school document in MongoDB collection
"""


def update_topics(mongo_collection, name, topics):
    """Updates topics of a school document based on its name"""
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
