from selenium import webdriver
import unittest
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

class TestPatient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """初始化瀏覽器，執行所有測試前的設置"""
        cls.driver = webdriver.Chrome()  # 確保 ChromeDriver 已安裝並配置好
        cls.driver.get("https://7545-61-216-116-70.ngrok-free.app/login")  # 替換成實際 URL
        cls.wait = WebDriverWait(cls.driver, 10)

    def test_patient(self):

        # 點擊 Visit Site 按鈕
        visit_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Visit Site')]"))
        )
        visit_button.click()
        time.sleep(2)  # 等待頁面過渡效果

        # 找到 username 輸入框並輸入內容
        username_input = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_input.clear()  # 清空輸入框，防止有預設值
        username_input.send_keys("B")  # 替換成實際的使用者名稱

        # 找到 password 輸入框並輸入內容
        password_input = self.wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_input.clear()  # 清空輸入框
        password_input.send_keys("B1234567")  # 替換成實際的密碼

        # 登入按鈕點擊
        login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        login_button.click()


        submit_button1 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '病患總覽')]")))
        submit_button1.click()

        folder_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//p[contains(text(), 'A123456789')]")))
        folder_button.click()

        folder_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '修改資料')]")))
        folder_button.click()

        patient_name_input= self.wait.until(EC.presence_of_element_located((By.ID, "name-input")))
        patient_name_input.clear() 
        patient_name_input.send_keys("Tom")  # 替換名字

        saved_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '儲存資料')]")))
        saved_button.click()
        print("修改成功")
    @classmethod
    def tearDownClass(cls):
        """測試結束後關閉瀏覽器"""
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()