import os
import pandas as pd

# Function to convert CSV to Excel
def convert_csv_to_excel(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Get the directory and filename of the CSV file
    directory = os.path.dirname(csv_file)
    filename = os.path.splitext(os.path.basename(csv_file))[0]

    # Create the output Excel file path
    excel_file = os.path.join(directory, f"{filename}.xlsx")

    # Convert and save as Excel file
    df.to_excel(excel_file, index=False)
    print(f"Successfully converted '{csv_file}' to '{excel_file}'")

# Main function
def main():
    # Get the path of the dragged file from the command-line argument
    dragged_file = input("Drag and drop the CSV file here: ").strip('"')

    # Check if the dragged file is a CSV file
    if dragged_file.endswith(".csv"):
        # Convert the CSV to Excel
        convert_csv_to_excel(dragged_file)
    else:
        print("Please drag and drop a CSV file.")

# Entry point
if __name__ == "__main__":
    main()