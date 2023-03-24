import cv2
import depthai as dai
import numpy as np

# Create pipeline
pipeline = dai.Pipeline()

# Define source and output
camRgb = pipeline.create(dai.node.ColorCamera)
xoutRgb = pipeline.create(dai.node.XLinkOut)

xoutRgb.setStreamName("rgb")

# Properties
camRgb.setPreviewSize(300, 300)
camRgb.setInterleaved(False)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

# Linking
camRgb.preview.link(xoutRgb.input)

# min max values, only if you satisfy all will you be displayed
rgbRange = np.loadtxt('rgbRange')#[[40, 100], [20, 150], [200, 255]]
change1 = 0
change2 = 0
font = cv2.FONT_HERSHEY_SIMPLEX
fcol = (255, 255, 255)

def limitColor(img):
    rgbMin, rgbMax = np.array(rgbRange).T
    barr = ((rgbMin <= img) & (img <= rgbMax)).all(axis=2)
    barr = np.repeat(barr, 3).reshape(img.shape)
    return np.uint8(np.where(barr, 255, 0))

def blur(img):
    k = np.ones((5,5)) / 25
    return cv2.filter2D(src=img, ddepth=-1, kernel=k)


def componen(img):
    w, h, d = img.shape
    img2 = np.uint8(img[:,:,0])
    return cv2.connectedComponentsWithStats(img2)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:
    qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)

    while True:
        inRgb = qRgb.get()  
        raw = inRgb.getCvFrame()

        # limit rgb values, output black and white
        rgbLim = (limitColor(raw))

        # get connected components from bw image
        n, labels, stats, centroid = componen(rgbLim)
        
        lArea, lInd = -1, 0
        for i in range(n):
            
            # skip the large black patch
            upLeft = stats[i][0] == stats[i][1] and stats[i][0] == 0
            botRight = stats[i][2] == stats[i][3] and stats[i][2] == 300
            if upLeft and botRight:
                continue

            # skip this white patch if its too small
            if stats[i][4] <= 250:
                continue
            
            
            if (stats[i][4] > lArea):
                lArea = stats[i][4]
                lInd = i

        if (lArea > 0):
            # draw the bounding box around the largest white
            x, y, w, h, a = stats[lInd]
            rgbLim = cv2.rectangle(rgbLim, (x,y), (x+w,y+h), (0,0,255), 2)

            # calculate steering angle
            x, y = centroid[lInd]
            steer = (np.arctan((300-y)/(x-150)) * 180 / np.pi + 180) % 180
            print("Steer:", steer)
        

        # display the text rgbRanges we work with
        rgbLimText = cv2.putText(rgbLim, str(rgbRange), (25,25), font, 0.4, fcol, 1, cv2.LINE_AA)

        # output img
        frameOut = np.hstack((raw, rgbLim))
        cv2.imshow("rgb", frameOut)

    
        # setup keyboard presses
        key = cv2.waitKey(1)
        if key == ord('a'):
            change1 = (change1+2)%3
        elif key == ord('d'):
            change1 = (change1+1)%3
        elif key == ord('q') or key == ord('e'):
            change2 = (change2+1)%2
        elif key == ord('w'):
            rgbRange[change1][change2] += 5
        elif key == ord('s'):
            rgbRange[change1][change2] -= 5
        elif key == 27:
            break

np.savetxt('rgbRange', rgbRange)
