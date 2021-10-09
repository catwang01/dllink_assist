import pytest
import cv2

from icons import Icon
from role import RoleCollection


class TestRole:

    @pytest.mark.parametrize('imgPath,roleName,expected', 
    [
        ('test/test_role/screenshot1.png', 'AlexisRhodes', True),
        ('test/test_role/screenshot2.png', 'JadenYuki', True),
        ('test/test_role/screenshot3.png', 'ChazzPrinceton', True),
        ('test/test_role/screenshot4.png', 'AsterPhoenix', True),
        ('test/test_role/screenshot5.png', 'JesseAnderson', True),
    ])
    def test_role(self, imgPath, roleName, expected):
        collection = RoleCollection('img/roles/roleDict.txt')
        icon = Icon(collection.getRole(roleName).homePageImgPath)
        icon.background = cv2.imread(imgPath)
        assert icon.exists() == expected

        
