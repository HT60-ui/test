from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# 1. Cấu hình Chrome chuyên sâu để ép cấp quyền vị trí
options = Options()

# Tham số ép Chrome tự động ALLOW vị trí cho TẤT CẢ các trang (kể cả các thành phần nhúng)
options.add_argument("--always-authorize-plugins")
options.add_argument("--grant-high-content-permissions")

# Tự động cho phép Geolocation ở cấp độ Profile hệ thống
prefs = {
    "profile.default_content_setting_values.geolocation": 1,
    "profile.managed_default_content_settings.geolocation": 1
}
options.add_experimental_option("prefs", prefs)

# Tắt thanh thông báo "Chrome đang bị điều khiển bởi phần mềm tự động"
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# 2. Khởi chạy trình duyệt Chrome thông qua Selenium
driver = webdriver.Chrome(options=options)
driver.maximize_window()

# Ép trình duyệt nhận tọa độ giả lập (Ví dụ dưới đây là tọa độ Hà Nội)
driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
    "latitude": 21.028511,
    "longitude": 105.804817,
    "accuracy": 100
})

# =========================================================================
# 3. ĐƯỜNG DẪN TRANG WEB ONLINE (GITHUB PAGES)
# =========================================================================
# Khai báo chính xác link GitHub Pages của bạn để bot truy cập trực tiếp
target_url = "https://ht60-ui.github.io/test/"

# Ép cửa sổ Chrome của Selenium tự động mở link này lên
driver.get(target_url)

print("Đã kích hoạt tự động mở trang web GitHub và bypass vị trí thành công!")

# Vòng lặp giữ cho script Python chạy ngầm để cửa sổ trình duyệt không bị đóng
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print("\nĐang đóng trình duyệt...")
        driver.quit()
        break
