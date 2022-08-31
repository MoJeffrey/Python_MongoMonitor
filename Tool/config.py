import configparser
import os


class config(object):
    """
    MongoDB
    """
    MongoDB_IP = None
    MongoDB_Port = None
    MongoDB_Name = None
    MongoDB_Password = None
    MongoDB_tlsCAFile = None
    MongoDB_Database = None

    def Init(self, ConfigFile: str = None) -> None:
        """
        初始化配置文件
        :param ConfigFile:
        :return:
        """
        self.__ReadConfigFile(ConfigFile)
        self.__Analyze()

    def __ReadConfigFile(self, ConfigFile: str = None) -> None:
        """
        讀取配置文件

        如果沒有傳入文件路徑
        則在環境變量中獲取
        :param ConfigFile:
        :return:
        """
        if ConfigFile is None:
            if "CONFIG_PATH" not in os.environ:
                raise NoSetCONFIGError()
            else:
                self.__CONFIG_PATH = os.environ['CONFIG_PATH']
        else:
            self.__CONFIG_PATH = ConfigFile

        self.__File = configparser.ConfigParser()
        self.__File.read(self.__CONFIG_PATH, encoding="utf-8")

    def __Analyze(self) -> None:
        """
        解析配置文檔
        :return:
        """
        self.__Analyze_MongoDB()

    def __Analyze_MongoDB(self) -> None:
        """
        在配置文檔中解析MongoDB 的配置資料
        :return:
        """
        MongoDBConfig = self.__File['MongoDB']
        config.MongoDB_IP = MongoDBConfig['IP']
        config.MongoDB_tlsCAFile = MongoDBConfig['tlsCAFile']
        config.MongoDB_Port = MongoDBConfig.getint("Port")
        config.MongoDB_Name = MongoDBConfig['Name']
        config.MongoDB_Password = MongoDBConfig['Password']

class NoSetCONFIGError(Exception):

    def __init__(self):
        super().__init__(self)

    def __str__(self):
        return "no environment variables configured : CONFIG_PATH"
