from __future__ import print_function
import sys, os
import cv2

cnt = 0
lines = open(sys.argv[1], 'r').readlines()
lines_num = len(lines)
output_file = open(sys.argv[2], 'w')

print("begin ...")
for i, line in enumerate(lines):
	if i % 2 == 0:
		print("{}/{}".format(i, lines_num), end="\r")

	items = line.split()
	if len(items) > 1:
		image = cv2.imread("../../" + items[0])
		l = "{} {} {} {}".format(cnt, items[0], image.shape[1], image.shape[0])

		for item in items[1:]:
			x,y,x2,y2,t = item.split(",")
			if int(x2) >= image.shape[1] or int(y2) >= image.shape[0]:
				l = ""
				break
			else:
				l += " " + " ".join([t, x, y, x2, y2])

		if l:
			output_file.write(l + "\n")
			cnt += 1
