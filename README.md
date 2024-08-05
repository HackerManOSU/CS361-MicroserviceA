# CS361-MicroserviceA
File age analyzer microservice using Flask API for teammates file analyzer python script

## Setup

### 1. Install Packages
```bash Install packages
pip install flask
pip install requests
```
### 2. Start Microservice
```bash Run Microservice
python3 microservice.py
```

or

```bash Run Microservice

python microservice.py

```

### 3. Update and Run Your Modified Script
```bash Run Main Program
python3 mainprogram.py
```

or

```bash Run Main Program
python mainprogram.py
```

## Requesting Data

To request the age of a file, you need to send a POST request to the microservice with the file path included in the JSON payload. Below is an example using Python's requests library:

```python Request Example

import requests

def get_file_age(file_path):
    url = 'http://127.0.0.1:5000/file_age'
    payload = {'file_path': file_path}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return response.json()['error']

# Example usage
print(get_file_age('/path/to/your/file'))

```

## Receiving Data

The microservice responds with JSON data containing either the file age or an error message:

### Success Response
```json Success Response
{
  "file_age": "3 days, 4:23:00",
  "status": "success"
}
```
### Failure Response
```json Failure Response
{
  "error": "File does not exist",
  "status": "fail"
}
```

### Update function
You can update your function to read the json and return strings:
```python Update Function
def get_file_age(file_path):
    url = 'http://127.0.0.1:5000/file_age'
    payload = {'file_path': file_path}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        return f"File age: {data['file_age']}"
    else:
        return "Failed to get file age. " + response.json().get('error', 'Unknown error')
```

## UML Sequence Diagram
<img width="537" alt="Screenshot 2024-08-04 at 8 09 28 PM" src="https://github.com/user-attachments/assets/49052a9d-8db1-4630-b978-38f4a614c113">
