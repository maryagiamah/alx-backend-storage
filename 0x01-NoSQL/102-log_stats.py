#!/usr/bin/env python3
"""Write a Python script that provides some stats about Nginx logs"""
from pymongo import MongoClient


def count_logs(nginx_col):
    """Provides some stats about Nginx logs"""
    count = nginx_col.estimated_document_count()
    print(f'{count} logs')
    print('Methods:')

    for stat in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = nginx_col.count_documents({"method": stat})
        print(f'\tmethod {stat}: {count}')

    count = nginx_col.count_documents({"method": "GET", "path": "/status"})
    print(f'{count} status check')

    top_IPs = nginx_col.aggregate([
        {
            '$sortByCount': '$ip'
        },
        {
            '$limit': 10
        }
        ])

    print('IPs:')
    for ip_count in top_IPs:
        print(f"\t{ip_count.get('_id')}: {ip_count.get('count')}")


if __name__ == '__main__':
    client = MongoClient('mongodb://127.0.0.1:27017')
    count_logs(client.logs.nginx)
