import pandas as pd
from dbfread import DBF

def display_dbf_file(file_path):
    table = DBF(file_path, ignore_missing_memofile=True, load=True)
    df = pd.DataFrame(iter(table))
    print(df)
    print("\nData Types:\n", df.dtypes)
    print("DataFrame loaded successfully!")
    return df

def add_minutes_to_time(df, minutes_to_add):
    
    def update_time(time_str):
        hours, minutes = map(int, time_str.split(":"))
        total_minutes = hours * 60 + minutes + minutes_to_add
        updated_hours = (total_minutes // 60) % 24
        updated_minutes = total_minutes % 60
        return f"{updated_hours:02d}:{updated_minutes:02d}"

    df["O_CLOCK"] = df.apply(
        lambda row: update_time(row["O_CLOCK"]) 
        if pd.notnull(row["O_CLOCK"]) and isinstance(row["O_CLOCK"], str) 
        and row["O_CLOCK"] != "--:--" 
        and pd.notnull(row["J_NO"]) 
        and row["J_NO"] != ""
        else row["O_CLOCK"], axis=1
    )
   
    print("O_CLOCK column updated successfully!")
    return df

# File path to the DBF file
file_path = r"C:\Users\SSagynov\python_exp\oclock_position_change\refrence.dbf"
output_csv_path = r"C:\Users\SSagynov\python_exp\oclock_position_change\updated_reference.csv"

# Number of minutes to add
minutes_to_add = 20

df = display_dbf_file(file_path)
df = add_minutes_to_time(df, minutes_to_add)
df.to_csv(output_csv_path, index=False)

print(df)
print(f"DataFrame saved as CSV to {output_csv_path}")
