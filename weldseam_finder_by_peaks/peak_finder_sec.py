import pandas as pd

def calculate_moving_std(input_file, output_file, window_size=5, fluctuation_threshold=1):
    
    try:
        # Load the CSV file
        df = pd.read_csv(input_file)
        
        # Filter columns that start with "IRC"
        irc_columns = [col for col in df.columns if col.startswith("IRC")]
        
        if not irc_columns:
            print("No columns starting with 'IRC' found.")
            return
        
        # Create a new DataFrame for moving standard deviation
        df_moving_std = pd.DataFrame()
        for col in irc_columns:
            df_moving_std[f"{col}_moving_std"] = df[col].rolling(window=window_size).std()
        
        # Calculate the average standard deviation for each column
        avg_std = df[irc_columns].std()
        
        # Initialize fluctuation detection
        fluctuation_flags = pd.DataFrame(index=df.index)
        
        # Detect fluctuations where moving standard deviation > average standard deviation
        for col in irc_columns:
            
            fluctuation_flags[col] = df_moving_std[f"{col}_moving_std"] > (avg_std[col] * fluctuation_threshold)

        # Determine paternal fluctuations (90% of channels showing fluctuation)
        paternal_fluctuations = fluctuation_flags.sum(axis=1) > (0.8 * len(irc_columns))

        # Save the moving standard deviations and fluctuation flags DataFrame to a new file
        df_moving_std['paternal_fluctuation'] = paternal_fluctuations
        df_moving_std.to_csv(output_file, index=False)
        print(f"Moving standard deviations and paternal fluctuations saved to: {output_file}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Example usage
    input_file = r"c:\Users\SSagynov\python_exp\peak_finder_scipy\IRC.csv" 
    output_file = r"c:\Users\SSagynov\python_exp\peak_finder_scipy\sec_flags.csv"
    window_size = 5  # Adjust the window size for the moving standard deviation
    fluctuation_threshold = 1  # Adjust the threshold factor for fluctuation detection
    
    calculate_moving_std(input_file, output_file, window_size, fluctuation_threshold)
