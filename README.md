# UFO50-Bingo-Casting-Tool
Python program that finds the next scheduled bingo match and saves all the info the caster needs for their OBS scene to text files.

# How to Use
Place BingoTool.exe in an empty folder, it will be creating several text files so you want to keep them organised.

Run the exe, you should see an empty command prompt. This takes some time (about 10 seconds on my PC) so don't worry if it looks like it's doing nothing.

When the window closes you will see the text files in the directory like in the image below.

<img width="132" height="234" alt="image" src="https://github.com/user-attachments/assets/3630e570-943a-4918-a2d6-e1c18da0fcd8" />

This image shows how the text files correspond to the bingo scene.

<img width="1920" height="1080" alt="example" src="https://github.com/user-attachments/assets/bd92dd72-d794-4636-bac3-f361d9bc55e3" />

Create a text source or open properties for an existing one and you will see a checkbox for "Read from file".

<img width="653" height="247" alt="image" src="https://github.com/user-attachments/assets/3d7bd186-55c8-4b23-986a-3a358e59e8c9" />

Check this then browse to the directory of the tool and select the text file that corresponds with this text source. Do the same for every text source you want on your scene.

From now on, when you want to cast a match, simply run the tool and all of these text sources will be updated. (You still need to capture the discord streams yourself, I can't do everything for you)

# What if there are multiple matches at once?

You will get a list of all matches scheduled for the same time and you will have to enter a number to select the one you want.

<img width="416" height="55" alt="image" src="https://github.com/user-attachments/assets/a76485b3-6b51-4733-8396-e02e450181b7" />
