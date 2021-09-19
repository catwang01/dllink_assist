import tool
import time

n = 10
startTime = time.time()
source = None
for i in range(n):
        tool.capture_screenshot()
endTime = time.time()
print("TimeUsed: {}s, avg: {}s".format(endTime - startTime, (endTime-startTime)/n))