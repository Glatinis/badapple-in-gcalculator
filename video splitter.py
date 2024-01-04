import cv2

vidcap = cv2.VideoCapture("bad apple.mp4")
success, image = vidcap.read()
count = 0

while success:
  cv2.imwrite("frames/frame%d.jpg" % count, image)     # save frame as JPEG file      
  success, image = vidcap.read()
  print("Read frame number: ", count)
  count += 1