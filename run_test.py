from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import time

# =========================================================================
# CẤU HÌNH TẠI ĐÂY: Bạn có thể điền 1, 2 hoặc cả 3 trình duyệt (phân cách bằng dấu phẩy)
# =========================================================================
BROWSER_TYPE = "chrome" 

# Nhập đường dẫn Opera trên máy bạn (chỉ dùng nếu có chạy "opera")
OPERA_PATH = r"C:\Users\Admin\AppData\Local\Programs\Opera\opera.exe"

# Đường dẫn URL mục tiêu cần kiểm thử cấp quyền tự động
TARGET_URL = "https://ht60-ui.github.io/test/"
# =========================================================================

def setup_options(options_obj):
    # Loại bỏ cờ báo hiệu trình duyệt đang bị điều khiển tự động (Automation)
    # Điều này giúp trình duyệt hoạt động ổn định và tự nhiên hơn
    options_obj.add_experimental_option("excludeSwitches", ["enable-automation"])
    options_obj.add_experimental_option('useAutomationExtension', False)
    return options_obj

# Danh sách chứa các driver đang chạy để quản lý ở cuối script
drivers = []

# Tách chuỗi BROWSER_TYPE thành danh sách các trình duyệt cần bật
selected_browsers = [b.strip().lower() for b in BROWSER_TYPE.split(",")]

# Khởi chạy song song các trình duyệt được chọn
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
        
        # 🌟 ĐÂY LÀ PHẦN SỬA ĐỔI CHÍNH ĐỂ TỰ ĐỘNG "ALLOW":
        # Sử dụng lệnh Browser.grantPermissions của CDP để cấp trực tiếp quyền vị trí (geolocation)
        # cho chính xác tên miền (Origin) của trang web trước khi trang được tải.
        driver.execute_cdp_cmd("Browser.grantPermissions", {
            "origin": "https://ht60-ui.github.io",
            "permissions": ["geolocation"]
        })
        
        # Ép trình duyệt nhận tọa độ giả lập để kiểm tra luồng dữ liệu (Bypass GPS thực tế)
        driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
            "latitude": 21.028511,
            "longitude": 105.804817,
            "accuracy": 100
        })
        
        # Sau khi quyền đã được cấp ngầm thành công, tiến hành điều hướng tới trang web
        driver.get(TARGET_URL)
        
        # Lưu driver vào danh sách để giữ cửa sổ không bị tắt
        drivers.append(driver)
        print(f"✅ Đã kích hoạt và TỰ ĐỘNG CẤP QUYỀN cho {browser.upper()} thành công!")
        
    except Exception as e:
        print(f"❌ Lỗi khi khởi chạy {browser.upper()}: {e}")

print(f"\n🚀 Đã kích hoạt xong tất cả trình duyệt yêu cầu!")

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
