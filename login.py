from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 初始化 WebDriver
driver = webdriver.Chrome()  # 確保 ChromeDriver 已安裝並配置好

try:
    # 開啟目標網頁
    driver.get("https://ce68-2001-b011-e606-5d96-246e-262a-9cb1-5578.ngrok-free.app/login")  # 替換成表單所在的實際 URL

    # 顯式等待直到輸入框出現在頁面上
    wait = WebDriverWait(driver, 10)

    # 找到 username 輸入框並輸入內容
    username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
    username_input.clear()  # 清空輸入框，防止有預設值
    username_input.send_keys("B")  # 替換成實際的使用者名稱

    # 找到 password 輸入框並輸入內容
    password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
    password_input.clear()  # 清空輸入框
    password_input.send_keys("B1234567")  # 替換成實際的密碼

    # 找到並點擊登入按鈕
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    login_button.click()

    # # 驗證登入是否成功（可選）
    # # 這裡可以檢查登入後是否跳轉到預期的頁面，例如透過檢查某個特定元素是否存在
    # success_element = wait.until(EC.presence_of_element_located((By.ID, "success_element_id")))
    # print("登入成功")

except Exception as e:
    print("操作出現問題：", e)

finally:
    # 關閉瀏覽器
    driver.quit()
