#!/usr/bin/env python3


"""
list all
"""


def list_all(mongo_collection):
    """list all documents"""
    documents = mongo_collection.find()
    document_list = list(documents)
    return document_list
