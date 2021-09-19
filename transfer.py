'''
Author: your name
Date: 2021-02-24 06:17:11
LastEditTime: 2021-03-07 03:48:52
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \dllink_assist\transfer.py
'''


import numpy as np
import random
from tool import capitalize
import inspect
from typing import Optional
import tool
import sys
import networkx as nx
import matplotlib.pyplot as plt
import logging
import threading
import time
from dict_recursive_update import recursive_update
import collections
import cv2 as cv
import importlib
import duel
import mystatus
from mystatus import *

delay_dict = {
    'STATUS_GATE_DUEL': 16000,
    'STATUS_PVP_DUEL': 20000,
    "STATUS_NPC_DUEL_AUTO": 10000,
    'STATUS_PVP_HOME': 2000,
    'STATUS_PVP_PREPARE': 2000,
    'STATUS_SEND_NICE': 1000
}

duel_list = ['STATUS_PVP_DUEL', 'STATUS_GATE_DUEL']

class StatusControlThread(threading.Thread):

    now_status = None
    statusList = [
        startPage,
        notificationPage,
        kuloNoSuOccurPage,
        homePage,
        recieveKeys,
        inDiagLog,
        selectDuelMode,
        duelFinishedPage, 
        duelResultsPage,
        notFinishLoadingDuelResultsPage,
        getSaiStatus,
        recommendFriendPage,
        switchingWorldStatus,
        generalYesPage,
        generalNextPage,
        generalClosePage,
    ] 
    statusList.sort(key=lambda x: x.level, reverse=True)
    refreshScreenTime = -1
    minRefreshInterval = 1
    # target_status = 'STATUS_BASE'
    # next_status = 'STATUS_BASE'
    # status_dict = d1 = collections.OrderedDict()
    # G = nx.DiGraph()
    # short_path_dict = {}
    thread_close_flag = False
    # img_dict = {}

    def __init__(self):
        super().__init__()
        tool.Operation()

        # for mn in tool.get_all_modules('status'):
        #     importlib.import_module(mn)
        #     for name, class_ in inspect.getmembers(sys.modules[mn], inspect.isclass):
        #         self.status_dict[name] = class_()
        #         for k, _ in self.status_dict[name].transfer_dict.items():
        #             self.G.add_edge(name, k)
        #         for img in (self.status_dict[name].staimg_list['yes'] + self.status_dict[name].staimg_list['no']):
        #             if False == Path(img).exists():
        #                 logging.error(f'[{img}] not exist')
        #                 assert(None)
        #             self.img_dict[img] = cv.imread(img)

        # self.status_dict.pop('STATUS_BASE')
        # z = list(zip(self.status_dict.keys(), self.status_dict.values()))
        # z = sorted(z, key=lambda x: x[1].priority, reverse=True)
        # self.status_dict = dict(z)

        # self.short_path_dict = dict(nx.all_pairs_shortest_path(self.G))
        # self.search_status()

    def __str__(self):
        return f'now[{self.now_status}] next[{self.next_status}] target[{self.target_status}]'

    def goto_status(self, status, delay_s=180):
        logging.info(f'start go to status[{status}] ')
        if self.now_status == status:
            return True
        self.set_target_status(status)
        if delay_s == 0:
            while self.now_status != status:
                time.sleep(1)
        else:
            while delay_s >= 0 and self.now_status != status:
                time.sleep(1)
                delay_s -= 1
        if self.now_status == status:
            logging.info(f'start go to status[{status}] success')
            return True
        else:
            logging.warn(f'start go to status[{status}] fail')
            return False

    def exec_delay(self, status):
        if status in delay_dict.keys():
            logging.info(f'exec [{status}] delay[{delay_dict[status]}]')
            time.sleep(delay_dict[status] / 1000)
        else:
            time.sleep(1000 / 1000)

    def transfer(self, status, delay_ms=500):
        next_status_dict = self.status_dict[self.now_status].transfer_dict

        default_dict = {'xy': [0, 0], 'img': ''}
        recursive_update(default_dict, next_status_dict[status])
        ope = tool.Operation(default_dict['act_name'], [
            default_dict['xy']], default_dict['img'])
        ope.action()

        self.exec_delay(status)

    def showScreen(self):
        tool.showImg(tool.get_appshot())

    def refreshScreen(self):
        """
        Control refresh frequency
        """

        now = time.time()
        interval = now - max(mystatus.lastClickTime, self.refreshScreenTime)
        logging.debug("laskClickTime: {}, self.refreshScreenTime: {} now: {}".format(mystatus.lastClickTime, self.refreshScreenTime, now))
        if interval < self.minRefreshInterval:
            sleepTime = np.ceil(self.minRefreshInterval - interval)
            logging.info("Refresh screen too frequently! Sleep for {}s".format(sleepTime))
            time.sleep(sleepTime)
            self.refreshScreen()
        else:
            self.refreshScreenTime = time.time()
            tool.capture_screenshot()
            logging.debug("The screen has been refreshed! refreshScreenTime: {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.refreshScreenTime))))

    def getCurrentStatus(self, refresh=True) -> Optional[Status]:
        if refresh:
            self.refreshScreen()
        logging.debug('Getting current status')
        curStatus = None
        for status in self.statusList:
            if status.check():
                curStatus = status 
                break
        logging.debug("Current status: {}".format(curStatus))
        return curStatus

    def changeWorld(self, targetWorld=None):
        while True:
            self.now_status = self.getCurrentStatus()
            if str(self.now_status) == 'homePage':
                self.now_status.transfer("switchWorld", 1)
            elif str(self.now_status) == "switchingWorldStatus":
                if targetWorld is None or targetWorld == "DMWorld":
                    self.now_status.transfer('switchToDMWorld', 5)
                else:
                    self.now_status.transfer('switchToGXWorld', 5)
                logging.debug("Goto world: {}".format(targetWorld))
                return
            else:
                break

    def handleHomePage(self):
        for world in ['DMWorld', 'GXWorld']:
            self.changeWorld(world)
            self.collectKeys()
            self.duelWithNormalNpcs()

    def collectKeys(self):
        self.now_status = self.getCurrentStatus()
        if str(self.now_status) != 'homePage':
            return
        channels = ['pvp', 'transportGate', 'store', 'workshop', 'monsterGate']
        nChannels = len(channels)
        logging.info("Collecting keys...")
        startTime = time.time()
        nTotalCollected = 0
        while len(channels):
            channel = random.choice(channels)
            nCollected = 0
            logging.debug("goto {}".format(channel))
            currentChannel = self.now_status.inWhichChannel()
            logging.debug("current: {} goto: {}".format(currentChannel, channel))
            if  currentChannel != channel:
                self.now_status.transfer('select{}'.format(capitalize(channel)))
            else:
                logging.debug("Staying current channel")
            logging.info("Collecting keys in {}".format(channel))
            while True:
                self.now_status = self.getCurrentStatus()
                if str(self.now_status) == 'homePage':
                    nKeys = self.now_status.countKeys()
                    if nKeys > 0:
                        logging.info("Find {} keys in current channel".format(nKeys))
                        self.now_status.transfer('collectOneKey')
                        nCollected += 1
                    else:
                        logging.info("Find no keys in current channel!".format(nKeys))
                        break
                elif str(self.now_status) == 'recieveKeys':
                    self.now_status.transfer('click')
            logging.info("Collected {} keys in current channel: {}".format(nCollected, channel))
            channels.remove(channel)
            logging.info("Total channels: {} Collected: {} Left: {}".format(nChannels, nChannels - len(channels), len(channels)))
            nTotalCollected += nCollected 
        endTime = time.time()
        logging.info("Collecting finished! TimeUsed: {}s Total collected keys: {}".format(int(endTime - startTime), nTotalCollected))
        return

    def duelWithOneNormalNpc(self):
        nDiagLog = 0
        while True:
            self.now_status = self.getCurrentStatus()
            if str(self.now_status) == 'inDiagLog':
                self.now_status.transfer('next')
                nDiagLog += 1
            elif str(self.now_status) == "selectDuelMode":
                self.now_status.transfer('autoDuel')
            elif str(self.now_status) == "duelFinishedPage":
                self.now_status.transfer("yes")
            elif str(self.now_status) == 'notFinishLoadingDuelResultsPage':
                self.now_status.transfer("randomClick")
            elif str(self.now_status) == "duelResultsPage":
                self.now_status.transfer("next")
            elif str(self.now_status) == 'getSaiFragment':
                self.now_status.transfer("yes")
            elif str(self.now_status) == 'recommendFriendPage':
                self.now_status.transfer("cancel")
            else:
                if nDiagLog >= 2:
                    print('Duel finished!')
                    break

    def duelWithNormalNpcs(self):
        self.now_status = self.getCurrentStatus()
        if str(self.now_status) != 'homePage':
            return
        channels = ['pvp', 'transportGate', 'store', 'workshop', 'monsterGate']
        nChannels = len(channels)
        logging.info("Searching normal npcs...")
        startTime = time.time()
        nTotalSearched = 0
        while len(channels):
            channel = random.choice(channels)
            nSearched = 0
            logging.debug("goto {}".format(channel))
            currentChannel = self.now_status.inWhichChannel()
            logging.debug("current: {} goto: {}".format(currentChannel, channel))
            if  currentChannel != channel:
                self.now_status.transfer('select{}'.format(capitalize(channel)), 5)
            else:
                logging.debug("Staying current channel")
            logging.info("Searching normal npcs in {}".format(channel))
            while True:
                self.now_status = self.getCurrentStatus()
                if str(self.now_status) == 'homePage':
                    nNpcs = self.now_status.countNormalNpcs()
                    if nNpcs > 0:
                        logging.info("Find {} normal npcs in current channel".format(nNpcs))
                        self.now_status.transfer('clickOneNormalNpc')
                        self.duelWithOneNormalNpc()
                        nSearched += 1
                    else:
                        logging.info("Find no normal npcs in current channel!".format(nNpcs))
                        break
                elif str(self.now_status) == 'recieveKeys':
                    self.now_status.transfer('click')
            logging.info("Searched {} normal npcs in current channel: {}".format(nSearched, channel))
            channels.remove(channel)
            logging.info("Total channels: {} Searched: {} Left: {}".format(nChannels, nChannels - len(channels), len(channels)))
            nTotalSearched += nSearched 
        endTime = time.time()
        logging.info("Searching finished! TimeUsed: {}s Total search normal npcs: {}".format(int(endTime - startTime), nTotalSearched))
        return

    def run(self):  # 必须有的函数
        self.thread_close_flag = False

        while True:
            if self.thread_close_flag:
                exit()

            # notificationPage.check()
            # homePage.check()
            self.now_status = self.getCurrentStatus()
            if str(self.now_status) == "startPage":
                self.now_status.transfer('startGame')
            elif str(self.now_status) ==  'notificationPage':
                self.now_status.transfer('return')
            elif str(self.now_status) == 'kuloNoSuOccurPage':
                self.now_status.transfer('close')
            elif str(self.now_status) == 'homePage':
                self.handleHomePage()
            elif str(self.now_status) == 'generalYesPage':
                self.now_status.transfer('yes')
            elif str(self.now_status) == 'generalNextPage':
                self.now_status.transfer('next')

            # if self.target_status == 'STATUS_BASE':
            #     time.sleep(0.5)
            #     continue


            # if self.now_status == 'STATUS_BASE':
            #     continue
            
            # if self.now_status != 'STATUS_BASE':
            #     next_status = random.choice(list(self.status_dict[self.now_status].transfer_dict.keys()))
            #     xy = self.status_dict[self.now_status].transfer_dict[next_status]['xy']
            #     tool.Operation().click(xy)
            #     self.search_status(refresh=True)

            # self.collectKeys()
            
            # if self.now_status in duel_list:
            #     duel.run_loop(self.now_status)
            #     self.now_status = 'STATUS_BASE'
            #     continue

            # if self.now_status != self.target_status:
            #     if self.target_status not in self.short_path_dict[self.now_status]:
            #         logging.error(f'can not reach targer status, {self}')
            #         assert(None)
            #     self.next_status = self.short_path_dict[self.now_status][self.target_status][1]
            #     logging.info(f'start transfer, {self}')
            #     self.transfer(self.next_status)
            #     continue

    # def getCurrentChannel(self, refresh=True):
    #     if refresh:
    #         tool.capture_screenshot()
    #     for channel, icon in channelIcons.items():
    #         selectXy = tool.find_img(tool.get_appshot(), icon.selectPath)
    #         print(channel, selectXy)
    #         if selectXy is not None:
    #             return channel
    #     raise Exception("No channel is selected")

    # def clickOnImg(self, img, allowNotExist=False):
    #     xy = tool.find_img(tool.get_appshot(), img)
    #     if not xy:
    #         if allowNotExist:
    #             logging.warn("img {} not in app".format(xy))
    #             return None 
    #         else:
    #             raise Exception("img {} not in app".format(xy))
    #     mid_point = tool.get_center_point(xy)
    #     mid_point = [mid_point[0] / 2, mid_point[1] / 2]
    #     tool.Operation().click(mid_point)
    #     time.sleep(2.5)
    #     tool.capture_screenshot()
    #     return xy

    # def collectKeys(self):
    #     for channel, icon in channelIcons.items():
    #         if channel != self.getCurrentChannel():
    #             self.clickOnImg(icon.nonSelectPath)
    #         logging.debug('channel: {}'.format(channel))
    #         nSelectedKeys = 0
    #         for keyPath in keyIcon.paths:
    #             while True:
    #                 if self.clickOnImg(keyPath, allowNotExist=True):
    #                     nSelectedKeys += 1
    #                     self.clickOnImg(yesIcon.path, allowNotExist=True)
    #                 else:
    #                     break
    #         logging.info("Select {} keys in channel {}".format(nSelectedKeys, channel))

    def stop(self):
        self.thread_close_flag = True
        self.join()

    def show_map(self):
        for k, v in self.short_path_dict.items():
            print(k)
            print(v)
        nx.draw(self.G, with_labels=True, edge_color='b',
                node_color='g', node_size=1000)
        plt.show()

    def check_status(self, expect_status, refresh=True):
        if refresh == True:
            tool.capture_screenshot()
        cs = self.status_dict[expect_status]

        res = True
        for img in cs.staimg_list['yes']:
            xy = tool.find_img(tool.get_appshot(), self.img_dict[img])
            if xy == None:
                logging.debug(
                    f'expect status[{expect_status}] can not find img[{img}]')
                res = False
                break

        for img in cs.staimg_list['no']:
            xy = tool.find_img(tool.get_appshot(), self.img_dict[img])

            if xy != None:
                logging.debug(
                    f'expect status[{expect_status}] find illgal img[{img}]')
                res = False
                break

        return res

    def search_status(self, refresh=True):

        def check():
            if refresh == True:
                tool.capture_screenshot()
            self.now_status = 'STATUS_BASE'

            for s in self.status_dict.keys():
                if self.check_status(s, False) == True:
                    self.now_status = s
                    return True
            # tool.kick_ass()
            return False

        # if tool.retry(check, 60, 1000) == False:
        #     logging.error('can not search status')
        #     tool.log_error_screen('search_status')
        #     assert(None)
        #     return False
        logging.info(f'search status finished, {self}')
        return True

    def set_target_status(self, expect_status):
        self.target_status = expect_status
