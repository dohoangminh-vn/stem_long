# 🌊 Hệ Thống Sa Bàn Cửa Chắn Ngập Thủy Lực Inox 304 Tự Động (0° → 90°)
### 🏆 Đề Tài Nghiên Cứu Khoa Học Kỹ Thuật & STEM — THPT Nguyễn Hữu Tiến

[![GitHub Pages](https://img.shields.io/badge/Demo-GitHub%20Pages-brightgreen?style=for-the-badge&logo=github)](https://dohoangminh-vn.github.io/stem_long/)
[![Three.js](https://img.shields.io/badge/3D-Three.js%20r128-blue?style=for-the-badge&logo=three.js)](https://threejs.org/)
[![ESP8266](https://img.shields.io/badge/Hardware-ESP8266%20Wemos%20D1%20Mini-red?style=for-the-badge&logo=arduino)](https://www.arduino.cc/)
[![Voice AI](https://img.shields.io/badge/Voice%20AI-Ti%E1%BA%BFng%20Vi%E1%BB%87t-yellow?style=for-the-badge)](web_app_3d/audio/)

---

## 🌟 Trải Nghiệm Trực Tiếp Trên Web (Live Demo)

👉 **Mở Bản sao số 3D tương tác miễn phí tại:**
**`https://<your-username>.github.io/<repository-name>/`**

*(Ví dụ nếu repository tên là `stem_long`: [https://dohoangminh-vn.github.io/stem_long/](https://dohoangminh-vn.github.io/stem_long/))*

---

## 📌 Tổng Quan Dự Án

Dự án nghiên cứu, thiết kế và chế tạo mô hình **Sa Bàn Cửa Chống Ngập Tự Động Thủy Lực Inox 304** chuẩn hóa 100% theo các công trình chống ngập công nghiệp cao cấp thực tế:
1. **Mặt đường dốc kết hợp 2 rãnh âm sàn (Recessed Floor Slots):** Khi cửa hạ phẳng $0^\circ$, bộ đôi xi-lanh ben thủy lực và đường ống tuy-ô lặn chìm hoàn toàn xuống dưới đáy rãnh, giúp xe cộ lưu thông êm ái không vướng gầm.
2. **Cánh cửa Inox 304 tôn gân quả trám (Diamond Tread Plate):** Chống trơn trượt lốp xe khi khô ráo, mặt sau gia cường khung hộp Inox và dầm chữ U đan lưới chịu tải trọng lớn và áp lực thủy tĩnh.
3. **Cơ cấu xi-lanh đẩy chéo 63% lưng cửa:** Chân đế xi-lanh bắt tại đáy rãnh âm $B(95, -8\text{ mm})$, đẩy vào 2 tai chốt mắt trâu $P(16, 60\text{ mm})$, tạo góc chống nén $\approx 40.7^\circ$ triệt tiêu áp lực nước tam giác, bảo vệ bản lề không bị bẻ cong.
4. **Hệ thống 3 cảm biến phối hợp (3-Sensor Fusion):**
   * 🌊 **Cảm biến Siêu âm HC-SR04:** Đo liên tục mực nước đường phố từ xa không tiếp xúc.
   * 🚰 **Cực điện cực Inox 304 Hố thu nước (Sump Pit Probes):** Xác nhận ngập tức thời khi nước tràn vào hố thu ở mép cổng.
   * 🔴 **Cảm biến Hồng ngoại IR (Anti-pinch):** Chống kẹp an toàn khi có xe hoặc người đi qua cửa.
5. **Bản sao số 3D Digital Twin + AI Tiếng Việt:** Ứng dụng Three.js xoay 360°, mô phỏng động học thời gian thực, tích hợp 17 file giọng nói tiếng Việt chuẩn (`.mp3`) và nhận diện giọng nói tiếng Việt ra lệnh qua micro.
6. **Vi điều khiển ESP8266 Wemos D1 Mini:** Tự phát Wi-Fi Soft-AP `SaBan_ChongNgap_IoT`, cung cấp REST API hai chiều đồng bộ thời gian thực với Web App.

---

## 🗂️ Cấu Trúc Thư Mục Dự Án

```text
stem_long/
├── index.html                 # Trang chuyển hướng tức thì cho GitHub Pages
├── .nojekyll                  # Vô hiệu hóa Jekyll để GitHub Pages load 100% file 3D và Audio
├── .gitignore                 # Cấu hình bỏ qua file tạm, OS files
├── README.md                  # Hướng dẫn chi tiết dự án
├── DE_XUAT_SA_BAN_CUA_CHAN_NGAP.md # Thuyết minh kỹ thuật & Cẩm nang DIY cho học sinh
├── SO_DO_CO_KHI_CUA_LAT.svg   # Bản vẽ CAD mặt cắt động học xi-lanh
│
├── web_app_3d/                # 🌐 Ứng dụng Web 3D Digital Twin
│   ├── index.html             # Bản sao số 3D Three.js + AI Tiếng Việt
│   ├── generate_vn_audio.py   # Script tạo âm thanh tiếng Việt MP3
│   └── audio/                 # 17 file âm thanh giọng nói tiếng Việt chuẩn
│
├── ban_ve_ky_thuat/           # 📐 Bản vẽ kỹ thuật 2D CAD
│   └── BAN_VE_KY_THUAT_XI_LANH_90_DO.svg # Bản vẽ động học xi-lanh 90° & 3 cảm biến
│
├── mo_hinh_3d/                # 📦 Bộ file 3D CAD chuẩn in 3D (.STL / .OBJ)
│   ├── generate_3d_cad.py     # Script Python sinh mô hình tham số tự động
│   ├── cua_chan_ngap_90do.stl # Cánh cửa Inox 304 tôn gân quả trám + tai P
│   ├── xi_lanh_thuy_luc_bo_doi.stl # Bộ đôi xi-lanh ben thủy lực âm sàn
│   ├── khung_ho_am_san_va_tru_cong.stl # Sàn dốc granite 2 rãnh âm, hố thu & trụ cổng
│   └── sa_ban_tong_the.obj    # Tổ hợp sa bàn tổng thể lắp ghép 3D hoàn chỉnh
│
└── firmware_esp8266/          # ⚡ Mã nguồn nhúng nạp cho ESP8266
    ├── cua_chan_ngap_iot.ino  # Firmware chính (Wi-Fi Soft-AP, REST API, 3 Sensor)
    └── cua_chan_ngap_iot/
        └── cua_chan_ngap_iot.ino # Bản sao chuẩn cho Arduino IDE
```

---

## 🚀 Hướng Dẫn Bật GitHub Pages Xem Web Trực Tuyến

Sau khi push mã nguồn lên GitHub, bạn chỉ cần thực hiện 3 bước đơn giản:

1. Vào repository trên GitHub của bạn.
2. Bấm vào tab **Settings** (ở thanh menu phía trên).
3. Ở menu bên trái, chọn mục **Pages**.
4. Tại mục **Build and deployment**:
   * **Source:** Chọn `Deploy from a branch`
   * **Branch:** Chọn branch `main` (hoặc `master`), thư mục chọn `/ (root)`
   * Bấm **Save**.
5. Sau 1–2 phút, GitHub sẽ cấp cho bạn một đường link xanh:
   `https://<username>.github.io/<repository-name>/`
   Bấm vào link là bạn và Ban Giám Khảo có thể trải nghiệm ngay trên điện thoại hoặc máy tính mà không cần cài đặt gì thêm!

---

## 🛠️ Hướng Dẫn Chạy Cục Bộ (Localhost)

Nếu muốn chạy trực tiếp trên máy tính:
1. Bạn có thể mở trực tiếp file `web_app_3d/index.html` bằng trình duyệt (Chrome, Edge).
2. Hoặc khởi động một web server nhẹ bằng Python:
   ```bash
   python -m http.server 8080
   ```
   Sau đó truy cập: `http://localhost:8080/`

---

## 📡 Kết Nối Với Mạch ESP8266 Ngoài Đời Thực

1. Dùng **Arduino IDE** mở file `firmware_esp8266/cua_chan_ngap_iot/cua_chan_ngap_iot.ino`.
2. Chọn Board: `LOLIN(WEMOS) D1 R2 & mini` và nạp vào mạch qua cáp USB.
3. Mạch sẽ tự phát Wi-Fi tên `SaBan_ChongNgap_IoT` (Mật khẩu: `12345678`).
4. Kết nối điện thoại hoặc máy tính vào mạng Wi-Fi này, sau đó mở web app 3D để đồng bộ góc quay và cảm biến thời gian thực!

---

*Thực hiện bởi Đội ngũ NCKHKT & STEM — THPT Nguyễn Hữu Tiến*
