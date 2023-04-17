import dotenv
import requests
import json
import sys
import subprocess
import os

# Set your OpenAI API key
OPENAI_API_KEY = dotenv.get_key(".env", "OPENAI_API_KEY")
# Set the API endpoint
url = "https://api.openai.com/v1/chat/completions"
# Set the request headers
headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}

conversation = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {
            "role": "system", 
            "content": "You will act as a compiler : you will receives messages in any language and will have to translate them in C. You will only respond with code , NO TEXT. Sometimes you will receive code that will not compile, in this case you will have to retry until you get a valid C code.",
        },
        {
            "role": "user",
            "content": "print(\"Hello World\")",
        },
        {
            "role": "assistant",
            "content": "#include <stdlib.h> \n  int main() { printf(\"Hello World\"); return 0;}",
        },
        # more complex example
        {
            "role": "user",
            "content": "def hello():\n    print(\"Hello World\") \nhello()",
        },
        # error
        {
            "role": "assistant",
            "content": "#include <stdlib.h> \n  int main() { printf(\"Hello World\") return 0;}",
        },
        # error message
        {
            "role": "system",
            "content": """Compilation failed : error.c:2:36: error: expected ‘;’ before ‘return’
        2 |  int main() { printf("Hello World") return 0;}
          |                                    ^~~~~~~
          |                                    ;
         """,
        },
        # retry
        {
            "role": "assistant",
            "content": "#include <stdlib.h> \n  int main() { printf(\"Hello World\"); return 0;}",
        },
        

    ]
}

infile = sys.argv[1]
outfile = sys.argv[2]

with open(infile, "r") as f:
    conversation["messages"].append({
        "role": "user",
        "content": f.read()
    })


max_retries = 5

for i in range(max_retries):
    response = requests.post(url, headers=headers, json=conversation);
    response = response.json()
    print(json.dumps(response,indent=4))
    conversation["messages"].append({
        "role": "assistant",
        "content": response["choices"][0]["message"]["content"]
    })
    code  = response["choices"][0]["message"]["content"]
    # Save the C code to a temporary file
    with open('temp.c', 'w') as f:
        f.write(code)

    # Compile the C code using GCC
    gcc_command = f"gcc -o {outfile} temp.c"
    result = subprocess.run(gcc_command, shell=True, text=True, capture_output=True)

    # Check for errors and warnings
    if result.returncode == 0:
        print("Compilation successful!")
        os.remove('temp.c')
        exit(0)
    else:
        print("Compilation failed. Retrying code...")
        os.remove('temp.c')
        # add the error to the conversation
        conversation["messages"].append({
            "role": "system",
            "content": f"Compilation failed : {result.stderr + result.stdout}"
        })


