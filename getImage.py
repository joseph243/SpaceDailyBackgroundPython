import os
import requests
import json
import datetime
import shutil

URL = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
FILENAME = "/home/joe/Pictures/nasa/" + str(datetime.date.today().day) + "-" + str(datetime.date.today().month) + "-" + str(datetime.date.today().year) + ".jpg"
TODAYPATH = "/home/joe/Pictures/nasa/today/"
TODAYFILE = TODAYPATH + "today.jpg"
NOTEFILE = "/home/joe/.config/cinnamon/spices/deskNote@BrainAxe/0.json"

if not os.path.isfile(FILENAME):
    #send request
    r = requests.get(URL)
    result = json.loads(r.text)

    #grab json where note will be sent
    with open(NOTEFILE) as f:
        notefilejson = json.load(f)

    #get note
    note = result["explanation"]

    #add newlines /n every 175 ch
    if len(note) > 175:
        morelinesneeded = 1
    else:
        morelinesneeded = 0

    noteMultiLine = ""
    while morelinesneeded:
        thisLine = note[:175] + '-' + "\n"
        noteMultiLine = noteMultiLine + thisLine
        note = note[175:]
        if len(note) > 175:
            morelinesneeded = 1
        else:
            morelinesneeded = 0
            noteMultiLine = noteMultiLine + note
    
    #write note and save to json for desktop notepad
    print("SAVING NOTE")
    notefilejson["note-entry"]["value"] = noteMultiLine
    with open (NOTEFILE, "w") as f:
        json.dump(notefilejson, f)

    #create and write jpg to archive
    print("SAVING IMAGE")
    file = open(FILENAME, "wb")
    file.write(requests.get(result["url"]).content)

    #remove current background
    for a in os.listdir(TODAYPATH):
        print("REMOVING FILE: " + TODAYPATH + a)
        os.remove(TODAYPATH + a)

    #copy jpg to todays background
    print("SAVING FILE FOR TODAYS BACKGROUND: " + TODAYFILE)
    shutil.copy(FILENAME, TODAYFILE)
else:
    print("NASA DAILY IMAGE ALREADY EXISTS FOR TODAY, TOOK NO ACTION.")
