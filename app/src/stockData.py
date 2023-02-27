from numpy import float32

class StockData():
    # structure for storing data about a stock, including its name, prediction from ai, and a message derived from the prediction (should you purchase?)
    def __determineMessage(self) -> None:
        if(self.__prediction):
            if(self.__prediction < 0.3): msg = "This stock should not be purchased"
            elif(self.__prediction < 0.5): msg = "This stock should probably not be purchased"
            elif(self.__prediction < 0.7): msg = "This stock should probably be purchased"
            else: msg = "This stock should be purchased"
        else: msg = None
        self.__message = msg
        return
    def __init__(self, name: str = None, prediction: float32 = None) -> None:
        self.__name = name
        self.__prediction = float(prediction)
        self.__determineMessage()
        return
    def setName(self, name: str) -> None: self.__name = name
    def setPrediction(self, prediction: float32) -> None: self.__prediction = prediction
    def setMessage(self) -> None:
        if(self.__prediction): self.__determineMessage()
    def getName(self) -> str: return self.__name
    def getPrediction(self) -> float32: return self.__prediction
    def getMessage(self) -> str | None: return self.__message
    def formatToml(self) -> dict: return {"prediction": self.__prediction, "message": self.__message} # formats data to be written to a toml file

stocks = list()