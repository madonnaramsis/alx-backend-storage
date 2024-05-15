#!/usr/bin/env python3
"""Using pymongo"""
from pymongo import MongoClient

if __name__ == "__main__":
    """Get Nginx stats"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginxCollection = client.logs.nginx

    logsCounter = nginxCollection.count_documents({})
    print(f'{logsCounter} logs')

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('Methods:')
    for method in methods:
        count = nginxCollection.count_documents({"method": method})
        print(f'\tmethod {method}: {count}')

    status_check = nginxCollection.count_documents(
        {"method": "GET", "path": "/status"}
    )

    print(f'{status_check} status check')

    ips = nginxCollection.aggregate([
        {"$group":
            {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])

    print("IPs:")
    for ip in ips:
        ip = ips.get("ip")
        count = ip.get("count")
        print(f'\t{ip}: {count}')
