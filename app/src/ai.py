import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

"""
this was modeled after an example from ChatGTP
"""

def stock_predictor(csv_file_path: str, epochCount: int) -> np.float32:
    # Load CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Normalize the data
    data = df[['open', 'high', 'low', 'close']].values
    data = (data - np.mean(data, axis=0)) / np.std(data, axis=0)
    
    # Create X and y arrays for training the neural network
    X = data[:-1]
    y = (df['close'].shift(-1) > df['close']).values[:-1].astype(int)
    
    # Create a neural network model
    model = Sequential([
        Dense(64, activation='relu', input_shape=(4,)),
        Dense(64, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy')
    
    # Train the model
    model.fit(X, y, epochs=epochCount, validation_split=0.2)
    
    # Use the model to predict whether the stock should be purchased
    last_data = data[-1:]
    prediction = model.predict(last_data)[0][0]
    
    return prediction