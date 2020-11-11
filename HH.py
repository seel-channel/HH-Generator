import os
import time
import numpy as np
import obspy as obs
import scipy.signal as sg
import matplotlib.pyplot as plt
from BaselineRemoval import BaselineRemoval

class HH:
    def __init__(self, 
            files_hpath, 
            files_lpath, 
            progress = None, 
            folder = None, 
            segment_length = 4096, 
            sampling_rate= 250,
            start_whole = [25000, 25000],
            end_whole = [50000, 100000],
            use_baseline_correction = True):
        self.end_whole = end_whole
        self.start_whole = start_whole
        self.files_hpath = files_hpath
        self.files_lpath = files_lpath
        self.segment_length = segment_length
        self.sampling_rate = sampling_rate
        self.partial_frec = 1 / self.sampling_rate
        self.channel_name = ['N90E', 'N00E', 'VERTICAL']
        self.use_baseline_correction = use_baseline_correction
        self.sensors = 2 if files_hpath and files_lpath else 1
        self.plots_amount = 3
        
        if files_hpath and files_lpath:
            self.files_len = len(min(files_hpath, files_lpath))
        else:
            self.files_len = len(files_hpath) if files_hpath else len(files_lpath)
        
        self.folder = folder
        self.progress = progress
        self.percentageComplete = 0
        
        self.all_data = []
        self.all_welch = []
        self.all_baseline = []
        
        
        for sensor in range(self.sensors):
            if files_hpath and files_lpath:
                files_path = files_hpath if sensor == 0 else files_lpath
            else: 
                files_path = files_hpath if files_hpath else files_lpath
            
            computedChannelsData = self.computeChannel(files_path, sensor)
                
            self.all_data.append(computedChannelsData[0])
            self.all_baseline.append(computedChannelsData[1])
            self.all_welch.append(computedChannelsData[2])
            print(14*"--" + "\n")
        
        print("GENERATING GRAPHS")
        plt.rcParams['agg.path.chunksize'] = 10000
        self.updatePercentage(7, f"GRAPHING DATA AND BASELINE")
        self.updatePercentage(0, "")
        self.graphSensorsDataAndBaseline()
        self.updatePercentage(5, f"GRAPHING BASELINE AND WELCH")
        self.updatePercentage(0, "")
        self.graphBaselineAndWelch()
        self.updatePercentage(10, f"GRAPHING VHSR")
        self.updatePercentage(0, "")
        self.graphHVSR()
        if files_hpath and files_lpath: 
            self.updatePercentage(3, f"GRAPHING HHSR")
            self.updatePercentage(0, "")
            self.graphHHSR()
        self.updatePercentage(6, f"DONE")
        self.updatePercentage(0, "")
        print("\n" + 14*"--" + "\n")
    
    
    #LOADING DATA FUNCTIONS
    def loadFileData(self, filepath):
        filename = filepath.split("/")[-1]
        extension = filename.split(".")[-1].lower()
        if extension == "mseed" or extension == "sac":
            data = obs.read(filepath)[0].data
        else: data = np.loadtxt(filepath)
        return data
    
    def computeChannel(self, files_path, sensor):
        #Convert the data from data merge
        #FROM: [[x y z], [x y z], [x, y z], ..., [x y z]]
        #TO:   [[x, x, x, ..., x], [y, y, y, ..., y], [z, z, z, ..., z]]
        data = []
        loadingTimes = []
        if self.files_len == 1:
            timeMethod = time.time()
            fileData = self.loadFileData(files_path[0])
            x, y, z = [], [], []
            for i in range(len(fileData)):
                x.append(fileData[i][0])
                y.append(fileData[i][1])
                z.append(fileData[i][2])
            data.append(x)
            data.append(y)
            data.append(z)
            for i in range(self.plots_amount):
                loadingTimes.append("({:0.2f}s)".format(
                    (time.time() - timeMethod) / self.plots_amount))

        length = self.plots_amount
        data_sensor = []
        welch_sensor = []
        baseline_sensor = []
        for i in range(length):
            sensorTimeInit = time.time()
            completed = "{}/{}".format(i + 1, length)
            sensor_letter = self.getSensorLetter(sensor)
            progress = 6 if self.files_hpath and self.files_lpath else 12
            print("SENSOR{} - CHANNEL {}".format(sensor_letter, completed))
            
            #LOADING DATA
            print(" - LOADING DATA")
            self.updatePercentage(progress, f"LOADING{sensor_letter} DATA ({completed})")
            self.updatePercentage(0, "")
            timeMethod = time.time()
            if self.files_len > 1:
                dataVector = self.loadFileData(files_path[i])
                print("   {} DONE".format(self.timeDiff(timeMethod)))
            else:
                dataVector = data[i]
                print("   {} DONE".format(loadingTimes[i]))
            data_sensor.append(dataVector)
            
            #DATA TRIM
            end = self.end_whole[sensor]
            start = self.start_whole[sensor]
            totalWhole = start + end
            lenghtVector = len(dataVector)
            start = 1 if start < 1 else start
            end = 1 if end < 1 else end
            if totalWhole >= lenghtVector:
                print("   COULDNT TRIM DATA BEACAUSE (start_whole + end_whole) >= len(dataVector) ({} > {})".format(totalWhole, lenghtVector))
                data_trim = dataVector
            else: data_trim = dataVector[start:-end]
            
            #CORRECTION DATA
            print(" - BASELINE CORRECTION")
            self.updatePercentage(progress,  f"CORRECTING{sensor_letter} DATA ({completed})")
            self.updatePercentage(0, "")
            timeMethod = time.time()
            baseline_corr = self.baselineCorretion(data_trim)
            baseline_sensor.append(baseline_corr)
            print("   {} DONE".format(self.timeDiff(timeMethod)))
            
            #WELCH METHOD
            print(" - WELCH METHOD")
            timeMethod = time.time()
            welch_sensor.append(self.welchMethod(baseline_corr[1]))
            print("   {} DONE".format(self.timeDiff(timeMethod)))
           
            print("{} CHANNEL DATA LOADED \n".format(self.timeDiff(sensorTimeInit)))
        
        return data_sensor, baseline_sensor, welch_sensor
    
    
    #UTILS FUNCTIONS
    def updatePercentage(self, toComplete, message):
        self.percentageComplete += toComplete
        if self.progress is not None:
            self.progress(self.percentageComplete, message)
        
    def getSensorLetter(self, index):
        if self.files_hpath and self.files_lpath:
            letter = " H" if index == 0 else " L"
        else: letter = ""
        return letter  
        
    def timeDiff(self, timeInit):
        return "({:0.2f}s)".format(time.time() - timeInit)
    
    def smoothHV(self, hv):
        return sg.savgol_filter(hv, 3, 1)
    
    def figTitle(self, fig, title):
        fig.suptitle(title, fontweight="bold")
    
    def saveFig(self, fig, fname = None):
        actual = os.path.dirname(os.path.abspath(__file__))
        newpath = actual + "/generated/" + (self.folder + "/") if self.folder else ""
        if not os.path.exists(newpath) and self.folder:
            os.makedirs(newpath)
            
        fig.tight_layout(pad=2.0)
        if fname != None:
            fig.savefig(newpath + fname + ".jpg", dpi=300)
            
            
    #METHODS
    def baselineCorretion(self, data):
        data_len = len(data)
        x = np.arange(data_len) * self.partial_frec
        if self.use_baseline_correction:
            y = BaselineRemoval(data).ZhangFit(data_len)
            y = y - np.mean(y)
        else: y = data
        return  x,  y 
    
    def welchMethod(self, data):
        lenght = self.segment_length
        return sg.welch(
            data, 
            fs = self.sampling_rate,
            nfft = lenght,
            window = np.hamming(lenght),
            nperseg = lenght, 
            noverlap = lenght / 2)
    
    
    #STYLES
    def axSetGrid(self, ax):
        ax.grid('#CCCCCC', which='major', linestyle='--')
        ax.grid('#CCCCCC', which='minor', linestyle=':')
        
    def axLogLimits(self, ax, x):
        xMax = 10**1 + 2
        yMin = 10**-1 - 0.02
        ax.set_xlim(yMin, xMax)
        for j in range(len(x)):
            if x[j] > xMax:
                skip = j
                break
        return skip
    
    
    
    #SUBPLOT GENERATION FUNCTIONS
    def plotBaselineCorrection(self, ax, sensor, i):
        label_plot = "Baseline Correction " + self.channel_name[i]
        x, y = self.all_baseline[sensor][i]
        x_len = len(x)
        ax.grid()
        ax.plot(x, y, 'b', label=label_plot)
        ax.plot(x, np.zeros(x_len), 'r', label="Origin")
        ax.set_xlim(0, x_len * self.partial_frec)
        ax.legend(loc="upper right")
        
        
    def plotWelchMethod(self, ax, sensor, i):
        f, Pxx = self.all_welch[sensor][i]
        label_plot = "WELCH PEAK " + self.channel_name[i]
        self.axSetGrid(ax)
        skip = self.axLogLimits(ax, f)
        ax.semilogx(f[:skip], Pxx[:skip], 'k', label=label_plot)
        ax.legend(loc="upper left")
    
    
    #GRAPHICATION FUNCTIONS
    def graphSensorsDataAndBaseline(self):
        print(" - INITIALIZING SENSOR DATA AND BASELINE GRAPH...")
        timeInit = time.time()
        for sensor in range(self.sensors):
            title = "SENSOR{} DATA - BASELINE".format(self.getSensorLetter(sensor))
            fig, ax = plt.subplots(2, 3, figsize=(12, 6))
            frec = self.partial_frec
            
            for i in range(self.plots_amount):
                data = self.all_data[sensor][i]
                self.plotBaselineCorrection(ax[1, i], sensor, i)
                ax[0, i].plot(np.arange(len(data)) * frec, data, 'r', label=self.channel_name[i])
                ax[0, i].set_xlim(0, len(data) * frec)
                ax[0, i].legend(loc="upper left")
                
            self.figTitle(fig, title)
            self.saveFig(fig, title)
        print("   {} GRAPHS GENERATED".format(self.timeDiff(timeInit)))
    
    def graphBaselineAndWelch(self):
        print(" - INITIALIZING BASELINE AND WELCH GRAPHS...")
        timeInit = time.time()
        for sensor in range(self.sensors):
            letter = self.getSensorLetter(sensor)
            for i in range(self.plots_amount):
                title = "SENSOR{} - {} (BASELINE - WELCH)".format(letter, self.channel_name[i])
                fig, ax = plt.subplots(2, 1, figsize=(12, 6))
                self.plotBaselineCorrection(ax[0], sensor, i)
                self.plotWelchMethod(ax[1], sensor, i)
                self.figTitle(fig, title)
                self.saveFig(fig, title)
        print("   {} GRAPHS GENERATED".format(self.timeDiff(timeInit)))

    def graphHVSR(self):
        print(" - INITIALIZING HVSR GRAPHS...")
        timeInit = time.time()
        for sensor in range(self.sensors):
            fig, ax = plt.subplots(2, 1, figsize=(12, 8))
            sensor_letter = self.getSensorLetter(sensor)
            title = "SENSOR{} (HnV - HVSR)".format(sensor_letter)
            welch = self.all_welch[sensor]
            meanHV = np.sqrt(welch[0][1] * welch[1][1]) / welch[2][1]
            meanHV = self.smoothHV(meanHV)
            
            #Son las subplots de H1/V y H2/V
            for i in range(2):
                hvlabel = "{}/VSR".format(self.channel_name[i])
                x, y = welch[i]
                hv = y / welch[2][1]
                self.axSetGrid(ax[i])
                skip = self.axLogLimits(ax[i], x)
                ax[i].semilogx(x[:skip], meanHV[:skip], "y", label="HVSR")
                ax[i].semilogx(x[:skip], self.smoothHV(hv)[:skip], "k", label=hvlabel)
                ax[i].set_ylabel("H{}/V".format(i + 1))
                ax[i].set_xlabel("Frecuency (Hz)")
                ax[i].legend(loc="upper left")
            self.figTitle(fig, title)
            self.saveFig(fig, title)
            
            #Es la plot del HVSR
            verticalx = welch[2][0]
            fig, ax = plt.subplots(1, 1, figsize=(12, 6))
            title = "SENSOR{} HVSR".format(sensor_letter)
            self.axSetGrid(ax)
            skip = self.axLogLimits(ax, verticalx)
            ax.semilogx(verticalx[:skip], meanHV[:skip], "k", label="HVSR")
            ax.set_xlabel("Frecuency (Hz)")
            ax.legend(loc="upper left")
            self.figTitle(fig, title)
            self.saveFig(fig, title)
        print("   {} GRAPHS GENERATED".format(self.timeDiff(timeInit)))
        
    def graphHHSR(self):
        print(" - INITIALIZING HHSR GRAPHS...")
        timeInit = time.time()
        welch = self.all_welch
        colors = ["k", "b", "r"]
        channel = self.channel_name
        fig, ax = plt.subplots(3, 1, figsize=(12, 10))
        
        for i in range(self.plots_amount):
            x = welch[0][i][0]
            hh = welch[0][i][1] / welch[1][i][1]
            hh_label = "{}h/{}l SR".format(channel[i], channel[i])
            self.axSetGrid(ax[i])
            skip = self.axLogLimits(ax[i], x)
            ax[i].semilogx(x[:skip], hh[:skip], colors[i], label=hh_label)
            ax[i].set_xlabel("Frecuency (Hz)")
            ax[i].legend(loc="upper left")
            
        self.figTitle(fig, "HHSR")
        self.saveFig(fig, "HHSR")
        print("   {} GRAPHS GENERATED".format(self.timeDiff(timeInit)))
        

'''
# TESTING SPLITTED DATA
if __name__ == '__main__':
    viewData = []
    high = "/media/felipe/Estudio/Proyectos/Otros/HH Generator/data/MSEED/20/"
    low = "/media/felipe/Estudio/Proyectos/Otros/HH Generator/data/MSEED/0/"
    
    HH([high + "9CG.e.mseed", high + "9CG.n.mseed", high + "9CG.z.mseed"], 
           [low + "R1235.CG.e.mseed", low + "R1235.CG.n.mseed", low + "R1235.CG.z.mseed"])


# TESTING MERGED DATA
if __name__ == '__main__':
    viewData = []
    path = "/media/felipe/Estudio/Proyectos/Otros/HH Generator/data/ASCII merge/SNRA9510.091"
    HH([path], [path], start_whole=[1,1], end_whole=[1,1])
    
'''
    
    
    
