this python script will download the nasa daily space image and its description.
then it will put these into specific folders to be displayed on the deskop with an image and a text box

the description text uses a cinnamon desklet called "Desktop Note Desklet", and there are some hard coded values 
in here to use the 0th note.

i run this via cron:
```
00 9	* * *	joe	python3 /home/joe/PythonWorkspace/spaceBackground/getImage.py
```

https://cinnamon-spices.linuxmint.com/desklets/view/36

![image](https://github.com/user-attachments/assets/79e596ac-f627-4bf7-b99a-8c5e71d6bd78)
