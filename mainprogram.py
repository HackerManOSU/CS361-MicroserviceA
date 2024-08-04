import os
import mimetypes
import inquirer
import time
import requests #for microservice
from tkinter import Tk, filedialog

# Define a dictionary with security-related information for different file types
security_info = {
    'pdf': """
PDF files can contain malicious code embedded in the form of scripts, links, or macros. 
These can be used to execute malicious actions when the file is opened. 
Always ensure PDFs are from trusted sources.
""",
    'jpg': """
JPEG files are generally safe, but they can contain steganographic malware hidden within the image. 
Malicious code can be embedded in the image data, which can be extracted and executed by an attacker.
""",
    'png': """
PNG files are generally safe, but they can be used to hide malware using steganography. 
This method hides malicious code within the image that can be extracted later by attackers.
""",
    'gif': """
GIF files are generally safe, but they can potentially contain embedded scripts. 
While rare, these scripts can be executed to perform malicious actions.
""",
    'mp4': """
MP4 files can contain embedded malware or malicious code. 
These can be used to exploit vulnerabilities in media players to execute malicious actions.
""",
    'mp3': """
MP3 files are generally safe, but they can be used to exploit certain media players. 
Malicious code can be embedded in the file to trigger exploits when played.
""",
    'docx': """
DOCX files can contain malicious macros that execute upon opening the file. 
These macros can perform various harmful actions, such as downloading malware or stealing data.
""",
    'xlsx': """
XLSX files can also contain malicious macros that execute upon opening the file. 
These macros can automate harmful actions, similar to DOCX file macros.
""",
    'pptx': """
PPTX files can contain embedded scripts or macros that are potentially harmful. 
Opening such files can trigger these scripts to perform malicious activities.
""",
    'exe': """
EXE files are executable and can be harmful if they contain malicious code. 
Running an unknown executable file can compromise your system by installing malware.
""",
    'zip': """
ZIP files can contain multiple files, some of which may be malicious. 
Extracting and opening unknown files from a ZIP archive can be risky.
""",
    'rar': """
RAR files, like ZIP files, can contain multiple files, some of which may be malicious. 
Be cautious when extracting and opening files from an unknown RAR archive.
""",
    'html': """
HTML files can contain embedded scripts, which may be used for cross-site scripting (XSS) attacks. 
Opening such files in a browser can execute the malicious scripts.
""",
    'js': """
JavaScript files can contain malicious code that can be executed when opened in a browser. 
These scripts can perform various harmful actions, such as stealing information or redirecting to malicious websites.
""",
    'css': """
CSS files are generally safe, but they can be used in conjunction with HTML and JS for attacks. 
Malicious CSS can be used to manipulate web page content in harmful ways.
""",
    'py': """
Python script files can contain malicious code that executes when run. 
Running untrusted Python scripts can compromise your system by performing malicious actions.
""",
    'json': """
JSON files are generally safe but can be used in attacks when parsed by vulnerable applications. 
Malformed JSON can exploit parsing vulnerabilities to perform harmful actions.
""",
    'xml': """
XML files can contain entities that might be used in XML External Entity (XXE) attacks. 
These attacks can exploit vulnerabilities in XML parsers to access sensitive data or execute malicious code.
""",
    'txt': """
TXT files are generally safe as they contain plain text. 
However, be cautious of scripts that might rename malicious files with a .txt extension to evade detection.
""",
    'csv': """
CSV files are generally safe, but can be used in attacks when opened with vulnerable applications. 
Malformed CSV content can exploit certain vulnerabilities in spreadsheet software.
"""
}

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


# Function to determine the file type and provide security information
def analyze_file(file_path):
    # Remove surrounding quotation marks if present
    file_path = file_path.strip('\"')
    
    if not os.path.isfile(file_path):
        return "Invalid file path. Please try again."

    # Guess the file type using mimetypes
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        return "Cannot determine the file type."

    extension = os.path.splitext(file_path)[1][1:]
    info = security_info.get(extension, "No specific security information available for this file type.")
    file_age = get_file_age(file_path)  # Call to the new API function

    
    return f"File type: {extension}\nMIME type: {mime_type}\n{file_age}\nSecurity info: {info}" # Example Call


# Function to analyze files in a directory
def analyze_directory(directory_path):
    # Remove surrounding quotation marks if present
    directory_path = directory_path.strip('\"')
    
    results = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            results.append(analyze_file(file_path))
    return "\n".join(results)

# Function to open file dialog and return the selected file path
def select_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

# Interactive CLI using inquirer
def main():
    print("--------------------------------------")
    print("Welcome to the File Security Analyzer!")
    print("--------------------------------------")
    print("                                      ")
    print("This tool will help you determine if a file")
    print("can contain dangerous code.")
    print("                                      ")
    print("                                      ")
    time.sleep(5)
    print("DISCLAIMER: While this software is frequently updated, cybersecurity threats are")
    print("constantly evolving and it is recommended to consult more than one source when")
    print("determining the safety profile of a particular file.")
    print("                                      ")
    print("                                      ")
    time.sleep(2)

    while True:
        method_questions = [
            inquirer.List('method', message="How would you like to input the file path?", choices=['Copy and Paste', 'Select File', 'Directory Path']),
        ]
        method_answers = inquirer.prompt(method_questions)
        
        if method_answers['method'] == 'Copy and Paste':
            questions = [
                inquirer.Text('file_path', message="Copy file path here to get its security-related info: "),
            ]
            answers = inquirer.prompt(questions)
            file_path = answers['file_path']
        elif method_answers['method'] == 'Select File':
            file_path = select_file()
        else:
            questions = [
                inquirer.Text('directory_path', message="Enter the directory path to analyze all files: "),
            ]
            answers = inquirer.prompt(questions)
            directory_path = answers['directory_path']
            file_path = None

        print("                                       ")
        print("Please wait while the system processes...")
        
        time.sleep(5)

        if file_path:
            result = analyze_file(file_path)
        else:
            result = analyze_directory(directory_path)

        print("\n" + result + "\n")

        continue_questions = [
            inquirer.Confirm('continue', message="Do you want to analyze another file?", default=True),
        ]
        continue_answers = inquirer.prompt(continue_questions)
        
        if not continue_answers['continue']:
            break

    print("Thank you for using the File Security Analyzer! Goodbye!")

if __name__ == "__main__":
    main()