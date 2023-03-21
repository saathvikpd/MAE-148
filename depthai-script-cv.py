from roboflowoak import RoboflowOak
import cv2
import time
import numpy as np

if __name__ == '__main__':
    # instantiating an object (rf) with the RoboflowOak module
    rf = RoboflowOak(model="basketball-detection-s1n00", confidence=0.2, overlap=0.05,
    version="1", api_key="2BobK1pwIsrmsOnyp12s", rgb=True,
    depth=True, device=None, blocking=True)
    # Running our model and displaying the video output with detections
    while True:
        t0 = time.time()
        # The rf.detect() function runs the model inference
        result, frame, raw_frame, depth = rf.detect()
        predictions = result["predictions"]
        #{
        #    predictions:
        #    [ {
        #        x: (middle),
        #        y:(middle),
        #        width:
        #        height:
        #        depth: ###->
        #        confidence:
        #        class:
        #        mask: {
        #    ]
        #}
        #frame - frame after preprocs, with predictions
        #raw_frame - original frame from your OAK
        #depth - depth map for raw_frame, center-rectified to the center camera
        
        preds = [p.json() for p in predictions]
        
        bottom = (frame.shape[0] // 2, frame.shape[1])
        
        def dist(p1, p2):
            return (((p1[0] - p2[0])**2) + ((p1[1] - p2[1])**2))**0.5
        
        mean_angle = 0
        if len(preds) >= 1:
            for p in preds:
                x = p['x']
                y = p['y']
                
                cv2.line(frame, (frame.shape[0] // 2, frame.shape[1]), (int(x), int(y)), color = (0, 0, 0), thickness = 1)
                
                adj = frame.shape[1] - y
                hyp = dist((x, y), bottom)
                cos = adj / hyp
                angle = np.arccos(cos)
                if x < bottom[0]:
                    angle = -1 * angle 
                mean_angle += angle
            mean_angle = mean_angle / len(preds)
        
        # timing: for benchmarking purposes
        t = time.time()-t0
        print("INFERENCE TIME IN MS ", 1/t)
        print("PREDICTIONS ", preds)
        
        cv2.line(frame, (frame.shape[0] // 2, frame.shape[1]), (frame.shape[0] // 2, 0), color = (0, 0, 0), thickness = 1)
        
        cv2.putText(frame, str(mean_angle * 180 / np.pi) + " degrees", org = (0, 25), color = (0, 0, 0), fontFace = cv2.FONT_HERSHEY_DUPLEX, fontScale = 0.7, thickness = 1)
        
        # setting parameters for depth calculation
        max_depth = np.amax(depth)
        cv2.imshow("depth", depth/max_depth)
        # displaying the video feed as successive frames
        cv2.imshow("frame", frame)

        # how to close the OAK inference window / stop inference: CTRL+q or CTRL+c
        if cv2.waitKey(1) == ord('q'):
            break