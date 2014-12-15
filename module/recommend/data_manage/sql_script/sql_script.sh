#localDir=$(pwd)/module/recommend/data_manage/sql_script
localDir=$(pwd)/sql_script
python $localDir/sql_script.py $1 < $localDir/sql_script.txt | mysql -uroot
