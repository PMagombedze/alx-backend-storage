#!/usr/bin/env python3


"""
Nginx stats
"""


from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient("mongodb://127.0.0.1:27017")
    nginxStats = client.logs.nginx

    print(nginxStats.count_documents({}), "logs")
    print("Methods:")
    print("\tmethod GET:", nginxStats.count_documents({"method": "GET"}))
    print("\tmethod POST:", nginxStats.count_documents({"method": "POST"}))
    print("\tmethod PUT:", nginxStats.count_documents({"method": "PUT"}))
    print("\tmethod PATCH:", nginxStats.count_documents({"method": "PATCH"}))
    print("\tmethod DELETE:", nginxStats.count_documents({"method": "DELETE"}))
    print(nginxStats.count_documents({"method": "GET", "path": "/status"}),
          "status check")
