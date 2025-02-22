#!/usr/bin/env python3
"""
Script to provide statistics about Nginx logs stored in MongoDB
"""


from pymongo import MongoClient


def print_stats(collection):
    """Prints statistics about Nginx logs"""
    # Total number of documents
    total_logs = collection.count_documents({})
    print("{} logs".format(total_logs))
    
    # Count documents for each HTTP method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({"method": method})
        print("    method {}: {}".format(method, count))
    
    # Count documents where method=GET and path=/status
    status_check = collection.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(status_check))



if __name__ == "__main__":
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs  # Connect to 'logs' database
    collection = db.nginx  # Connect to 'nginx' collection
    
    # Print statistics
    print_stats(collection)
