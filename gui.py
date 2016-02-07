from Tkinter import *
import string
import json
import os
import pyhk


"""
Tkinter wrapper around eSpeak.  Configures sliders for changing espeak parameters.

Patrick Liesveld
Mike Adkison
"""


class MuteSpeak(Frame):
    def __init__(self, master=None,**kwargs):
        Frame.__init__(self, master)
        Pack.config(self)

        self.createVars()
        self.reset(**kwargs)
        self.createFileMenu()
        self.createWidgets()

    def createVars(self):
        self.amplitude = IntVar()
        self.pitch = IntVar()
        self.wpm = IntVar()
        self.gap = IntVar()
        self.clearOnMessage = BooleanVar()
        self.hot = pyhk.pyhk()

    def reset_defaults(self):
        self.amplitude.set(100)
        self.pitch.set(50)
        self.wpm.set(175)
        self.gap.set(3)


    def reset(self,amplitude,pitch,wpm,gap):

        self.reset_defaults()
        self.clearOnMessage.set(True)

        try:
            self.amplitude.set(amplitude)
            self.pitch.set(pitch)
            self.wpm.set(wpm)
            self.gap.set(gap)

        except (ValueError, TypeError, NameError, RuntimeError):
            pass


    def createFileMenu(self):
        """
        Constructs file.  Must be called first.
        """
        mBar = Frame(self, relief=RAISED, borderwidth=2)
        mBar.pack(fill=X)

        File_button = Menubutton(mBar, text='File', underline=0)
        File_button.pack(side=LEFT, padx="1m")
        File_button.menu = Menu(File_button)

        File_button.menu.add_command(label='Save',     underline=0,command=self.saveit)
        File_button.menu.add_command(label='Reset', underline=0,command=self.reset_defaults)

        File_button['menu'] = File_button.menu

        mBar.tk_menuBar(File_button)



    def createWidgets(self):
        """
        Adds slider widgets for amplitude, pitch, word per minute, and word gap.
        Contains a textbox to hold the message to send.
        """

        frame_sliders = Frame(self,bd=4,width=200)
        self.slider_amplitude = Scale(frame_sliders, from_=0, to=200,
                            orient=HORIZONTAL,
                            length="3i",
                            label="amplitude",
                            variable=self.amplitude)

        self.slider_amplitude.pack(side=TOP, expand=1, fill=X)

        self.slider_pitch = Scale(frame_sliders, from_=0, to=99,
                            orient=HORIZONTAL,
                            length="3i",
                            label="pitch",
                            variable=self.pitch)

        self.slider_pitch.pack(side=TOP, expand=1, fill=X)

        self.slider_wpm = Scale(frame_sliders, from_=80, to=450,
                            orient=HORIZONTAL,
                            length="3i",
                            label="words per minute",
                            variable=self.wpm)

        self.slider_wpm.pack(side=TOP, expand=1, fill=X)

        self.slider_wpm = Scale(frame_sliders, from_=1, to=450,
                            orient=HORIZONTAL,
                            length="3i",
                            label="word gap",
                            variable=self.gap)

        self.slider_wpm.pack(side=TOP, expand=1, fill=X)

        frame_sliders.pack(side=TOP, expand=1, fill=BOTH)

        self.toggle_clear = Checkbutton(self, 
                text = "Clear message after speaking",
                onvalue = 1, offvalue = 0,
                variable=self.clearOnMessage)

        self.toggle_clear.pack(side=TOP)


        frame_msg = Frame(self,bd=4)

        lbl_msg = Label(frame_msg,text="Message")
        lbl_msg.pack(side=LEFT,expand=1,fill=X)

        self.entry_message = Entry(frame_msg)
        self.entry_message.pack(side=RIGHT)
        self.entry_message.focus()

        frame_msg.pack(side=BOTTOM)

        self.message = StringVar()
        self.message.set("Hello")
        self.entry_message.config(textvariable=self.message)

        self.hot.addHotkey(['Return'], self.speak_contents, isThread=True)
        #self.entry_message.bind('<Key-Return>', self.speak_contents)




    def speak_contents(self):
        """
        Launches eSpeak.  Espeak must be in the path Environment.
        """
        message = self.message.get()

        if self.clearOnMessage.get():
            self.message.set("")

        print("Message: ",  message )

        args = self.espeaks_args()

        ## TODO: launch as a daemon thread so gui main thread remains responsive
        os.system("espeak " + args + ' '+ '"' + repr(message) + '"')
        self.entry_message.focus()


    def settings(self):
        """
        Returns a dict of the settings for launching eSpeak
        """
        d = {
                'amplitude' : self.amplitude.get(),
                'pitch'     : self.pitch.get(),
                'wpm'       : self.wpm.get(),
                'gap'       : self.gap.get()
             };

        return d;

    def espeaks_args(self):
        """
        Computes the stringed argument for the eSpeak application to be called.
        """
        d = self.settings()
        return '-z -p {pitch} -s {wpm} -a {amplitude} -g {gap}'.format(**d);

    def saveit(self):
        """
        Saves the eSpeak settings into mutespeak.json
        """
        data = self.settings()
        print(data)

        try:
            with open('mutespeak.json', 'w') as fp:
                json.dump(data,fp)
        except IOError:
            print('Could not save settings')


def load_defaults():
    """
    Loads the eSpeak settings from mutespeak.json
    """
    default_dict = {
            'amplitude' : 100,
            'pitch'     : 50,
            'wpm'       : 175,
            'gap'       : 3
    }

    data = {}
    try:
        with open('mutespeak.json', 'r') as fp:
            data = json.load(fp);
    except IOError:
        pass


    default_dict.update(data);
    return default_dict;


if __name__ == '__main__':
    defaults = load_defaults()
    mute = MuteSpeak(**defaults)
    mute.mainloop()
