import os
import time
from queue import Queue
import logging
from threading import Thread

from matplotlib import pyplot as plt

from log.log import setupLogging

setupLogging()

class SaveImgThread(Thread):

    def __init__(self, queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'SaveImgThread'
        self.queue = queue

    def run(self):
        while True:
            try:
                imgName, img = self.queue.get(timeout=20)
            except Exception:
                break
            plt.imsave(imgName, img[..., -1::-1])
            logging.debug("Img {} saved".format(imgName))
        logging.debug("exit!")

queue = Queue()
SaveImgThread(queue).start()
