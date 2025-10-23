import os
import requests
import json
import datetime
import shutil

def read_config_file(inPath):
	print("reading configuration from " + inPath)
	inPath = os.path.expanduser(inPath)
	configs = {}
	with (open(inPath)) as file:
		for line in file:
			if ":" in line:
				key, value = line.split(':', 1)
				configs[key.strip()] = value.strip()
	assert "dailyPhotoPath" in configs, "config file at " + inPath + " must contain dailyPhotoPath."
	assert "photoSet" in configs, "config file at " + inPath + " must contain photoSet."
	assert "savePictures" in configs, "config file at " + inPath + " must contain savePictures"
	return configs

FILENAME = "/home/joe/Pictures/nasa/" + str(datetime.date.today().day) + "-" + str(datetime.date.today().month) + "-" + str(datetime.date.today().year) + ".jpg"
TODAYPATH = "/home/joe/Pictures/nasa/today/"
DATESTR = str(datetime.date.today().year) + str(datetime.date.today().month) + str(datetime.date.today().day)
NASAURL = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
PICSUMURL = "https://picsum.photos/seed/" + DATESTR + "/1920/1080"
FILENAME = "/home/joe/Pictures/nasa/" + DATESTR + ".jpg"
TODAYPATH = "/home/joe/Pictures/today/"
TODAYFILE = TODAYPATH + "today.jpg"
NOTEFILE = "/home/joe/.config/cinnamon/spices/deskNote@BrainAxe/0.json"

print("debugg..")
print(DATESTR)

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
