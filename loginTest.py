from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

# 打開頁面
driver.get("https://ce68-2001-b011-e606-5d96-246e-262a-9cb1-5578.ngrok-free.app/login")  # 本地網址

# 定位帳號欄位
email = driver.find_element(By.ID,"username")
 
# 定位密碼欄位
password = driver.find_element(By.ID, "password")

# 輸入帳號欄位資料
email.send_keys("B")
 
# 輸入密碼欄位資料
password.send_keys("B1234567")

password.submit()

submit_button1 = driver.find_element(By.ID, "detect_page")
driver.execute_script("arguments[0].click();", submit_button1)
try:
    # 上傳圖片
    upload_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "file-input"))
    )
    upload_element.send_keys("C:/Users/user/OneDrive/桌面/胸腔辨識/00028174_000.png")

    # 點擊辨識按鈕
    submit_button = driver.find_element(By.ID, "predict-button")
    driver.execute_script("arguments[0].click();", submit_button)

    # 加入延遲，確保結果返回
    time.sleep(5)  # 等待5秒

    # 查找結果
    result_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "detect-disease"))
    )
    
    # 列印出 result_element 的文本
    print(result_element.text)
    
    # 驗證結果是否正確
    assert "辨識結果: Cardiomegaly" in result_element.text

    data_saved_button = driver.find_element(By.ID, "data-saved")
    driver.execute_script("arguments[0].click();", data_saved_button)
finally:
    driver.quit()
    print("Test Finished")
