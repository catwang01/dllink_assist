from icons import CoordinateIcon, Icon, MultiIcon
import glob

imgPath = 'img/duel'

duelButton = Icon('img/duelButton.png', colorCloseThreshold=1)
autoDuelButton = MultiIcon(glob.glob('img/autoDuelButton*.png'), colorCloseThreshold=1, clickSleepTime=1)
autoDuelOffButton = Icon('img/autoDuelOffButton.png')

saveVideoButton = Icon('img/saveVideo.png')
recordButton = Icon('img/recordButton.png')

duelResultsPageTitle = MultiIcon(glob.glob('img/duelResultsPageTitle*.png'))
duelWinIcon  = Icon('img/duelWinIcon.png')
leftZeroAutoButton = Icon(f'img/transportGateDuel/leftZeroButton.png')

autoControlButton = Icon(f'img/duel/autoControlButton.png')
autoControlOffButton = Icon(f'img/duel/autoControlOffButton.png')

actionButton = Icon(f'{imgPath}/actionButton.png', clickSleepTime=0.1)
battleButton = MultiIcon(glob.glob(f'{imgPath}/battleButton*.png'), similarity=0.6, colorCloseThreshold=1, clickSleepTime=0.1)
endTurnButton = MultiIcon(glob.glob(f'{imgPath}/endTurnButton*.png'), similarity=0.6, colorCloseThreshold=1, clickSleepTime=0.1)

blankPlace = CoordinateIcon(position=[(190, 560), (275, 570)], name='blackPlace', clickSleepTime=0)
skillButton = Icon(f'{imgPath}/skillButton.png')
firstTurnIcon = Icon(f'{imgPath}/firstTurnIcon.png', similarity=0.95)

perspectiveSwitchButton = Icon(f'{imgPath}/perspectiveSwitchButton.png')
settingButton = Icon(f'{imgPath}/settingButton.png', colorCloseThreshold=1)

useSkillButton = Icon(f'{imgPath}/useSkillButton.png', clickSleepTime=1.5)
useSkillPageTitle = Icon(f'{imgPath}/useSkillPageTitle.png')

yourMainPhraseIcon = Icon(f'{imgPath}/yourMainPhraseIcon.png', similarity=0.95)
yourBattlePhraseIcon = Icon(f'{imgPath}/yourBattlePhraseIcon.png', similarity=0.95)
yourDrawCardPhraseIcon = Icon(f'{imgPath}/yourDrawCardPhraseIcon.png', similarity=0.95)
rivalPharseIcon = Icon(f'{imgPath}/rivalPhraseIcon.png', similarity=0.95)

setCardButton = Icon(f'{imgPath}/setCardButton.png')
sumonButton = Icon(f'{imgPath}/sumonButton.png', clickSleepTime=3)
useCardButton = Icon(f'{imgPath}/useCardButton.png', clickSleepTime=3)

selectTargetPageTitle = Icon(f'{imgPath}/selectTargetPageTitle.png')
selectTargetConfirmButton = Icon(f'{imgPath}/selectTargetConfirmButton.png', colorCloseThreshold=0.1)