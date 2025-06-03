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
        self.setFixedWidth(350)
        # self.setFixedSize(self.size())
        # self.setMinimumHeight(200)
        # windowGeometry = self.size()
        
        # Reset the Window's size after timer progress bar is removed
        # Dynamically resize the window in a nutshell
        
        ## IT LITERALLY FROZE MY LINUX MINT DESKTOP SO I SHALL REFRAIN FROM
        ## USING THIS METHOD OF STOPPING WINDOW RESIZE LMAOOOOOOOOO
        # windowReset = QTimer(self)
        # def windowGeo():
        #     self.adjustSize()
        #     self.resize(self.minimumSize())
        # windowReset.timeout.connect(windowGeo)
        # windowReset.start()

        # Define Containers
        canvas = QWidget()                                   # Define Modifiable Space
        self.setCentralWidget(canvas)                        # Set Modifiable Space in the Middle so we can see it
        baseGrid = QGridLayout()                             # Define Adressable Coordinates
        topBarContent = QHBoxLayout()                        # Horizontal Layout
        mainContent = QVBoxLayout()                          # Vertical Layout
        mainContent.addSpacerItem(QSpacerItem(0,5))          # Add gap between mainContent and topBar
        self.timerBarContent = QVBoxLayout()                 # Active Timers List
        self.timerBarContent.addSpacerItem(QSpacerItem(0,5)) # Add gap between mainContent and timerBarContent
        
        
        # Define Contents
        canvas.setLayout(baseGrid)  # Add the Grid
        # topBarContent.addStretch()
        # topBarContent.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
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
        print('\nScanning for Timers...')
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
        # Load JSON, and pass data over
        # print(TimersIndex)
        for Files in TimersIndex:
            with open(xpfp(f"{path}/{Files}"),'r') as Data:
                jsonData = json.loads(Data.read())
                TimerData.append(jsonData)
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
                self.timerData = Data
                # Store data about the timer inside this button
                # Connect itself to a method which gets called when clicked
                self.clicked.connect(self.start)
            def start(self):
                timerProgress(self.timerData)
        
        # Create timer which is attached to the button's data
        class timerProgress(QProgressBar):
            def __init__(self, Data):
                super().__init__()
                # House Keeping
                self.name = Data[0]
                self.seconds = Data[1]
                print(f'Starting Timer: {self.name}_{self.seconds}s')
                # set progressbar bounds
                self.setRange(0, self.seconds)
                self.setValue(0)
                # create instance of timer
                self.time = QTimer(self)
                self.stopbutton = QPushButton("Stop")
                self.stopbutton.clicked.connect(self.stopTimer)
                # create container for timer progress and stop button for that timer
                self.content = QHBoxLayout()
                self.content.addWidget(self.stopbutton)
                self.content.addWidget(self)
                # @ timer timout, execute function
                self.time.timeout.connect(self.startTimer)
                # create progress bar in main window
                timerBarContent.addLayout(self.content)
                # Actually start timer
                self.time.start(1000) # 1s
                # Format Progress Bar Display
                self.setFormat(f"{self.time.timerId()}: {self.name}")
                
            def startTimer(self):
                # increment bar and stop when maxVal is reached
                self.curVal = self.value()
                self.maxVal = self.maximum()
                self.setValue(self.curVal+1) #increment
                # if maxVal is reached, or if timer isActive == False, delete relevant widgets
                if self.curVal >= self.maxVal or self.time.isActive() == False:
                    timerBarContent.removeWidget(self)
                    timerBarContent.removeWidget(self.stopbutton)
                    print(f"Finished Timer: {self.time.timerId()}-{self.name}") if self.time.timerId() != -1 else ''
            def stopTimer(self):
                    print(f"Stopped_ Timer: {self.time.timerId()}-{self.name}")
                    self.time.stop()
                    self.time.killTimer(self.time.timerId())
                    self.startTimer()
                
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
