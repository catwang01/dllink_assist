import pytest
import cv2
from activity.ddCastle.icons import ddCastleAutoDuelButton, ddCastleHomePageTitle

class TestDDCastle:

    @pytest.mark.parametrize('imgPath,icon,expected', [
        ('test/activity/test_ddCastle/screenshot1.png', ddCastleAutoDuelButton, True),
        ('test/activity/test_ddCastle/screenshot2.png', ddCastleHomePageTitle, True)
    ])
    def test_icon(self, imgPath, icon, expected):
        icon.background = cv2.imread(imgPath)
        assert icon.exists() == expected