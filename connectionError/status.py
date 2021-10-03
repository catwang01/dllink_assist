from mystatus import Status
from connectionError.icons import *

networkConnectionPage = Status(
    name='networkConnectionPage',
    iconDict={
        'title': connectionErrorPageTitle,
        'retryButton': retryButton,
        'rebootButton': rebootButton
    },
    transferDict={
        'reboot': lambda status: rebootButton.click(),
        'retry': lambda status: retryButton.click()
    },
    condition='title'
)