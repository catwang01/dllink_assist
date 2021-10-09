import pytest

from inference import DetectObject
from const import YOLOV5_MODEL_CLASSES, YOLOV5_MODEL_PATH

model = DetectObject(YOLOV5_MODEL_PATH, YOLOV5_MODEL_CLASSES)

class TestYolov5:

    @pytest.mark.parametrize('imgPath,expected', [
        ('test/test_yolov5/screenshot1.png', [0, 0, 0, 1, 0, 2])
    ])
    def test(self, imgPath, expected):
        res = model.detect(imgPath)
        nDetected =  [0] * len(YOLOV5_MODEL_CLASSES)
        for detected in res[1]:
            class_ = detected['cls']
            nDetected[class_] += 1
        assert nDetected == expected



        
