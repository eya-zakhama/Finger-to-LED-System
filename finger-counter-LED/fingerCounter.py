import cv2
import handTrackingModule as htm
import time
import serial

pTime = 0  # Previous time
cam = cv2.VideoCapture(0)   # Turns on the first camera
cam.set(3, 640)             # Sets the width of the frame
cam.set(4, 480)             # Sets the height of the frame

detector = htm.handDetector(detectionCon=0.75)  # Creates an object of handDetector class with a detection confidence of 0.75
tipIDs = [4, 8, 12, 16, 20]  # List of tip IDs for fingers

# Initialize serial connection with error handling
arduinoData = None
try:
    arduinoData = serial.Serial('COM7', 9600)  # Initializes serial communication with Arduino at 9600 baud rate
    time.sleep(2)  # Waits for 2 seconds to establish the connection with Arduino
except serial.SerialException as e:
    print(f"Error: Could not connect to COM7. {e}")
    print("Please check if Arduino is connected and the correct COM port is used.")
    exit()

while True:
    success, img = cam.read()  # Reads the camera
    img = detector.findHands(img)  # Detects hands in the frame
    img = cv2.flip(img, 1)  # Flips the frame horizontally for a mirror effect
    lmList = detector.findPosition(img, draw=False)  # Finds the position of the landmarks in the frame
    
    if (len(lmList)):   # Checks if any hand was detected
        fingers = ""    # Creates an empty list to store the status of fingers
        for id in range(0, 5):
            if not id:  # If the id is 0, it is the thumb
                if lmList[tipIDs[0]][1] > lmList[tipIDs[0] - 1][1]:  # If the tip of the thumb is to the right of the first joint, it is counted as open
                    fingers += "1"  # Thumb is open
                else:
                    fingers += "0"  # Thumb is closed
            elif lmList[tipIDs[id]][2] < lmList[tipIDs[id] - 2][2]: fingers += "1"  # If the tip of the finger is above the second joint, it is counted as open
            else: fingers += "0"                                                 # If the tip of the finger is below the second joint, it is counted as closed
            
        for id, finger in enumerate(fingers):
            if  finger == "1":
                cv2.circle(img, (20+id*35, 50), 15, (0, 255, 0), cv2.FILLED)  # Draws a filled circle at (10, 80) with radius 15 and color red if the finger is open
            else:
                cv2.circle(img, (20+id*35, 50), 15, (0, 0, 255), cv2.FILLED)  # Draws a filled circle at (10, 80) with radius 15 and color red if the finger is closed
        
        arduinoData.write((fingers + '\n').encode())  # Sends the fingers status to Arduino
        print(f"Sent to Arduino: {fingers}")
        time.sleep(0.02)   # Waits for 20 milliseconds to control the frame rate 
            
    cTime = time.time()  # Gets the current time
    fps = 1 / (cTime - pTime)   # Calculates the frames per second
    cv2.putText(img, f"FPS: {int(fps)}", (10, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)  # Displays the fps on the frame
    pTime = cTime               # Updates the previous time
    
    cv2.imshow("Image", img)    # Shows the frame
    cv2.waitKey(1)              # Waits for 1 millisecond