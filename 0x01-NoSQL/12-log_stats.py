#!/usr/bin/env python3
"""Provides statistics on Nginx logs."""
from pymongo import MongoClient

METHODS_TO_CHECK = ["GET", "POST", "PUT", "PATCH", "DELETE"]

def log_statistics(collection, option=None):
    """Displays stats on Nginx logs."""
    query = {}
    if option:
        count = collection.count_documents({"method": {"$regex": option}})
        print(f"\tmethod {option}: {count}")
        return
    
    total_logs = collection.count_documents(query)
    print(f"{total_logs} logs")
    print("Methods:")
    for method in METHODS_TO_CHECK:
        log_statistics(collection, method)
    
    status_count = collection.count_documents({"path": "/status"})
    print(f"{status_count} status check")

if __name__ == "__main__":
    nginx_collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx
    log_statistics(nginx_collection)
