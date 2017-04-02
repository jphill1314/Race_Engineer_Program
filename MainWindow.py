import tkinter as tk
import math

class MainWindow:

    """
    initializes all variables and call function to create main UI
    """
    def __init__(self):
        self._window = tk.Tk()

        self._nextPit = 0
        self._lastPitLap = 1
        self._currentLap = 1
        self._totalLaps = 39

        self._pitLaps = [22, 35, self._totalLaps, self._totalLaps, self._totalLaps]

        self._wearCliff = 35

        self._lfWear = 100
        self._rfWear = 100
        self._lrWear = 100
        self._rrWear = 100

        self._lfWearRate = 0
        self._rfWearRate = 0
        self._lrWearRate = 0
        self._rrWearRate = 0

        self._lfCliff = self._totalLaps
        self._rfCliff = self._totalLaps
        self._lrCliff = self._totalLaps
        self._rrCliff = self._totalLaps

        self._startFuel = 95.0
        self._currentFuel = 95.0
        self._normalFuelPerLap = 2.3
        self._highMixFuelPerLap = 2.8
        self._highMixLaps = self._highMixCalc()

        self._initUI()

    """
    initializes main UI
    """
    def _initUI(self):
        self._window.title("Race Engineer")

        self._r = 0
        self._pitLap = tk.Label(text="Pitting Lap: " + str(self._pitLaps[self._nextPit]))
        self._pitLap.grid(row=self._r,columnspan=4, rowspan=2)
        self._lapNum = tk.Label(text="Lap " + str(self._currentLap) + " / " + str(self._totalLaps))
        self._lapNum.grid(row=self._r, column=4, columnspan=2, rowspan=2, sticky="w")
        self._increaseLapTotal = tk.Button(text="+", width=5, command=self._increaseLapCount)
        self._increaseLapTotal.grid(row=self._r, column=6)

        self._r +=1
        self._decreaseLapTotal = tk.Button(text="-", width=5, command=self._decreaseLapCount)
        self._decreaseLapTotal.grid(row=self._r, column=6)

        self._r += 1
        self._pitStrat = tk.Button(text="Pit Strategy", command=self._initPitStratWindow)
        self._pitStrat.grid(row=self._r, column=1, columnspan=2)
        self._editValuesButton = tk.Button(text="Edit Values", command=self._editValuesWindow)
        self._editValuesButton.grid(row=self._r, column=4, columnspan=2)

        self._r += 1
        self._cliffLeft = tk.Label(text="Cliff Lap")
        self._cliffLeft.grid(row=self._r, column=0)
        self._lfLabel = tk.Label(text="LF")
        self._lfLabel.grid(row=self._r, column=1)
        self._rfLabel = tk.Label(text='RF')
        self._rfLabel.grid(row=self._r, column=2)
        self._cliffRight = tk.Label(text="Cliff Lap")
        self._cliffRight.grid(row=self._r, column=3)
        self._fuelLabel = tk.Label(text="Fuel")
        self._fuelLabel.grid(row=self._r, column=4)

        self._r += 1
        self._lfCliffLap = tk.Label(text=str(self._lfCliff))
        self._lfCliffLap.grid(row=self._r, column=0)
        self._lfWearEntry = tk.Entry(width=5)
        self._lfWearEntry.grid(row=self._r, column=1)
        self._rfWearEntry = tk.Entry(width=5)
        self._rfWearEntry.grid(row=self._r, column=2)
        self._rfCliffLap = tk.Label(text=str(self._rfCliff))
        self._rfCliffLap.grid(row=self._r, column=3)
        self._fuelEntry = tk.Entry(width=5)
        self._fuelEntry.grid(row=self._r, column=4)
        '''self._highMixCheck = tk.Checkbutton()
        self._highMixCheck.grid(row=self._r, column=5)
        self._highMixQ = tk.Label(text="Mix 2?")
        self._highMixQ.grid(row=self._r, column=6)'''

        self._r += 1
        self._lrCliffLap = tk.Label(text=str(self._lrCliff))
        self._lrCliffLap.grid(row=self._r, column=0)
        self._lrWearEntry = tk.Entry(width=5)
        self._lrWearEntry.grid(row=self._r, column=1)
        self._rrWearEntry = tk.Entry(width=5)
        self._rrWearEntry.grid(row=self._r, column=2)
        self._rrCliffLap = tk.Label(text=str(self._rrCliff))
        self._rrCliffLap.grid(row=self._r,  column=3)
        self._highMixLapsLabel = tk.Label(text="Mix 2 Laps: " + str(self._highMixLaps))
        self._highMixLapsLabel.grid(row=self._r, column = 4, columnspan=3, sticky="w")

        self._r += 1
        self._lrLabel = tk.Label(text="LR")
        self._lrLabel.grid(row=self._r, column=1)
        self._rrLabel = tk.Label(text="RR")
        self._rrLabel.grid(row=self._r, column=2)

        self._r += 1
        self._nextLap = tk.Button(text="Next Lap", command=self._nextLap)
        self._nextLap.grid(row=self._r, columnspan=7)

        self._updateLabels()

    """
    public function to open the window
    """
    def openWindow(self):
        self._window.mainloop()


    """
    updates all labels that change each lap or when new info is added

    needs to change color of cliff laps if they are before / after next pit
    """
    def _updateLabels(self):
        if self._pitLaps[self._nextPit] != self._totalLaps:
            self._pitLap.config(text="Pitting Lap: " + str(self._pitLaps[self._nextPit]))
        else:
            self._pitLap.config(text="No more scheduled pits")

        self._lapNum.config(text="Lap " + str(self._currentLap) + " / " + str(self._totalLaps))

        self._highMixLaps = self._highMixCalc()
        self._highMixLapsLabel.config(text="Mix 2 laps: " + str(self._highMixLaps))

        self._calcTireWearRate()
        if self._lfCliff >= self._pitLaps[self._nextPit]:
            self._lfCliffLap.config(text=str(self._lfCliff), fg="green")
        else:
            self._lfCliffLap.config(text=str(self._lfCliff), fg="red")

        if self._rfCliff >= self._pitLaps[self._nextPit]:
            self._rfCliffLap.config(text=str(self._rfCliff), fg="green")
        else:
            self._rfCliffLap.config(text=str(self._rfCliff), fg="red")

        if self._lrCliff >= self._pitLaps[self._nextPit]:
            self._lrCliffLap.config(text=str(self._lrCliff), fg="green")
        else:
            self._lrCliffLap.config(text=str(self._lrCliff), fg="red")

        if self._rrCliff >= self._pitLaps[self._nextPit]:
            self._rrCliffLap.config(text=str(self._rrCliff), fg="green")
        else:
            self._rrCliffLap.config(text=str(self._rrCliff), fg="red")

    """
    calculates the number of high mix laps left based on predetermined per lap usages of fuel

    should also do the calc based on the rates that could be calculated on the data entered each lap
    """
    def _highMixCalc(self):
        lapsLeft = self._totalLaps - self._currentLap + 1
        highMixDiff = self._highMixFuelPerLap - self._normalFuelPerLap

        if highMixDiff > 0:
            extraFuel = self._currentFuel - (lapsLeft * self._normalFuelPerLap)
            return math.floor(extraFuel / highMixDiff)
        else:
            return 0


    """
    function called by + button
    used when driver unlaps self
    """
    def _increaseLapCount(self):
        self._totalLaps += 1
        self._updateLabels()

    """
    function called by - button
    used when driver is lapped
    """
    def _decreaseLapCount(self):
        self._totalLaps -= 1
        self._updateLabels()


    """
    called every lap
    calculates the wear rate of the current tires and is based only on the current stint
    (might be a good idea to use data from earlier runs but need to add way to indicate option vs. primes)
    """
    def _calcTireWearRate(self):
        if self._currentLap != self._lastPitLap:
            self._lfWearRate = (100.0 - self._lfWear) / (self._currentLap - self._lastPitLap)
            self._rfWearRate = (100.0 - self._rfWear) / (self._currentLap - self._lastPitLap)
            self._lrWearRate = (100.0 - self._lrWear) / (self._currentLap - self._lastPitLap)
            self._rrWearRate = (100.0 - self._rrWear) / (self._currentLap - self._lastPitLap)
        else:
            return
        self._lfCliff = self._currentLap + self._calcCliffLap(self._lfWearRate, self._lfWear)
        self._rfCliff = self._currentLap + self._calcCliffLap(self._rfWearRate, self._rfWear)
        self._lrCliff = self._currentLap + self._calcCliffLap(self._lrWearRate, self._lrWear)
        self._rrCliff = self._currentLap + self._calcCliffLap(self._rrWearRate, self._rrWear)


    """
    calculates when current tires will reach predefined cliff
    """
    def _calcCliffLap(self, wearRate, currWear):
        lapsToCliff = 0
        while currWear > self._wearCliff:
            currWear -= wearRate
            lapsToCliff += 1
        return lapsToCliff

    """
    called by Next Lap button
    calls functions that update data based on the new data gained
    """
    def _nextLap(self):
        if self._currentLap < self._totalLaps:
            self._currentLap += 1

            prvWear = self._lfWear

            if str(self._lfWearEntry.get()) != "":
                self._lfWear = int(self._lfWearEntry.get())

            if str(self._rfWearEntry.get()) != "":
                self._rfWear = int(self._rfWearEntry.get())

            if str(self._lrWearEntry.get()) != "":
                self._lrWear = int(self._lrWearEntry.get())

            if str(self._rrWearEntry.get()) != "":
                self._rrWear = int(self._rrWearEntry.get())

            if str(self._fuelEntry.get()) != "":
                self._currentFuel = float(self._fuelEntry.get())


            if prvWear < self._lfWear:
                self._lastPitLap = self._currentLap
                self._pitLaps[self._nextPit] = self._currentLap - 1
                self._nextPit += 1

            self._updateLabels()


    """
    Called by Pit Strat button
    Opens window to edit pit strategy

    could be changed to dynamically add / delete pit stops rather than always have 5 --- would make could nicer looking
    """
    def _initPitStratWindow(self):
        self._stratWindow = tk.Toplevel()
        self._stratWindow.title("Pit Strategy")

        self._pitOneLabel = tk.Label(self._stratWindow, text="Pit 1 lap: ")
        self._pitOneLabel.grid(row=0, column=0)
        self._pitOneEntry = tk.Entry(self._stratWindow, width=10)
        self._pitOneEntry.insert(0, str(self._pitLaps[0]))
        self._pitOneEntry.grid(row=0, column=1)

        self._pitTwoLabel = tk.Label(self._stratWindow, text="Pit 2 lap: ")
        self._pitTwoLabel.grid(row=1, column=0)
        self._pitTwoEntry = tk.Entry(self._stratWindow, width=10)
        self._pitTwoEntry.insert(0, str(self._pitLaps[1]))
        self._pitTwoEntry.grid(row=1, column=1)

        self._pitThreeLabel = tk.Label(self._stratWindow, text="Pit 3 lap: ")
        self._pitThreeLabel.grid(row=2, column=0)
        self._pitThreeEntry = tk.Entry(self._stratWindow, width=10)
        self._pitThreeEntry.insert(0, str(self._pitLaps[2]))
        self._pitThreeEntry.grid(row=2, column=1)

        self._pitFourLabel = tk.Label(self._stratWindow, text="Pit 4 lap: ")
        self._pitFourLabel.grid(row=3, column=0)
        self._pitFourEntry = tk.Entry(self._stratWindow, width=10)
        self._pitFourEntry.insert(0, str(self._pitLaps[3]))
        self._pitFourEntry.grid(row=3, column=1)

        self._pitFiveLabel = tk.Label(self._stratWindow, text="Pit 5 lap: ")
        self._pitFiveLabel.grid(row=4, column=0)
        self._pitFiveEntry = tk.Entry(self._stratWindow, width=10)
        self._pitFiveEntry.insert(0, str(self._pitLaps[4]))
        self._pitFiveEntry.grid(row=4, column=1)

        self._finishButton = tk.Button(self._stratWindow, text="Done", command=self._finishEdit)
        self._finishButton.grid(row=5, columnspan=2)


    """
    Called by Done button in Pit Strat window
    Updates current pit strat based on entered values
    """
    def _finishEdit(self):
        self._pitLaps[0] = int(self._pitOneEntry.get())
        self._pitLaps[1] = int(self._pitTwoEntry.get())
        self._pitLaps[2] = int(self._pitThreeEntry.get())
        self._pitLaps[3] = int(self._pitFourEntry.get())
        self._pitLaps[4] = int(self._pitFiveEntry.get())

        for p in range(5):
            if self._pitLaps[p] == 0 or self._pitLaps[p] > self._totalLaps:
                self._pitLaps[p] = self._totalLaps

        self._updateLabels()
        self._stratWindow.destroy()

    """
    called when program is launched and when the edit values button is pressed
    updates variables when Done button is pressed
    """
    def _editValuesWindow(self):
        self._editWindow = tk.Toplevel()

        rn = 0

        self._LapsLabel = tk.Label(self._editWindow, text="Total Laps: ")
        self._LapsLabel.grid(row=rn, column=0)
        self._LapsEntry = tk.Entry(self._editWindow, width=10)
        self._LapsEntry.insert(0, self._totalLaps)
        self._LapsEntry.grid(row=rn, column=1)

        rn += 1

        self._normalFuelLabel = tk.Label(self._editWindow, text="Normal Fuel Usage per Lap: ")
        self._normalFuelLabel.grid(row=rn, column=0)
        self._normalFuelEntry = tk.Entry(self._editWindow, width=10)
        self._normalFuelEntry.insert(0, self._normalFuelPerLap)
        self._normalFuelEntry.grid(row=rn, column=1)

        rn += 1

        self._highFuelLabel = tk.Label(self._editWindow, text="High Mix Fuel Usage per Lap: ")
        self._highFuelLabel.grid(row=rn, column=0)
        self._highFuelEntry = tk.Entry(self._editWindow, width=10)
        self._highFuelEntry.insert(0, self._highMixFuelPerLap)
        self._highFuelEntry.grid(row=rn, column=1)

        rn += 1

        self._editFuelLabel = tk.Label(self._editWindow, text="Starting Fuel: ")
        self._editFuelLabel.grid(row=rn, column=0)
        self._editFuelEntry = tk.Entry(self._editWindow, width=10)
        self._editFuelEntry.insert(0, self._startFuel)
        self._editFuelEntry.grid(row=rn, column=1)

        rn += 1

        self._editCliffLabel = tk.Label(self._editWindow, text="Tire Cliff %: ")
        self._editCliffLabel.grid(row=rn, column=0)
        self._editCliffEntry = tk.Entry(self._editWindow, width=10)
        self._editCliffEntry.insert(0, self._wearCliff)
        self._editCliffEntry.grid(row=rn, column=1)

        rn += 1

        self._editWindowButton = tk.Button(self._editWindow, text="Done", command=self._editWindowFinish)
        self._editWindowButton.grid(row=rn, columnspan=2)

    """
    Closes edit window and saves all values entered
    """
    def _editWindowFinish(self):
        self._totalLaps = int(self._LapsEntry.get())
        self._normalFuelPerLap = float(self._normalFuelEntry.get())
        self._highMixFuelPerLap = float(self._highFuelEntry.get())
        self._startFuel = float(self._editFuelEntry.get())
        self._wearCliff = int(self._editCliffEntry.get())

        self._updateLabels()
        self._editWindow.destroy()