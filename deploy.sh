echo "deploy $EnvName start!"
echo "$Now_IP"
mkdir -p ~/.ssh
chmod 700 ~/.ssh
ssh-keyscan $Now_IP > ~/.ssh/known_hosts
chmod 644 ~/.ssh/known_hosts
echo "$Now_SSH" > /home/Dev_SSH.cer
chmod 400 /home/Dev_SSH.cer
ssh -i /home/Dev_SSH.cer $Now_User@$Now_IP > /home/Deploy.log 2>&1 << exitDeploy
sudo su

# 中轉
# ssh -i $SSHHub > /home/Deploy.log 2>&1 << exitDeploy
if ["$SSHHub" != ""]; 
  then
    ${SSHHub} > /home/Deploy.log 2>&1;
    sudo su;
  fi

# 創建工作目錄
mkdir -p /home/BGX/TheSportsWebSocket$EnvName
cd /home/BGX/TheSportsWebSocket$EnvName

# 拉取最新代碼
git init
git remote add origin $CI_REPOSITORY_URL
git fetch --all
git reset --hard origin/main
git pull origin main

# 設置 Config File
echo "$Now_Config" > ./src/config/Config.ini

docker build -t thesports_websocket .
docker stop TheSportsWebSocket$EnvName
docker container rm TheSportsWebSocket$EnvName

# 需要选择采用那个Confi File
docker run --restart=always -e CONFIG_PATH="config/Config.ini" -it -d --name=TheSportsWebSocket$EnvName thesports_websocket
docker ps

# 退出中轉
if ["$SSHHub" != ""];
then
  exit;
  exitDeploy;
  cat /home/Deploy.log;
fi

exit
exitDeploy
cat /home/Deploy.log

echo "deploy $EnvName done!"