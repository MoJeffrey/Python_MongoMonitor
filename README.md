# Python-EC2-Mongo-Monitor

![AppVeyor](https://img.shields.io/static/v1?label=MoJeffrey&message=Python-EC2-Mongo-Monitor&color=blue)


## 前言
該項目主要用於搜索Mongo 日誌， 用於查看DataSource 源數據 的處理。 <br>

## 程序工作流程
1. 根據環境變量 CONFIG_PATH 獲取配置文檔
2. 根據配置文檔連接 Mongo
3. 啟動輕量級 Web Server (Flask)

## 環境依賴
Python 3.9

## 開發環境部署
懶

## EC2 部署 (手動部署)

### Ubuntu 20.04

1. 安裝 docker (已安裝則無視)
    ```shell
    # apt包列表完全更新
    apt-get update -y
    # 安装Get
    apt install git
    # 安裝Docker
    curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
    service docker start
    ```
   
2. 修改Config 和 Deploy
    ```shell
    # 創建目錄
    mkdir -p /home/Python_MongoMonitor
    cd /home/Python_MongoMonitor
   
    # 拉取最新代碼
    git init
    git remote add origin [該Project Pull URL]
    git pull origin main
    
    # 修改配置文件/home/Python_MongoMonitor/src/config/Temp.ini
    
    # 打包鏡像 和 運行
    docker build -t python_mongo_monitor .
    docker stop Python_MongoMonitor
    docker container rm Python_MongoMonitor
    
    # 需要选择采用那个Confi File
    docker run --restart=always -e CONFIG_PATH="config/Temp.ini" -t -p 8000:8000 --name=Python_MongoMonitor python_mongo_monitor

    ```

## 文件結構
```
.
│   .gitignore
│   .gitlab-ci.yml --CICD
│   Dockerfile --Docker
│   README.md
│
├───doc --相關詳細資料
│
├───Script --相關腳本文件
│
├───src --程序主代碼
│   │   app.py --程序入口
│   │   requirement.txt --依賴
│   ├───config --配置文件目錄
│   ├───static --靜態文件 Ccs,Js,Img
│   ├───templates --html 代碼
│   └───Tools --鏈接各種第三方工具代碼
│
└───UnitTest --測試代碼
```
