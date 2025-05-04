import os 
import camelot
from joblib import Memory
import json
from askai import get_response_with_cached_context
# Create a memory object that will cache to the 'cache' directory
memory = Memory('cache', verbose=0)

@memory.cache
def extract_table_from_pdf(pdf_path):
    """Extract table from PDF and cache the result to disk"""
    table_list = camelot.read_pdf(
        pdf_path, 
        pages="all"
    )
    
    # Find the first table with 11 rows
    latest_table = None
    for table in table_list:
        if table.df.shape[0] == 11:
            latest_table = table
            break
    
    if latest_table is None:
        raise ValueError("No table with 11 rows found in the PDF")
    
    return latest_table.df

def convert_table_to_df(table):
    table = table.replace({"\n": " "}, regex=True)
    # Use the first row as the column names
    column_names = table.iloc[0]
    # Use the remaining rows as the data
    table = table[1:]
    table.columns = column_names
    
    # Convert Nationality column to list by splitting on double spaces
    if 'Nationality' in table.columns:
        table['Nationality'] = table['Nationality'].str.split('  ')
    
    return table

def df_to_json_save(df, output_file="output.json"):
    """
    Convert DataFrame to JSON format and save to file
    Args:
        df: pandas DataFrame
        output_file: path to save JSON file
    """
    # Convert DataFrame to records format
    json_data = df.to_dict(orient='records')
    
    # Get absolute path for output file
    output_path = os.path.join(os.getcwd(), output_file)
    
    # Save to file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    print(f"JSON saved to {output_path}")

def df_to_json(df):
    """
    Convert DataFrame to JSON format and save to file
    Args:
        df: pandas DataFrame
        output_file: path to save JSON file
    """
    # Convert DataFrame to records format
    json_data = df.to_dict(orient='records')
    
    return json_data

QUESTIONS = ["What's the Elon Musk's net worth?", "What's the Mark Zuckerberg's net worth?", "Who is the richest person in the world?", "What is Arham Hasan's net worth?"]

if __name__ == "__main__":
    file_path = "./demo2.pdf"
    table = extract_table_from_pdf(file_path)
    df = convert_table_to_df(table)
    
    # Convert to JSON and save to file
    json_data = df_to_json(df)

    for question in QUESTIONS:
        response = get_response_with_cached_context(question, json_data)
        print(response)

