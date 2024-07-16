#!/usr/bin/env python3
"""
Module to insert a new school document in MongoDB collection
"""
from pymongo import MongoClient

def insert_school(mongo_collection, **kwargs):
    """Inserts a new document in the collection"""
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
