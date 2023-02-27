from utils import *
from sys import argv
from stockData import StockData
from typing import Any, NoReturn
from ai import stock_predictor

"""
notes && things to do:
	...
"""

class HistoricalData():
	# for storing historical data about a stock (one day)
    def __isDividend(self) -> bool:
        if "dividend" in self.__open.lower() or "stock split" in self.__open.lower(): return True
        return False
    def __init__(self, open: int, high: int, low: int, close: int, date: str) -> None:
        self.__open = open
        self.__close = close
        self.__high = high
        self.__low = low
        self.__date = format_date(date)
        return
    def as_csv_line(self) -> str:
        if(not self.__isDividend()): return f"\n{self.__date},{self.__open},{self.__high},{self.__low},{self.__close}"
        else: return ""

def checkStock(stockName: str, epochs: int = None) -> None:
	global openThreads, stockLock

	# call server
	serverResponse = get(f"http://localhost:3000/historicalData/{stockName}", "json")
	
	if(serverResponse["status"] == "OK"):
		csvFile = stockName+".csv"

		# store historical data
		historicalData = list()
		for item in serverResponse["content"]["data"]: historicalData.append(HistoricalData(item["open"], item["high"], item["low"], item["close"], item["date"]))
		csvBuffer = "date,open,high,low,close"
		for item in historicalData: csvBuffer += item.as_csv_line()
		writeFile(csvBuffer, csvFile)

		# run ai
		stockData = StockData(stockName, stock_predictor(csvFile, epochs))
		# stockData = StockData(stockName, 0.0)

		# delete temp file
		deleteFile(csvFile)

		# store stock data in shared memory
		data = stockLock.access()
		data.append(stockData)
		stockLock.relock(data)
	else: print(f"Server error --> Stock: {stockName}")

	# decrement thread count
	openThreads -= 1

def main(epochs: int = None, inputFn: str = None) -> int:
	"""
	solving the too many threads open at one time problem:
			run cpu_count() number of stocks at a time, with limiter outside of thread pool
			pseudocode:
				read data from input file
				create counter variable
				WHILE counter variable is less than number of symbols:
					IF number of open threads is less than number of logical cores minus 1:
						open new thread:
							increment number of open threads
							get request historical stock data
							write data from response to csv file
							run ai
							put results into shared memory diction
							decrement number of open threads
						END THREAD
					ELSE:
						cull dead threads out of thread pool
						sleep n seconds
					END IF
					increment counter
				END LOOP
				join remaining threads
				write dictionary to file
	"""
	# initialize variables
	global openThreads
	if inputFn is None: inputFn = "symbol_list.txt"
	if epochs is None: epochs = 100
	count = 0

	# read stock symbols and split lines into list
	outputFn = "stock_results.toml"
	stockSymbols = list(set(readFile(inputFn, splitLines = True)))
	for i in range(len(stockSymbols)): stockSymbols[i] = stockSymbols[i].lower() # not case sensitive

	# main loop
	while(count < len(stockSymbols)):
		symbol = stockSymbols[count]
		if(openThreads < cpu_count()-1):
			# open thread available
			stockThreads.open(checkStock, symbol, epochs)
			openThreads += 1
			count += 1
		else:
			# no space for new thread, try to cull and sleep
			stockThreads.cull()
			sleep(3)
	
	# format shared memory to be written to toml file
	stockDict = dict()
	while(openThreads != 0 or len(stockLock) > 0):
		stockList = stockLock.access()
		# print("open threads: ", openThreads, "\n\tstock list: ", stockList, "\n\tlength: ", len(stockList))
		# for i in range(len(stockList)-1, -1):
		# 	print("in for loop --> i: ", i)
		# 	stockDict[stockList[i].getName()] = stockList[i].formatToml()
		# 	stockList.pop(i)
		for stock in stockList:
			stockDict[stock.getName()] = stock.formatToml()
			stockList.remove(stock)
		stockLock.relock(stockList)
		sleep(5)
	
	# write data to toml file
	writeFile(stockDict, outputFn)
	return 0

if(__name__ == "__main__"):
	epochs = None # number of epochs for ai training (per stock)
	fn = None # input file name
	if(len(argv) >= 2):
		try: epochs = int(argv[1])
		except KeyboardInterrupt: panic(KeyboardInterrupt)
		except Exception: pass
	if(len(argv) >= 3):
		if(isFile(argv[2])): fn = argv[2]
	res = main(epochs, fn)