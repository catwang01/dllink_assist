from mystatus import Status
from activity.sai.icons import *
from general.status import generalReturnButton, generalYesButton, generalCloseButton

class SaiHomePage(Status):

        def canFlipSai(self):
                return not self.iconDict['flipSaiOffButton'].exists()

        def canEnterLottery(self):
                return self.iconDict['cardLotteryButton'].exists()

        def canActivityDuel(self):
                return self.iconDict['activityDuel'].exists()

class LotteryHomePage(Status):

        def canBuyLottery(self):
                return self.iconDict['buyLotteryButton'].exists()

        def hasClose(self):
                return self.iconDict['closeButton'].exists()

saiHomePage = SaiHomePage(
        name="saiHomePage",
        iconDict={
            "flipSaiButton":  flipSaiButton,
            'cardLotteryButton': cardLotteryButton,
            'flipSaiOffButton': flipSaiOffButton,
            'returnButton': generalReturnButton,
            'activityDuel': activityDuelButton,
            'itemsButton': itemsButton,
            'useItemButton': useItemButton
        },
        transferDict={
                'flip': lambda status: flipSaiButton.click(),
                'enterLottery': lambda status: cardLotteryButton.click(),
                'activityDuel': lambda status: activityDuelButton.click(),
                'return': lambda status: generalReturnButton.click(),
                'enterItemMenu': lambda status: itemsButton.click(),
                'useItem': lambda status: useItemButton.click()
        },
       condition="flipSaiButton | activityDuel",
)

selectLevelPage = Status(
        name="selectLevelPage",
        iconDict={
            'difficultLevel' : difficultLevel
        },
        transferDict={
                'selectDifficultLevel' : lambda status: difficultLevel.click()
        },
        condition="difficultLevel",
)

coinRepoPage = Status(
        name="coinRepoPage",
        iconDict={
            'yesIcon' : generalYesButton
        },
        transferDict={
                'yes':  lambda status: generalYesButton.click()
        },
        condition="yesIcon",
)

lotteryHomePage = LotteryHomePage(
        name="lotteryHomePage",
        iconDict={
            'buyLotteryButton': buyLotteryButton,
            'generalReturnButton': generalReturnButton,
            "lotteryHomePageTitle": lotteryHomePageTitle,
            "closeButton": generalCloseButton 
        },
        transferDict={
                'buyLottery': lambda status: buyLotteryButton.click(),
                'return': lambda status: generalReturnButton.click(),
                'close': lambda status: generalCloseButton.click()
        },
        condition="lotteryHomePageTitle",
)


class UseItemHomePage(Status):

        def hasUsableItem(self):
                return self.iconDict['useItemButton'].exists()

        def hasClose(self):
                return self.iconDict['closeButton'].exists()


useItemHomePage = UseItemHomePage(
        name="useItemHomePage",
        iconDict={
            'itemsButton': itemsButton,
            'useItemButton': useItemButton,
            'title': useItemHomePageTitle,
            'closeButton': generalCloseButton
        },
        transferDict={
                'enterItemMenu': lambda status: itemsButton.click(),
                'useItem': lambda status: useItemButton.click(),
                'close': lambda status: generalCloseButton.click()

        },
        condition="title",
)
