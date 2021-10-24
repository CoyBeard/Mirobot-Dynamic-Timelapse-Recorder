from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
from tkinter import filedialog
import os.path



root = Tk()

root.title('Mirobot Dynamic Timelapse GCode Generator')
root.iconbitmap('wlkataiconIcon.ico')
root.geometry('1000x600')
root.configure(background="#d9dade")



#Vars
Photos = 5;                                        #Number of photos
TimelapseLength = 60;                              #Seconds How long the timelapse will record   (TimelapseLength / Photos) - (LongestMovementTime * 2) - PhotoStablizationDelay - PostPhotoDelay - GripperHoldTime - GripperClosingTime  MUST BE > 0
StartPosition = [200, -100, 175, 0, 0, 0]          #X, Y, Z, A, B, C Cordinate where the first photo is taken 
EndPosition = [200, 100, 175, 0, 0, 0]             #X, Y, Z, A, B, C Cordinate where the last photo is taken 
global RestPositionJ1
global RestPositionJ2
global RestPositionJ3
global RestPositionJ4
global RestPositionJ5
global RestPositionJ6
RestPositionJ1 = StringVar()
RestPositionJ2 = StringVar()
RestPositionJ3 = StringVar()
RestPositionJ4 = StringVar()
RestPositionJ5 = StringVar()
RestPositionJ6 = StringVar()
#Set defalt Settings
RestPositionJ1.set(0)                              #J1, J2, J3, J4, J5, J6 Angle Where robot will rest in between Photos
RestPositionJ2.set(-40)
RestPositionJ3.set(60)
RestPositionJ4.set(0)
RestPositionJ5.set(-14)
RestPositionJ6.set(0)
MovementSpeed = 2000                               #0 - 2000 Speed when robot moves to position

#Set Movement Time
#Find LongestMovementTime by running FindLongestMovementTime subtract one second form stopwatch result:
global LongestMovementTime
LongestMovementTime = StringVar()
#Set defalt
LongestMovementTime.set(2.75)                      #Seconds it takes the robot to make its longest movement from rest position, crucial to keep timelapse at set duritation MAKE ACCURATE TO 2 DECIMAL PLACES

#Advanced Settings 
global PhotoStablizationDelay
global GripperHoldTime
global PostPhotoDelay
global GripperClosingTime
PhotoStablizationDelay = StringVar()               #Seconds robot waits before taking the photo so the camra isn't shaking from movement
GripperHoldTime = StringVar()                      #Seconds gripper holds down to trigger photo
PostPhotoDelay = StringVar()                       #Seconds robot waits after trigger photo to return to rest position
GripperClosingTime = StringVar()                   #Seconds it takes to close the gripper 
#Set Defalts
PhotoStablizationDelay.set(2)
GripperHoldTime.set(0.25)
PostPhotoDelay.set(0.5)
GripperClosingTime.set(0.2)



#Math Vars:
StartEndCarttesianDiffrence = [0, 0, 0, 0, 0, 0]    #Diffrence of each cordinates start and end position
global PhotoDelay
PhotoDelay = 0;                                     #Rest period between photos
Photo = 0;                                          #What photo the program is on, starts at photo number 0
XStep = 0;                                          #Distance on X axis travled per photo
YStep = 0;                                          #Distance on Y axis travled per photo
ZStep = 0;                                          #Distance on Z axis travled per photo
AStep = 0;                                          #Distance on A axis travled per photo
BStep = 0;                                          #Distance on B axis travled per photo
CStep = 0;                                          #Distance on C axis travled per photo


global SetProgramName
SetProgramName = StringVar()
#Set Defalt
SetProgramName.set('Set Program Name')
    
global DirectoryChosen
DirectoryChosen = StringVar()
#Set Defalt
DirectoryChosen.set('NULL')

global Version
Version = StringVar()
#Set Defalt
Version.set('V1.0.2')

  
#Exicute FindLongestMovementTime
def FindLongestMovementTime ():
    #Fill All Fields Errer Detection
    if len(StartPositionXEntry.get()) == 0 or len(StartPositionYEntry.get()) == 0 or len(StartPositionZEntry.get()) == 0 or len(StartPositionAEntry.get()) == 0 or len(StartPositionBEntry.get()) == 0 or len(StartPositionCEntry.get()) == 0 or len(EndPositionXEntry.get()) == 0 or len(EndPositionYEntry.get()) == 0 or len(EndPositionZEntry.get()) == 0 or len(EndPositionAEntry.get()) == 0 or len(EndPositionBEntry.get()) == 0 or len(EndPositionCEntry.get()) == 0 or len(RestPositionJ1.get()) == 0 or len(RestPositionJ2.get()) == 0 or len(RestPositionJ3.get()) == 0 or len(RestPositionJ4.get()) == 0 or len(RestPositionJ5.get()) == 0 or len(RestPositionJ6.get()) == 0 or len(PhotosEntry.get()) == 0 or len(TimelapseLengthEntry.get()) == 0 or len(LongestMovementTimeEntry.get()) == 0:
        messagebox.showerror('info', 'Please fill out all fields!')
    else:
        #Destination File Chosen Errer Detection
        if str(DirectoryChosen.get()) == 'NULL':
            messagebox.showerror('info', 'Please chose a destination file!')
        else:    
            #Compile File Name and Address
            completeName = os.path.join(str(folder_selected), str(SetProgramName.get())+'.gcode')
            f = open(completeName, 'w')

            #Write GCode
            
            #Defalt Title Paragraph
            f.write(';File generated by Mirobot Dynamic Timelapse GCode Generator\n')
            f.write(';' + str(Version.get()) + '\n')
            f.write('\n')
            f.write('\n')
            f.write(';Mode: Find Longest Movement Time\n')
            f.write('\n')
            f.write(';READ ME:\n')
            f.write(';This program will run the Mirobot from the chosen rest position\n')
            f.write(';to the chosen start position for the purpose of timing the movement.\n')
            f.write(';This is necessary because there is no direct way to time movements\n')
            f.write(';live in the Mirobot. So in order to to calculate the rest periods we\n')
            f.write(';need to roughly predict this by timing the movement in the real world.\n')
            f.write(';Do to there being no usable inputs and outputs on the Mirobot the\n')
            f.write(';stopwatch can be triggered by the gripper. Run this code and subtract\n')
            f.write(';one second from the results from the timer.\n')
            f.write('\n')
            
            #GCode
            #Home Robot
            f.write(';Home\n')
            f.write('$h\n')
            #Set Feedrate
            f.write('G01 F' + str(MovementSpeedSlider.get()) + '\n')
            f.write('\n')
            #Move to Rest Position
            f.write(';Rest Position\n')
            f.write('M21 G90 G01 ' + 'X' + str(int(float(RestPositionJ1.get()) * 100) / 100) + ' ' + 'Y' + str(int(float(RestPositionJ2.get()) * 100) / 100) + ' ' + 'Z' + str(int(float(RestPositionJ3.get()) * 100) / 100) + ' ' + 'A' + str(int(float(RestPositionJ4.get()) * 100) / 100) + ' ' + 'B' + str(int(float(RestPositionJ5.get()) * 100) / 100) + ' ' + 'C' + str(int(float(RestPositionJ6.get()) * 100) / 100) + '\n')
            f.write('\n')
            #Trigger the Gripper
            f.write(';Trigger Gripper\n')
            f.write('M3S60 M4E65\n')
            #Gripper Hold
            f.write('G4 P' + str(int(float(GripperHoldTime.get()) * 100) / 100) + '\n')
            #Gripper Release
            f.write('M3S40 M4E45\n')
            f.write('\n')
            #Move to Start Position
            f.write(';Start Position\n')
            f.write('M20 G90 G01 ' + 'X' + str(int(float(StartPositionXEntry.get()) * 100) / 100) + ' ' + 'Y' + str(int(float(StartPositionYEntry.get()) * 100) / 100) + ' ' + 'Z' + str(int(float(StartPositionZEntry.get()) * 100) / 100) + ' ' + 'A' + str(int(float(StartPositionAEntry.get()) * 100) / 100) + ' ' + 'B' + str(int(float(StartPositionBEntry.get()) * 100) / 100) + ' ' + 'C' + str(int(float(StartPositionCEntry.get()) * 100) / 100) + '\n')
            f.write('\n')
            #Trigger the Gripper
            f.write(';Trigger Gripper\n')
            f.write('M3S60 M4E65\n')
            #Gripper Hold
            f.write('G4 P' + str(round(float(GripperHoldTime.get()), 2)) + '\n')
            #Gripper Release
            f.write('M3S40 M4E45\n')
            f.write('\n')
            #Move to Rest Position
            f.write(';Return to Rest Position\n')
            f.write('M21 G90 G01 ' + 'X' + str(int(float(RestPositionJ1.get()) * 100) / 100) + ' ' + 'Y' + str(int(float(RestPositionJ2.get()) * 100) / 100) + ' ' + 'Z' + str(int(float(RestPositionJ3.get()) * 100) / 100) + ' ' + 'A' + str(int(float(RestPositionJ4.get()) * 100) / 100) + ' ' + 'B' + str(int(float(RestPositionJ5.get()) * 100) / 100) + ' ' + 'C' + str(int(float(RestPositionJ6.get()) * 100) / 100) + '\n')
            
            
            #Close File
            f.close
            
            #Feedback
            messagebox.showinfo('info', 'File Complete!')
    
    
#Exicute GenerateGCode
def GenerateGCode():
    #Error Messages 
    #Fill All Fields Errer Detection
    if len(StartPositionXEntry.get()) == 0 or len(StartPositionYEntry.get()) == 0 or len(StartPositionZEntry.get()) == 0 or len(StartPositionAEntry.get()) == 0 or len(StartPositionBEntry.get()) == 0 or len(StartPositionCEntry.get()) == 0 or len(EndPositionXEntry.get()) == 0 or len(EndPositionYEntry.get()) == 0 or len(EndPositionZEntry.get()) == 0 or len(EndPositionAEntry.get()) == 0 or len(EndPositionBEntry.get()) == 0 or len(EndPositionCEntry.get()) == 0 or len(RestPositionJ1.get()) == 0 or len(RestPositionJ2.get()) == 0 or len(RestPositionJ3.get()) == 0 or len(RestPositionJ4.get()) == 0 or len(RestPositionJ5.get()) == 0 or len(RestPositionJ6.get()) == 0 or len(PhotosEntry.get()) == 0 or len(TimelapseLengthEntry.get()) == 0 or len(LongestMovementTimeEntry.get()) == 0:
        messagebox.showerror('info', 'Please fill out all fields!')
    else:
        #Calculate Rest Period Time Errer Detection
        PhotoDelay = (float(TimelapseLengthEntry.get()) / int(PhotosEntry.get())) - float(PhotoStablizationDelay.get()) - (float(LongestMovementTimeEntry.get()) * 2) - float(PostPhotoDelay.get()) - float(GripperHoldTime.get()) - float(GripperClosingTime.get())

        #Negitive Rest Periods Errer Detection
        if PhotoDelay <= 0:
            messagebox.showerror('info', 'Mirobot has negitive rest periods!')
        else:
            #Destination File Chosen Errer Detection
            if str(DirectoryChosen.get()) == 'NULL':
                messagebox.showerror('info', 'Please chose a destination file!')
            else:
                #One Time Calculations:
                StartEndCarttesianDiffrence[0] = float(EndPositionXEntry.get()) - float(StartPositionXEntry.get()) #X
                StartEndCarttesianDiffrence[1] = float(EndPositionYEntry.get()) - float(StartPositionYEntry.get()) #Y
                StartEndCarttesianDiffrence[2] = float(EndPositionZEntry.get()) - float(StartPositionZEntry.get()) #Z
                StartEndCarttesianDiffrence[3] = float(EndPositionAEntry.get()) - float(StartPositionAEntry.get()) #A
                StartEndCarttesianDiffrence[4] = float(EndPositionBEntry.get()) - float(StartPositionBEntry.get()) #B
                StartEndCarttesianDiffrence[5] = float(EndPositionCEntry.get()) - float(StartPositionCEntry.get()) #C

                XStep = StartEndCarttesianDiffrence[0] / (int(PhotosEntry.get()) - int(1)) #X
                YStep = StartEndCarttesianDiffrence[1] / (int(PhotosEntry.get()) - int(1)) #Y
                ZStep = StartEndCarttesianDiffrence[2] / (int(PhotosEntry.get()) - int(1)) #Z
                AStep = StartEndCarttesianDiffrence[3] / (int(PhotosEntry.get()) - int(1)) #A
                BStep = StartEndCarttesianDiffrence[4] / (int(PhotosEntry.get()) - int(1)) #B
                CStep = StartEndCarttesianDiffrence[5] / (int(PhotosEntry.get()) - int(1)) #C
                
                

                #Compile File Name and Address
                completeName = os.path.join(str(folder_selected), str(SetProgramName.get())+'.gcode')
                f = open(completeName, 'w')

                #Write GCode
                    
                #Defalt Title Paragraph
                f.write(';File generated by Mirobot Dynamic Timelapse GCode Generator\n')
                f.write(';' + str(Version.get()) + '\n')
                f.write('\n')
                f.write('\n')
                f.write(';Mode: Timelapse\n')
                f.write('\n')
                f.write(';READ ME:\n')
                f.write(';The Mirobot has been programed to take a photo by closing and\n')
                f.write(';opening the gripper. The idea is that the gripper activates some\n')
                f.write(';sort of trigger that takes the photo from a diffrent system\n')
                
                #GCode
                f.write('\n')
                #Home the Robot
                f.write(';Home\n')
                f.write('$h\n')
                #Set Feedrate
                f.write('G01 F' + str(MovementSpeedSlider.get()) + '\n')
                f.write('\n')

                #Keep Track of the Current Photo Being Taken for Positoning Reasons
                CurrentPhoto = 0
                
                for count in range(int(PhotosEntry.get())): #Repeat for how many photos
                    #Start at Rest Position
                    f.write(';Rest Position\n')
                    f.write('M21 G90 G01 ' + 'X' + str(int(float(RestPositionJ1.get()) * 100) / 100) + ' ' + 'Y' + str(int(float(RestPositionJ2.get()) * 100) / 100) + ' ' + 'Z' + str(int(float(RestPositionJ3.get()) * 100) / 100) + ' ' + 'A' + str(int(float(RestPositionJ4.get()) * 100) / 100) + ' ' + 'B' + str(int(float(RestPositionJ5.get()) * 100) / 100) + ' ' + 'C' + str(int(float(RestPositionJ6.get()) * 100) / 100) + '\n')
                    f.write('\n')
                    #Pause Untill Timing is Good for Photo
                    f.write(';Time of Rest\n')
                    f.write('G4 P' + str(int(float(PhotoDelay) * 100) / 100) + '\n')
                    f.write('\n')     
                    #Move to Photo Position
                    f.write(';Photo Position\n')
                    f.write('M20 G90 G01 ' + 'X' + str((int(float(StartPositionXEntry.get()) * 100) / 100) + ((int(float(XStep) * 100) / 100) * int(CurrentPhoto))) + ' ' + 
                                             'Y' + str((int(float(StartPositionYEntry.get()) * 100) / 100) + ((int(float(YStep) * 100) / 100) * int(CurrentPhoto))) + ' ' + 
                                             'Z' + str((int(float(StartPositionZEntry.get()) * 100) / 100) + ((int(float(ZStep) * 100) / 100) * int(CurrentPhoto))) + ' ' + 
                                             'A' + str((int(float(StartPositionAEntry.get()) * 100) / 100) + ((int(float(AStep) * 100) / 100) * int(CurrentPhoto))) + ' ' + 
                                             'B' + str((int(float(StartPositionBEntry.get()) * 100) / 100) + ((int(float(BStep) * 100) / 100) * int(CurrentPhoto))) + ' ' + 
                                             'C' + str((int(float(StartPositionCEntry.get()) * 100) / 100) + ((int(float(CStep) * 100) / 100) * int(CurrentPhoto))) + '\n')
                    f.write('\n')
                    #Let Camra Steady
                    f.write(';Wait for arm to stop shaking before camra takes photo\n')
                    f.write('G4 P' + str(int(float(PhotoStablizationDelay.get()) * 100) / 100) + '\n')
                    f.write('\n')
                    #Take Photo
                    f.write(';Take Photo\n')
                    f.write('M3S60 M4E65\n')
                    f.write('G4 P' + str(int(float(GripperHoldTime.get()) * 100) / 100) + '\n')
                    f.write('M3S40 M4E45\n')
                    f.write('\n')
                    #Small Delay After Photo
                    f.write(';Small delay after photo\n')
                    f.write('G4 P' + str(int(float(PostPhotoDelay.get()) * 100) / 100) + '\n')
                    f.write('\n')
                    
                    #Keep track of what photo the robot is on
                    CurrentPhoto = CurrentPhoto + 1
                    
                    
                #End at rest position
                f.write('\n')
                f.write(';End in rest position\n')
                f.write('M21 G90 G01 ' + 'X' + str(int(float(RestPositionJ1.get()) * 100) / 100) + ' ' + 'Y' + str(int(float(RestPositionJ2.get()) * 100) / 100) + ' ' + 'Z' + str(int(float(RestPositionJ3.get()) * 100) / 100) + ' ' + 'A' + str(int(float(RestPositionJ4.get()) * 100) / 100) + ' ' + 'B' + str(int(float(RestPositionJ5.get()) * 100) / 100) + ' ' + 'C' + str(int(float(RestPositionJ6.get()) * 100) / 100) + '\n')
                    
                #Close File
                f.close
                
                #Feedback
                messagebox.showinfo('info', 'File Complete!')
    
#Exicute Change_Export_Destination Setting
def Change_Export_Destination():
    global folder_selected
    folder_selected = filedialog.askdirectory()
    print(folder_selected)
    
    
    #Show File Destination on Main Window
    FileDestinationLabel = Label(root, text= 'File Destination: ' + folder_selected, width = 108, height= 1,font= ('Arial', 12))
    FileDestinationLabel.place(x=10, y=540)
    
    #Bolian
    DirectoryChosen.set('Chosen')
  
    
#Exicute Info
def Info ():
    #Show Program Verson
    messagebox.showinfo('info', str(Version.get()))
    
#Exicute Advanced_Settings
def Advanced_Settings():
    #Window Perameters
    AdvancedSettings = Toplevel()
    AdvancedSettings.title('Advanced Settings')
    AdvancedSettings.iconbitmap('wlkataiconIcon.ico')
    AdvancedSettings.geometry('400x400')
        
    #Exicute Restore to defalt Settings 
    def RestoreDefalts ():
        PhotoStablizationDelay.set(2)
        GripperHoldTime.set(0.25)
        PostPhotoDelay.set(0.5)
        GripperClosingTime.set(0.2)
    
    
    #Buttons
    #Photo Stablization Delay
    PhotoStablizationDelayLabel = Label(AdvancedSettings, text= 'Photo Stablization Delay ', font= ('Arial', 12))
    PhotoStablizationDelayLabel.place(x=15, y= 30, anchor='w')

    PhotoStablizationDelayEntry = Entry(AdvancedSettings, width = 10, fg = 'black', font= ('Arial', 12), textvariable = PhotoStablizationDelay)
    PhotoStablizationDelayEntry.place(x=230, y= 30, anchor='w')
    
    
    #Gripper Hold Time
    GripperHoldTimeLabel = Label(AdvancedSettings, text= 'Gripper Hold Time ', font= ('Arial', 12))
    GripperHoldTimeLabel.place(x=15, y= 65, anchor='w')

    GripperHoldTimeEntry = Entry(AdvancedSettings, width = 10, fg = 'black', font= ('Arial', 12), textvariable = GripperHoldTime)
    GripperHoldTimeEntry.place(x=230, y= 65, anchor='w')
    
    
    #Post Photo Delay
    PostPhotoDelayLabel = Label(AdvancedSettings, text= 'Post Photo Delay ', font= ('Arial', 12))
    PostPhotoDelayLabel.place(x=15, y= 100, anchor='w')

    PostPhotoDelayEntry = Entry(AdvancedSettings, width = 10, fg = 'black', font= ('Arial', 12), textvariable = PostPhotoDelay)
    PostPhotoDelayEntry.place(x=230, y= 100, anchor='w')
    
    
    #Gripper Closing Time
    GripperClosingTimeLabel = Label(AdvancedSettings, text= 'Gripper Closing Time ', font= ('Arial', 12))
    GripperClosingTimeLabel.place(x=15, y= 135, anchor='w')

    GripperClosingTimeEntry = Entry(AdvancedSettings, width = 10, fg = 'black', font= ('Arial', 12), textvariable = GripperClosingTime)
    GripperClosingTimeEntry.place(x=230, y= 135, anchor='w')


    #Restore Defalts
    CancelButton = Button(AdvancedSettings, text='Restore Defalts', command= RestoreDefalts)
    CancelButton.place(x=90, y= 300, anchor='w')


    #Save and Close (Settings are Saved Once Changed)
    CancelButton = Button(AdvancedSettings, text='Save and Close', command= AdvancedSettings.destroy)
    CancelButton.place(x=190, y= 300, anchor='w')
    
    


#Top Menu
my_menu = Menu(root)
root.config(menu = my_menu)

#File Menu (1)
file_menu = Menu(my_menu, tearoff= 0)
my_menu.add_cascade(label = 'File', menu = file_menu)
file_menu.add_command(label= 'Change Export Destination', command= Change_Export_Destination)


#Settings Menu (2)
settings_menu = Menu(my_menu, tearoff= 0)
my_menu.add_cascade(label= 'Settings', menu = settings_menu)
settings_menu.add_command(label = 'Advanced Settings', command= Advanced_Settings)


#Help Menu (3)
Help_menu = Menu(my_menu, tearoff= 0)
my_menu.add_cascade(label= 'Help', menu = Help_menu)
Help_menu.add_command(label = 'About', command= Info)

Help_menu.add_command(label = 'Exit', command= root.destroy)


#Home Page Settings
#Photos
PhotosLabel = Label(root, text= 'Photos (#) ', font= ('Arial', 15))
PhotosLabel.place(x=15, y= 30, anchor='w')

PhotosEntry = Entry(root, width = 10, fg = 'black', font= ('Arial', 15))
PhotosEntry.place(x=325, y= 30, anchor='w')

#Timelapse Length
TimelapseLengthLabel = Label(root, text= 'Timelapse Length (Sec)', font= ('Arial', 15))
TimelapseLengthLabel.place(x=15, y= 65, anchor='w')

TimelapseLengthEntry = Entry(root, width = 10, fg = 'black', font= ('Arial', 15))
TimelapseLengthEntry.place(x=325, y= 65, anchor='w')

#Start Position
StartPositionLabel = Label(root, text= 'Start Position (X,Y,Z,A,B,C) ', font= ('Arial', 15))
StartPositionLabel.place(x=15, y= 100, anchor='w')

#X
StartPositionXEntry = Entry(root, width = 3, fg = 'black', font= ('Arial', 15))
StartPositionXEntry.place(x=325, y= 100, anchor='w')

#Y
StartPositionYEntry = Entry(root, width = 3, fg = 'black', font= ('Arial', 15))
StartPositionYEntry.place(x=365, y= 100, anchor='w')

#Z
StartPositionZEntry = Entry(root, width = 3, fg = 'black', font= ('Arial', 15))
StartPositionZEntry.place(x=405, y= 100, anchor='w')

#A
StartPositionAEntry = Entry(root, width = 3, fg = 'black', font= ('Arial', 15))
StartPositionAEntry.place(x=445, y= 100, anchor='w')

#B
StartPositionBEntry = Entry(root, width = 3, fg = 'black', font= ('Arial', 15))
StartPositionBEntry.place(x=485, y= 100, anchor='w')

#C
StartPositionCEntry = Entry(root, width = 3, fg = 'black', font= ('Arial', 15))
StartPositionCEntry.place(x=525, y= 100, anchor='w')


#End Position
EndPositionLabel = Label(root, text= 'End Position (X,Y,Z,A,B,C) ', font= ('Arial', 15))
EndPositionLabel.place(x=15, y= 135, anchor='w')

#X
EndPositionXEntry = Entry(root, width = 3, fg = 'black', font= ('Arial', 15))
EndPositionXEntry.place(x=325, y= 135, anchor='w')

#Y
EndPositionYEntry = Entry(root, width = 3, fg = 'black', font= ('Arial', 15))
EndPositionYEntry.place(x=365, y= 135, anchor='w')

#Z
EndPositionZEntry = Entry(root, width = 3, fg = 'black', font= ('Arial', 15))
EndPositionZEntry.place(x=405, y= 135, anchor='w')

#A
EndPositionAEntry = Entry(root, width = 3, fg = 'black', font= ('Arial', 15))
EndPositionAEntry.place(x=445, y= 135, anchor='w')

#B
EndPositionBEntry = Entry(root, width = 3, fg = 'black', font= ('Arial', 15))
EndPositionBEntry.place(x=485, y= 135, anchor='w')

#C
EndPositionCEntry = Entry(root, width = 3, fg = 'black', font= ('Arial', 15))
EndPositionCEntry.place(x=525, y= 135, anchor='w')


#Rest Position
RestPositionLabel = Label(root, text= 'Rest Position (J1,J2,J3,J4,J5,J6) ', font= ('Arial', 15))
RestPositionLabel.place(x=15, y= 170, anchor='w')

#X
RestPositionXEntry = Entry(root, width = 3, fg = 'black', textvariable= RestPositionJ1, font= ('Arial', 15))
RestPositionXEntry.place(x=325, y= 170, anchor='w')

#Y
RestPositionYEntry = Entry(root, width = 3, fg = 'black', textvariable= RestPositionJ2, font= ('Arial', 15))
RestPositionYEntry.place(x=365, y= 170, anchor='w')

#Z
RestPositionZEntry = Entry(root, width = 3, fg = 'black', textvariable= RestPositionJ3, font= ('Arial', 15))
RestPositionZEntry.place(x=405, y= 170, anchor='w')

#A
RestPositionAEntry = Entry(root, width = 3, fg = 'black', textvariable= RestPositionJ4, font= ('Arial', 15))
RestPositionAEntry.place(x=445, y= 170, anchor='w')

#B
RestPositionBEntry = Entry(root, width = 3, fg = 'black', textvariable= RestPositionJ5, font= ('Arial', 15))
RestPositionBEntry.place(x=485, y= 170, anchor='w')

#C
RestPositionCEntry = Entry(root, width = 3, fg = 'black', textvariable= RestPositionJ6, font= ('Arial', 15))
RestPositionCEntry.place(x=525, y= 170, anchor='w')


#Movement Speed
MovementSpeedLabel = Label(root, text= 'Movement Speed ', font= ('Arial', 15))
MovementSpeedLabel.place(x=15, y= 235, anchor='w')

MovementSpeedSlider = Scale(root, from_ = 0, to = 2000, orient= HORIZONTAL ,length=230)
MovementSpeedSlider.set(2000)
MovementSpeedSlider.place(x=225, y=215)

#Mirobot Logo Image
MirobotLogoImage = ImageTk.PhotoImage(Image.open('WlkataLogo.png'))
label = Label(root, image = MirobotLogoImage )
label.place(x=15, y=350)


#Set Program Name
SetProgramNameEntry= Entry(root, width = 40, textvariable = SetProgramName, fg = 'black', font= ('Arial', 15))
SetProgramNameEntry.place(x=15, y=290)

#File Destination
FileDestinationLabel = Label(root, text= 'Chose File to set File Destination', width = 108, height= 1,font= ('Arial', 12))
FileDestinationLabel.place(x=10, y=540)



#Right Hand Pannel
panel_1= PanedWindow(bd = 4, relief= 'sunken', bg = '#d9dade')
panel_1.place(x=575, y=25, width = 400, height= 500)


#Longest Movement Time
LongestMovementTimeLabel = Label(root, text= 'Longest Movement Time ', font= ('Arial', 15))
LongestMovementTimeLabel.place(x=665, y= 65, anchor='w')

LongestMovementTimeEntry = Entry(root, width = 20, fg = 'black', font= ('Arial', 15), textvariable= LongestMovementTime)
LongestMovementTimeEntry.place(x=665, y= 105, anchor='w')


#Longest Movement Time Description
message ='''    The Longest Movement Time
is the seconds it takes the robot
to make its longest movement from
rest position, crucial to keep 
timelapse at set duritation MAKE 
ACCURATE TO 2 DECIMAL PLACES
    Find Longest Movement Time by
running "Find Longest Movement 
Time" subtract one second form 
stopwatch result
 '''

text_box = Text(root,height=10,width=33,)
text_box.place(x = 640, y = 130 )
text_box.insert('end', message)
text_box.config(state='disabled')


#Find Longest Movement Time
FindLongestMovementTimeButton = Button (root, text='Find Longest Movement Time', command= FindLongestMovementTime, font= ('Arial', 15), bg= '#48b1b5')
FindLongestMovementTimeButton.place(x= 640, y= 315, width= 275, height= 75)


#Generate GCode
FindLongestMovementTimeButton = Button (root, text='Generate GCode', command= GenerateGCode, font= ('Arial', 15), bg= '#ce5912')
FindLongestMovementTimeButton.place(x= 640, y= 415, width= 275, height= 75)


mainloop()