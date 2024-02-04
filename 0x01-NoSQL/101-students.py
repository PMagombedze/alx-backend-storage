#!/usr/bin/env python3


from pymongo import MongoClient

def top_students(mongo_collection):
    # Use the aggregate function to calculate the average and sort
    pipeline = [
        {"$unwind": "$scores"},
        {"$group": 
            {"_id": "$_id", 
             "averageScore": {"$avg": "$scores.score"}, 
             "name": {"$first": "$name"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ]
    return list(mongo_collection.aggregate(pipeline))
