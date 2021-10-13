from mystatus import Status
from activity.ddCastle.icons import *
from general.status import generalReturnButton, generalCloseButton
import tool

ddCastleHomePage = Status(
        name="ddCastleHomePage",
        iconDict={
                "autoDuelButton": ddCastleAutoDuelButton,
                "title": ddCastleHomePageTitle,
                "returnButton": generalReturnButton,
                'cardLotteryButton': cardLotteryButton,
                'firstFloorIcon': ddCastleFirstFloorIcon
        },
        transferDict={
                'enterLottery': lambda status: cardLotteryButton.click(),
                'autoDuel': lambda status: ddCastleAutoDuelButton.click(),
                "return": lambda status: generalReturnButton.click(),
                'downSlide': lambda status: tool.Operation().slide((228, 536), (228,223))
        },
       condition="title",
)

ddCastleLotteryHomePage = Status(
        name= "ddCastleLotteryHomePage",
        iconDict={
                'title': ddCastleLotteryHomePageTitle,
                'returnButton': generalReturnButton,
                'buyLotteryButton': buyLotteryButton,
                'closeButton': generalCloseButton
        },
        transferDict={
                'buyLottery': lambda status: buyLotteryButton.click(),
                'close': lambda status: generalCloseButton.clici(),
                'return': lambda status: generalReturnButton.click()
        },
        condition="title",
)