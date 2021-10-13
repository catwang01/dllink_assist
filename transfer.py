'''
Author: your name
Date: 2021-02-24 06:17:11
LastEditTime: 2021-03-07 03:48:52
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \dllink_assist\transfer.py
'''

import threading
import logging
from duel.fsm import ManualDuelFSM

import tool
from FSM import FSM
from mystatus import startPage, notificationPage, kuloNoSuOccurPage
from general.status import generalStatusList
from login.status import loginPage
from log.log import setupLogging
from login.fsm import LoginFSM
from homepage.fsm import HomePageFSM
from homepage.status import homePage
from connectionError.status import networkConnectionPage


setupLogging()
logger = logging.getLogger(__name__)

delay_dict = {
    'STATUS_GATE_DUEL': 16000,
    'STATUS_PVP_DUEL': 20000,
    "STATUS_NPC_DUEL_AUTO": 10000,
    'STATUS_PVP_HOME': 2000,
    'STATUS_PVP_PREPARE': 2000,
    'STATUS_SEND_NICE': 1000
}

duel_list = ['STATUS_PVP_DUEL', 'STATUS_GATE_DUEL']

class StatusControlThread(threading.Thread, FSM):

    statusList = [
        startPage,
        homePage,
        kuloNoSuOccurPage,
        notificationPage,
        loginPage,
        networkConnectionPage
    ] + generalStatusList
    def __init__(self):
        super().__init__()
        tool.Operation()

    def run(self):  # 必须有的函数
        self.thread_close_flag = False

        while True:
            if self.thread_close_flag:
                exit()

            # notificationPage.check()
            # homePage.check()
            # self.maze()
            # ManualDuelFSM().run()
            curStatus = self.getCurrentStatus()
            if curStatus == startPage:
                curStatus.transfer('startGame')
            elif curStatus ==  notificationPage:
                curStatus.transfer('return')
            elif curStatus == kuloNoSuOccurPage:
                curStatus.transfer('close')
            elif curStatus == homePage:
                HomePageFSM().run()
            elif curStatus in generalStatusList:
                curStatus.transfer('default')
            elif curStatus == loginPage:
                LoginFSM().run()
            elif curStatus == networkConnectionPage:
                curStatus.transfer('reboot', 1)