import pandas as pd
from dbfread import DBF
from joblib import load
import json

# Step 1: Load the trained model
def load_model(model_path):
    model = load(model_path)
    print(f"Model loaded from {model_path}")
    return model

# Step 2: Preprocess the new dataset
def preprocess_new_data(df, training_columns):
    df = df.dropna()
    df = pd.get_dummies(df, drop_first=True)

    # Ensure the new data has the same columns as the training data
    for col in training_columns:
        if col not in df.columns:
            df[col] = 0  # Add missing columns with default values

    # Align columns to match the training set
    df = df[training_columns]

    return df

# Step 3: Predict using the loaded model
def predict_on_new_data(model, new_file_path, training_columns):
    table = DBF(new_file_path, ignore_missing_memofile=True, load=True)
    new_df = pd.DataFrame(iter(table))

    print(f"New dataset loaded successfully from {new_file_path}")

    new_X = preprocess_new_data(new_df, training_columns)

    predictions = model.predict(new_X)
    new_df["Predictions"] = predictions

    print("Predictions added to the dataset.")

    # **RED: Add decoding logic for classification**
    # Load the reverse mapping
    with open(r"c:\Users\SSagynov\python_exp\exchange_compare\reverse_mapping.json", "r") as f:
        reverse_mapping = json.load(f)

    # Decode predictions
    def decode_predictions(predictions, reverse_mapping):
        rounded_preds = [round(pred) for pred in predictions]  # Round to nearest integer
        decoded_preds = [reverse_mapping[str(label)] for label in rounded_preds]
        return decoded_preds

    # **RED: Add the decoded predictions as a new column**
    new_df["Predicted_Class"] = decode_predictions(new_df["Predictions"], reverse_mapping)

    print("Classified predictions added to the dataset.")

    return new_df

# Step 6: Save predictions to a file
def save_predictions(predicted_df, output_file):
    predicted_df.to_csv(output_file, index=False)
    print(f"Predictions saved to {output_file}")

# Main Execution
if __name__ == "__main__":
    # Define paths
    model_path = r"C:\Users\SSagynov\python_exp\exchange_compare\2_random_forest_model.joblib"  
    new_file_path = r"c:\Users\SSagynov\python_exp\exchange_compare\12602.dbf"  
    output_file = r"c:\Users\SSagynov\python_exp\exchange_compare\predicted_results.csv"  

    # Load the trained model
    model = load_model(model_path)

    # Columns used in the training set
    # Manually add or read these from a saved file
    with open(r"c:\Users\SSagynov\python_exp\exchange_compare\training_columns.json", "r") as f:
        training_columns = json.load(f)

    # Predict on the new dataset
    predicted_df = predict_on_new_data(model, new_file_path, training_columns)

    # Save the predictions to a file
    save_predictions(predicted_df, output_file)
