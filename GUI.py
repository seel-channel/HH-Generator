from HH import HH
from tkinter import (Tk, Button, Frame, Label, Toplevel, IntVar, Entry, Checkbutton)
from tkinter.ttk import Progressbar
from tkinter.filedialog import askopenfilename

#-----------------
#WIDGETS CLASSES
#-----------------
class TransparentButton(Button):
    def __init__(self, master, **kw):
        bg = window_bg
        Button.__init__(self, 
            padx = 0,
            pady = 0,
            master = master,
            background = bg, 
            foreground = "black",
            activebackground = bg, 
            activeforeground = "black",
            borderwidth = '0',
            highlightthickness = '0', **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def on_enter(self, e):
        self['background'] = self["activebackground"]
    def on_leave(self, e):
        self['background'] = self.defaultBackground  
    def loading(self):
        self['state'] = "disable"
        self['cursor'] = "wait"
    def reset(self):
        self['state'] = "enable"
        self['cursor'] = ""
        
class ProgressBarScreen(Toplevel):
    def __init__(self, master):
        super().__init__(master = master) 
        self.title("Progress Screen") 
        self.geometry("300x150") 
        setWindowStyle(self)
        self.labelFrame = Frame(self)
        self.labelFrame.configure(background=window_bg)
        self.minLabel = createLabel(self.labelFrame)
        self.maxLabel = createLabel(self.labelFrame)
        setStyleText(self.minLabel, "0%")
        setStyleText(self.maxLabel, "100%")
        self.minLabel.grid(row = 0, column= 0, padx = 20)
        self.maxLabel.grid(row = 0, column= 4, padx = 20)
        self.labelFrame.grid(row = 0, column = 1, pady = (40, 0))
        
        self.progressBar = Progressbar(self)
        self.progressBar.grid(row = 1, column = 1, pady = 5)
        self.progressLabel = createLabel(self)
        setStyleText(self.progressLabel, "INITIALIZING...")
        self.progressLabel.grid(row = 2, column = 1)
        
    def updatePercentage(self, percentage, message):
        if percentage < 98:
            self.progressBar["value"] = percentage
            self.progressBar.update_idletasks()
            self.minLabel["text"] = str(percentage) + "%"
            self.progressLabel["text"] = message
        else:
            global usingMergedData
            if not usingMergedData:
                clearSplittedChannelsSelected(0)
                clearSplittedChannelsSelected(1)
            else:
                clearMergedChannelsSelected(0)
                clearMergedChannelsSelected(1)
            generate_btn["state"] ="normal"
            self.destroy()
            
class AdvancedSettingsScreen(Toplevel):
    def __init__(self, master):
        super().__init__(master = master) 
        self.inputs = []
        self.title("Advanced Settings") 
        self.geometry("190x350") 
        setWindowStyle(self)
        label = createLabel(self)
        setStyleText(label, "", True)
        label.grid(row=0, column=0, sticky="nw", padx=(20, 0), pady=5)
        
        self.textAndInput("Sampling Rate:", 2)
        self.textAndInput("Segment Lenght:", 3)
        self.textAndInput("Start H Whole:", 4)
        self.textAndInput("Start L Whole:", 5)
        self.textAndInput("End H Whole:", 6)
        self.textAndInput("End L Whole:", 7)
        self.loadData()
        
        global usingMergedData, use_baseline_correction
        self.checkMerge = IntVar(value=usingMergedData)
        self.checkBaseline = IntVar(value=use_baseline_correction)
        check1 = Checkbutton(self, variable=self.checkMerge)#, command =self.changeCheckValue)
        check2 = Checkbutton(self, variable=self.checkBaseline)
        setStyleText(check1, " Use Merged Data")
        setStyleText(check2, " Use Baseline Corr.")
        check1.grid(row=8, column=0, padx=(20, 0), pady=(10, 0), sticky="nw")
        check2.grid(row=9, column=0, padx=(20, 0), sticky="nw")
        
        frame = Frame(self)
        frame.configure(background=window_bg)
        submit = Button(frame, command = self.submit)
        cancel = Button(frame, command = lambda: self.destroy())
        setStyleText(cancel, "Cancel")
        setStyleText(submit, "Submit")
        submit.grid(row=0, column=0, padx=(0, 5), sticky="nw")
        cancel.grid(row=0, column=1, padx=(0, 5), sticky="nw")
        frame.grid(row=10, column=0, padx=(20, 0), pady=(10, 0))
        
    '''
    def changeCheckValue(self):
        global usingMergedData 
        value = self.checkMerge.get()
        if value == 1:
            selectSplittedData.grid_remove()
            selectMergedData.grid()
            usingMergedData = True
        else:
            selectMergedData.grid_remove()
            selectSplittedData.grid()
            usingMergedData = False
    '''
        
    def loadData(self):
        self.inputs[0].insert(0, advaced_setting["sampling_rate"])
        self.inputs[1].insert(0, advaced_setting["segment_length"])
        self.inputs[2].insert(0, advaced_setting["start_whole"][0])
        self.inputs[3].insert(0, advaced_setting["start_whole"][1])
        self.inputs[4].insert(0, advaced_setting["end_whole"][0])
        self.inputs[5].insert(0, advaced_setting["end_whole"][1])

    def submit(self):
        global usingMergedData, use_baseline_correction
        advaced_setting["sampling_rate"] = int(self.inputs[0].get())
        advaced_setting["segment_length"] = int(self.inputs[1].get())
        advaced_setting["start_whole"][0] = int(self.inputs[2].get())
        advaced_setting["start_whole"][1] = int(self.inputs[3].get())
        advaced_setting["end_whole"][0] = int(self.inputs[4].get())
        advaced_setting["end_whole"][1] = int(self.inputs[5].get())
        use_baseline_correction = True if self.checkBaseline.get() == 1 else False
        value = self.checkMerge.get()
        self.destroy()
        if value == 1:
            selectSplittedData.grid_remove()
            selectMergedData.grid()
            usingMergedData = True
        else:
            selectMergedData.grid_remove()
            selectSplittedData.grid()
            usingMergedData = False

    def textAndInput(self, text, row):
        frame = Frame(self)
        frame.configure(background=window_bg)
        label = createLabel(frame)
        setStyleText(label, text)
        vcmd = (self.register(self.validateInput))
        inputText = Entry(frame, 
            validate='all', 
            validatecommand=(vcmd, '%P'))
        inputText.grid(row=1, column=0)
        label.grid(row=0, column=0, padx=(0, 20), sticky="nw")
        frame.grid(row = row, column= 0, padx=(20, 0), sticky="nw")
        self.inputs.append(inputText)
        
    def validateInput(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False


#-----------------
#BUTTONS WIDGETS  
#-----------------
def clearChannelsButton(frame, i, command):
    red = "#db1414"
    btn_clear = Button(frame, 
        command = command,
        activeforeground = "white",
        activebackground = red, 
        foreground = "white",
        background = red, 
        borderwidth = '0',
        highlightthickness = '0')
    setStyleText(btn_clear, "X")
    btn_clear.grid(row=i + 1, column=4, padx=10, pady=2)
    return btn_clear

def buildSplittedDataButtons(row):
    fr_buttons = Frame(window)
    fr_buttons.configure(background=window_bg)
    channel = ['N90E', 'N00E', 'VERTICAL']
    
    for i in range(len(channel)):
        label = createLabel(fr_buttons)
        setStyleText(label, channel[i], True)
        label.grid(row=0, column=i + 1, padx=5, pady=5)
        
    for sensor in range(2):
        btns = []
        names = []
        sensors = []
        btn_select = Button(
            fr_buttons, 
            command = lambda x=sensor:selectFilesSystem(x))
        setStyleText(btn_select, f"SELECT {'H' if sensor == 0 else 'L'} DATA")
        btn_select.grid(row=sensor + 1, column=0, padx=10, pady=2)
        clearChannelsButton(
            fr_buttons, sensor, 
            lambda x=sensor: clearSplittedChannelsSelected(x))
        for i in range(len(channel)):
            btn_channel = TransparentButton(
                fr_buttons, 
                command = lambda x=sensor, y=i:selectFilesSystem(x, y))
            btn_channel.grid(row=sensor + 1, column=i+1, padx=5, pady=5)
            setStyleText(btn_channel, "NOT SELECTED")
            names.append([])
            sensors.append([])
            btns.append(btn_channel)
        fr_buttons.grid(row=row, column=1)
        splittedData_filepath.append(sensors)
        splittedData_buttons.append(btns)
        splittedData_names.append(names)  
    return fr_buttons

def buildMergedDataButtons(row):
    fr_buttons = Frame(window)
    fr_buttons.configure(background=window_bg)
    
    label = createLabel(fr_buttons)
    setStyleText(label, "N90E, N00E and VERTICAL", True)
    label.grid(row=0, column=1, padx=5, pady=5)
        
    for sensor in range(2):
        clearChannelsButton(
            fr_buttons, sensor, 
            lambda x=sensor: clearMergedChannelsSelected(x))
        btn_channel = TransparentButton(fr_buttons, 
            command = lambda index=sensor:selectFilesSystem(index))
        setStyleText(
            btn_channel, 
            "NOT SELECTED {} DATA".format("H" if sensor == 0 else "L"))
        btn_channel.grid(row=sensor + 1, column=1, padx=5, pady=5)
        fr_buttons.grid(row=row, column=1) 
        mergedData_buttons.append(btn_channel)
        mergedData_filepath.append([])
        mergedData_names.append([])  
    return fr_buttons


#STYLE WIDGETS
def createLabel(frame):
    return Label(frame, background=window_bg)    

def setStyleText(element, text, bold = False):
    element.configure(
        text=text, 
        font = ("Roboto", 10, "bold" if bold else "normal"))
    
def setWindowStyle(master):
    master.resizable(0, 0)
    master.rowconfigure(0, weight=0)
    master.columnconfigure(1, weight=1)
    master.configure(background=window_bg)
  

#-----------------
#BACKEND FUNCTIONS
#-----------------
#SPLITTED FILES FUNCTIONS
def updateSplittedFilesSelected(filepath, sensorIndex, channelIndex):
    filename = filepath.split("/")[-1]
    splittedData_names[sensorIndex][channelIndex] = filename
    splittedData_filepath[sensorIndex][channelIndex] = filepath
    if len(filename) > 12: 
        filename = filename[:12] + "..."
    setStyleText(splittedData_buttons[sensorIndex][channelIndex], filename, True)
    
def clearSplittedChannelsSelected(sensorIndex):
    for i in range(3):
        setStyleText(splittedData_buttons[sensorIndex][i], "NOT SELECTED") 
        splittedData_filepath[sensorIndex][i] = []
        splittedData_names[sensorIndex][i] = []    
  
#MERGED FILES FUNCTIONS      
def updateMergedFilesSelected(filepath, index):
    filename = filepath.split("/")[-1]
    mergedData_names[index] = filename
    mergedData_filepath[index] = filepath
    if len(filename) > 12:
        filename = filename[:12] + "..."
    setStyleText(mergedData_buttons[index], filename, True)
    
def clearMergedChannelsSelected(sensorIndex):
    text = "NOT SELECTED {} DATA".format("H" if sensorIndex == 0 else "L")
    setStyleText(mergedData_buttons[sensorIndex], text) 
    mergedData_filepath[sensorIndex] = []
    mergedData_names[sensorIndex] = []    
    

#SELECT FILES FUNCTION
def selectFilesSystem(sensorIndex, channelIndex = None):
    filepath = askopenfilename(
        filetypes = [
            ("Todos los archivos", "*.*"), 
            ("Archivos .sac", "*.sac"), 
            ("Archivos .mseed", "*.mseed")],
        title = 'Selecciona los archivos',
        multiple = True if channelIndex == None and not usingMergedData else False)
    
    if not filepath: return 
    if not usingMergedData:
        if channelIndex is None:
            maxFiles = 3
            filepath = list(filepath)
            filepath.sort()
            filepath = filepath[:maxFiles]
            for i in range(len(filepath)):
                if filepath[i]: 
                    updateSplittedFilesSelected(filepath[i], sensorIndex, i)
        else: updateSplittedFilesSelected(filepath, sensorIndex, channelIndex)
    else: updateMergedFilesSelected(filepath, sensorIndex)


#GENERATE GRAPHS FUNCTIONS
def removeExtension(name):
    extension = name.split(".")[-1]
    return name.replace("." + extension, "")

def generateGraphs():
    isComplete = [True, True]
    for sensor in range(len(isComplete)):
        if not usingMergedData:
            for i in range(3):
                if not splittedData_filepath[sensor][i]:
                    isComplete[sensor] = False
        else:
            if not mergedData_filepath[sensor]:
                isComplete[sensor] = False
        
    if isComplete[0] or isComplete[1]:
        if isComplete[0] and isComplete[1]:
            names = []
            for i in range(2): 
                name = splittedData_names[i][0] if not usingMergedData else mergedData_names[i]
                names.append(removeExtension(name))
            folder = "{} - {}".format(names[0], names[1])
        else: 
            if not usingMergedData:
                folder = splittedData_names[0][0] if isComplete[0] else splittedData_names[1][0]
            else:
                folder = mergedData_names[0] if isComplete[0] else mergedData_names[1]
            folder = removeExtension(folder)
            
        pbs = ProgressBarScreen(window)
        generate_btn["state"] ="disabled"
        hfiles = splittedData_filepath[0] if not usingMergedData else [mergedData_filepath[0]]
        lfiles = splittedData_filepath[1] if not usingMergedData else [mergedData_filepath[1]]
        HH(hfiles if isComplete[0] else None, 
           lfiles if isComplete[1] else None, 
           folder = folder,
           progress = lambda percen, message: pbs.updatePercentage(percen, message),
           sampling_rate = advaced_setting["sampling_rate"],
           segment_length = advaced_setting["segment_length"],
           start_whole = advaced_setting["start_whole"],
           end_whole = advaced_setting["end_whole"],
           use_baseline_correction = use_baseline_correction)


#MAIN FUNCTION
if __name__ == '__main__':
    use_baseline_correction = True
    usingMergedData = False
    splittedData_filepath = []
    splittedData_buttons = []
    splittedData_names = []
    mergedData_filepath = []
    mergedData_buttons = []
    mergedData_names = []
    window_bg = '#F5F5F5'
    advaced_setting = {
        "sampling_rate": 250,
        "segment_length": 4096,
        "start_whole": [25000, 25000],
        "end_whole": [50000, 100000]}
    
    window = Tk()
    setWindowStyle(window)
    window.geometry("600x240")
    window.title("HH Graphs Generator")
    
    label = createLabel(window)
    setStyleText(label, "BASELINE CORRECTION, WELCH, HVSP AND HHSP GRAPHS GENERATOR")
    label.grid(row=0, column=1, pady=20)
    
    selectMergedData = buildMergedDataButtons(row=1)
    selectMergedData.grid_remove()
    selectSplittedData = buildSplittedDataButtons(row=1)
    
    generate_btn = Button(window, command = generateGraphs)
    setStyleText(generate_btn, "GENERATE")
    generate_btn.grid(row = 2, column = 1, pady=(20, 10)) 
    advanced_settings_btn = TransparentButton(window, command = lambda: AdvancedSettingsScreen(window))
    setStyleText(advanced_settings_btn, "ADVANCED SETTINGS")
    advanced_settings_btn.grid(row=3, column=1)
        
    window.mainloop()
    
    
    
    
    
    