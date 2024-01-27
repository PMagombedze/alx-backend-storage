#!/usr/bin/env python3


"""
insert school
"""


def insert_school(mongo_collection, **kwargs):
    """insert school"""
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
