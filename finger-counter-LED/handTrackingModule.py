# Importing necessary libraries
import cv2
import mediapipe as mp
import time

class handDetector():
    # Setting up the parameters
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # Gets required methods to detect hand and draw on the frame from the Mediapipe library
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode, 
            max_num_hands=self.maxHands, 
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils
        
    # Defining the functions to detect hand and draw landmarks on the frame
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # Converts the camera image to RGB
        self.results = self.hands.process(imgRGB)                 # detects and process hands in the RGB image
        
        # Checking if any hand was detected
        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:    # Loops and draw points of multiple hands
                if draw:
                    self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)

        return img
    
    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        
        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                myHand = self.results.multi_hand_landmarks[handNo]
                
                for id, lm in enumerate(myHand.landmark):  # Loops and gets each landmark information
                    # Gets the position on the frame of each landmarks
                    h, w, c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    lmList.append([id, cx, cy])
                    
                    if draw:
                        self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)
        
        return lmList
    
def main():
    cap = cv2.VideoCapture(0)   # Turns on the first camera
    cTime, pTime = 0, 0
    detector = handDetector()   # Calling handDetector class to an object called detector

    # Runs an infinite loop
    while True:
        # Reads the camera
        success, img = cap.read()
        
        # Applying necessary methods to detect hands
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if (len(lmList)):
            print(lmList[4])
        
        # Measuring fps
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 3)
        
        # Shows the frame
        cv2.imshow("Image", img)
        cv2.waitKey(1)
    
if __name__ == "__main__":
    main()