# LabelTool : A Tool for create the label applicate on Object detection #
一種製作標籤的工具應用在物件偵測上：訓練object detect neural network前的資料製作 
- Utilize which programming language/使用的程式語言 ： Python 3.6 
- Import package/引入的套件 ： os、tkinter、PIL(Image,ImageTk)、functools(partial)、json、shutil 
- Dependencies/需要套件 : [anaconda3-5.1 (python 3.6)](https://repo.continuum.io/archive/) 
- Download/下載 : [LabelTool](https://github.com/kevinbear/LabelTool)

## How to use/如何使用: ##
 ### 1. 以下會介紹Label_Maker的畫面與控制方式與按鈕功能 ###
 A. ImageDisplay分為三大部分:
  <img width="500" align=right alt="2018-05-21 3 58 12" src="https://user-images.githubusercontent.com/13515719/40297279-d9ff418c-5d11-11e8-9a49-38e1d58f17dd.png">
 1. 輸入路徑載入：  
    > (1)  路徑名稱：Directory Path  
    > (2)  路徑輸入位置：＿＿＿＿＿＿＿＿＿  
    > (3)  載入按鈕：LOAD  
 2. 顯示：  
     > (1)  畫布：顯示圖片畫面與邊界匡的位置  
     > (2)  Image Name：顯示目前圖片  
     > (3)  x:,y:：顯示鼠標位置 
 3. 圖片位移控制：
     > (1)  <<Prev：前一頁  
     > (2)  Next>>：下一頁  
     > (3)  (Image No.:)(Jump)：直接跳躍至第幾張圖片  
     > (4)Path:資料集路徑

 B. Attribute Options分為四大部分： 
 
 4. 基本圖片資料：  
     > (1)Size:圖片 w x h  
     > (2)Scale:放大或縮效的 w x h  
     > (3)Name:圖片名稱  
     > (4)Path:資料集路徑
 5. 邊界框：顯示在畫布上邊界框的位置
      > (1)< delete all >:刪除所有邊界框包含在圖片上的位置  
      > (2)<->:刪除單一邊界框包含圖片上的位置  
 6. 類別屬性：可以自行增加想要的類別，包含名稱、編號、顏色  
      > (1)<+>:增加屬性  
      > (2)<->:移除屬性  
 7. 標籤輸出格式  
      >(1)Yolo Label:label格式選擇，可以自訂路徑名稱(請在打勾前先輸入，否則系統會輸出至預設路徑Ylabel)  
      >(2)Normal Label:label格式選擇，可以自訂路徑名稱請在打勾前先輸入，否則系統會輸出至預設路徑Nlabel)  
      >(3)Gerenate button:產生目前資料及已經標記過的標籤檔至勾選的標籤路徑中
      
### 2. Open Terminal or Command Prompt / 開啟終端機或命令提示字元 ###

### 3. Enter the following command / 輸入以下指令開啟Label_Maker程式 ###
  ```bash
    $ cd ~/your/computer/path/LabelTool
    $ python Label_Maker.py
  ```

### 4. Copy the DataSet Path on Label_Maker "Directory Path" Entry and press "LOAD" button / 複製資料集的路徑至Label_Maker的輸入欄並按下LOAD  ###

### 5. WorkFlow/工作流程： 
- (1)輸入圖片路徑載入圖片  
- (2)新增屬性  
- (3)點及屬性才可畫框不然會報錯  
- (4)畫邊界框至畫布圖片的物件上   
- (5)如果劃錯可以至邊界框欄刪除框   
- (6)點選下一頁或前一頁繼續框選，直到所有資料集的圖片都匡選完  
- (7)勾選輸出模式，點選產生，即完成  
 
### 6. [Video tutorial](https://www.youtube.com/watch?time_continue=2&v=SLLNUS_MG4w)
#### Note:
     - 1. Directory Path --> 資料集的路徑(請不要把照片的檔案名稱也放入)  
     - 2. DataSet --> 資料集的格式請都放入圖片檔(*.png ,*.jpg ,*.JPEG ,*.tif ,etc...)，請不要放入不是圖片檔的檔案格式，否則會有錯誤
