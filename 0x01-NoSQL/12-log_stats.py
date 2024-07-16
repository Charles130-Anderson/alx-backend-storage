#!/usr/bin/env python3
"""Script to analyze Nginx logs in MongoDB."""
from pymongo import MongoClient

HTTP_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def log_stats(collection, method_filter=None):
    """Analyze logs and print statistics."""
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    if method_filter:
        method_count = collection.count_documents({"method": method_filter})
        print(f"\tmethod {method_filter}: {method_count}")
        return

    print("Methods:")
    for method in HTTP_METHODS:
        log_stats(collection, method)

    status_checks = collection.count_documents({"path": "/status"})
    print(f"{status_checks} status checks")


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    log_stats(nginx_collection)
