# import the necessary packages
from threading import Thread
import sys
import cv2
from queue import Queue
import time


class FileVideoStream:
	def __init__(self, queueSize=512):
		# initialize the file video stream along with the boolean
		# used to indicate if the thread should be stopped or not
		self.stream = cv2.VideoCapture('video/hightway.mp4')
		# self.stream.set(3,1920) #set frame width
		# self.stream.set(4,1080) #set frame height
		# self.stream.set(cv2.CAP_PROP_FPS, 24) #adjusting fps to 5
		self.stopped = False
		(self.grabbed, self.frame) = self.stream.read()
		# initialize the queue used to store frames read from
		# the video file
		self.Q = Queue(maxsize=queueSize)

	def start(self):
		# start a thread to read frames from the file video stream
		t = Thread(target=self.update, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
		count = 0
		# keep looping infinitely
		while True:
			# if the thread indicator variable is set, stop the
			# thread
			if self.stopped:
				return
			# read the next frame from the file
			# start_time = time.time()
			(grabbed, frame) = self.stream.read()
			# end_time = time.time()
			# if count%1000 == 0:
			# 	print("Read FPS : ", 1/(end_time-start_time))
			self.grabbed, self.frame = grabbed, frame
			# if the `grabbed` boolean is `False`, then we have
			# reached the end of the video file
			if not self.grabbed:
				self.stop()
				return
			# otherwise, ensure the queue has room in it
			if not self.Q.full():					
				# add the frame to the queue
				if count%30 == 1 or count%30 == 11 or count%30 == 21:
					if self.frame is not None:
						self.Q.put(self.frame)
				count += 1
			else :
				with self.Q.mutex:
					self.Q.queue.clear()
				if self.frame is not None:
					self.Q.put(self.frame)

	def read(self):
		# return next frame in the queue
		if self.Q.empty():
			return None
		frame = self.Q.get()
		if self.frame is not None:
			return frame
		else:
			print("restart")
			self.stopped = True
			self.stream = cv2.VideoCapture('rtsp://192.168.24.1')
			# time.sleep(400)
			self.stopped = False
			return frame


	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True