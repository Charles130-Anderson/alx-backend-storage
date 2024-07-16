#!/usr/bin/env python3
"""
Module to list all documents in a MongoDB collection
"""
from pymongo import MongoClient

def list_all(mongo_collection):
    """Return a list of all documents in the collection"""
    documents = list(mongo_collection.find())
    return documents if documents else []
