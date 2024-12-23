import pandas as pd
from dbfread import DBF
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
from joblib import dump
import json


# Step 1: Load the .dbf file into a DataFrame
def load_dbf(file_path):
    
    table = DBF(file_path,ignore_missing_memofile=True, load=True)  
    df = pd.DataFrame(iter(table))
    print("DataFrame loaded successfully!")
    return df

# Step 2: Explore the DataFrame
def explore_data(df):
   
    print("Head of the DataFrame:\n", df.head())
    print("\nData Types:\n", df.dtypes)
    print("\nMissing Values:\n", df.isnull().sum())
    print("\nSummary Statistics:\n", df.describe())

# Step 3: Preprocess the Data
def preprocess_data(df, target_column):
    X = df.drop(["TYPE", "COMMENT", "ID", "ANOM_NBR", "_NullFlags"], axis=1)
    y = df[target_column]

    X = X.dropna()
    y = y.dropna()

    X = pd.get_dummies(X, drop_first=True)

    label_mapping = {}
    reverse_mapping = {}
    
    if y.dtype == 'object' or isinstance(y.dtype, pd.CategoricalDtype):
        le = LabelEncoder()
        y = le.fit_transform(y) 
        label_mapping = dict(zip(le.classes_, range(len(le.classes_))))
        reverse_mapping = dict(zip(range(len(le.classes_)), le.classes_))
        
        # Save mappings to JSON files
        with open("label_mapping.json", "w") as f:
            json.dump(label_mapping, f)
        with open("reverse_mapping.json", "w") as f:
            json.dump(reverse_mapping, f)

    # Save training columns
    with open("training_columns.json", "w") as f:
        json.dump(list(X.columns), f)

    return X, y


# Step 4: Train and Test Model
def train_and_evaluate(X, y):
   
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    
    print(f"Training Features Shape: {X_train.shape}")
    print(f"Testing Features Shape: {X_test.shape}")
    print(f"Training Target Shape: {y_train.shape}")
    print(f"Testing Target Shape: {y_test.shape}")

    
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    
    y_pred = model.predict(X_test)

    
    mse = mean_squared_error(y_test, y_pred)
    print("\nModel Evaluation:")
    print(f"Mean Squared Error: {mse}")

    return model


file_path = r"c:\Users\SSagynov\python_exp\exchange_compare\12301.dbf"  
target_column = "TYPE" 


df = load_dbf(file_path)
explore_data(df)


X, y = preprocess_data(df, target_column)


model = train_and_evaluate(X, y)

# Step 5: Save the trained model
def save_model(model, file_name):
    dump(model, file_name)
    print(f"Model saved to {file_name}")


save_model(model, "2_random_forest_model.joblib")