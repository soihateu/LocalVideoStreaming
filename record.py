import cv2
import numpy as np
import pyautogui

# define the codec and create VideoWriter Object
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output.avi", fourcc, 20.0, (1920, 1080))

while True:
    # make a screenshot
    ss = pyautogui.screenshot()
    # convert these pixels to a proper numpy array to work with OpenCV
    frame = np.array(ss)
    # convert colors from BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # write the frame
    out.write(frame)
    
# make sure everything is closed when exited
cv2.destroyAllWindows()
out.release()
