import os, sys, requests, json, datetime

def read_config_file():
	path = "space.config"
	print("reading configuration from " + os.getcwd() + "/" + path)
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

def alreadyRanToday(filepath):
    if not os.path.exists(filepath):
        return False
    mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
    return mod_time.date() == datetime.date.today()

def main():
	os.chdir(os.path.dirname(os.path.abspath(__file__)))
	configs = read_config_file()
	photoStyle = configs["photoStyle"]
	saveOldPictures = ("True" in configs["saveOldPictures"])
	pathForDailyBackground = configs["pathForDailyBackground"]
	pathForArchiveBackground = configs["pathForArchiveBackground"]
	DATESTR = str(datetime.date.today().year) + "-" + str(datetime.date.today().month) + "-" + str(datetime.date.today().day)
	if alreadyRanToday(pathForDailyBackground):
		print("ALREADY RAN TODAY.  EXITING.")
		sys.exit(0)
	match photoStyle.upper():
		case "NASA":
			includeDescription = True;
			URL = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
			NOTEFILE = "/home/joe/.config/cinnamon/spices/deskNote@BrainAxe/0.json"
			print("using NASA daily photo per config file. url = " + URL)
			r = requests.get(URL)
			result = json.loads(r.text)
			image = requests.get(result["url"]).content
			try:
				with open(NOTEFILE) as f:
					notefilejson = json.load(f)
				note = parseNote(result["explanation"])
				notefilejson["note-entry"]["value"] = note
				with open (NOTEFILE, "w") as f:
					json.dump(notefilejson, f)
			except FileNotFoundError:
				print("did not save note because note file is not found at " + NOTEFILE)
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
