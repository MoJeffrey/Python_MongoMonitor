源数数据查看 Web

用于连接MongoDB 查看收到的原始数据

追查数据走向和解析结果

http://54.151.135.80:8000/


# BGX-Python-Lambda-TheSports-Parse

![AppVeyor](https://img.shields.io/static/v1?label=MoJeffrey&message=BGX-Python-EC2-Mongo-Monitor&color=blue)


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

## AWS 環境部署

### Ubuntu 20.04

1. 安裝 docker
    ```shell
    # apt包列表完全更新
    apt-get update -y
    # 安装Get
    apt install git
    # 安裝Docker
    curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
    service docker start
    ```
   
2. 進入 Python 3.9 環境
    ```shell
    # 創建目錄
    mkdir -p /home/BGX/TheSportsParse
    cd /home/BGX/TheSportsParse
   
    # 拉取最新代碼
    git init
    git remote add origin http://gitlab.bgx.com.hk/jeffrey/pythonlambda_thesportsrawdataparse.git
    git pull origin main
   
    # 建立容器 已經創建則無視
    docker run -it -d --name=PythonLambda -v /home/BGX:/home/BGX python:3.9 bash
    docker exec -it PythonLambda bash
   
    # 安裝vim 用於修改config File
    apt-get update
    apt-get install vim
    ```
   
3. 安裝 awscli 和 SAM
    ```shell
    # 安裝 unzip
    apt install unzip
    # 安裝 awscli2
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    ./aws/install
    # 檢查 AWS CLI 版本2 內容
    aws --version
   
    # 安裝
    pip install aws-sam-cli
    # 驗證安裝
    sam --version
    ```

4. 設置AWS CLI 賬號
   * 找到該文件
      ```
      .
      └───AWS
           └───Temp
      ```
   * 複製重命名 e.g Dev
      ```
      .
      └───AWS
          ├───Temp
          └───Dev
      ```
   * 配置 ./AWS/Dev/credentials.csv
      ```cvs
      User Name,Access Key ID,Secret Access key
      {Name},{KeyId},{key
      ```
   * 導入賬號
      ```shell
      # 導入賬號
      aws configure import --csv file:///home/BGX/TheSportsAPIReceiver/AWS/Dev/Dev.csv
      # 設置地區
      aws configure set region ap-southeast-1 --profile Dev
      # 查看賬號是否成功導入
      aws configure list --profile Dev
      ```

5. Deploy
    ```shell
    # 添加 Lambda Function 運行配置文件 (我就不教了。看名字修改參數)
    cd /home/BGX/TheSportsParse/src/config
    vi ./Temp.ini
    
    # 修改Deploy config 文件 (我就不教了。看名字修改參數)
    cd /home/BGX/AWS/Dev
    vi ./template.yaml
    
    # 創建S3 有則跳過
    aws s3 mb s3://python-lanbda-thesports-parse --profile Dev
   
    # Deploy
    cd /home/BGX/TheSportsParse
    sam build --template ./AWS/Dev/template.yaml --build-dir ./.aws-sam/build
    sam package --template-file ./.aws-sam/build/template.yaml --output-template-file ./.aws-sam/build/packaged-template.yaml --s3-bucket python-lanbda-thesports-parse --profile Dev
    sam deploy --template-file ./.aws-sam/build/packaged-template.yaml --stack-name PythonLambdaTheSportsParse --s3-bucket python-lanbda-thesports-parse --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM --profile Dev
    ```
   
### Windows
懶

## 文件結構
```
.
│   .gitignore
│   Jenkinsfile --CICD
│   Jenkinsfile.deploy --CICD
│   README.md
│   sonar-project.properties --code scanner
│   template.yaml
│
├─── AWS -- AWS Deploy 文件
│
│
├───doc --相關詳細資料
│
├───events --觸發數據
│
├───ProduceSQL --去生成該數據源基礎數據的SQL Init 文件， 避免大量數據添加造成Lambda負擔
│
├───src --程序主代碼
│   │   app.py --程序入口
│   ├───config --配置文件目錄
│   ├───TheSports --TheSports libs
│   └───Tools --鏈接各種第三方工具代碼
│
└───UnitTest --測試代碼
```
