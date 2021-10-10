'''
Author: your name
Date: 2021-02-21 02:27:24
LastEditTime: 2021-03-07 04:28:43
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: findpic.py
'''

import random
import time
import inspect
import numpy as np
import matplotlib.pyplot as plt
import pyautogui
import pymouse
import cv2 as cv
import logging
import time
import subprocess
import os
import functools
import tool
from const import APP_SCREEN_HEIGHT, APP_HEIGHT, APP_WIDTH, APP_SCREEN_WIDTH, SCREEN_SAMPLE_RATE
import save_image

template = None

class TimerInnerStream:

    def __init__(self, func) -> None:
        self.func = func

    def write(self, *args, **kwargs):
        self.func(*args, **kwargs)

class Timer:

    def __init__(self, desc="Timer", stdout=None):
        self.desc = desc
        self.start = 0
        self.stdout = None
        if stdout:
            if callable(stdout):
                stdout = TimerInnerStream(stdout)
            self.stdout = stdout
        
    def __enter__(self):
        self.stdout.write("{} start!".format(self.desc))
        self.start = time.time()
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stdout.write("{} end! Time used: {}s".format(self.desc, time.time() - self.start))

def sleep(t):
    logging.debug(f'Sleep for {t}s')
    time.sleep(t)

def formatTime(timestamp=None):
    if timestamp is None:
        timestamp = time.time()
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

def getNparam(func):
    return len(inspect.signature(func).parameters)

def isValidAPPPoint(point):
    return 0 <= point[0] <= APP_WIDTH and 0 <= point[1] <= APP_HEIGHT

def move(position, xy):
    x, y = xy
    position = [
                (position[0][0] + x * 2, position[0][1] + y* 2),
                (position[1][0] + x * 2, position[1][1] + y * 2),
                ]
    return position

def getShotAtPosition(img, position, width=50):
    return img[position[1]-width:position[1]+width, position[0]-width:position[0]+width]

class HashableNdArray:

    def __init__(self, array) -> None:
        self.array = array

    def __hash__(self):
        return int(self.array.sum())

    def __eq__(self, o: object) -> bool:
        return id(o)

def imshow(img):
    if img.shape[-1] == 3:
        plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    else:
        plt.imshow(img, cmap=plt.gray())

def capitalize(s):
    return s[0].upper() + s[1:]

def wrapHashableNdArray(func):
    def wrapped(*args, **kwargs):
        args = list(args)
        for i, arg in enumerate(args):
            if isinstance(arg, np.ndarray):
                args[i] = HashableNdArray(arg)
        for key, arg in kwargs.items():
            if isinstance(arg, np.ndarray):
                kwargs[key] = HashableNdArray(arg)
        return func(*args, **kwargs)
    return wrapped

def unwrapHashableNdArray(func):
    def wrapped(*args, **kwargs):
        args = list(args)
        for i, arg in enumerate(args):
            if isinstance(arg, HashableNdArray):
                args[i] = arg.array
        for key, arg in kwargs.items():
            if isinstance(arg, HashableNdArray):
                kwargs[key] = arg.array
        return func(*args, **kwargs)
    return wrapped

def lru_cache(*args, **kwargs):
    def firstWrapped(func):
        @wrapHashableNdArray
        @functools.lru_cache(*args, **kwargs)
        @unwrapHashableNdArray
        def secondWrapped(*args, **kwargs):
            return func(*args, **kwargs)
        return secondWrapped
    return firstWrapped
    
@lru_cache()
def find_img(background, template, similarity=0.8, colorCloseThreshold=0.2):
    if isinstance(background, str):
        background = cv.imread(background)
    if isinstance(template, str):
        template = cv.imread(template)
    
    result = cv.matchTemplate(background, template, cv.TM_CCOEFF_NORMED) 
    _, sim, _, start_point = cv.minMaxLoc(result)
    end_point = [start_point[0] + template.shape[1],
                 start_point[1] + template.shape[0]]
    if sim < similarity:
        return None
    else:
        matchedImg = background[start_point[1]: end_point[1], start_point[0]: end_point[0]]
        diff = np.abs(matchedImg.mean() - template.mean()) / template.mean()
        isColorClose = diff < colorCloseThreshold
        logging.debug(f"diff {diff:1.3} isColorClose: {isColorClose}")
        if not isColorClose:
            return None
        return [start_point, end_point]

@lru_cache()
def cachedDetectAndCompute(detector, *args, **kwargs):
    return detector.detectAndCompute(*args, **kwargs)

@lru_cache()
def find_img_by_descriptor(img_object, 
                           img_scene, 
                           showImg=False,
                           distanceThreshold=None,
                           detector=None):
    if img_object.ndim == 3:
        img_object = cv.cvtColor(img_object, cv.COLOR_BGR2GRAY)
    if img_scene.ndim == 3:
        img_scene = cv.cvtColor(img_scene, cv.COLOR_BGR2GRAY)
    if distanceThreshold is None:
        distanceThreshold = 0.75
    #-- Step 1: Detect the keypoints using SURF Detector, compute the descriptors
    if detector is None:
        detector = cv.xfeatures2d.SIFT_create()
    with Timer('detectAndCompute', stdout=logging.debug):
        keypoints_obj, descriptors_obj = cachedDetectAndCompute(detector, img_object, None)
        keypoints_scene, descriptors_scene = cachedDetectAndCompute(detector, img_scene, None)
    # #-- Step 2: Matching descriptor vectors with a FLANN based matcher
    # matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)
    # knn_matches = matcher.knnMatch(descriptors_obj, descriptors_scene, 2)
    # #-- Filter matches using the Lowe's ratio test
    # good_matches = []
    # for m,n in knn_matches:
    #     if m.distance < distanceThreshold * n.distance:
    #         good_matches.append(m)
    # logging.debug(f'There are {len(good_matches)} matches points ')

    # bf = cv.BFMatcher()
    matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)
    knn_matches = []
    if descriptors_obj is not None and descriptors_scene is not None:
        knn_matches = matcher.match(descriptors_obj, descriptors_scene)
    good_matches = []
    for match in knn_matches:
        if match.distance < 150:
            good_matches.append(match)

    if len(good_matches) <= 4:
        logging.debug(f'matches points are not enough {len(good_matches)}')
        return None

    #-- Localize the object
    obj = np.empty((len(good_matches),2), dtype=np.float32)
    scene = np.empty((len(good_matches),2), dtype=np.float32)
    for i in range(len(good_matches)):
        #-- Get the keypoints from the good matches
        obj[i,0] = keypoints_obj[good_matches[i].queryIdx].pt[0]
        obj[i,1] = keypoints_obj[good_matches[i].queryIdx].pt[1]
        scene[i,0] = keypoints_scene[good_matches[i].trainIdx].pt[0]
        scene[i,1] = keypoints_scene[good_matches[i].trainIdx].pt[1]
    H, _ =  cv.findHomography(obj, scene, cv.RANSAC)
    if H is None:
        logging.debug(f'H is None')
        return None

    #-- Get the corners from the image_1 ( the object to be "detected" )
    # obj_corners stores 4 corner points of obj, thus shape = (4, 1, 2)
    obj_corners = np.empty((4,1,2), dtype=np.float32)
    obj_corners[0,0,0] = 0
    obj_corners[0,0,1] = 0
    obj_corners[1,0,0] = img_object.shape[1]
    obj_corners[1,0,1] = 0
    obj_corners[2,0,0] = img_object.shape[1]
    obj_corners[2,0,1] = img_object.shape[0]
    obj_corners[3,0,0] = 0
    obj_corners[3,0,1] = img_object.shape[0]
    scene_corners = cv.perspectiveTransform(obj_corners, H)
    if showImg:
        #-- Draw matches
        img_matches = cv.drawMatches(img_object, keypoints_obj, img_scene, keypoints_scene, good_matches, None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        #-- Draw lines between the corners (the mapped object in the scene - image_2 )
        cv.polylines(img_matches, 
                    np.array([scene_corners.squeeze() + [img_object.shape[1], 0]], np.int32), 
                    True, 
                    (255,0,0), 10)
        tool.imshow(img_matches)
        plt.show()
    return scene_corners


def get_center_point(xy):
    center = [sum(t) // 2 for t in zip(xy[0], xy[1])]
    return center


def get_left_lower_point(xy):
    left_lower = [xy[0][0], xy[1][1]]
    return left_lower


def get_right_upper_point(xy):
    right_upper = [xy[0][1], xy[1][0]]
    return right_upper


def capture_screenshot():
    global source
    img = pyautogui.screenshot()  # x,y,w,h
    source = np.array(img.convert('RGB'))[..., -1::-1]
    # sample rate 1%
    if base_point is not None and random.random() < SCREEN_SAMPLE_RATE:
        imgDirPath = 'collectImgs'
        if not os.path.exists(imgDirPath):
            os.makedirs(imgDirPath)
        imgName = os.path.join(imgDirPath, 'img_{}.png'.format(time.strftime("%Y_%m_%d_%H_%M_%S")))
        img = source[base_point[1]:(base_point[1] + APP_HEIGHT), base_point[0]:(base_point[0] + APP_WIDTH)]
        save_image.queue.put((imgName, img))
        logging.info(f'Add image {imgName} into queue')
    return source

def get_screenshot():
    global source
    return source


def get_appshot():
    global source
    appshot = source[base_point[1]:(base_point[1] + 1450), base_point[0]:(base_point[0] + 900)].copy()
    return appshot

base_point = None


class Operation:
    CLICK = 'click'
    SLIDE = 'slide'
    CLICK_ON_IMG = 'CLICK_ON_IMG'

    ope_name = ''
    act_name = ''
    cv_res = [None, None]
    img = ''

    def __init__(self, act_name='', cv_res=[None, None], img=''):
        self.act_name = act_name
        self.cv_res = cv_res
        self.img = img
        if base_point == None:
            self.reset_base_point()

    def __str__(self):
        return f'Operation[{self.ope_name}][{self.act_name}][{self.cv_res[0]}][{self.cv_res[1]}]'

    def reset_base_point(self):
        global base_point
        xy = find_img(capture_screenshot(), 'img/base/head.png')
        if xy == None:
            logging.error('can not find base_point')
            assert(None)
        else:
            base_point = get_left_lower_point(xy)
            logging.info(f'base point is {base_point}')

    def click(self, xy, bg='app'):
        global base_point
        if bg == 'app':
            adjusted_basepoints = [base_point[0]/2, base_point[1]/2]
            xy = list(map(sum, zip(xy, adjusted_basepoints)))
        pymouse.PyMouse().move(*xy)
        pymouse.PyMouse().click(*xy, 1)

    def slide(self, xy_start, xy_stop):
        adjusted_basepoints = [base_point[0]/2, base_point[1]/2]
        pymouse.PyMouse().move(*map(sum, zip(xy_start, adjusted_basepoints)))
        pyautogui.dragTo(*map(sum, zip(xy_stop, adjusted_basepoints)), button='left', duration=1, tween=pyautogui.easeInCubic) 

    def check_point(self, point):
        if point == None:
            logging.error(
                f'Operation[{self.ope_name}][{self.act_name}][{self.cv_res}][{self.img}] illgal')
            assert(None)

    def action(self, bg='app'):
        if self.act_name == self.CLICK:
            self.check_point(self.cv_res[0])
            self.click(self.cv_res[0])
        elif self.act_name == self.SLIDE:
            if self.cv_res[0] == None and self.cv_res[1] == None:
                self.check_point(None)
            self.slide(self.cv_res[0], self.cv_res[1])
        elif self.act_name == self.CLICK_ON_IMG:
            if bg == 'app':
                res = find_img(get_appshot(), self.img)
                if None == res:
                    logging.error(f'can not action click on img[{self.img}]')
                else:
                    self.click(get_center_point(res), bg)
            else:
                res = find_img(get_screenshot(), self.img)
                if None == res:
                    logging.error(f'can not action click on img[{self.img}]')
                else:
                    self.click(get_center_point(res), bg)

        else:
            self.check_point(None)


def retry(func, count=1, delay_ms=0):
    if count == 0:
        logging.error(f'retry count can not[{count}] < 0')
        assert(None)

    for n in range(count):
        if func() == True:
            return True
        time.sleep(delay_ms / 1000)
    return False


def log_error_screen(name):
    img = pyautogui.screenshot()  # x,y,w,h
    img.save(time.strftime('err_%m%d%H%M%S_',
                           time.localtime()) + name + '.png')


def check_lose_connect():
    if find_img(get_appshot(), 'img/base/loss_connect.png') != None:
        return True
    else:
        return False


def kick_ass():
    Operation(Operation.CLICK, [[2, 620]]).action()


class Internet():
    def open(self):
        logging.info('internet open')
        subprocess.call('NetDisabler_x64.exe /E')

    def close(self):
        logging.info('internet close')
        subprocess.call('NetDisabler_x64.exe /D')

    def reboot(self, time_s):
        logging.info(f'internet will reboot[{time_s}]')
        self.close()
        time.sleep(time_s)
        self.open()


class SwitchApp():
    def game(self):
        logging.info('switch to game')
        Operation(Operation.CLICK_ON_IMG,
                  img='img/base/game_ico.png').action('screen')

    def home(self):
        logging.info('switch to home')
        Operation(Operation.CLICK_ON_IMG,
                  img='img/base/head.png').action('screen')


def get_all_modules(dir_name):
    modules = []
    for root, _, fs in os.walk(dir_name):
        for f in fs:
            if f.startswith('__') or f.endswith('.pyc'):
                continue
            fullname = os.path.join(root, f)
            fullname = fullname.replace('.py', '')
            # fullname = fullname.replace('\\', '.')
            fullname = fullname.replace('/', '.')
            modules.append(fullname)
    return modules
