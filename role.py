class RoleCollection:

    def __init__(self, configFile=None) -> None:
        self.roleDict = self.init(configFile)

    def init(self, configFile=None):
        roleDict = {}
        if configFile is None:
            return roleDict
        with open(configFile) as f:
            for line in f:
                line = line.strip()
                if line == "": continue
                args =  line.split(',')
                roleDict[args[0]] = Role(*args)
        return roleDict

    def getRole(self, name):
        if name not in self.roleDict:
            raise Exception(f"No such role called {name}")
        return self.roleDict[name]

class Role:

    def __init__(self, name, homePageImgPath, avatarPath, world, chineseName) -> None:
        self.name = name
        self.homePageImgPath = homePageImgPath
        self.avatarPath = avatarPath
        self.world = world
        self.chineseName = chineseName
