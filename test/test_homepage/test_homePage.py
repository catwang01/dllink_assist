import pytest
import cv2
from homepage.status import homePage

class TestHomePage:

    @pytest.mark.parametrize('imgPath,expected', 
    [
        ('test/test_homepage/screenshot1.png', 'GX'),
        ('test/test_homepage/screenshot2.png', 'GX'),
        ('test/test_homepage/screenshot3.png', 'GX'),
        ('test/test_homepage/screenshot4.png', 'GX'),
        ('test/test_homepage/screenshot5.png', 'GX'),
        ('test/test_homepage/screenshot6.png', 'DM'),
    ]
    )
    def test_getCurrentWorld(self, imgPath, expected):
        assert homePage.getCurrentWorld(imgPath) == expected