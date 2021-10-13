import os
from queue import Queue, Empty
import logging
import threading

from matplotlib import pyplot as plt
from const import MAX_IMAGE_SIZE

from log.log import setupLogging

setupLogging()

class SaveImgThread(threading.Thread):

    def __init__(self, queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'SaveImgThread'
        self.queue = queue

    def run(self):
        while True:
            try:
                imgName, img = self.queue.get(timeout=20)
            except Empty:
                if not threading.main_thread().is_alive():
                    break
            else:
                images = os.listdir('collectImgs')
                if len(images) >= MAX_IMAGE_SIZE:
                    logging.info("Deleting images files!")
                    for imageName in images:
                        os.remove(os.path.join('collectImgs', imageName))
                plt.imsave(imgName, img[..., -1::-1])
                logging.info("Img {} saved".format(imgName))
        # print(f"{self.name} exit!")

queue = Queue()
SaveImgThread(queue).start()
