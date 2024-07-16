#!/usr/bin/env python3

"""
Counts logs and HTTP methods in MongoDB collection.
"""

from pymongo import MongoClient

def main():
    """
    Main function to gather and print log statistics.
    """
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['logs']
    collection = db['nginx']

    # Count total logs
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    # Count logs by HTTP methods
    methods_count = {"GET": 0, "POST": 0, "PUT": 0, "PATCH": 0, "DELETE": 0}
    for doc in collection.find({}, {"_id": 0, "method": 1}):
        methods_count[doc["method"]] += 1

    print("\nMethods:")
    for method, count in methods_count.items():
        print(f"\tmethod {method}: {count}")

    # Special case for GET requests to /status path
    status_get_count = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_get_count} status check")

if __name__ == "__main__":
    main()
