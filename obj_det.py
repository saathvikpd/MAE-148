import cv2
import numpy as np

def dist(p1, p2):
    return (((p1[0] - p2[0])**2) + ((p1[1] - p2[1])**2))**0.5

vid = cv2.VideoCapture(0)
    
while True:
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
#     _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
#     # using a findContours() function
#     contours, _ = cv2.findContours(
#         threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
# #     smoother = 5
# #     for contour in contours[1:]:
# #         for i in range(contour.shape[0] - smoother):
# #             cv2.line(gray, contour[i, 0, :], contour[i + smoother, 0, :], (255, 0, 0), 1)
            
    

#     for contour in contours[1:]:
        
#         approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
#         if len(approx) > 6:

#             M = cv2.moments(contour)
#             if M['m00'] != 0.0:
#                 x = int(M['m10'] / M['m00'])
#                 y = int(M['m01'] / M['m00'])
                
#                 color = frame[y, x, :]
#                 print(color)
    
#             r_low, r_high = 200, 255
#             g_low, g_high = 50, 150
#             b_low, b_high = 20, 100
#             if (r_low <= color[2] <= r_high) and (g_low <= color[1] <= g_high) and (b_low <= color[1] <= b_high):
#                 print('orange')
#                 cv2.drawContours(frame, [contour], 0, (0, 128, 255), 5)

    # #             dists = []
    # #             for pt in contour:
    # #                 dists.append(dist(pt[0, :], (x, y)))
    # #             dists = np.array(dists)
    # #             if np.isclose(0, dists - dists.mean()).all():
    
            
#             cv2.putText(frame, 'o', (x, y),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)


    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 30, param1 = 25, param2 = 75, minRadius = 20, maxRadius = 80)
  
    if circles is not None:
  
        # Convert the circle parameters a, b and r to integers.
        circles = np.uint16(np.around(circles))

        for pt in circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            # Draw the circumference of the circle.
            
            samp_rads = np.random.uniform(0, r, 5).astype(int)
            print(samp_rads)
            
            try:
                tally = 0
                for rad in samp_rads:
                    samp_point = (a, b + rad)
                    color = frame[samp_point[1], samp_point[0], :]

        #             cv2.circle(frame, (a, b), r, (255, 255, 255), 2)
                    r_low, r_high = 155, 255
                    g_low, g_high = 50, 150
                    b_low, b_high = 0, 100

                    if (r_low < color[2] < r_high) and (g_low < color[1] < g_high) and (b_low < color[1] < b_high):
                        tally += 1
                if tally == 5:
                    cv2.circle(frame, (a, b), r, (255, 255, 255), 2)
            except:
                print('out of bounds')
    
    
    
    # Display the resulting frame
    
#     color = cv2.cvtColor(, cv2.COLOR_GRAY2BGR)
    
    cv2.imshow('frame', frame)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
