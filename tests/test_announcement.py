from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import unittest

class TestAnnouncement(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """初始化瀏覽器，執行所有測試前的設置"""
        cls.driver = webdriver.Chrome()  # 確保 ChromeDriver 已安裝並配置好
        cls.driver.get("https://0a1e-61-216-55-185.ngrok-free.app/login")  # 替換成實際 URL
        cls.wait = WebDriverWait(cls.driver, 10)

    def test_announcement(self):

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


        # 等待並滾動頁面確保按鈕可見
        submit_button_next = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-next")))
        submit_button_prev = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn-prev")))

        for i in range(3):
            # 點擊下一頁按鈕
            submit_button_next.click()
            time.sleep(1)  # 等待頁面過渡效果
        for i in range(3):
            # 點擊上一頁按鈕
            submit_button_prev.click()
            time.sleep(1)  # 等待頁面過渡效果

        # 可以加上時間等待，確保操作能完成
        time.sleep(5)

    @classmethod
    def tearDownClass(cls):
        """測試結束後關閉瀏覽器"""
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
