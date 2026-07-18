import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
# Sử dụng webdriver-manager để tự động tải driver tương thích với từng máy
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService

# =========================================================================
# CẤU HÌNH
# =========================================================================
BROWSER_TYPE = "chrome" 
TARGET_URL = "https://ht60-ui.github.io/test/"

def setup_options(options_obj):
    options_obj.add_experimental_option("excludeSwitches", ["enable-automation"])
    options_obj.add_experimental_option('useAutomationExtension', False)
    # Tắt bảng hỏi quyền tự động ở mức trình duyệt
    prefs = {
        "profile.default_content_setting_values.geolocation": 1,
        "profile.managed_default_content_settings.geolocation": 1
    }
    options_obj.add_experimental_option("prefs", prefs)
    options_obj.add_argument("--start-maximized")
    options_obj.add_argument("--no-sandbox")
    options_obj.add_argument("--disable-dev-shm-usage")
    return options_obj

drivers = []
selected_browsers = [b.strip().lower() for b in BROWSER_TYPE.split(",")]

for browser in selected_browsers:
    try:
        print(f"Đang khởi tạo trình duyệt: {browser.upper()}...")
        
        if browser == "chrome":
            options = setup_options(ChromeOptions())
            # Tự động tải driver phù hợp với máy hiện tại
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
        elif browser == "edge":
            options = setup_options(EdgeOptions())
            # Tự động tải driver phù hợp với máy hiện tại
            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=options)
        
        else:
            print(f"⚠️ Trình duyệt '{browser}' không hỗ trợ tự động driver, bỏ qua.")
            continue
        
        # Cấp quyền Geolocation ngầm bằng CDP
        driver.execute_cdp_cmd("Browser.grantPermissions", {
            "origin": "https://ht60-ui.github.io",
            "permissions": ["geolocation"]
        })
        
        # Giả lập tọa độ
        driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
            "latitude": 21.028511,
            "longitude": 105.804817,
            "accuracy": 100
        })
        
        time.sleep(0.5) # Chờ một chút để trình duyệt áp dụng quyền
        driver.get(TARGET_URL)
        
        drivers.append(driver)
        print(f"✅ Đã khởi chạy {browser.upper()} thành công!")
        
    except Exception as e:
        print(f"❌ Lỗi tại máy này (Kiểm tra kết nối hoặc phiên bản trình duyệt): {e}")

print(f"\n🚀 Đã kích hoạt xong! Nhấn Ctrl+C tại cửa sổ này để đóng trình duyệt.")

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        for driver in drivers:
            driver.quit()
        break
