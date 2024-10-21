#!/usr/bin/env python3
"""Write a Python function that returns the list of school"""


def schools_by_topic(mongo_collection, topic):
    """Returns the list of school having a specific topic"""
    return list(mongo_collection.find({"topics": topic}))
