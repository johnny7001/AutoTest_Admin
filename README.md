# 自動化測試-廠商後台-聯絡人信箱-有無分號測試  
####
* 填入的信箱大於一個以上時,需用分號來做區分,否則會阻擋
* 範例：  
* Pass = abc123@gmail.com;johnny@gmail.com
* Fail = abc123@gmail.comjohnny@gmail.com
* 目前在githubActions執行兩種情況的腳本, 執行時間星期一到日每日9:30及14:00, 會通知寄信測試結果
