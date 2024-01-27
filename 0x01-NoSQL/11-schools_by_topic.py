#!/usr/bin/env python3


"""
specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """returns the list of school having a specific topic"""
    items = mongo_collection.find({"topics": topic})
    list_docs = [x for x in items]
    return list_docs
