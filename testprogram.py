import os
import time
import requests #for microservice
from tkinter import Tk, filedialog

# Microservice function to get the age of the file from the API
def get_file_age(file_path):
    url = 'http://127.0.0.1:5000/file_age'
    payload = {'file_path': file_path}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        return f"File age: {data['file_age']}"
    else:
        return "Failed to get file age. " + response.json().get('error', 'Unknown error')


# Function to determine the file type
def print_file_info(file_path):
    file_path = file_path.strip('\"')
    
    if not os.path.isfile(file_path):
        return "Invalid file path. Please try again."

    extension = os.path.splitext(file_path)[1][1:]
    file_age = get_file_age(file_path)  # Call to the new API function

    
    return f"File type: {extension}\nFile age: {file_age}" # Example Call


# Function to open file dialog and return the selected file path
def select_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

# Interactive CLI using inquirer
def main():
    print("--------------------------------------")
    print("Opening File Explorer")
    print("--------------------------------------")

    time.sleep(2)

    file_path = select_file()
    
    time.sleep(2)

    if file_path:
        result = print_file_info(file_path)

    print("\n" + result)
        
    time.sleep(5)


    print("\nThank you for using")
    print("\nExiting Program\n")

if __name__ == "__main__":
    main()
