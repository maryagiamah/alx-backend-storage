#!/usr/bin/env python3
"""
Write a Python function that
lists all documents in a collection
"""


def list_all(mongo_collection):
    """lists all documents in a collection"""
    return [col for col in mongo_collection.find()]
