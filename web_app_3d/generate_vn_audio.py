# -*- coding: utf-8 -*-
"""
Script tạo bộ file âm thanh giọng nói tiếng Việt (.mp3) cho Sa bàn Cửa chắn ngập Thủy lực IoT.
Sử dụng Google Translate TTS API (vi-VN) qua thư viện chuẩn urllib của Python.
"""
import os
import urllib.parse
import urllib.request
import time

AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

PHRASES = {
    "welcome.mp3": [
        "Hệ thống sa bàn cửa chắn ngập thủy lực thông minh đã sẵn sàng hoạt động."
    ],
    "raise_gate.mp3": [
        "Mình đã kích hoạt xi lanh thủy lực nâng cửa chắn ngập lên góc 90 độ rồi đó!"
    ],
    "lower_gate.mp3": [
        "Đã hạ cửa chắn ngập xuống phẳng mặt sàn 0 độ rồi nhé!"
    ],
    "auto_flood_alert.mp3": [
        "Cảnh báo ngập lụt! Mực nước dâng vượt ngưỡng 5 xen ti mét.",
        "Hệ thống tự động kích hoạt xi lanh nâng cửa chắn ngập lên 90 độ để ép kín gioăng cao su."
    ],
    "water_safe.mp3": [
        "Mực nước đã rút xuống mức an toàn. Người vận hành có thể bấm nút hạ cửa."
    ],
    "inspect_open.mp3": [
        "Mình đã nhấc nắp mô đun để bạn quan sát cơ cấu xi lanh thủy lực lệch tâm và hệ thống cảm biến bên trong."
    ],
    "inspect_close.mp3": [
        "Đã đóng nắp mô đun sa bàn lại như cũ rồi nhé!"
    ],
    "ir_obstacle_on.mp3": [
        "Cảnh báo an toàn! Cảm biến hồng ngoại phát hiện có vật cản trên mặt cửa, lập tức tạm dừng xi lanh để chống kẹp."
    ],
    "ir_obstacle_off.mp3": [
        "Vật cản đã rời khỏi vùng cảm biến hồng ngoại. Cửa chắn ngập tiếp tục hành trình."
    ],
    "rain_on.mp3": [
        "Đang bơm nước giả lập mưa ngập vào máng thử nghiệm."
    ],
    "rain_off.mp3": [
        "Đã dừng bơm nước giả lập."
    ],
    "auto_on.mp3": [
        "Đã bật chế độ tự động đóng cửa theo tổ hợp cảm biến siêu âm và cảm biến mực nước."
    ],
    "auto_off.mp3": [
        "Đã chuyển sang chế độ điều khiển nâng hạ bằng tay."
    ],
    "alarm_on.mp3": [
        "Đã bật đèn và còi cảnh báo ngập lụt."
    ],
    "alarm_off.mp3": [
        "Đã tắt đèn cảnh báo rồi nhé."
    ],
    "cutaway_view.mp3": [
        "Đây là góc nhìn mặt cắt kỹ thuật thể hiện cơ cấu xi lanh đẩy cánh cửa từ 0 độ lên vuông góc 90 độ."
    ],
    "pitch_full.mp3": [
        "Xin chào Ban Giám Khảo! Đây là sa bàn cửa chắn ngập thủy lực thông minh tích hợp bản sao số 3D của trường Trung học phổ thông Nguyễn Hữu Tiến.",
        "Khác với các cơ cấu nghiêng 75 độ thông thường, cửa được thiết kế tai bắt xi lanh lệch tâm đặt trong hố âm sàn, giúp đẩy tấm chắn dựng đứng vuông góc 90 độ và ép chặt vào gioăng cao su ở hai trụ cổng.",
        "Hệ thống kết hợp cảm biến siêu âm đo mực nước liên tục, cảm biến mực nước tiếp xúc xác nhận ngưỡng ngập, và cảm biến hồng ngoại chống kẹp vật cản an toàn."
    ]
}

def fetch_tts_chunk(text: str) -> bytes:
    params = urllib.parse.urlencode({
        "ie": "UTF-8",
        "client": "tw-ob",
        "tl": "vi",
        "q": text
    })
    url = f"https://translate.google.com/translate_tts?{params}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read()

def main():
    for filename, sentences in PHRASES.items():
        out_path = os.path.join(AUDIO_DIR, filename)
        combined = bytearray()
        for s in sentences:
            chunk = fetch_tts_chunk(s)
            combined.extend(chunk)
            time.sleep(0.2)
        with open(out_path, "wb") as f:
            f.write(combined)
        print(f"[OK] Created {filename} ({len(combined)} bytes)")

if __name__ == "__main__":
    main()

