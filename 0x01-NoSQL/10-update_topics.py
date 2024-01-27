#!/usr/bin/env python3


"""
MongoDB Operations with Python using pymongo
"""


def update_topics(mongo_collection, name, topics):
    """changes all topics of a school document based on the name"""
    var = {"name": name}
    NewVars = {"$set": {"topics": topics}}

    mongo_collection.update_many(var, NewVars)
