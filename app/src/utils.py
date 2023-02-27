from os import path, remove
from sys import platform
from json import load, dump
from subprocess import Popen
from threading import Thread, Lock
from multiprocessing import Process, cpu_count
from typing import NoReturn
from datetime import datetime
from inspect import stack as programStack
from toml import load as tomlLoad, dump as tomlDump
from time import sleep
from typing import Any, NoReturn

import requests

# threading && processes
class Processes():
    # DEPRECATED --> USE THREADS INSTEAD <-- DEPRECATED
    def __init__(self) -> None:
        self.__processes = list()
    def open(self, func, *args) -> int:
        # open new process
        key = -1
        try:
            self.__processes.append(Process(target = func, args = tuple(args), daemon = True))
            key = len(self.__processes)-1
            if(key > -1): self.__processes[key].start()
        except Exception as e: panic(e)
        return key
    def close(self, key: int) -> bool:
        # close a process
        try:
            if(self.__processes[key] and self.__processes[key].is_alive()):
                self.__processes[0].terminate()
                self.__processes[0].pop()
            return True
        except KeyError: print(f"{key} is invalid key")
        except Exception as e: panic(e)
        return False
    def panic(self) -> None:
        # error occurred, kill processes (deprecated, processes are now daemons)
        for process in self.__processes:
            if(process and process.is_alive()): process.terminate()
class Threads():
    def __len__(self) -> int: return len(self.__threads) # number of open threads
    def __init__(self) -> None: self.__threads = list()
    def open(self, func, *params) -> int:
        # open a new thread that runs function func with arguments args
        t = Thread(target = func, args = params, daemon=True)
        # while(len(self.__threads) >= cpu_count): pass
        t.start()
        self.__threads.append(t)
        return len(self.__threads)-1
    def join(self, key: int) -> bool:
        # attempt to join a thread by its current id
        try:
            self.__threads[key].join()
            self.__threads.pop(key)
        except KeyboardInterrupt: panic(KeyboardInterrupt)
        except Exception: return False
    def joinThreadPool(self) -> None:
        # attempts to join all threads in thread pool
        count = 0
        while(len(self.__threads) > 0):
            if(count < len(self.__threads)):
                self.__threads[count].join()
                self.__threads.pop(count)
            if(count < len(self.__threads)-1): count += 1
            else: count = 0
            sleep(2)
        return
    def cull(self) -> None:
        # joins dead threads in thread pool
        count = 0
        while(count < len(self.__threads)):
            if(not self.__threads[count].is_alive()):
                self.__threads[count].join()
                self.__threads.pop(count)
            count += 1
        return
class ListLock(): # for making sure that only one thread can modify a list at a time
    def __len__(self) -> int: return len(self.__data) # length of list
    def __init__(self, data: list = None) -> None:
        self.__lock = Lock()
        if data is None: data = list()
        self.__data = data
        self.__length = len(self.__data)
        return
    def access(self) -> list | None:
        # locks the list and returns the list
        self.__lock.acquire()
        try: return self.__data
        except KeyboardInterrupt: panic(KeyboardInterrupt)
        except Exception as e: print(e)
        return None
    def relock(self, updated: list = None) -> bool:
        """ !!! PLEASE RENAME THIS, IT DOESN'T MAKE SENSE !!! """
        # updates the data if not null and unlocks the list
        try:
            if(updated):
                self.__data = updated
                self.__length = len(self.__data)
            self.__lock.release()
            return True
        except KeyboardInterrupt: panic(KeyboardInterrupt)
        except Exception as e: print(e)
        return False
def runThread(func, *params) -> Thread:
    # consider making a structure similar to Processes?
    # DEPRECATED --> FOR ABOVE REASON, USE THREADS CLASS INSTEAD <-- DEPRECATED
    t = Thread(target=func, args = params)
    t.start()
    return t
def multiProcess(func, *args) -> Process:
    # DEPRECATED --> USE PROCESSES.OPEN() INSTEAD <-- DEPRECATED
    p = Process(target = func, args = tuple(args))
    p.start()
    return p

# globals (shared memory)
stockThreads = Threads()
openThreads = 0
stockLock = ListLock(list())
processes = Processes() # deprecated

# error handling
def panic(error: str | Exception = None) -> NoReturn:
    if(not error): error = "Something went wrong!"
    callingFunc = programStack()[1].function
    writeFile(f"{datetime.now()}:\n\t{callingFunc}\n\t{str(error)}", "./error.log", "a")
    processes.panic()
    exit()

# file i/o
def readFile(fn: str, binary: bool = None, splitLines: bool = None) -> str | dict | list:
    if binary is None: binary = False
    if splitLines is None: splitLines = False
    data = ""
    mode = "r"
    if(binary): mode = "rb"
    try:
        with open(fn, mode) as file:
            match fn.split(".")[-1]:
                case "json": data = load(file)
                case "txt" | "csv": data = file.read()
                case "toml": data = tomlLoad(file)
                case other:
                    print(f"tried to read unknown file extension: {fn.split('.')[-1]}")
                    return False
            if(splitLines):
                try: data = data.split("\n")
                except KeyboardInterrupt: panic(KeyboardInterrupt)
                except Exception as e: print(e)
    except KeyboardInterrupt: panic(KeyboardInterrupt)
    except Exception as e: print(e)
    return data
def writeFile(data: str | dict, fn: str, mode: str = None) -> bool:
    if mode not in {"w", "a", "wb", "ab"} or not path.isfile(fn): mode = "w"
    if mode == "a" and type(data) == type(str()): data = f"\n{data}"
    try:
        with open(fn, mode) as file:
            match fn.split(".")[-1]:
                case "json": dump(data, file, indent = 4)
                case "txt" | "csv": file.write(data)
                case "toml": tomlDump(data, file)
                case other:
                    print(f"Warning: writing data to extension {fn.split('.')[-1]}. readFile will not be able to read this data!")
                    file.write(data)
        return True
    except KeyboardInterrupt: panic(KeyboardInterrupt)
    except Exception as e: print(e)
    return False
def isFile(fn: str) -> bool: return path.isfile(fn)
def readLine(fn: str, lineNumber: int) -> str:
    data = ""
    try:
        if(isFile(fn)):
            count = 0
            line = ""
            with open(fn) as file:
                while(count < lineNumber):
                    line = file.readline()
                    if(line == "" or line is None): break # terrible solution, i know
                    count += 1
            data = line
    except Exception as e: panic(e)
    return data
def deleteFile(fn: str) -> bool:
    if(isFile(fn)):
        remove(fn)
        return True
    return False

# system
def pout(command: str) -> bool:
    try:
        Popen(command).wait()
        return True
    except KeyboardInterrupt: panic(KeyboardInterrupt)
    except Exception as e: print(e)
    return

# requests
def get(url: str, type: str = None, params: list = None) -> str | dict | None:
    if type is None: type = "json"
    try:
        r = requests.get(url = url, params = params)
        if(type == "json"): return r.json()
        if(type == "txt"): return r.text()
        else:
            print(f"unrecognized type: {type}")
            return None
    except KeyboardInterrupt: panic(KeyboardInterrupt)
    except Exception as e: print(e)
    return None
def post(url: str, headers: dict = None, data: dict | list = None) -> str | dict | None: return requests.post(url = url, headers = headers, json = data)

# datetime
def format_date(dateString: str) -> str:
    # Parse the date string into a datetime object
    date = datetime.strptime(dateString, '%b %d, %Y')

    # Convert the datetime object to a string in "YYYY-MM-DD" format
    formatted_date = date.strftime('%Y-%m-%d')

    return formatted_date

# typing
def isNumber(string: str) -> bool:
    try: int(string)
    except KeyboardInterrupt: panic(KeyboardInterrupt)
    except Exception: return False
    return True