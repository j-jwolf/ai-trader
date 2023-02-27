# Artificial Intelligence Trading Partner
## John Wolf

## Table of Contents:
1. Before Using
2. Use
3. Troubleshooting

## 1. Before Using
Please note that it is impossible to predict the stock market with only historical data. The purpose o f this program is to showcase my abilities with multithreading, artificial intelligence, web and software development, and concurrency. This tool may give you insight into a good stock to purchase, but it is not, and will never be, 100% accurate, or even close to it. Please note this if you decide to purchase a stock this AI recommends.

## 2. Use
To use this tool, you will need to use the command line to run a Python program. There is also the option of using the <a href="https://github.com/j-jwolf/fox-package-manager">Fox Package Manager</a> to run this program and manage all of the dependencies for you.

You will need Node.js to run the backend of this program. You will also need the following modules installed:
1. Express
2. Cheerio
3. Request
4. CORS

You can install Node.js <a href="https://nodejs.org/en/download/">here</a>.

To install a node module, run the following:
```
npm install moduleName
```

Replace moduleName with every required module.

### Without the Fox Package Manager
To run the program without the package manager, you will need the following dependencies:
1. numpy
2. pandas
3. tensorflow
4. scikit-learn
5. toml

#### If you do not have them installed
Run the following command:
```
python -m pip install dependency-name
```
and replace 'dependency-name' with the names of the dependencies.

With all of the packages installed, finally run the following command:
```
python main.py numberOfEpochs inputFilename
```

### With the Fox Package Manager
Simply run the following command:
```
%fox% run numberOfEpochs inputFilename
```


The number of epochs and input filename are optional. The default values are 100 epochs and symbol_list.toml, respectively.

### What will happen?
The program will read the data from the input file. The data will be stock symbols (not case sensitive) and each symbol will be separated by a new line.

Example:
DUOL
BOWL
AAPL

The program will open threads to handle this quickly.

#### What will each thread do?
The program will contact the backend, which will scrape the stock's Yahoo Finance page for the historical data and return it to the application. The application will then move the data into a csv file named after its stock symbol and run the AI using that file as its input data. After the AI finishes, the thread will terminate.

The program has a read/write lock on the global data to ensure that the most updated copy of the data is used.

### Troubleshooting
...