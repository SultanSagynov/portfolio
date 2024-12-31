import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def process_column_x(file_path, output_path, window_size, prominence):

    # Load the CSV file
    try:
        df = pd.read_csv(file_path)
        if 'avg' not in df.columns:
            print("Error: Column 'avg' not found in the CSV file.")
            return
    except Exception as e:
        print(f"Error reading the file: {e}")
        return

    # Standardized data
    df['prim_standardized'] = (df['avg'] - df['avg'].mean()) / df['avg'].std()

    # Moving average
    df['prim_moving_average'] = df['avg'].rolling(window=window_size).mean()

    # Detect peaks
    peaks_standardized, _ = find_peaks(df['prim_standardized'].fillna(0), prominence=prominence)
    peaks_moving_average, _ = find_peaks(df['prim_moving_average'].fillna(0), prominence=prominence)
    
    # Mark peaks
    df['X_standardized_peaks'] = False
    df['X_moving_average_peaks'] = False
    df.loc[peaks_standardized, 'X_standardized_peaks'] = True
    df.loc[peaks_moving_average, 'X_moving_average_peaks'] = True
    
    # Save the processed data
    try:
        df.to_csv(output_path, index=False)
        print(f"Processed data with peaks saved to: {output_path}")
    except Exception as e:
        print(f"Error saving the file: {e}")
    
    
    # Visualization
    plt.figure(figsize=(14, 10))

    # Standardized data plot
    plt.subplot(2, 1, 1)
    plt.plot(df['prim_standardized'],label='Standardized Data', color='blue')
    plt.scatter(peaks_standardized, df['prim_standardized'][peaks_standardized], color='red', label='Peaks')
    plt.title('Peaks in Standardized Data')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.legend()

    # Moving average plot
    plt.subplot(2, 1, 2)
    plt.plot(df['prim_moving_average'], label='Moving Average', color='green')
    plt.scatter(peaks_moving_average, df['prim_moving_average'][peaks_moving_average], color='orange', label='Peaks')
    plt.title('Peaks in Moving Average Data')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.legend()

    # Show the plots
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
   
    input_file = r"c:\Users\SSagynov\python_exp\peak_finder_scipy\PHH.csv" 
    output_file = r"c:\Users\SSagynov\python_exp\peak_finder_scipy\prim_flags.csv"  
   
    process_column_x(input_file,output_file, window_size=5, prominence=1)

# further changes: change for dynamic URLs