#!/usr/bin/env python3
"""Using redis with python"""
import redis
from typing import Union, Callable
from uuid import uuid4
from functools import wraps


def replay(function: Callable):
    """Display the history of calls of a particular function"""
    connection = redis.Redis()
    functionName = function.__qualname__
    functionCalls = connection.get(functionName)
    try:
        functionCalls = functionCalls.decode('utf-8')
    except Exception:
        functionCalls = 0
    print(f'{functionName} was called {functionCalls} times:')

    inputs = connection.lrange(functionName + ":inputs", 0, -1)
    outputs = connection.lrange(functionName + ":outputs", 0, -1)

    for input, output in zip(inputs, outputs):
        try:
            input = input.decode('utf-8')
        except Exception:
            input = ""
        try:
            output = output.decode('utf-8')
        except Exception:
            output = ""
        print(f'{functionName}(*{input}) -> {output}')


def count_calls(method: Callable) -> Callable:
    """ A counter decorator that counts the calls and store it in redis """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ The counter callable """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ A decorator that stores the history of inputs and outputs """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ The store logic callable """
        inputKey = method.__qualname__ + ":inputs"
        outputKey = method.__qualname__ + ":outputs"
        output = method(self, *args, **kwargs)
        self._redis.rpush(inputKey, str(args))
        self._redis.rpush(outputKey, str(output))
        return output
    return wrapper


class Cache:
    """ Class Cache that handles redis connection and methods """
    def __init__(self) -> None:
        """ Class constructor which starts the connection """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Stores the given data and return it's uuid generated key """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> str:
        """
        Retrieves the data of the given key
        and convert it with the given conversion function
        """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """ Retrieves the data of the given key and decode it """
        data = self._redis.get(key)
        return data.decode("utf-8")

    def get_int(self, key: str) -> int:
        """ Retrieves the data of the given key and convert it to int """
        data = self._redis.get(key)
        try:
            data = int(data)
        except Exception:
            data = 0
        return data
