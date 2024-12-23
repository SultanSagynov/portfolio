import pandas as pd

def merge_and_define_results(prim_file, sec_file, output_file):
 
    try:
        # Load primary and secondary flags files
        prim_df = pd.read_csv(prim_file)
        sec_df = pd.read_csv(sec_file)
        
        # Ensure both DataFrames have the same number of rows
        if len(prim_df) != len(sec_df):
            raise ValueError("The primary and secondary files must have the same number of rows.")
        
        # Check required columns in primary and secondary files
        required_prim_columns = ['X_standardized_peaks', 'X_moving_average_peaks', 'dist_m']
        required_sec_columns = ['paternal_fluctuation']
        
        if not all(col in prim_df.columns for col in required_prim_columns):
            raise ValueError(f"The primary file must contain the following columns: {required_prim_columns}")
        
        if not all(col in sec_df.columns for col in required_sec_columns):
            raise ValueError(f"The secondary file must contain the following columns: {required_sec_columns}")
        
        # Define final results based on conditions
        final_flags = (
            (prim_df['X_standardized_peaks'] | prim_df['X_moving_average_peaks']) & 
            sec_df['paternal_fluctuation']
        )
        
        # Create the result DataFrame
        result_df = pd.DataFrame({
            'dist_m': prim_df['dist_m'],
            'final_flag': final_flags
        })
        
        # Filter only rows where final_flag is True
        result_df = result_df[result_df['final_flag']]
        
        # Save the result to a new file
        result_df.to_csv(output_file, index=False)
        print(f"Final results saved to: {output_file}")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Example usage
    prim_file = r"c:\Users\SSagynov\python_exp\peak_finder_scipy\prim_flags.csv" 
    sec_file = r"c:\Users\SSagynov\python_exp\peak_finder_scipy\sec_flags.csv"   
    output_file = r"c:\Users\SSagynov\python_exp\peak_finder_scipy\final_flags.csv"  
    
    merge_and_define_results(prim_file, sec_file, output_file)

