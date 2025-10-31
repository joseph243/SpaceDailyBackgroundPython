import os
import requests
import json
import datetime
import shutil

def read_config_file():
	path = "space.config"
	print("reading configuration from " + path)
	path = os.path.expanduser(path)
	configs = {}
	with (open(path)) as file:
		for line in file:
			if ":" in line:
				key, value = line.split(':', 1)
				configs[key.strip()] = value.strip()
	assert "photoStyle" in configs, "config file at " + path + " must contain photoStyle."
	assert "saveOldPictures" in configs, "config file at " + path + " must contain saveOldPictures."
	assert "pathForDailyBackground" in configs, "config file at " + path + " must contain pathForDailyBackground"
	if ("True" in configs["saveOldPictures"]):
		assert "pathForArchiveBackground" in configs, "config file at " + path + " must contain pathForArchiveBackground"
	return configs

def parseNote(inNote):
	#add newlines /n every 175 ch
	if len(inNote) > 175:
		morelinesneeded = 1
	else:
		morelinesneeded = 0
	noteMultiLine = ""
	while morelinesneeded:
		thisLine = inNote[:175] + '-' + "\n"
		noteMultiLine = noteMultiLine + thisLine
		inNote = inNote[175:]
		if len(inNote) > 175:
			morelinesneeded = 1
		else:
			morelinesneeded = 0
			noteMultiLine = noteMultiLine + inNote
	return noteMultiLine

def main():
	configs = read_config_file()
	photoStyle = configs["photoStyle"]
	saveOldPictures = ("True" in configs["saveOldPictures"])
	pathForDailyBackground = configs["pathForDailyBackground"]
	pathForArchiveBackground = configs["pathForArchiveBackground"]
	DATESTR = str(datetime.date.today().year) + "-" + str(datetime.date.today().month) + "-" + str(datetime.date.today().day)
	match photoStyle.upper():
		case "NASA":
			includeDescription = True;
			URL = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
			NOTEFILE = "/home/joe/.config/cinnamon/spices/deskNote@BrainAxe/0.json"
			print("using NASA daily photo per config file. url = " + URL)
			r = requests.get(URL)
			result = json.loads(r.text)
			with open(NOTEFILE) as f:
				notefilejson = json.load(f)
			note = parseNote(result["explanation"])
			notefilejson["note-entry"]["value"] = note
			with open (NOTEFILE, "w") as f:
				json.dump(notefilejson, f)
			image = requests.get(result["url"]).content
		case "PICSUM":
			includeDescription = False;
			URL = "https://picsum.photos/seed/" + DATESTR + "/1920/1080"
			print("using picsum daily photo per config file.  url = " + URL)
			image = requests.get(URL).content

	if saveOldPictures:
		#create and write jpg to archive
		print("ARCHIVING IMAGE")
		file = open(pathForArchiveBackground + DATESTR, "wb")
		file.write(image)

	#write jpg to todays background
	print("SAVING TODAYS IMAGE: " + pathForDailyBackground)
	file = open(pathForDailyBackground, "wb")
	file.write(image)

if __name__ == "__main__":
	main()
