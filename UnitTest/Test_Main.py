import os
import unittest
import time

from loguru import logger
import pymongo

from Tools.config import config

if 'CI_PROJECT_NAME' not in os.environ:
    os.environ['CI_PROJECT_NAME'] = 'MatchServerMongoMonitor'

logger.add("./UnitTest.log")


class ConfigTestCase(unittest.TestCase):
    """
    驗證Config 配置是否正確

    1. 關鍵字是否齊全
    """
    ConfigFilePath = ''
    def setUp(self) -> None:
        logger.info("啟動")
        config().Init()

    @staticmethod
    def test_MongoDB():
        client = pymongo.MongoClient(host=config.MongoDB_IP,
                                     port=config.MongoDB_Port,
                                     username=config.MongoDB_Name,
                                     ssl=True,
                                     tlsCAFile=config.MongoDB_tlsCAFile,
                                     password=config.MongoDB_Password)
        client.list_database_names()


if __name__ == '__main__':
    unittest.main()
