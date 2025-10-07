with open("map.txt", "r") as maptxt:
    lineslist = maptxt.readlines()
    print(lineslist)
    lineslist.reverse()
with open("newmap.txt", "w") as newmap:
    text = ""
    for line in lineslist:
        text += line.strip("\n") + "\n"
    newmap.write(text)
        
        