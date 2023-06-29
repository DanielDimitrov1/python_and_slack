#!/usr/bin/python3

import os
import logging #for logging in log file what is going on wiht program
import time
import json
import requests   #for the slack
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def send_slack_notification(message): #here we will give the message that shoudl be send
    webhook_url = "https://hooks.slack.com/services/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"
    headers = {"Content-type" : "/application/json"}
    data = {'text': message} #this is what we are giving to it
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data)) #тук ще разберем дали сме изпратили съобщението или има грешка
    # дата.dumps защото датата тръв от python dictionery to json file
    if response.status_code == 200: #aко върне код 200 значи че се е изпълтнил
        print(f"Send slack notification: {message}")
    else: # обаче ако не се е изпратило
        print(f"Error sending slack notification: {response.status_code} - {response.text}")

    #какво се креира когато преместим файл, креираме, трием ?? трябва да получим съобщение

def on_created(event): #this event will come from a header
    if event.is_directory:
        return None
    log_file.info(f"Created {event.src_path}") #everything that happens in the application goes in log file, info means that everyhitng will go in log, from where notifications come
    send_slack_notification(f"New file created: {event.src_path}") #this is the message that we are sending

def on_deleted(event):
    if event.is_directory:
        return None
    log_file.info(f"Deleted {event.src_path}")
    send_slack_notification(f"Deleted : {event.src_path}") #this is the message that we are sending

def on_moved(event):
    if event.is_directory:
        return None
    log_file.info(f"Moved {event.src_path} to {event.dest_path}")
    send_slack_notification(f"Moved: {event.src_path} to {event.dest_path}") #this is the message that we are sending


#da definirame logginga i handler-a za vs neshata koito shte se sluchvat

if __name__ == "__main__": #iskame da se izvikva SAMO KOGATO SE STARTIRA PROGRAMTA
    # Set up logging to a file and sto stdout
    log_file = logging.getLogger(__name__) #imeto na programkata, zahstoto mu tr da ima nekakv lgoger name
    log_file.setLevel(logging.INFO) #setvame nekakav logger name
    #posochvame kade da lognva
    file_handler = logging.FileHandler("file.log")
    file_handler.setLevel(logging.INFO)
    #this is only for the file, but we want to log to output, we want to see in the real time what is going on not to wait to create the file...this can be done with creating console_handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    #tr da mu podadem file handler za da znae kak da formatira
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter) #za da izliza pravilno loga na ekrana
    log_file.addHandler(file_handler)
    log_file.addHandler(console_handler)
    #tova beshse samo za loginga

    #sega za eventa

    #setting up event handling
    event_handler = FileSystemEventHandler() #tuk izvikvame tova koeto sme mu imprtnali
    event_handler.on_created = on_created   #za vseki edin event izivikvai opredelenata funkcija
    event_handler.on_deleted = on_deleted
    event_handler.on_moved = on_moved
    observer = Observer() #kreirame observer
    path = "/home/ec2-user/my_dir/"
    #kazvame kade da sledi za promeeneni failove
    observer.schedule(event_handler, path=path, recursive=True)

    #start the observer
    observer.start()
    print("Wathing for file changes...")
    try: #ako handlene mn eventi na vednysh
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

#ideata e da hvashtame vs promeni koieto se sluchat v nashte failove
#gotino da imash logging zashtot mojesh da si centralizirash loggovete, osobeno ako imas elastic search
