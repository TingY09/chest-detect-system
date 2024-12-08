from selenium import webdriver  # 瀏覽器驅動模組
from webdriver_manager.chrome import ChromeDriverManager  # Chrome瀏覽器驅動模組
from selenium.webdriver.chrome.options import Options  # 瀏覽器選項設定模組
from selenium.webdriver.common.by import By  # 定位元素模組
import time  # 時間模組

driver = webdriver.Chrome()

# 打開頁面
driver.get("http://127.0.0.1:5000/about")  # 本地網址
# <div class="btnContainer">
#         <button class="">⟨</button>
#         <button class="">⟩</button>
#       </div>

submit_button_prev= driver.find_element(By.CSS_SELECTOR, ".btn btn-prev")
driver.execute_script("arguments[0].click();", submit_button_prev)

submit_button_prev= driver.find_element(By.CSS_SELECTOR, ".btn btn-next")
driver.execute_script("arguments[0].click();", submit_button_prev)