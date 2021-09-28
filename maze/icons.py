from icons import Icon, MultiIcon
import re
import tool
from general.icons import *
import glob

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

def nextDirectionStrToInt(s):
        if s == "UP":
                return UP
        elif s == "DOWN":
                return DOWN
        elif s == "LEFT":
                return LEFT
        elif s == "RIGHT":
                return RIGHT
        else:
                raise Exception(f"No corresponding direction: {s}")

imgRootPath = 'img/maze'

class LocationIcon(Icon):

        def getPosition(self, direction=None):
                shift = self.getShift(direction)
                centerPoint = tool.get_center_point(self.position)
                centerPoint = [centerPoint[0] + 2 * shift[0], centerPoint[1] + 2 * shift[1]]
                return centerPoint

        def getClickImg(self, direction=None):
                return tool.getShotAtPosition(tool.get_appshot(), self.getPosition(direction), width=90)

        def getShift(self, direction):

                shift = None
                if direction == UP:
                        shift = (-66, -19)
                elif direction == DOWN:
                        shift = (78, 70)
                elif direction == LEFT:
                        shift = (-60, 60)
                elif direction == RIGHT:
                        shift = (70, -12)
                return shift

        def clickWithDirection(self, direction=None):
                self.click(*self.getShift(direction))

currentLocation = LocationIcon(f'{imgRootPath}/currentLocation.png')
mazeTitleIcon = Icon(f'{imgRootPath}/mazeTitleIcon.png')

class StepIcon(MultiIcon):
        def __init__(self, *args, **kwargs) -> None:
            if 'nextDirection' in kwargs:
                    self.nextDirection = kwargs['nextDirection']
                    del kwargs['nextDirection']
            super().__init__(*args, **kwargs)
            self.floorNo, self.stepNo = self.getNo(self.name)

        @classmethod
        def getNo(self, s):
                reg = re.search("floor(\d+)step(\d+)", s)
                return int(reg.group(1)), int(reg.group(2))
stepIcons = []
for filename in glob.glob(f'{imgRootPath}/YukiJudai/floor*step*.png'):
        floorNo, stepNo = StepIcon.getNo(filename)
        name = f'floor{floorNo}step{stepNo}'
        if "_" in filename:
                nextDirectionStr = os.path.splitext(os.path.basename(filename))[0].split('_')[-1]
                nextDirection = nextDirectionStrToInt(nextDirectionStr)
        else:
                nextDirection = LEFT
        icon = StepIcon(glob.glob(f'{imgRootPath}/YukiJudai/floor{floorNo}step{stepNo}_*.png'), 
                        name=name, 
                        nextDirection=nextDirection)
        stepIcons.append(icon)
stepIcons.sort(key=lambda icon: (icon.floorNo, icon.stepNo))

# mazeFloor1Step0 = Icon(f'{imgRootPath}/YukiJudai/floor1step0.png')
# mazeFloor1Step1 = Icon(f'{imgRootPath}/YukiJudai/floor1step1.png')
# mazeFloor1Step2 = Icon(f'{imgRootPath}/YukiJudai/floor1step2.png')
# mazeFloor1Step10 = Icon(f'{imgRootPath}/YukiJudai/floor1step10.png')
# mazeFloor2Step0 = Icon(f'{imgRootPath}/YukiJudai/floor2step0.png')
# mazeFloor2Step2 = MultiIcon(glob.glob(f'{imgRootPath}/YukiJudai/floor2step2_*.png'))
# mazeFloor2Step3 = Icon(f'{imgRootPath}/YukiJudai/floor2step3.png')
# mazeFloor2Step4 = MultiIcon(glob.glob(f'{imgRootPath}/YukiJudai/floor2step4_*.png'))
# mazeFloor2Step5  = Icon(f'{imgRootPath}/YukiJudai/floor2step5.png')
# mazeFloor2Step6 = MultiIcon(glob.glob(f'{imgRootPath}/YukiJudai/floor2step6_*.png'))
# mazeFloor2Step7 = MultiIcon(glob.glob(f'{imgRootPath}/YukiJudai/floor2step7_*.png'))
# mazeFloor2Step8  = Icon(f'{imgRootPath}/YukiJudai/floor2step8.png')
# mazeFloor2Step9 = MultiIcon(glob.glob(f'{imgRootPath}/YukiJudai/floor2step9_*.png'))
# mazeFloor2Step10  = Icon(f'{imgRootPath}/YukiJudai/floor2step10.png')
# mazeFloor2Step11  = Icon(f'{imgRootPath}/YukiJudai/floor2step11.png')
# mazeFloor3Step0 = Icon(f'{imgRootPath}/YukiJudai/floor3step0.png')
# mazeFloor3Step1 = Icon(f'{imgRootPath}/YukiJudai/floor3step1.png')
# mazeFloor3Step2 = Icon(f'{imgRootPath}/YukiJudai/floor3step2.png')
# mazeFloor3Step3 = Icon(f'{imgRootPath}/YukiJudai/floor3step3.png')
# mazeFloor3Step4 = Icon(f'{imgRootPath}/YukiJudai/floor3step4.png')
# mazeFloor3Step5 = MultiIcon(glob.glob(f'{imgRootPath}/YukiJudai/floor3step5_*.png'))
# mazeFloor3Step6 = Icon(f'{imgRootPath}/YukiJudai/floor3step6.png')
# mazeFloor3Step7 = Icon(f'{imgRootPath}/YukiJudai/floor3step7.png')
# mazeFloor3Step8 = Icon(f'{imgRootPath}/YukiJudai/floor3step8.png')
# mazeFloor3Step9 = Icon(f'{imgRootPath}/YukiJudai/floor3step9.png')
# mazeFloor3Step10 = Icon(f'{imgRootPath}/YukiJudai/floor3step10.png')
# mazeFloor3Step11 = Icon(f'{imgRootPath}/YukiJudai/floor3step11.png')
# mazeFloor3Step12 = Icon(f'{imgRootPath}/YukiJudai/floor3step12.png')
# mazeFloor3Step13 = Icon(f'{imgRootPath}/YukiJudai/floor3step13.png')
# mazeFloor3Step14 = Icon(f'{imgRootPath}/YukiJudai/floor3step14.png')
# mazeFloor3Step15 = Icon(f'{imgRootPath}/YukiJudai/floor3step15.png')
# mazeFloor3Step16 = Icon(f'{imgRootPath}/YukiJudai/floor3step16.png')
# mazeFloor3Step17 = Icon(f'{imgRootPath}/YukiJudai/floor3step17.png')
# mazeFloor3Step18 = Icon(f'{imgRootPath}/YukiJudai/floor3step18.png')
# mazeFloor3Step19 = Icon(f'{imgRootPath}/YukiJudai/floor3step19.png')
# mazeFloor3Step20 = Icon(f'{imgRootPath}/YukiJudai/floor3step20.png')
# mazeFloor3Step21 = Icon(f'{imgRootPath}/YukiJudai/floor3step21.png')
# mazeFloor3Step22 = Icon(f'{imgRootPath}/YukiJudai/floor3step22.png')
# mazeFloor3Step23 = Icon(f'{imgRootPath}/YukiJudai/floor3step23.png')
# mazeFloor3Step24 = Icon(f'{imgRootPath}/YukiJudai/floor3step24.png')

guessCoinIcon = Icon(f'{imgRootPath}/mazeSelectCoin2.png')
guessCoinSelect2 = Icon(f'{imgRootPath}/mazeSelectCoin2.png')

selectCardsLocator = Icon(f'{imgRootPath}/selectCardsLocator.png')
checkBlank = Icon(f'{imgRootPath}/checkBlank.png')
addToStorageIcon = Icon(f'{imgRootPath}/addToStorageIcon.png')
checkedIcon = MultiIcon(glob.glob(f'{imgRootPath}/checked*.png'))

