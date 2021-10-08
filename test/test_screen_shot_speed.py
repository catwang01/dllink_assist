import sys
import os
thisFile = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname(thisFile)))
import tool
import time

class TestSpeed:
        def test_speed(self):
                n = 10
                startTime = time.time()
                for i in range(n):
                        tool.capture_screenshot()
                endTime = time.time()
                avgTime = (endTime-startTime) / n
                # print(f"TimeUsed: {endTime - startTime}s, avg: {avgTime}s")
                assert avgTime < 2