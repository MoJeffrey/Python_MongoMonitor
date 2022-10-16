echo "Unit test start!"
echo "$CI_PROJECT_NAME!"
cp $Now_Config_Path ./src/config/Config.ini
export PYTHONPATH=$CI_PROJECT_DIR/src
export CONFIG_PATH=./config/Config.ini
cd ./src
pip install -r requirement.txt
pytest ../UnitTest/Test_Main.py --junitxml=Report.xml
python ../UnitTest/Test_Main.py
echo "Unit test done!"