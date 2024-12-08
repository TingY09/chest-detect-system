from selenium import webdriver  # 瀏覽器驅動模組
from webdriver_manager.chrome import ChromeDriverManager  # Chrome瀏覽器驅動模組
from selenium.webdriver.chrome.options import Options  # 瀏覽器選項設定模組
from selenium.webdriver.common.by import By  # 定位元素模組
import time  # 時間模組

driver = webdriver.Chrome()

# 打開頁面
driver.get("https://ce68-2001-b011-e606-5d96-246e-262a-9cb1-5578.ngrok-free.app/login")  # 本地網址

# 定位帳號欄位
email = driver.find_element(By.ID, "username")
 
# 定位密碼欄位
password = driver.find_element(By.ID, "password")

# 輸入帳號欄位資料
email.send_keys("B")
 
# 輸入密碼欄位資料
password.send_keys("B1234567")

password.submit()