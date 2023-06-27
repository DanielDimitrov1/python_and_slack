#!/usr/bin/python3

import os #need for file opening
import logging #we want everything to go in /log/
import time
import json
import requests #for slack
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def send_slack_notification(message):
    webhook_url = ""
    headers = {"Content-type": "application/json"}
    data = {'text': message}
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data)) #from python dictionary to json file
    if response.status_code == 200:
        print(f"Send slack notification: {message}")
    else:
        print(f"Error sending slack notification: {response.status_code} - {response.text}")

#What is going on the move, function if file is created what should happen?
def on_created(event):
    if event.is_directory:
        return None
    log_file.info(f"Created {event.src_path}")
    send_slack_notification(f"New file created: {event.src_path}") #we said that there is a new file created and we are providing the path to that file


def on_deleted(event):
    if event.is_directory:
        return None
    log_file.info(f"Deleted {event.src_path}")
    send slack_notification(f"Deleted: {event.src_path}")


def on_moved(event):
    if event.is_directory:
        return None
    log_file.info(f"Moved {event.src_path} to {event.dest_path}")
    send_slack_notification(f"Moved : {event.src_path} to {event.dest_path}")


if __name__== "__main__":
    # Set up logging to a file and sto stdout
    log_file = logging.getLogger(__name__)
    log_file.setLevel(logging.INFO)
    file_handler = logging.FileHandler("file.log")
    file_handler.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    log_file.addHandler(file_handler)
    log_file.addHandler(console_handler)
    #until here is just for the logging

#Setting up event 
    event_handler = FileSystemEventHandler()
    #for each event call the appropriate function
    event_handler.on_created = on_created
    event_handler.on_deleted = on_deleted
    event_handler.on_moved = on_moved
    observer = Observer()
    path = "/home/ec2-user/my_dir/"
    observer.schedule(event_handler, path=".", recursive=True)


    #Start the observer
    osberver.start()
    print("Watching for file changes...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
