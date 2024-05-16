#!/usr/bin/env python3
""" Get Page function """
import requests
import redis
from functools import wraps

CONNECTION = redis.Redis()


def trackAndCache(method):
    """
    A decorator which:
        Cache url data if it's not cached
        Return cached data if exists
        Track the access of the url and cache it
    """
    @wraps(method)
    def wrapper(url):
        urlKey = "cached:" + url
        urlData = CONNECTION.get(urlKey)
        if urlData:
            return urlData.decode("utf-8")
        urlAccessCounter = "count:" + url
        data = method(url)
        CONNECTION.incr(urlAccessCounter)
        CONNECTION.set(urlKey, data)
        CONNECTION.expire(urlKey, 10)
        return data
    return wrapper


@trackAndCache
def get_page(url: str) -> str:
    """ Retrieves the HTML content of a given url """
    data = requests.get(url)
    return data.text
