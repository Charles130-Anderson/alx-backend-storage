#!/usr/bin/env python3
"""Nginx log statistics from MongoDB."""
from pymongo import MongoClient

def display_nginx_log_stats():
    """Displays statistics about Nginx logs stored in MongoDB."""
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        method_count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    status_check_count = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )
    print(f"{status_check_count} status check")

if __name__ == "__main__":
    display_nginx_log_stats()
