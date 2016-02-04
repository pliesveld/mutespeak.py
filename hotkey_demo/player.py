import winsound, sys, pyhk

def playSound():
    winsound.PlaySound('piano2.wav', winsound.SND_FILENAME)
    
hot = pyhk.pyhk()
hot.addHotkey(['P'], playSound)
hot.start()