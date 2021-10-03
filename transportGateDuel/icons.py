from icons import Icon, MultiIcon
import glob
import os

imgDirPath = 'img/transportGateDuel'


transportGatePageTitle = Icon(f'{imgDirPath}/transportGateTitle.png')
selectTransportGateRoles = Icon(f'{imgDirPath}/switchTransportGateRoles.png')
selectTransportGateBar = Icon(f'{imgDirPath}/switchTransportGateBar.png')

gxTransportGateItem = Icon(f'{imgDirPath}/gxTransportGate.png')
dmTransportGateItem = Icon(f'{imgDirPath}/dmTransportGate.png')

yukijudaiIcon = Icon(f'{imgDirPath}/yukijudai.png')
tianjoyinIcon = Icon(f'{imgDirPath}/tianjioyin.png')
mutouyougiIcon = Icon(f'{imgDirPath}/mutouyougi.png')

transportGateDuelButton = Icon(f'{imgDirPath}/duelButton.png')
levelSelected = MultiIcon(glob.glob(f'{imgDirPath}/levels/level*Selected.png'), similarity=0.95)
level10Button = Icon(f'{imgDirPath}/levels/level10.png', similarity=0.95)
level20Button = Icon(f'{imgDirPath}/levels/level20.png', similarity=0.95)
level30Button = Icon(f'{imgDirPath}/levels/level30.png', similarity=0.95)
level40Button = Icon(f'{imgDirPath}/levels/level40.png', similarity=0.95)

npcAlreadyExistsTitle = Icon(f'{imgDirPath}/npcAlreadyExistsTitle.png', similarity=0.95)