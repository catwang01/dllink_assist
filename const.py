import pyautogui

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
PIXEL_WIDTH, PIXEL_HEIGHT = pyautogui.screenshot().size
SCALER = PIXEL_HEIGHT / SCREEN_HEIGHT

APP_WIDTH, APP_HEIGHT = 450, 720
APP_PIXEL_WIDTH, APP_PIXEL_HEIGHT = int(APP_WIDTH * SCALER), int(APP_HEIGHT * SCALER)

MIN_REFRESH_INTERVAL = 0.2
ICON_DEFAULT_SLEEP_CLICK_TIME = 0.2

SCREEN_SAMPLE_RATE = 1

YOLOV5_MODEL_PATH = '/Users/ed/Git/yolov5/runs/train/exp38/weights/best.pt'
YOLOV5_MODEL_CLASSES = [ 'tv', 'seller', 'unionForce' , 'pvp' , 'key' , 'normalNpc' ]

CARD_DICT_FILE = 'img/cards/cardMap.txt'
ROLE_DICT_FILE = 'img/roles/roleDict.txt'
