from icons import Icon, MultiIcon, CoordinateIcon, Yolov5Icon
import glob


# keysIcon = MultiIcon(glob.glob('img/base/key*.png'))
modelPath = '/Users/ed/Git/yolov5/runs/train/exp38/weights/best.pt'
classes = [ 'tv', 'seller', 'unionForce' , 'pvp' , 'key' , 'normalNpc' ]
# keysIcon = Yolov5Icon(modelPath, name='keysIcon', class_ = 'key', classes=classes)
keysIcon = MultiIcon(glob.glob('img/base/key*.png'))

homePageTransportGateSelected = Icon('img/home/channels/transport_gate_selected.png')
homePageTransportGateNonSelected = Icon('img/home/channels/transport_gate_non_selected.png')

homePagePvpSelected = Icon('img/home/channels/pvp_selected.png')
homePagePvpNonSelected = Icon('img/home/channels/pvp_non_selected.png')

homePageStoreSelected = Icon('img/home/channels/store_selected.png')
homePageStoreNonSelected = Icon('img/home/channels/store_non_selected.png')

homePageMonsterGateSelected = Icon('img/home/channels/monster_gate_selected.png')
homePageMonsterGateNonSelected = Icon('img/home/channels/monster_gate_non_selected.png')

homePageWorkshopSelected = Icon('img/home/channels/workshop_selected.png')
homePageWorkshopNonSelected = Icon('img/home/channels/workshop_non_selected.png')

normalNpcIcons = Yolov5Icon(modelPath, name='normalNpcIcons', class_ = 'normalNpc', classes=classes)
# normalNpcIcons = MultiIcon(glob.glob('img/npc/npc*.png'))

saiEnterButton = CoordinateIcon([[190, 620], [270, 650]])

switchWorldButton = CoordinateIcon(position=[(20, 210), (40, 230)])

DMWorldIcon = MultiIcon(['img/DMWorldIcon_load.png', 'img/DMWorldIcon_nonload.png'])
GXWorldIcon = MultiIcon(['img/GXWorldIcon_load.png', 'img/GXWorldIcon_nonload.png'])