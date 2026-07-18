from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import os
import time

# =========================================================================
# CẤU HÌNH TẠI ĐÂY: Bạn muốn chạy trình duyệt nào?
# Điền một trong ba chữ: "chrome" hoặc "edge" hoặc "opera"
# =========================================================================
BROWSER_TYPE = "chrome, opera, edge" 

# Nhập đường dẫn Opera trên máy bạn (chỉ dùng nếu CHỌN BROWSER_TYPE = "opera")
OPERA_PATH = r"C:\Users\Admin\AppData\Local\Programs\Opera\opera.exe"
# =========================================================================

# 1. Cấu hình ép tự động ALLOW vị trí chung cho nhân Chromium
prefs = {
    "profile.default_content_setting_values.geolocation": 1,
    "profile.managed_default_content_settings.geolocation": 1
}

def setup_options(options_obj):
    options_obj.add_argument("--always-authorize-plugins")
    options_obj.add_argument("--grant-high-content-permissions")
    options_obj.add_experimental_option("prefs", prefs)
    options_obj.add_experimental_option("excludeSwitches", ["enable-automation"])
    options_obj.add_experimental_option('useAutomationExtension', False)
    return options_obj

# 2. Khởi chạy trình duyệt dựa theo lựa chọn của bạn
print(f"Đang khởi tạo trình duyệt: {BROWSER_TYPE.upper()}...")

if BROWSER_TYPE.lower() == "chrome":
    options = setup_options(ChromeOptions())
    driver = webdriver.Chrome(options=options)

elif BROWSER_TYPE.lower() == "edge":
    options = setup_options(EdgeOptions())
    driver = webdriver.Edge(options=options)

elif BROWSER_TYPE.lower() == "opera":
    options = setup_options(ChromeOptions())
    options.binary_location = OPERA_PATH
    driver = webdriver.Chrome(options=options)
else:
    raise ValueError("Trình duyệt không hợp lệ! Vui lòng chọn 'chrome', 'edge' hoặc 'opera'.")

driver.maximize_window()

# 3. Ép trình duyệt nhận tọa độ giả lập (Bypass GPS thực tế)
driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
    "latitude": 21.028511,
    "longitude": 105.804817,
    "accuracy": 100
})

# 4. Đường dẫn trang web online GitHub Pages của bạn
target_url = "https://ht60-ui.github.io/test/"
driver.get(target_url)

print(f"Đã kích hoạt tự động mở {BROWSER_TYPE.upper()} và bypass vị trí thành công!")

# Vòng lặp giữ cho trình duyệt không bị đóng tự động
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print("\nĐang đóng trình duyệt...")
        driver.quit()
        break
