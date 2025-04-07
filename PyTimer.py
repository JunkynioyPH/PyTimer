from PyQt6.QtCore import QDateTime, Qt, QTimer, QSize
from PyQt6.QtWidgets import *
from xpfpath import *
import json, os, time

class MainWindow(QMainWindow):
    ## Define Main Window
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyTimer")

        # Define Containers
        canvas = QWidget()            # Define Modifiable Space
        self.setCentralWidget(canvas) # Set Modifiable Space in the Middle so we can see it
        baseGrid = QGridLayout()      # Define Adressable Coordinates
        topBarContent = QHBoxLayout() # Horizontal Layout
        mainContent = QVBoxLayout()   # Vertical Layout
        
        # Define Contents
        canvas.setLayout(baseGrid)  # Add the Grid
        topBarContent.addStretch(1) # Idk what it does yet but we'll see
        
        ## Define Grid Elements
        ## baseGrid.addLayout(Element, ROW, COL)
        #
        # Layout
        baseGrid.addLayout(topBarContent,0,0) # Add the [Top Bar Contents] to r0,c0
        baseGrid.addLayout(mainContent,1,0)   # Add the [Main Contents   ] to r1,c0
        
        ## Add Widgets to Layouts
        #
        # Top Bar
        for each in self.addTopBarContents():
            topBarContent.addWidget(each)
        # Main Contents
        for each in self.addMainContents():
            mainContent.addLayout(each)
        # self.addMainContents()

    # Scan for Timers in a PATH
    def scanForTimers(self):
        TimersIndex = []
        global TimerData
        TimerData = []
        path = xpfp('./timer_data')
        print('Scanning for Timers...')
        time.sleep(0.5)
        # Scan Folder for Timers
        try:
            Files = os.scandir(path)
        except Exception as ERR:
            print(f'You do not have any timers saved. [ {ERR} ]')
            os.mkdir('timer_data')
        # Scan Specifically for JSON files
        for Entry in Files:
            _ = str(Entry.name).split('.')
            TimersIndex.append(Entry.name) if _[-1] == "json" else print(f"{Entry} != *.json")
            try: print(TimersIndex[-1])
            except: pass
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
        _ = [
            QLabel("Create or Start Timer"),
            QPushButton("New")
        ]
        return _
    
    # Create QHBoxLayout Objects List            
    def addMainContents(self):
        global StartTimer
        # Create objects of QHBoxLayout and return a list of them
        TimerLayouts = []
        for each in self.scanForTimers():
            # Create new Instances
            timer: QHBoxLayout = QHBoxLayout()
            class button(QPushButton):
                def __init__(self, seconds, parent=None):
                    super(QPushButton, self).__init__(parent=parent)
                    self.seconds = seconds
                    self.text = "test" # Timers work but the button text doesnt
                    self.clicked.connect(self.start)
                def start(self):
                    print("Start")
                    time.sleep(self.seconds/100)
                    print("Done")
            # Add widgets
            timer.addWidget(QLabel(f'{each["Name"]}: {each["Seconds"]}s'))
            b: button = button(each["Seconds"])
            timer.addWidget(b)
            TimerLayouts.append(timer)
        return TimerLayouts

APP = QApplication([])

MainFrame = MainWindow()
MainFrame.show()

APP.exec()
