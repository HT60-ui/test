from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import time

# 1. Cấu hình Chrome chuyên sâu để ép cấp quyền vị trí
options = Options()

# BỔ SUNG: Tham số ép Chrome tự động ALLOW vị trí cho TẤT CẢ các trang (kể cả iframe)
options.add_argument("--always-authorize-plugins")
options.add_argument("--grant-high-content-permissions")

# Tự động cho phép Geolocation ở cấp độ Profile
prefs = {
    "profile.default_content_setting_values.geolocation": 1,
    "profile.managed_default_content_settings.geolocation": 1
}
options.add_experimental_option("prefs", prefs)

# Tắt chế độ thông báo "Chrome đang bị điều khiển..."
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Đánh lừa Chrome để chạy được Geolocation từ file cục bộ (file:///)
options.add_argument("--unsafely-treat-insecure-origin-as-secure=file://")

# 2. Khởi chạy trình duyệt Chrome của hệ thống
driver = webdriver.Chrome(options=options)
driver.maximize_window()

# Ép trình duyệt nhận tọa độ giả lập (Ví dụ: Hà Nội)
driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
    "latitude": 21.028511,
    "longitude": 105.804817,
    "accuracy": 100
})

# 3. Đường dẫn mở file
current_folder = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_folder, "test.html")
target_url = f"http://localhost:{PORT}/index.html"

# Ép trình duyệt tự động mở link lên màn hình
driver.get(target_url)

print("Đã kích hoạt tự động mở và bypass vị trí thành công!")

# Giữ cửa sổ trình duyệt không bị đóng
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print("\nĐang đóng trình duyệt...")
        driver.quit()
        break