# import pandas as pd

# def convert_to_long_format(input_csv_path, output_csv_path):
#     # Read the initial CSV into a DataFrame
#     dataframe = pd.read_csv(input_csv_path)
    
#     # Unpivot the DataFrame
#     long_format_df = dataframe.melt(id_vars=['seat_number', 'seat_coordinates'], 
#                                     var_name='snapshot', value_name='Status')
    
#     # Separate snapshot and date_time
#     long_format_df[['Snapshotname', 'snapshot_date_time']] = long_format_df['snapshot'].str.extract(r'^(snapshot_\d+)(_date_time)?$')
#     long_format_df = long_format_df.drop(columns=['snapshot'])
#     long_format_df = long_format_df.dropna(subset=['Snapshotname'])
#     long_format_df['snapshot_date_time'] = long_format_df['snapshot_date_time'].fillna(method='ffill')

#     # Save to a new CSV file
#     long_format_df[['seat_number', 'seat_coordinates', 'Status', 'Snapshotname', 'snapshot_date_time']].to_csv(output_csv_path, index=False)

# def main():
#     input_csv_path = 'test.csv'  # Input CSV file path
#     output_csv_path = 'seat_cord_long.csv'  # Output CSV file path

#     convert_to_long_format(input_csv_path, output_csv_path)
#     print(f"Converted file saved to {output_csv_path}")

# if __name__ == "__main__":
#     main()
import pandas as pd

def convert_to_long_format(input_csv_path, output_csv_path):
    # Read the initial CSV into a DataFrame
    dataframe = pd.read_csv(input_csv_path)
    
    # Unpivot the DataFrame
    long_format_df = dataframe.melt(id_vars=['seat_number', 'seat_coordinates'], 
                                    var_name='Snapshotname', value_name='Status')
    
    # Filter out date_time columns
    long_format_df = long_format_df[~long_format_df['Snapshotname'].str.contains('_date_time')]
    
    # Save to a new CSV file
    long_format_df[['seat_number', 'seat_coordinates', 'Status', 'Snapshotname']].to_csv(output_csv_path, index=False)

def main():
    input_csv_path = 'test.csv'  # Input CSV file path
    output_csv_path = 'seat_cord_long1.csv'  # Output CSV file path

    convert_to_long_format(input_csv_path, output_csv_path)
    print(f"Converted file saved to {output_csv_path}")

if __name__ == "__main__":
    main()
