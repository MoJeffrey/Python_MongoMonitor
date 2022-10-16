import os
import unittest

from loguru import logger

from Tools.config import config
from Tools.MongoDB import MongoDB

if 'CI_PROJECT_NAME' not in os.environ:
    os.environ['CI_PROJECT_NAME'] = 'MatchServerMongoMonitor'

logger.add("./UnitTest.log")
config().Init()


class ConfigTestCase(unittest.TestCase):
    """
    驗證Config 配置是否正確

    1. 關鍵字是否齊全
    """
    ConfigFilePath = ''

    @staticmethod
    def test_MongoDB():
        logger.info("測試 MongoDB 連接")
        MongoDB(host=config.MongoDB_IP, port=config.MongoDB_Port,
                username=config.MongoDB_Name, tlsCAFile=config.MongoDB_tlsCAFile,
                password=config.MongoDB_Password)
        client = MongoDB.GetMongoDB()
        NameList = client.list_database_names()
        logger.info(NameList)


if __name__ == '__main__':
    unittest.main()
