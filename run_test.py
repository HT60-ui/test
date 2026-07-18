from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import time

# =========================================================================
# CẤU HÌNH TẠI ĐÂY: Bạn có thể điền 1, 2 hoặc cả 3 trình duyệt (phân cách bằng dấu phẩy)
# Ví dụ: "chrome" hoặc "chrome, edge" hoặc "chrome, opera, edge"
# =========================================================================
BROWSER_TYPE = "chrome, opera, edge" 

# Nhập đường dẫn Opera trên máy bạn (chỉ dùng nếu có chạy "opera")
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

# Danh sách chứa các driver đang chạy để quản lý ở cuối script
drivers = []

# Tách chuỗi BROWSER_TYPE thành danh sách các trình duyệt cần bật
selected_browsers = [b.strip().lower() for b in BROWSER_TYPE.split(",")]

# 2. Khởi chạy song song các trình duyệt được chọn
for browser in selected_browsers:
    try:
        print(f"Đang khởi tạo trình duyệt: {browser.upper()}...")
        
        if browser == "chrome":
            options = setup_options(ChromeOptions())
            driver = webdriver.Chrome(options=options)
            
        elif browser == "edge":
            options = setup_options(EdgeOptions())
            driver = webdriver.Edge(options=options)
            
        elif browser == "opera":
            options = setup_options(ChromeOptions())
            options.binary_location = OPERA_PATH
            driver = webdriver.Chrome(options=options)
            
        else:
            print(f"⚠️ Trình duyệt '{browser}' không hợp lệ, bỏ qua.")
            continue
            
        driver.maximize_window()
        
        # 3. Ép trình duyệt nhận tọa độ giả lập (Bypass GPS thực tế)
        driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
            "latitude": 21.028511,
            "longitude": 105.804817,
            "accuracy": 100
        })
        
        # 4. Điều hướng tới link GitHub Pages của bạn
        target_url = "https://ht60-ui.github.io/test/"
        driver.get(target_url)
        
        # Lưu driver vào danh sách để giữ cửa sổ không bị tắt
        drivers.append(driver)
        print(f"✅ Đã kích hoạt {browser.upper()} thành công!")
        
    except Exception as e:
        print(f"❌ Lỗi khi khởi chạy {browser.upper()}: {e}")

print(f"\n🚀 Đã kích hoạt xong tất cả trình duyệt yêu cầu và bypass vị trí thành công!")

# Vòng lặp giữ cho TẤT CẢ các trình duyệt không bị đóng tự động
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print("\nĐang đóng toàn bộ trình duyệt...")
        for driver in drivers:
            try:
                driver.quit()
            except:
                pass
        break
