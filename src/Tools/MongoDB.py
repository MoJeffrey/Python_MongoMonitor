"""
儲存資料到MongoDB工具
DataBase = 平台名稱
集合 = 腳本名稱
"""
from time import time

from pymongo import MongoClient
from pymongo.database import Database


class MongoDB:
    __NowDatabase: Database = None
    Client: MongoClient = None

    def __init__(self, host: str, port: int,
                 username: str, password: str,
                 tlsCAFile: str = None):

        keys = {
            "host": host,
            "port": port,
            "username": username,
            "password": password,
            "maxPoolSize": 100,
            "retryWrites": False
        }

        if tlsCAFile is not None:
            keys.update({"ssl": True, "tlsCAFile": tlsCAFile})

        client = MongoClient(**keys)
        MongoDB.Client = client

    @staticmethod
    def GetMongoDB() -> MongoClient:
        return MongoDB.Client

    @staticmethod
    def GetDatabase() -> Database:
        return MongoDB.__NowDatabase

    @staticmethod
    def SaveConfigFunc(Config: dict) -> None:
        MongoDB.StoreData('Config', Config)

    @staticmethod
    def CheckConfigFunc(Name: str) -> bool:
        Config = MongoDB.GetOne('Config', {'Name': Name})
        if Config is None:
            return False
        return True

    @staticmethod
    def SetDatabase(DatabaseName: str) -> None:
        """
        选择使用的DataBase Name
        :param DatabaseName:
        :return:
        """
        MongoDB.__NowDatabase = MongoDB.Client[DatabaseName]

    @staticmethod
    def Close():
        if MongoDB.Client is None:
            return
        return MongoDB.Client.close()

    @staticmethod
    def Exist(Collection: str, Id: str, ExpansionData: dict = None) -> bool:
        """
        該數據是否存在
        :return:
        """
        if ExpansionData is None:
            ExpansionData = {}
        Find = {'PlatformId': Id}
        Find.update(ExpansionData)
        count = MongoDB.__NowDatabase[Collection].count_documents(Find)
        return False if count == 0 else True

    @staticmethod
    def UpdateOne(Collection: str, Find: dict, UpdateData: dict) -> None:
        """
        更新一條數據
        :param Collection:
        :param Find:
        :param UpdateData:
        :return:
        """
        MongoDB.__NowDatabase[Collection].update_one(Find, UpdateData)

    @staticmethod
    def GetOne(Collection: str, Find: dict) -> dict:
        """
        傳回查到的一條數據
        :param Collection:
        :param Find:
        :return:
        """
        return MongoDB.__NowDatabase[Collection].find_one(Find)

    @staticmethod
    def GetList(Collection: str, Find: dict) -> list:
        """
        傳回查到的列表
        :param Collection:
        :param Find:
        :return:
        """
        DataList = []
        for Item in MongoDB.__NowDatabase[Collection].find(Find):
            DataList.append(Item)
        return DataList

    @staticmethod
    def StoreData(Collection: str, Data: dict) -> None:
        """
        储存数据
        直接存入传入的Dict
        :param Collection:
        :param Data:
        :return:
        """
        MongoDB.__NowDatabase[Collection].insert_one(Data)

    @staticmethod
    def StoreSpecificData(Data: dict,
                          MySqlID: int,
                          ID: str,
                          Type: str,
                          Time: int,
                          ExpansionData: dict) -> None:
        """
        儲存指定資料
        :param Data: 該數據內容
        :param MySqlID: 儲存在數據中心的ID
        :param ID: 該平台給予的ID
        :param Type: 該數據的類型 e.g Team, League
        :param Time: 該數據儲存時間
        :param ExpansionData: 擴充資料
        :return:
        """
        SaveData = {
            'data': Data,
            'MySqlID': str(MySqlID),
            'time': Time,
            'PlatformId': ID
        }
        SaveData.update(ExpansionData)
        MongoDB.__NowDatabase[Type].insert_one(SaveData)

    @staticmethod
    def Del(Collection: str, Data: dict) -> None:
        """
        删除
        :param Collection:
        :param Data:
        :return:
        """
        MongoDB.__NowDatabase[Collection].delete_one(Data)

    @staticmethod
    def AddTaskToMongoDB(Theme: str, Type: str, Parameter: str) -> None:
        """
        添加任務到MongoDB，定時讀取時執行
        :return:
        """
        Data = {
            "Theme": Theme,
            "Type": Type,
            "Parameter": Parameter,
        }
        MongoDB.StoreData("Task", Data)
