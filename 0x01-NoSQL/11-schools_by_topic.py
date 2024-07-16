#!/usr/bin/env python3
"""
Module to retrieve schools by topic from MongoDB collection
"""
from pymongo import MongoClient

def schools_by_topic(mongo_collection, topic):
    """Returns a list of schools having a specific topic"""
    schools = mongo_collection.find({"topics": topic})
    return list(schools)
