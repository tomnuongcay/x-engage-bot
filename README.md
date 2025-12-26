# X-ENGAGE BOT - Bot tự động tương tác X (Twitter) với Anti-Detect và Human Behavior

## ✨ Tính năng
- 🎯 Auto Like Feed: Tự động like bài viết trên trang chủ
- 👥 Target Follow: Follow người dùng mục tiêu với kiểm tra thông minh
- 🌱 Nuôi Nick: Mô phỏng hành vi người dùng thực tế
- 🔧 Mở Profile Thủ Công: Mở nhiều profile cùng lúc để can thiệp thủ công
- 🛡️ Anti-Detect: Tạo danh tính duy nhất cho mỗi profile
- 🤖 Human Behavior: Hành vi tự nhiên, tránh bị phát hiện

## 📋 Yêu cầu hệ thống
- Python 3.8+
- Chrome/Chromium browser
- RAM: ít nhất 4GB (khuyến nghị 8GB+)

## 🔧 Cài đặt
1. Clone repository: `git clone <repository-url> && cd x-engage-bot`
2. Tạo môi trường ảo: `python -m venv venv`
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
3. Cài đặt thư viện: `pip install -r requirements.txt`
4. Tool tự động cài ChromeDriver qua SeleniumBase

## 📝 Cấu hình
1. Tạo file `accounts.txt` trong thư mục chính với định dạng:
   ```
   username|password|2fa_secret|proxy
   username2|password2|2fa_secret2|
   ```
   - `2fa_secret`: Mã bí mật 2FA (TOTP secret)
   - `proxy` (tùy chọn): `http://user:pass@ip:port`

2. File `profile_config.json` tự động tạo để lưu cấu hình danh tính

## 🚀 Sử dụng
Chạy chương trình: `python main.py`

### Menu chức năng:
1. 🎯 Auto Like Feed - Tự động like 3-6 bài viết trên trang chủ
2. 👥 Target Follow - Follow người dùng mục tiêu với kiểm tra thông minh
3. 🌱 Nuôi Nick - Mô phỏng hành vi người dùng thực trong 30-60 giây
4. 🔧 Mở Profile Thủ Công - Mở nhiều cửa sổ Chrome cùng lúc
5. 📊 Xem Danh Sách Profile - Hiển thị profile đã tạo

## ⚙️ Cấu hình nâng cao
- Sửa kích thước cửa sổ trong code: `WIN_WIDTH = 380`, `WIN_HEIGHT = 700`, `COLS_PER_ROW = 5`
- Tùy chỉnh độ trễ trong hàm `human_delay()`
- Thêm User-Agent mới trong hàm `generate_profile_identity()`

## 🛡️ Tính năng Anti-Detect
Mỗi profile có danh tính độc lập: User-Agent ngẫu nhiên, độ phân giải màn hình, platform, ngôn ngữ, bộ nhớ, số lõi CPU. Hành vi người dùng: cuộn trang mượt, di chuyển chuột ngẫu nhiên, gõ phím tự nhiên, đọc bài viết thời gian thực.

## 📊 Báo cáo
Hiển thị sau mỗi lần chạy: danh sách tài khoản đã xử lý, kết quả (✅ SUCCESS / ❌ FAILED), thống kê tổng quan.

## ⚠️ Lưu ý quan trọng
1. Sử dụng có trách nhiệm: Tuân thủ điều khoản sử dụng của X (Twitter)
2. Giới hạn hợp lý: Tránh thực hiện quá nhiều hành động trong thời gian ngắn
3. Proxy: Sử dụng proxy chất lượng để tránh bị chặn IP
4. Bảo mật: Bảo vệ file `accounts.txt` và `profile_config.json`
5. Cập nhật: Theo dõi thay đổi từ X (Twitter) để điều chỉnh selector

## 🔒 Bảo mật
Mã hóa cơ bản cho thông tin tài khoản, lưu trữ cục bộ, không gửi dữ liệu ra ngoài, tự động xóa session khi cần.

## 📞 Hỗ trợ
- **Tác giả**: Nguyễn Trọng Huấn
- **Telegram**: t.me/tomnuongcay
- **MB Bank**: 9886786789

## 📄 Giấy phép
Dự án mã nguồn mở cho mục đích học tập và nghiên cứu.

## 🐛 Xử lý lỗi thường gặp
1. Lỗi ChromeDriver: Xóa và cài đặt lại `rm -rf .sbase_driver` rồi chạy lại `python main.py`
2. Lỗi login: Kiểm tra tài khoản/mật khẩu, xác minh 2FA secret, thử login thủ công
3. Lỗi proxy: Kiểm tra định dạng proxy, đảm bảo proxy hoạt động, thử không dùng proxy
4. Lỗi bộ nhớ: Giảm số lượng thread, giảm số profile mở cùng lúc, đóng ứng dụng không cần thiết

## 🔄 Cập nhật
Theo dõi repository để nhận các bản cập nhật và cải tiến mới.

---

**Lưu ý**: Tool này chỉ dành cho mục đích giáo dục và nghiên cứu. Người dùng tự chịu trách nhiệm cho việc sử dụng tool.

## 📁 Cấu trúc project
```
x-engage-bot/
├── main.py              # File chính
├── accounts.txt         # File chứa tài khoản
├── profile_config.json  # File cấu hình profile
├── ENGAGE BOT_profiles/ # Thư mục lưu profile
├── requirements.txt     # Thư viện cần thiết
└── README.md           # Hướng dẫn sử dụng
```
