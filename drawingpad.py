import cv2 as cv
import numpy as np
def nothing(x):
	pass

video = cv.VideoCapture(0)	
cv.namedWindow("Drawing_pad")
cv.namedWindow("hsv")
cv.createTrackbar("hl","hsv",0,360,nothing)
cv.createTrackbar("sl","hsv",0,255,nothing)
cv.createTrackbar("vl","hsv",0,255,nothing)
cv.createTrackbar("hu","hsv",0,360,nothing)
cv.createTrackbar("su","hsv",0,255,nothing)
cv.createTrackbar("vu","hsv",0,255,nothing)
cv.createTrackbar("pen-B","Drawing_pad",0,255,nothing)
cv.createTrackbar("pen-G","Drawing_pad",0,255,nothing)
cv.createTrackbar("pen-R","Drawing_pad",0,255,nothing)
cv.createTrackbar("clear","Drawing_pad",0,1,nothing)
img = np.zeros((500,700,3),np.uint8)
img[:] = [255,255,255]
initialx = 0
initialy = 0
while(True):
	r,frame =video.read()
	hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
	hl = cv.getTrackbarPos("hl","hsv")
	sl = cv.getTrackbarPos("sl","hsv")
	vl = cv.getTrackbarPos("vl","hsv")
	hu = cv.getTrackbarPos("hu","hsv")
	su = cv.getTrackbarPos("su","hsv")
	vu = cv.getTrackbarPos("vu","hsv")
	rl = np.array([hl,sl,vl])
	ru = np.array([hu,su,vu])
	maskr = cv.inRange(hsv,rl,ru)
	trackg = cv.bitwise_and(frame,frame,mask =maskr)
	cv.imshow("hsv",trackg)
	k = cv.waitKey(1)
	if k == 27:
		break

print(rl)
print(ru)

while(True):
	
	pb = cv.getTrackbarPos("pen-B","Drawing_pad")
	pg = cv.getTrackbarPos("pen-G","Drawing_pad")
	pr = cv.getTrackbarPos("pen-R","Drawing_pad")
	clear = cv.getTrackbarPos("clear","Drawing_pad")
	
	r,frame =video.read()
	H,W = frame.shape[:2]
	frame = cv.resize(frame,(2*W,2*H),interpolation = cv.INTER_LINEAR)
	hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
	#rl = np.array([50,100,100])
	#ru = np.array([131,255,255])
	maskr = cv.inRange(hsv,rl,ru)
	trackg = cv.bitwise_and(frame,frame,mask =maskr)
	gray = cv.cvtColor(trackg,cv.COLOR_BGR2GRAY)
	ret,thr = cv.threshold(gray,0,255,cv.THRESH_BINARY)
	thr = cv.medianBlur(thr,5)
	con,her = cv.findContours(thr,1,cv.CHAIN_APPROX_SIMPLE)
	try:
		(x,y),rad = cv.minEnclosingCircle(con[-1])
	except:
		cv.imshow("final",frame)
		initialx = 0
		initialy = 0
		k = cv.waitKey(1)
		if k == 27:
			break
			break
		continue
	center = (int(x),int(y))
	rad = int(rad)
	print(rad)
	if rad > 9:
		frame= cv.circle(frame,center,rad,(0,255,0),2)
	cv.imshow("final",frame)
	if rad > 9:
		if initialx != 0 and initialy != 0:
			img =cv.line(img,(int(initialx),int(initialy)),center,(pb,pg,pr),3)
			initialx = center[0]
			initialy = center[1]
		if initialx == 0 and initialy == 0:
			initialx = center[0]
			initialy = center[1]
			#print(initialx)
			#print(initialy)
		
	cv.imshow("Drawing_pad",img)
	if clear == 1:
		img = np.zeros((500,700,3),np.uint8)
		img[:] = [255,255,255]
		initialx = 0
		initialy = 0
	#cv.imshow("final",frame)
	k = cv.waitKey(1)
	if k == 27:
		break


cv.destroyAllWindows()
"""
img1 = cv.imread('/home/sushlok/Desktop/red_bottle_cap_aih.jpg',1)
#H,W = imgk.shape[:2]
#img1 = cv.resize(imgk,(int(H/2),int(W/2)),interpolation = cv.INTER_LINEAR)
hsv =cv.cvtColor(img1,cv.COLOR_BGR2HSV)
cv.imshow("Display window", img1)
k = cv.waitKey(0)
rl = np.array([0,100,166])
ru = np.array([356,255,255])
maskr = cv.inRange(hsv,rl,ru)
trackg = cv.bitwise_and(img1,img1,mask =maskr)
gray = cv.cvtColor(trackg,cv.COLOR_BGR2GRAY)
ret,thr = cv.threshold(gray,0,255,cv.THRESH_BINARY)
thr = cv.medianBlur(thr,5)
cv.imshow("final",thr)
k = cv.waitKey(0)
con,her = cv.findContours(thr,1,cv.CHAIN_APPROX_SIMPLE)
(x,y),rad = cv.minEnclosingCircle(con[-1])
center = (int(x),int(y))
rad = int(rad)
img = cv.circle(img1,center,rad,(0,255,0),2)
cv.imshow("final",img)
k = cv.waitKey(0)
print(center)
"""
