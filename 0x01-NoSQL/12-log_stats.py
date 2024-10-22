#!/usr/bin/env python3
"""Write a Python script that provides some stats about Nginx logs"""
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_col = client.logs.nginx
    
    count = nginx_col.count_documents({})
    print(f'{count} logs')
    print('Methods:')

    for stat in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = nginx_col.count_documents({"method": stat})
        print(f'    method {stat}: {count}')

    count = nginx_col.count_documents({"method": "GET", "path": "/status"})
    print(f'{count} status check')
