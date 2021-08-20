import os, random, subprocess
import subprocess
import time
import sys
import string

# checking if the user has passed the -n command
# if the -n command is passed then no need to retreive the previous song played information
try:
    if(sys.argv[1] == "-n"):
        old = False
    else:
        old = True
except IndexError:
    old = True


# function to write the song played to the txt file
def writeSong(songName):

    with open("played.txt" , "a") as fil:
        fil.write("\n{}".format(songName))


# function to reset the txt file
def writeSongBlank():

    with open("played.txt" , "w") as fil:
        fil.write("")


# function to retrive the song name from the txt file
def readSongList():

    with open("played.txt" , "r") as fil:
        dataList = fil.readlines()

    return dataList


"""your folder name / folder path here"""
folderName = "English"

# list containig the lower case and space
allowed = list(string.ascii_lowercase)
allowed.append(" ")





# renaming the files to eliminate any special chars from them
for count, filename in enumerate(os.listdir(folderName)):
        
        filename1 = filename.lower()[:-4]
        dst = ""

        for i in filename1:
            if(i in allowed):
                dst = dst + i

        src = folderName + "/" + filename
        dst = folderName + "/" + dst + filename[-4:]

        os.rename(src, dst)

# list containing the already played songs
played = []

# if old songs need to be played
if(old):

    # read the songs from txt file
    dataList = readSongList()
    newDatalist = []

    # remove "\n" from the elements in list
    for i in dataList:
        i = i[:-1]

        if(i != ""):
            newDatalist.append(i)

    played.extend(newDatalist)


# function to get the video length
def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

# list containing the song names
myList = os.listdir("/winSddOne/0Share/music/{}".format(folderName))

# remove the song which is already played from the song list
for i in myList:
    if(i in played):
        myList.remove(i)

# function to play a random song
def playRandomSong():

    global myList

    # if old music is remembered
    if(old):
        if(len(myList) > 0):
            randomfile = random.choice(myList)
        else:

            # if the music list is empty means the all songs as alredy been played
            writeSongBlank()

            # so re creating the list
            myList = random.choice(os.listdir("/winSddOne/0Share/music/{}".format(folderName)))
    else:
        randomfile = random.choice(myList)

    file = """/winSddOne/0Share/music/{}/{}""".format(folderName , randomfile)
    

    
    try:
        # re conforming the song as not already been played
        if(randomfile not in played):
            print("\nplaying {}".format(randomfile))
            played.append(randomfile)

        # writing the song for record
        if(old):
            writeSong(str(file))
        

        # playing it 
        os.system("xdg-open '{}'".format(file))

        # wait until the song it completed
        try:
                time.sleep(get_length(file))
        except KeyboardInterrupt:
            pass

    except Exception as e:
        print("\nExpection while playing {} = {}".format(file , str(e)))

    
    
    


n = int(input("Enter the number of songs to play : "))

for i in range(n):
    playRandomSong()

