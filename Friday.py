import threading
import time
import eel
import os

from logic_brain import friday_brain

# Ensure the web directory exists
web_dir = "web"
if not os.path.exists(web_dir):
    os.makedirs(web_dir)

# Initialize eel
eel.init(web_dir)

# Expose the display_response function to JavaScript
@eel.expose
def display_response(element_id):
    while True:
        try:
            # Check if input and response files exist
            input_file = "input.txt"
            response_file = "output.txt"
            if not os.path.exists(input_file):
                print(f"Error: {input_file} does not exist.")
                continue
            if not os.path.exists(response_file):
                print(f"Error: {response_file} does not exist.")
                continue

            # Read data from input file
            with open(input_file, 'r') as f:
                input_data = f.read().strip()
            # Read data from response file
            with open(response_file, 'r') as f:
                response_data = f.read().strip()

            # Update the content of the element using JavaScript
            js_script = f"document.getElementById('{element_id}').innerText = 'Input: {input_data}\\nResponse: {response_data}';"
            eel.js(js_script)()
        except Exception as e:
            print("Error:", e)
        time.sleep(1)  # Adjust the interval according to your needs

def ui():
    print("Starting UI thread...")
    eel.start("index.html", mode='chrome', port=8080, cmdline_args=['--start-fullscreen'])

def friday():
    print("Starting friday_brain thread...")
    t1 = threading.Thread(target=friday_brain)
    t2 = threading.Thread(target=ui)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

# Start the application
friday()