from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtWidgets import *
from xpfpath import *
from pygame import mixer
import json, os

class MainWindow(QMainWindow):
    ## Define Main Window
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyTimer")

        # Define Containers
        canvas = QWidget()              # Define Modifiable Space
        self.setCentralWidget(canvas)   # Set Modifiable Space in the Middle so we can see it
        baseGrid = QGridLayout()        # Define Adressable Coordinates
        topBarContent = QHBoxLayout()   # Horizontal Layout
        mainContent = QVBoxLayout()     # Vertical Layout
        self.timerBarContent = QVBoxLayout() # Active Timers List
        
        # Define Contents
        canvas.setLayout(baseGrid)  # Add the Grid
        topBarContent.addStretch() # Idk what it does yet but we'll see
        
        ## Define Grid Elements
        ## baseGrid.addLayout(Element, ROW, COL)
        #
        # Layout
        baseGrid.addLayout(topBarContent,0,0)   # Add the [Top Bar Contents] to r0,c0
        baseGrid.addLayout(mainContent,1,0)     # Add the [Main Contents   ] to r1,c0
        baseGrid.addLayout(self.timerBarContent,2,0) # Add Display for Current Active Timers
        
        
        ## Add Widgets to Layouts
        #
        # Top Bar
        for each in self.addTopBarContents():
            topBarContent.addWidget(each)
        # Main Contents
        for each in self.addMainContents():
            mainContent.addLayout(each)

    # Scan for Timers in a PATH
    def scanForTimers(self):
        # Timer files
        TimersIndex = []
        # Timer JSON data
        global TimerData
        TimerData = []
        # path to timers folder
        path = xpfp('./timer_data')
        # Verbose info
        print('Scanning for Timers...')
        # Scan Folder for Timers
        try:
            # scan path
            Files = os.scandir(path)
        except Exception as ERR:
            # oops you have no timers
            print(f'You do not have any timers saved. [ {ERR} ]')
            os.mkdir('timer_data')
        # Scan Specifically for JSON files
        for Entry in Files:
            _ = str(Entry.name).split('.')
            TimersIndex.append(Entry.name) if _[-1] == "json" else print(f"{Entry} != *.json")
        print(TimersIndex)
        # Load JSON
        # print(TimersIndex)
        for Files in TimersIndex:
            # Sound: SoundButton = SoundButton(f"{Files}")
            # jsonData: dict = {}
            with open(xpfp(f"{path}/{Files}"),'r') as Data:
                jsonData = json.loads(Data.read())
                TimerData.append(jsonData)
        # print(TimerData)
                
            # TimerData.append([f"{name}", timer])
            # print([f"{y}", timer])
            # time.sleep(0.0015625)
        return TimerData
    
    ## Define Contents of Each Layout
    def addTopBarContents(self):
        # topBarContents.addWidget(Element, ROW, COL)
        #
        def createNewTimer():
            print('New Button Pressed!')
        NewButton = QPushButton("New")
        NewButton.clicked.connect(createNewTimer) # 'print' is TEMPORARY
        _ = [
            QLabel("Create or Start Timer"),
            NewButton
        ]
        return _
    
    # Create QHBoxLayout Objects List            
    def addMainContents(self):
        timerBarContent = self.timerBarContent
        # Create objects of QHBoxLayout and return a list of them
        TimerLayouts = []
        # Create a button which stores data about the timer
        class TimerButtonStart(QPushButton):
            def __init__(self, *Data):
                super().__init__()
                self.setText("Start") # Set label of the button, same as 'Button = QPushButton("Start")'
                # Store data about the timer inside this button
                self.name = Data[0]
                self.seconds = Data[1]
                # Connect itself to a method which gets called when clicked
                self.clicked.connect(self.createProgressBar)

            ### <--- ### == Sections which needs to be re-written later
            ### I will have to somehow make this instanced so that i can create as much timers as i want/stop each timer instance
            ### May need to slap this into a 'class className():'
            def advanceProgressBar(self):
                curVal = self.progressBar.value()
                maxVal = self.progressBar.maximum()
                self.progressBar.setValue(curVal+1)
                if curVal == maxVal:
                    print(f"Finished Timer: {self.name}")
                    self.progressBar.close()
                    self.timerStart.stop()
            ###
            # Create the Progress Bar and show it
            def createProgressBar(self):
                try:
                    timerBarContent.removeWidget(self.progressBar)
                    self.timerStart.stop()
                    print(f"Stopping Timer: {self.name}")
                except:pass
                print(f"Starting Timer: {self.name}")
                # create a for loop to create timers and get timer ID or create another class which holds the timer
                # To be decided!
                self.timerStart = QTimer(self)
                self.timerStart.timeout.connect(self.advanceProgressBar)
                self.progressBar = QProgressBar()
                timerBarContent.addWidget(self.progressBar)
                self.progressBar.setRange(0, self.seconds)
                self.progressBar.setValue(0)

                self.timerStart.start(1000)
                self.progressBar.setFormat(f"{self.timerStart.timerId()}: {self.name}")
                self.progressBar.show()
        # Create List of Layouts containing TimerLabel and TimerStartButton
        for each in self.scanForTimers():
            # Create new Instances
            timer: QHBoxLayout = QHBoxLayout()
            timer.addWidget(QLabel(f'{each["Name"]}: {each["Seconds"]}s'))  
            timer.addWidget(TimerButtonStart(each["Name"],each["Seconds"])) # I can finally pass data over to the button
            TimerLayouts.append(timer)
        return TimerLayouts


APP = QApplication([])

MainFrame = MainWindow()
MainFrame.show()

APP.exec()
