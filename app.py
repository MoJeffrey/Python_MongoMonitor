import json
from http import HTTPStatus
from bson.objectid import ObjectId, InvalidId
from flask import Flask, jsonify, render_template, request
import pymongo

import config

client = pymongo.MongoClient(host=config.MongoDB_IP,
                             port=config.MongoDB_Port,
                             username=config.MongoDB_Name,
                             ssl=True,
                             tlsCAFile=config.MongoDB_PEM,
                             password=config.MongoDB_Password)
client.list_database_names()
app = Flask(__name__)
app.DEBUG = True
app.jinja_env.auto_reload = True


@app.route('/')
def index():
    return render_template("List.html")


@app.route('/api/GetList', methods=['POST'])
def GetList():
    POST = request.form

    # 分頁
    limit = int(POST['limit'])
    Skip = limit * (int(POST['page']) - 1)

    # 選擇collection
    db = client[POST['DataBase']]
    collection = db[POST['Collection']]

    # 查詢時間
    Find = {}
    if POST['StartDate'] != "":
        StartDate = int(POST['StartDate'])
        Find['time'] = {"$gte": StartDate}

    if POST['EndDate'] != "":
        StartDate = int(POST['EndDate'])
        Find['time'].update({"$lte": StartDate})

    # 查詢ID
    if POST['ID'] != "":
        ID = POST['ID']
        Find['$or'] = [{"PlatformId": {"$regex": ID}},
                       {"ID": {"$regex": ID}},
                       {"MySqlID": {"$regex": ID}}]

    Data = collection.find(Find, {'data': 0})

    # 排序
    Data = Data.sort([('time', -1), ('_id', -1)]).limit(limit).skip(Skip)

    DataList = []
    for Item in Data:
        Item['_id'] = str(Item['_id'])
        DataList.append(Item)

    Data = {
        "code": 0,
        "count": collection.count_documents(Find),
        "data": DataList
    }
    return jsonify(Data)


@app.route('/api/GetDatabaseList', methods=['POST'])
def GetDatabaseList():
    Lists = client.list_database_names()

    Databases = []
    for Item in Lists:
        if Item == "admin" or Item == "config" or Item == "local":
            continue

        Databases.append({'id': Item, 'Name': Item})

    Data = {
        "code": HTTPStatus.OK,
        "data": Databases
    }
    return jsonify(Data)


@app.route('/api/GetCollectionList', methods=['POST'])
def GetCollectionList():
    POST = request.form
    if 'Name' not in POST:
        Data = {
            "code": HTTPStatus.BAD_REQUEST
        }
        return jsonify(Data)

    Lists = client[POST['Name']].list_collection_names()

    Databases = []
    for Item in Lists:
        Databases.append({'id': Item, 'Name': Item})

    Data = {
        "code": HTTPStatus.OK,
        "data": Databases
    }
    return jsonify(Data)


@app.route('/ViewData')
def ViewData():
    Get = request.args
    # 選擇collection
    db = client[Get.get("DB")]
    collection = db[Get.get('C')]

    # 查詢
    try:
        Find = {'_id': ObjectId(Get.get('ID'))}
        Data = collection.find_one(Find, {'_id': 0})
    except InvalidId:
        Find = {'_id': Get.get('ID')}
        Data = collection.find_one(Find, {'_id': 0})

    return render_template("ViewData.html", Data=Data)


@app.route('/api/GetMatchData', methods=['POST'])
def MatchData():
    POST = request.form
    # 獲取Match
    db = client[POST.get("DB")]
    ID = POST.get('ID')

    collection = db['Match']
    Find = {'_id': ID}
    Match = collection.find_one(Find, {'_id': 0})
    Match = Match['data']

    # 主隊
    Home = Match['HomeID']
    collection = db['Team']
    Find = {'_id': Home}
    Home = collection.find_one(Find, {'_id': 0})
    Home = Home['data']
    Home = Home['name']

    # 客隊
    Away = Match['AwayID']
    collection = db['Team']
    Find = {'_id': Away}
    Away = collection.find_one(Find, {'_id': 0})
    Away = Away['data']
    Away = Away['name']

    # 聯賽
    League = Match['League']
    collection = db['League']
    Find = {'_id': League}
    League = collection.find_one(Find, {'_id': 0})
    League = League['data']
    League = League['name']

    Data = {
        "Home": Home,
        "Away": Away,
        "League": League,
        "Time": Match['Time'],
    }

    Data = {
        "code": HTTPStatus.OK,
        'data': Data
    }
    return jsonify(Data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
