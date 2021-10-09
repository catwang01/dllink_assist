import pytest
import cv2

from homepage.icons import unionForceIcon

class TestUnionForce:

    @pytest.mark.parametrize('imgPath,expected', 
        [
            ('test/test_unionForce/screenshot1.png', True),
            ('test/test_unionForce/screenshot2.png', True),
        ]
    )
    def testUnionForceIcon(self, imgPath, expected):
        unionForceIcon.background = cv2.imread(imgPath)
        assert unionForceIcon.exists() == expected
