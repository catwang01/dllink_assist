from mystatus import Status
from general.icons import *

generalYesPage = Status(
        name='generalYesPage',
        iconDict={
                'yesButton': generalYesButton
        },
        transferDict={
                'yes': lambda status: generalYesButton.click(),
                'default': lambda status:generalYesButton.click()
        },
        condition="yesButton",
)

generalClosePage= Status(
        name='generalClosePage',
        iconDict={
                'closeButton': generalCloseButton
        },
        transferDict={
                'close': lambda status:generalCloseButton.click(),
                'default': lambda status:generalCloseButton.click()
        },
        condition="closeButton",
)


generalNextPage= Status(
        name='generalNextPage',
        iconDict={
                'nextButton': generalNextButton
        },
        transferDict={
                'next': lambda status:generalNextButton.click(),
                'default': lambda status:generalNextButton.click()
        },
        condition="nextButton",
)

generalCancelPage = Status(
        name='generalCancelPage',
        iconDict={
                'cancelButton': generalCancelButton
        },
        transferDict={
                'cancel': lambda status: generalCancelButton.click(),
                'default': lambda status: generalCancelButton.click(),
        },
        condition="cancelButton",
)

generalReturnPage= Status(
        name='generalReturnPage',
        iconDict={
                'returnButton': generalReturnButton
        },
        transferDict={
                'return': lambda status:generalReturnButton.click(),
                'default': lambda status:generalReturnButton.click()
        },
        condition="returnButton",
)

generalStatusList = [
        generalYesPage,
        generalClosePage,
        generalNextPage,
        generalCancelPage,
        generalReturnPage
]