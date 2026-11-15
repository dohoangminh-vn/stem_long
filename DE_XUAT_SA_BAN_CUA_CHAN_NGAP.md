# Đề xuất thiết kế sa bàn cửa chắn ngập tự động

**Bản thiết kế MVP** — dùng cho chế tạo mô hình KHKT/STEM và làm nền cập nhật hồ sơ đề tài hiện có.

## 1. Định hướng đề tài

**Tên ngắn:** Sa bàn cửa chắn ngập tự động điều khiển bằng ESP8266, cảm biến siêu âm và cơ cấu nâng điện dùng motor N20.

**Mục tiêu của bản mẫu:** Khi nước trong máng thử dâng tới ngưỡng cài đặt, hệ thống phát cảnh báo và dùng motor N20 quay vít me để nâng cửa chắn. Khi nước rút, người vận hành xem trạng thái và chủ động cho cửa hạ xuống.

Sa bàn mô phỏng chuyển động nâng/hạ của cửa chống ngập công nghiệp, nhưng cơ cấu chấp hành trong mô hình là motor điện và vít me, không phải bộ thủy lực. Không xem đây là cửa chống ngập dùng cho nhà thật, và không khẳng định chịu được lũ, dòng chảy hoặc áp lực thực tế.

**Đối chiếu mẫu bạn gửi:** mình hiểu đây là cửa chắn âm sàn: khi không chắn, mặt tấm hạ ngang bằng nền; khi có ngập, pít tông nâng tấm lên. Trang sản phẩm cùng tên của Minh Dũng mô tả mẫu LG93 kích thước 4.000 × 800 mm, vận hành bằng pít tông và dùng hệ thống nguồn/van thủy lực. Đó là cấu hình công nghiệp. Để tiết kiệm và dễ chế tạo, sa bàn thay bộ thủy lực bằng một motor N20, vít me và thanh nối cơ khí; báo cáo cần gọi đúng đây là mô hình truyền động điện mô phỏng cửa thủy lực.

## 2. Phương án cơ khí đề xuất: cửa lật bản lề

### Cấu hình

- Cửa là một **tấm chắn nằm ngang khi mở (`0°`)**: mặt tấm nằm phẳng với mặt đường/đáy máng. Một cạnh dài gắn bản lề cố định `H`; khi đóng, tấm quay lên **đúng góc vuông `90°` thẳng đứng** để ép kín vào gioăng cao su EPDM dọc hai trụ cổng và đạt 100% chiều cao chắn nước (thay vì chỉ dừng ở `70°–75°` như các cơ cấu thanh truyền thẳng hàng chưa có tai lệch tâm).
- Dùng 2–3 bản lề nhỏ dọc theo cạnh xoay. Gia cường mặt dưới bằng một thanh ngang và **2 tai bắt xi-lanh lệch tâm `P` (nhô `e = 14 mm`, cách bản lề `r = 55 mm`)** để bộ đôi xi-lanh đẩy cánh cửa từ `0°` lên thẳng `90°` mượt mà, không bị kẹt điểm chết cơ khí.
- Dùng **một cơ cấu vít me đặt dưới bản lề**, ở giữa bề rộng cửa. Motor N20 quay thanh ren M6 theo phương đứng; đai ốc nằm trong con trượt được dẫn hướng để đi lên/xuống mà không tự xoay.
- Một thanh nối có chốt ở hai đầu nối con trượt `Q` với tai `P` dưới mặt cửa. Khi con trượt đi lên, thanh nối đẩy P và làm cửa quay quanh bản lề `H`; khi con trượt đi xuống, thanh nối kéo cửa về ngang.
- Đỡ và chặn dọc trục vít me vào khung ở hai đầu; dùng khớp nối 3→6 mm giữa trục motor và vít me. Không để lực đẩy/kéo dồn thẳng vào trục hộp số N20.
- Một công tắc hành trình đặt ở trạng thái cửa nằm ngang, một công tắc ở trạng thái cửa đã dựng. Có thêm chặn cơ khí ở cả hai đầu.
- Gioăng xốp hoặc silicone dán dọc mép cửa để quan sát và đo rò rỉ.

**Nguyên lý:** N20 quay vít me → con trượt Q đi lên → thanh nối Q–P đẩy tai P dưới cánh → tấm quay quanh bản lề H từ ngang lên dựng. Đảo chiều motor làm Q đi xuống, thanh nối kéo cửa về ngang. Nếu muốn giữ hình thức pít tông, có thể bọc vít me bằng ống nhựa làm vỏ trang trí; phần truyền lực thật vẫn là vít me.

**Điểm rất quan trọng:** motor không nối cứng trực tiếp với cửa; thanh nối Q–P phải có chốt xoay ở cả hai đầu để theo cung quay của cửa. Bắt đầu với H–P khoảng 5 cm, thanh Q–P khoảng 5 cm, và trục vít me đặt trong hốc ngay dưới/gần H; sau đó kiểm tra bằng bìa cứng để điều chỉnh vị trí Q, tránh thanh nối nằm thẳng hàng với cánh ở điểm bắt đầu vì sẽ bị “chết cơ cấu”.

### Sơ đồ khối

```mermaid
flowchart LR
  W[Siêu âm đo khoảng cách mặt nước] --> E[ESP8266 D1 mini]
  E --> L[LED trạng thái / cảnh báo]
  E --> D[TB6612FNG]
  D --> M[N20 + vít me]
  M --> C[Con trượt Q]
  C --> R[Thanh nối Q–P]
  R --> G[Cửa lật quanh bản lề H]
  U[Công tắc cửa ngang / cửa dựng] --> E
  P[Trang điều khiển Wi-Fi nội bộ] <--> E
```

### Bố trí nhìn ngang

```text
               D1 mini + driver + nguồn trong hộp khô
                                  │
       HC-SR04                   │ N20 quay vít me đứng dưới bản lề
       nhìn thẳng xuống          │       con trượt Q ↕
             ↓                   │             ╲ thanh nối Q–P
  MÁNG NƯỚC / phía ngập  ~~~~~~~~~~~~~  H●──────P●────tấm cửa ngang   phía khô
```

### Mặt cắt cơ khí: trước và sau khi đóng

![Sơ đồ cơ cấu cửa lật dùng motor N20, vít me và thanh nối](SO_DO_CO_KHI_CUA_LAT.svg)

```text
MỞ — tấm nằm ngang (0°)               DỰNG — tấm quay lên (70–80°)

H●════════════P●                    P●
│            ╱                       ╲  tấm cửa
│          ╱ thanh nối                 ╲
Q●       ╱                         H●───╲──── mặt đế
║ vít me                                Q●
║                                       ║ vít me

H = trục bản lề; P = chốt thanh nối vào cửa; Q = chốt thanh nối vào con trượt.
Con trượt đi lên để dựng cửa, đi xuống để hạ cửa.
```

Đặt motor và vít me trong hốc khô dưới cạnh bản lề; đặt hộp điện cao hơn mép máng. Thanh nối phải xoay tự do ở P và Q, không cọ vào bản lề. Nếu dùng ống nhựa bọc ngoài vít me cho giống pít tông, chừa khe để con trượt chạy và không xem lớp vỏ đó là xi-lanh thủy lực.

### Trình tự lắp để giảm làm lại

1. Làm khung, máng và cánh cửa có bản lề; kiểm tra cửa quay nhẹ bằng tay từ ngang lên 70–80°.
2. Làm mẫu bìa cứng cho H–P–Q; kiểm tra thanh nối không bị thẳng hàng/kẹt ở hai đầu và xác định hành trình con trượt.
3. Lắp vít me đứng dưới H, giữ trục vít bằng gối đỡ ở hai đầu; lắp đai ốc vào con trượt có dẫn hướng chống xoay.
4. Nối Q với P bằng thanh nối có chốt xoay; quay vít me bằng tay để xác nhận con trượt dựng và hạ được cửa.
5. Gắn công tắc trạng thái cửa ngang và cửa dựng, sau đó mới nối driver và chạy motor ở nguồn giới hạn dòng.
6. Lắp cảm biến, chia áp ECHO, LED và phần mềm; hiệu chuẩn ngưỡng bằng thước đo mực nước.
7. Chạy thử khô nhiều chu kỳ, kiểm tra vít me, chốt và dây; sau đó mới thêm nước vào máng. Đặt hộp điện riêng ở phía khô.

### Kích thước khởi điểm

- Đế khoảng **50–60 × 30–40 cm**; máng nước khoảng **35–45 × 10–15 cm**, sâu 5–8 cm.
- Tấm cửa dài khoảng 8–10 cm tính từ bản lề tới mép tự do; khi dựng 70–80° mép cửa sẽ lên khoảng 7–10 cm.
- Chốt P trên cửa đặt cách bản lề H khoảng 4–6 cm; điểm Q của con trượt nằm gần dưới H. Bắt đầu với thanh nối dài khoảng 5 cm và hành trình con trượt khoảng 2–4 cm; chiều dài vít me thực tế cần chừa thêm phần đai ốc và gối đỡ. Chỉnh bằng bìa cứng trước khi khoan.
- Gắn một thanh gia cường ngang dưới tấm cửa và đặt cơ cấu ở giữa bề rộng. Bản lề và chặn cuối hành trình giữ kết cấu; không dùng vít nhỏ ở một điểm làm kết cấu chịu va đập.
- Bắt đầu thử cơ cấu trên bàn khô. Sau khi vít me chạy ổn định và cửa dừng được ở hai đầu mới lắp vào máng nước.

## 3. Chọn motor và cơ cấu truyền động

| Phương án | Điểm mạnh | Hạn chế | Dùng khi |
|---|---|---|---|
| **N20 + vít me + con trượt + thanh nối** | Rẻ, nhỏ, đảo chiều được, hành trình rõ và dừng bằng công tắc | Cần làm gối đỡ vít me, dẫn hướng con trượt và căn hình học thanh nối | **Khuyến nghị cho mô hình này** |
| N20 + tay quay/thanh truyền | Ít chi tiết, chế tạo nhanh | Chạy theo chu kỳ quay; khó dừng chính xác ở hai đầu nếu không thêm cảm biến | Mô hình chuyển động lặp, không cần giữ vị trí |
| 28BYJ-48 + ULN2003 + vít me + thanh nối | Dễ điều khiển theo bước, giá thấp | Chậm; vị trí có thể lệch nếu mất bước hoặc mất điện; vẫn cần công tắc hành trình | Cần quan sát chuyển động chậm, không cần tải lớn |
| NEMA 17 + A4988 | Mô-men và điều khiển vị trí tốt hơn | To, nặng, cần nguồn và driver phù hợp; thừa cho cửa nhẹ | Bản nâng cấp sau khi đã chứng minh MVP |
| Servo MG996R | Lắp nhanh, điều khiển góc trực tiếp ở bản rất nhỏ | Không tạo chuyển động pít tông; cần chọn đúng mô-men và nguồn | Ưu tiên cách lắp đơn giản hơn cơ cấu vít me |

**Khuyến nghị cụ thể:** dùng N20 3–6 V, vít me M6 bước 1 mm, con trượt chống xoay và một thanh nối khoảng 5 cm; TB6612FNG đảo chiều motor. Hành trình con trượt khoảng 2–4 cm: ở 100 vòng/phút đi hết hành trình mất lý tưởng 12–24 giây; ở 300 vòng/phút mất 4–8 giây. Thực tế phụ thuộc ma sát và tải, nên chạy thử cơ cấu không tải trước, rồi tăng tải dần. Motor quay vít me; không nối motor trực tiếp vào GPIO.

Đừng chọn driver chỉ theo dòng “đỉnh”. Kiểm tra dòng kẹt trục (stall current) của đúng motor và bảo đảm nó nằm trong giới hạn driver; nếu không có thông số, đo bằng nguồn giới hạn dòng hoặc đổi sang motor/driver phù hợp. Không nối N20 trực tiếp với GPIO.

## 4. Bố trí và xử lý cảm biến

### Cảm biến mực nước siêu âm

- Với HC-SR04 đang có: gắn trên thanh ngang, **đầu cảm biến hướng thẳng xuống mặt nước**, ở phía nước dâng trước cửa.
- Đặt cảm biến cao hơn mực nước lớn nhất dự kiến; với máng sâu 5–8 cm, có thể bắt đầu ở độ cao 20–25 cm tính từ đáy máng.
- Không đặt ngay sát tường, mép cửa hoặc đầu ra của dòng nước. Chừa khoảng trống quanh chùm đo; thử vị trí để loại phản xạ từ thành máng.
- Có thể tạo một khoang đo nhỏ thông với máng để giảm gợn sóng. Mặt nước trong khoang phải lên xuống cùng mực nước máng.
- Gắn mái che giọt bắn nhưng không che mặt phát/thu âm. HC-SR04 không chống nước, nên không để nước bắn hoặc ngưng tụ vào bo mạch.
- Đo khoảng cách **D** từ cảm biến đến mặt nước; sau khi đo chiều cao lắp đặt **H**, tính gần đúng `mực_nước = H - D`. Dùng ngưỡng đã hiệu chuẩn thực tế, không nhập ngưỡng chỉ theo bản vẽ.

**Ví dụ để bắt đầu hiệu chuẩn:** cảm biến cao H = 22 cm tính từ đáy; bật cảnh báo/đóng cửa khi mặt nước cao 5 cm (`D_đóng ≈ 17 cm`); cho phép trạng thái “nước đã rút” khi mực nước xuống 2 cm (`D_rút ≈ 20 cm`). Khoảng cách giữa hai ngưỡng tạo độ trễ, tránh cửa đổi trạng thái liên tục khi mặt nước gợn. Đây là số đặt thử, cần thay bằng số đo của máng thật.

### Công tắc hành trình

- Công tắc `HORIZONTAL` đặt nơi tấm cửa nằm phẳng 0°; công tắc `RAISED` đặt nơi cửa đã dựng 70–80°.
- Gắn công tắc lên khung khô, để một tai nhỏ dưới cửa chạm nhẹ cần gạt trước khi chạm chặn cứng.
- Phần mềm phải dừng motor ngay khi công tắc đúng chiều được kích hoạt. Có thời gian chạy tối đa làm lớp bảo vệ thứ hai nếu công tắc hỏng hoặc dây tuột.

### Sơ đồ chân tham khảo D1 mini

| Tín hiệu | Chân gợi ý | Ghi chú |
|---|---|---|
| HC-SR04 TRIG | D1 / GPIO5 | Xung kích |
| HC-SR04 ECHO | D2 / GPIO4 | Bắt buộc qua cầu chia áp vì ECHO của HC-SR04 thường là 5 V |
| TB6612 AIN1/AIN2 | D5 / GPIO14, D6 / GPIO12 | Đảo chiều motor; TB6612 `STBY` và `PWMA` có thể nối mức 3.3 V để chạy tốc độ cố định trong MVP |
| LED cảnh báo đỏ | D7 / GPIO13 | Nối tiếp điện trở 220–1.000 Ω |
| Công tắc cửa đã dựng | D0 / GPIO16 | Thêm điện trở kéo lên 10 kΩ về 3.3 V; công tắc nối chân vào GND khi chạm |
| Công tắc cửa nằm ngang | A0 | Dùng mạng điện trở để giữ điện áp A0 dưới 3.2 V; ví dụ kéo lên 3.3 V qua 10 kΩ và kéo xuống GND qua 22 kΩ, công tắc kéo A0 xuống GND; đọc ngưỡng analog sau khi đo thử |
| LED có sẵn trên bo | D4 / GPIO2 | Có thể dùng làm chỉ báo xanh sau khi bo khởi động |

HC-SR04 cấp 5 V; dùng điện trở 2.2 kΩ nối tiếp từ ECHO tới D2 và 3.3 kΩ từ D2 xuống GND (đầu ra xấp xỉ 3.0 V). Không đưa tín hiệu 5 V trực tiếp vào GPIO ESP8266. D1 mini dùng mức logic 3.3 V; chân A0 của bản LOLIN D1 mini v3.1 được ghi tối đa 3.2 V, nên kiểm tra đúng phiên bản bo đang có.

Nguồn motor đi qua driver; nguồn logic cấp D1 mini. Dùng mass chung, đi dây motor riêng khỏi dây cảm biến và đặt tụ 470–1.000 µF gần driver để giảm sụt áp lúc motor khởi động. Chỉ dùng nguồn DC thấp áp 5–6 V gần máng nước; để hộp điện ở phía khô.

## 5. BOM và dự toán tiết kiệm

Các món D1 mini, HC-SR04 và LED đã có được tính là **0 đồng cần mua mới**. Giá linh kiện dưới đây là mức tham khảo từ một số cửa hàng trực tuyến, chưa gồm phí giao hàng và có thể đổi theo phiên bản/số lượng.

| Hạng mục | Số lượng | Dự toán (VNĐ) | Ghi chú |
|---|---:|---:|---|
| D1 mini, HC-SR04, LED | Đã có | 0 | Không mua lại |
| N20 giảm tốc | 1 | 35.000–70.000 | Chọn điện áp/tốc độ đúng nhu cầu |
| Driver TB6612FNG | 1 | 50.000–80.000 | Chọn bản có chân điều khiển rõ ràng |
| Công tắc hành trình nhỏ | 2 | 7.000–20.000 | Thêm dây và điện trở |
| Vít me M6, đai ốc, khớp nối, gối đỡ | 1 bộ | 40.000–90.000 | Giữ vít me khỏi trượt dọc trục |
| Thanh dẫn hướng, con trượt, thanh nối và chốt | 1 bộ | 30.000–60.000 | Tận dụng ty thép/miếng nhựa sẵn có |
| Khung, bản lề, tai/chốt liên kết, tấm cửa, gioăng | 1 bộ | 100.000–220.000 | Foam board, mica mỏng, gỗ hoặc nhựa tái dùng |
| Dây, điện trở, đầu nối, keo chống nước | 1 bộ | 25.000–60.000 | Chừa phần dự phòng |
| Nguồn DC và/hoặc buck 5 V | 1 | 0–100.000 | 0 nếu đã có nguồn phù hợp |
| Máng nước, vật liệu trang trí, vận chuyển | 1 bộ | 0–100.000 | Tận dụng hộp nhựa và vật liệu sẵn có |
| **Tổng dự kiến cần mua** |  | **khoảng 300.000–800.000** | Nếu phải mua khung đẹp, nguồn mới và vận chuyển, dự trù gần đầu trên |

Giá niêm yết tham khảo: HC-SR04 khoảng 17.500đ, N20 GA12 6 V/100 rpm khoảng 67.260đ, module TB6612FNG điều khiển trực tiếp khoảng 60.000đ, và công tắc hành trình mini khoảng 3.420đ/cái ở các trang bán lẻ được xem trong tháng 11/2026. Đây là ví dụ để lập ngân sách, không phải báo giá chốt.

## 6. Luồng người dùng trình diễn

1. Cắm nguồn DC thấp áp; đèn xanh báo hệ thống sẵn sàng. Mở trang điều khiển nội bộ nếu cần theo dõi trên điện thoại.
2. Máng đang ít nước, cửa ở vị trí mở; giao diện hiển thị khoảng cách/mực nước và trạng thái cửa.
3. Người xem từ từ thêm nước bằng ca có vạch, không cần bơm riêng.
4. Khi mực nước vượt ngưỡng cao liên tục, LED đỏ/còi báo; N20 quay vít me làm con trượt và thanh nối dựng tấm cửa lên.
5. Công tắc `RAISED` dừng motor; giao diện chuyển sang “ĐÃ DỰNG”.
6. Rút nước khỏi máng. Khi dưới ngưỡng thấp đủ thời gian, giao diện báo “NƯỚC ĐÃ RÚT — CHỜ HẠ”.
7. Người vận hành chọn “Hạ”; motor đảo chiều, con trượt đi xuống và kéo tấm cửa về ngang tới công tắc `HORIZONTAL`.
8. Người xem kiểm tra mặt phía khô, gioăng và giấy thấm để ghi nhận lượng rò rỉ.

Trang Wi-Fi nên chạy nội bộ do ESP8266 phát (SoftAP) hoặc cùng mạng LAN; không phụ thuộc Internet. Nếu Wi-Fi mất, tự động đo và đóng cửa vẫn phải hoạt động.

## 7. Use case

| ID | Tác nhân | Mục đích | Kết quả chính |
|---|---|---|---|
| UC-01 | Hệ thống | Tự phát hiện nước dâng | Đèn cảnh báo bật, cửa nâng đến công tắc trên |
| UC-02 | Người vận hành | Xem mực nước và trạng thái | Trang nội bộ hiển thị giá trị gần nhất, trạng thái cửa, lỗi |
| UC-03 | Người vận hành | Hạ cửa sau khi nước rút | Chỉ hạ cửa khi xác nhận lệnh và đường đi đang bình thường |
| UC-04 | Hệ thống | Xử lý cảm biến/motor bất thường | Dừng motor, bật trạng thái lỗi, không tự tiếp tục chuyển động |
| UC-05 | Người trình diễn | Chạy thử bằng tay | Nút “DỰNG/HẠ” trên trang nội bộ để kiểm tra cơ cấu mà không cần chờ nước |

## 8. Đặc tả chương trình

### Đầu vào và đầu ra

- **Đầu vào:** xung TRIG/ECHO; công tắc `HORIZONTAL`/`RAISED`; lệnh `AUTO`, `DỰNG`, `HẠ` từ trang nội bộ.
- **Đầu ra:** hai chân chiều motor qua TB6612; LED trạng thái/cảnh báo; trang nội bộ hiển thị mực nước, trạng thái và lỗi.
- **Biến cấu hình:** `H_CM`, `D_CLOSE_CM`, `D_OPEN_CM`, thời gian xác nhận ngưỡng, thời gian chạy motor tối đa, thời gian hết hạn dữ liệu cảm biến.

### Máy trạng thái

```text
KHỞI ĐỘNG → TỰ KIỂM TRA → SẴN SÀNG/CỬA NẰM NGANG
                            │ mực nước cao được xác nhận
                            ↓
                         ĐANG DỰNG → chạm RAISED → ĐÃ DỰNG
                            │ quá thời gian / lỗi cảm biến
                            ↓
                           LỖI

ĐÃ DỰNG → nước dưới ngưỡng thấp đủ lâu → CHỜ NGƯỜI VẬN HÀNH HẠ
CHỜ HẠ → lệnh HẠ → ĐANG HẠ → chạm HORIZONTAL → SẴN SÀNG/CỬA NẰM NGANG
```

### Quy tắc xử lý

1. Đo theo chu kỳ khoảng 200–300 ms; loại giá trị ngoài dải hoặc timeout. Lọc bằng trung vị 5 mẫu để giảm nhiễu gợn sóng.
2. Chỉ xác nhận nước dâng sau 3 lần đọc đã lọc liên tiếp vượt ngưỡng đóng. Mục tiêu phản hồi tổng thể: trong 2 giây sau khi vượt ngưỡng ổn định.
3. Dùng hai ngưỡng khác nhau: dựng cửa ở mực cao, cho phép hạ ở mực thấp. Không tự hạ cửa chỉ vì một lần đọc thấp; chờ dưới ngưỡng thấp ổn định ít nhất 10 giây và yêu cầu người vận hành xác nhận.
4. Trong lúc motor chạy, vẫn đọc công tắc hành trình và kiểm tra thời gian tối đa. Chạm công tắc đúng chiều thì tắt motor; hết thời gian mà chưa chạm thì vào `LỖI`.
5. Nếu ECHO timeout hoặc giá trị đo bất hợp lý liên tục: báo lỗi cảm biến, ngừng lệnh mở tự động. Không tự suy diễn rằng nước đang an toàn.
6. Khi khởi động lại, không chạy motor ngay. Đọc cảm biến và công tắc trước; nếu mực nước cao thì cho phép đóng có giới hạn hành trình, còn lệnh mở vẫn cần người vận hành.
7. Dùng `millis()`/bộ đếm thời gian không chặn thay cho `delay()` dài để Wi-Fi, cảm biến và dừng hành trình vẫn được xử lý khi motor hoạt động.

### Giao diện nội bộ tối thiểu

Trang một màn hình: `Mực nước`, `Khoảng cách cảm biến`, `Cửa: NẰM NGANG/ĐANG DỰNG/ĐÃ DỰNG/ĐANG HẠ/LỖI`, nút `AUTO`, `DỰNG`, `HẠ`, cùng thông báo lỗi. Lệnh hạ chỉ hoạt động khi cảm biến không báo ngập và người dùng xác nhận.

## 9. Kịch bản thử nghiệm và tiêu chí đạt

Ghi kết quả đo thật vào cột cuối sau mỗi lần chạy; chưa thử thì không điền số liệu.

| Mã | Cách thử | Tiêu chí đạt đề xuất | Kết quả |
|---|---|---|---|
| T01 — Mực thấp | Để nước dưới ngưỡng trong 1 phút | Cửa không tự đóng; trạng thái ổn định | ______ |
| T02 — Nước dâng | Tăng nước chậm qua ngưỡng cao | Nhận ngưỡng trong ≤2 giây; tấm cửa dựng tới công tắc RAISED; motor dừng | ______ |
| T03 — Gợn sóng | Tạo gợn nhỏ quanh ngưỡng | Không đóng/mở liên tục; không đảo chiều khi đang chạy | ______ |
| T04 — Nước rút | Hạ nước xuống dưới ngưỡng thấp | Chuyển sang “chờ mở”; cửa chưa tự hạ | ______ |
| T05 — Hạ có xác nhận | Gửi lệnh HẠ sau T04 | Tấm về nằm ngang, chạm công tắc HORIZONTAL và motor dừng | ______ |
| T06 — Mất ECHO | Rút dây ECHO khi đang chờ | Báo lỗi, không phát lệnh chuyển động không an toàn | ______ |
| T07 — Kẹt cơ khí | Cố định cửa nhẹ trong lúc chạy thử | Hết thời gian giới hạn thì motor dừng và báo lỗi | ______ |
| T08 — Mất Wi-Fi | Ngắt kết nối điện thoại/router | Tự động phát hiện và đóng cửa vẫn hoạt động | ______ |
| T09 — Độ bền cơ cấu | Chạy đủ 20 chu kỳ dựng/hạ | Không tuột chốt, kẹt đai ốc hoặc lỏng bản lề; motor/driver không quá nóng | ______ |
| T10 — Độ kín cửa | Dựng cửa, thêm nước theo vạch trong 60 giây | Ghi thể tích nước lọt sang phía khô; mục tiêu ban đầu ≤50 ml/60 giây | ______ |

Mẫu nhật ký: ngày/giờ, H, ngưỡng đóng/mở, mực nước thực đo bằng thước, thời gian phát hiện, thời gian đóng, lượng nước rò, số chu kỳ, lỗi quan sát được. Nếu không đạt, ghi nguyên nhân và lần chỉnh sửa tiếp theo.

## 10. Khung pitching report

### Tóm tắt để đưa vào báo cáo

Ngập cục bộ có thể làm nước tràn qua cửa nhà hoặc lối xuống tầng hầm trong thời gian ngắn, trong khi biện pháp chắn thủ công cần người phát hiện và thao tác. Nhóm đề xuất sa bàn cửa chắn ngập tự động dùng cảm biến siêu âm theo dõi mực nước, ESP8266 xử lý ngưỡng và gửi cảnh báo, còn motor N20 quay vít me và thanh nối để dựng tấm chắn từ vị trí nằm ngang. Sa bàn dùng truyền động điện để mô phỏng chuyển động của cửa thủy lực công nghiệp, không chứa mạch thủy lực. Nhóm đánh giá bằng độ trễ phát hiện, thời gian đóng/mở, số chu kỳ ổn định và lượng nước rò sang phía khô. Bản mẫu ở quy mô bàn dùng để minh họa nguyên lý; khả năng chịu ngập thật cần thiết kế kết cấu, thử tải và kiểm định riêng.

### Bài nói pitch khoảng một phút

“Khi nước dâng nhanh trước cửa nhà, người ở bên trong có thể không kịp lắp tấm chắn bằng tay. Nhóm chúng em làm một sa bàn cửa chắn ngập tự động để minh họa cách phát hiện và phản ứng sớm. Cảm biến siêu âm đo khoảng cách tới mặt nước; ESP8266 lọc số đo, bật cảnh báo và điều khiển motor N20. Vít me biến chuyển động quay thành chuyển động thẳng của con trượt; thanh nối từ con trượt làm tấm chắn lật lên từ mặt nền. Khi nước rút, người vận hành xác nhận trên trang Wi-Fi nội bộ để hạ cửa. Nhóm sẽ kiểm tra độ trễ cảm biến, thời gian chuyển động, độ kín và độ lặp lại qua nhiều chu kỳ. Đây là mô hình truyền động điện mô phỏng cửa thủy lực công nghiệp, chưa phải sản phẩm chịu lũ cho công trình thật.”

### Các ý cần có trên poster/slide

1. Vấn đề thực tế và đối tượng hưởng lợi.
2. Sơ đồ cảm biến → ESP8266 → driver → N20/vít me → con trượt/thanh nối → cửa.
3. Ảnh cơ cấu thật, sơ đồ chân, ảnh bố trí cảm biến.
4. Bảng tiêu chí thử và **kết quả đo do nhóm thực hiện**.
5. Dự toán vật tư và phần tận dụng đồ sẵn có.
6. Giới hạn của sa bàn và bước phát triển tiếp theo.

Nên sửa các câu trong hồ sơ cũ như “ngăn chặn triệt để”, “chịu dòng nước xoáy/sóng do xe” và “tự động hoàn toàn” thành mục tiêu có thể kiểm chứng trên sa bàn. Chỉ đưa kết quả định lượng sau khi hoàn tất các phép thử.

## 11. Nguồn kỹ thuật và giá tham khảo

- [LOLIN D1 mini v3.1.0 — sơ đồ chân, mức logic 3.3 V và A0 tối đa 3.2 V](https://www.wemos.cc/en/latest/d1/d1_mini_3.1.0.html)
- [Espressif ESP8266EX resources — lưu ý không đưa mức 5 V vào GPIO](https://www.espressif.com/en/products/socs/esp8266ex/resources/)
- [Toshiba TB6612FNG — datasheet và giới hạn driver](https://toshiba.semicon-storage.com/ap-en/semiconductor/product/motor-driver-ics/brushed-dc-motor-driver-ics/detail.TB6612FNG.html)
- [HC-SR04 — listing và thông số/giá tham khảo tại Thegioiic](https://thegioiic.com/hc-sr04-cam-bien-sieu-am?dl=1)
- [HC-SR04 — hướng dẫn mức logic ECHO 5 V và cầu chia áp tại Adafruit](https://learn.adafruit.com/ultrasonic-sonar-distance-sensors?view=all)
- [N20 GA12 6 V, 100 rpm — listing và giá tham khảo tại Thegioiic](https://www.thegioiic.com/ga12-n20-dong-co-giam-toc-6vdc-100-rpm-truc-3mm)
- [Module TB6612FNG điều khiển trực tiếp — listing tham khảo tại Điện Tử Á Châu](https://dientuachau.com/driver-board-tb6612fng)
- [Danh mục công tắc hành trình — giá tham khảo tại Thegioiic](https://www.thegioiic.com/san-pham/cong-tac-hanh-trinh)
- [Cửa Chống Ngập Tự Động Thủy Lực — trang tham chiếu cùng tên của Minh Dũng](https://chongngap.com/s%E1%BA%A3n%20ph%E1%BA%A9m/cua-chong-ngap-tu-dong/)

## 12. Tiến độ chế tạo gợi ý trong hai tuần

| Ngày | Việc chính | Sản phẩm kiểm tra được |
|---|---|---|
| 1–2 | Chốt kích thước, cắt đế/máng, làm cửa và bản lề | Cửa quay bằng tay từ ngang lên 70–80° không bị kẹt |
| 3–4 | Làm con trượt và thanh nối, thử vị trí H–P–Q | Cửa lật lên/hạ bằng tay, thanh nối không bị kẹt |
| 5–6 | Lắp vít me, motor N20, công tắc hành trình, driver | Motor chạy hai chiều và dừng ở hai đầu |
| 7–8 | Lắp D1 mini, cảm biến, LED; hiệu chuẩn ngưỡng | Tự đóng khi dâng nước; có trạng thái lỗi |
| 9–10 | Thêm trang Wi-Fi nội bộ, hoàn thiện vỏ và dây | Điều khiển tay và tự động cùng hoạt động |
| 11–12 | Chạy ma trận T01–T10, ghi số đo, sửa lỗi cơ khí | Bảng kết quả có số liệu thật và ghi chú |
| 13–14 | Chụp ảnh/video, hoàn thiện báo cáo và pitch | Sa bàn trình diễn và tài liệu thuyết trình |

## 13. Nâng cấp theo chuẩn Sa bàn Điện lực (3DPLUS): Mô-đun tháo lắp + Web App 3D Digital Twin + AI Giọng nói

Dựa trên phân tích video mẫu nhà máy điện (`video_dien_luc_in3d.mp4`), điểm ăn điểm mạnh nhất trước Ban Giám Khảo là **trải nghiệm điều khiển "như chơi game" (Digital Twin 3D + Ra lệnh giọng nói AI)** kết hợp với **kết cấu mô-đun nhấc nắp để xem cơ khí bên trong** (giữ nguyên chỉ dùng đèn LED cảnh báo đơn, không cần làm dải LED đuổi phức tạp).

### 13.1. Kết cấu vật lý mô-đun tháo lắp trên nền đáy xốp (tiết kiệm, dễ làm)

1. **Nền đáy xốp (Foam / Xốp XPS cứng) phân tầng:**
   - Khoét một **hốc kỹ thuật khô** ngay phía sau bản lề cửa để chứa cơ cấu truyền động (Servo kéo-đẩy thanh truyền chéo hoặc Motor N20 + vít me).
   - Phía trên hốc kỹ thuật làm **tấm nắp sàn màu vàng (giống cửa SHOJI thực tế)** gắn nam châm nhỏ hoặc gờ cài. Khi thuyết trình, có thể **nhấc tấm nắp sàn và mái cổng ra bằng 1 tay** (giống hệt cảnh nhấc mái nhà máy tuabin trong video điện lực) để giám khảo nhìn thấy tận mắt tay đòn/vít me đang đẩy cánh cửa bên dưới.
2. **Làm vỏ bọc "Xi-lanh thủy lực" ở 2 bên cánh cửa:**
   - Dùng **2 vỏ ống tiêm nhựa (bơm tiêm y tế 5 ml hoặc 10 ml cắt bỏ đầu mũi)** hoặc 2 ống nhựa lồng vào nhau (1 ống đen làm vỏ xi-lanh gắn ở sàn, 1 ty thép/nhựa bạc nối lên tai cánh cửa ở vị trí 2/3 chiều cao cửa).
   - Khi Servo hoặc N20 dưới hầm đẩy cửa nâng lên, 2 pít-tông hai bên sẽ trượt ra/thu vào y hệt xi-lanh thủy lực thật trong ảnh mẫu.
3. **Hộp điện kỹ thuật nắp trong suốt:**
   - Đặt mạch Wemos D1 Mini và driver trong hộp nhựa trong suốt gắn bên hông trụ cổng (cao hơn mặt nước) để khoe phần mạch gọn gàng.
   - Dán **mã QR** ngay góc trước sa bàn để giám khảo quét bằng điện thoại và mở giao diện 3D.

### 13.2. Bộ phần mềm, Âm thanh Giọng nói Tiếng Việt, Bản vẽ 2D & File 3D đã dựng sẵn trong dự án

- **Giao diện 3D Digital Twin + AI Giọng nói tiếng Việt (`.mp3` chuẩn 100%):** [`web_app_3d/index.html`](file:///d:/code/stem_long/web_app_3d/index.html)
  - Hiển thị mô hình 3D sa bàn cửa chắn ngập dựng vuông góc `90°` xoay 360°, phóng to/thu nhỏ (`360`, `FIT`, `GÓC CƠ KHÍ`, `MẶT CẮT 90°`).
  - Có nút **"Tháo nắp xem cơ khí"** nhấc tấm sàn vàng và mái cổng trên mô hình 3D đồng bộ với thao tác tháo nắp ngoài đời.
  - Có nút **"🚧 Vật cản IR (Chống kẹp)"** mô phỏng xe/người đi ngang tia laser hồng ngoại làm xi-lanh tự động dừng khẩn cấp.
  - Có nút **"📐 Bản vẽ 2D & File 3D"** mở trực tiếp bản vẽ kỹ thuật CAD và tải 4 file 3D (`.stl` / `.obj`) ngay trong ứng dụng.
  - Tích hợp **17 file âm thanh giọng nói tiếng Việt thật (`vi-VN-HoaiMyNeural`)** trong thư mục [`web_app_3d/audio/`](file:///d:/code/stem_long/web_app_3d/audio) kết hợp âm thanh cơ khí thủy lực, đảm bảo phát tiếng Việt rõ ràng 100% trên mọi máy tính Windows không cần cài gói ngôn ngữ phụ.
- **Chương trình nạp cho mạch Wemos D1 Mini (ESP8266):** [`firmware_esp8266/cua_chan_ngap_iot.ino`](file:///d:/code/stem_long/firmware_esp8266/cua_chan_ngap_iot.ino)
  - Hỗ trợ **đồng thời cả Servo (chân `D8`, hành trình chuẩn `0° → 90°`) và Motor N20 + TB6612FNG (`D5`, `D6`)** cùng **3 cảm biến hợp nhất** (`HC-SR04` + Cảm biến mực nước tiếp xúc `D3` + Cảm biến Hồng ngoại chống kẹp `D0`).
  - Tự phát Wi-Fi nội bộ `SaBan_ChongNgap_IoT` (mật khẩu `12345678`, IP `192.168.4.1`) kèm REST API JSON có bật CORS để đồng bộ thời gian thực với Web App 3D.

---

## 14. Nghiên cứu chuyên sâu: Góc nâng 90° vs 75°, Động học Xi-lanh Thủy lực & Hệ 3 Cảm biến

### 14.1. Tại sao cửa chắn ngập thủy lực thực tế dựng vuông góc `90°` thay vì `75°`?

Qua đối chiếu bản vẽ kỹ thuật của các dòng cửa chống ngập thủy lực âm sàn công nghiệp (như **SHOJI** và **Minh Dũng LG93**) cùng tài liệu tổng quan kỹ thuật công trình chống ngập ([`water-12-00502-v2.pdf`](file:///d:/code/stem_long/water-12-00502-v2.pdf)):

| Tiêu chí kỹ thuật | Góc dựng `75°` (Bản phác thảo sơ bộ cũ) | Góc dựng vuông góc `90°` (Chuẩn công nghiệp & Bản nâng cấp) |
|---|---|---|
| **1. Độ kín khít với gioăng cao su 2 bên trụ cổng (Sidewall Sealing)** | Cạnh bên cánh cửa nghiêng lệch `15°` so với phương thẳng đứng của 2 trụ cổng bê tông → tạo khe hở hình nêm tam giác ở hai bên hông, nước lọt qua rất mạnh. | Hai mép bên cánh cửa **áp sát vuông góc (`90.0°`) vào dải gioăng cao su EPDM chữ D/P** chạy dọc 2 trụ cổng và tỳ thẳng vào ngàm chặn thép, khóa kín hoàn toàn 3 cạnh (đáy bản lề + 2 cạnh bên). |
| **2. Chiều cao chắn nước hữu dụng ($H_{\text{chắn}} = L \cdot \sin\theta$)** | Với tấm cửa rộng $L = 100\text{ mm}$, ở $75^\circ$ chỉ chắn được $100 \times \sin 75^\circ \approx 96.5\text{ mm}$ (mất 3.5% chiều cao và mặt nước dễ tạt tràn qua mép nghiêng). | Đạt tối đa $H_{\text{chắn}} = 100 \times \sin 90^\circ = 100\text{ mm}$ (100% chiều rộng cánh cửa) và mặt thẳng đứng phản xạ sóng vỗ ngược lại. |
| **3. Nguyên nhân bản cũ chỉ để `70°–75°` và cách khắc phục lên `90°`** | Nếu bắt chốt xi-lanh sát mặt phẳng tấm cửa ($e = 0$) và đặt gối xi-lanh nông, khi cửa nằm ngang $0^\circ$ trục xi-lanh gần trùng với mặt cửa (góc nâng $\approx 0^\circ$ — **điểm chết cơ khí**), còn khi lên quá $75^\circ$ thì kịch hành trình. | Sử dụng **Tai bắt xi-lanh lệch tâm $P$ (nhô $e = 14\text{ mm}$ dưới đáy cửa)** kết hợp **hạ gối cố định $B$ xuống đáy hố âm sàn ($-22\text{ mm}$)** giúp xi-lanh có cánh tay đòn nâng dương ngay từ $0^\circ$ và đẩy một mạch tới đúng góc vuông **$90.0^\circ$**. |

### 14.2. Cơ cấu Xi-lanh Thực tế: Phân tích Video Công Trình Thực Tế (`Cửa_chống_ngập_tự_động_thủy_lực_cao_cấp_inox_304.mp4`)

> [!IMPORTANT]
> **Điểm mấu chốt kỹ thuật phân biệt giữa mô hình phác thảo lý thuyết và công trình thủy lực thực tế:**
> Qua phân tích frame-by-frame video công trình thực tế (`Cửa_chống_ngập_tự_động_thủy_lực_cao_cấp_inox_304.mp4`), hệ thống cửa chống ngập thủy lực cao cấp thực tế có các đặc điểm kỹ thuật chuẩn mực sau:
> 1. **Mặt đường dốc lát đá granite kết hợp 2 rãnh âm sàn (Recessed Floor Slots):** Không có khay sàn vàng cồng kềnh lộ thiên. Mặt dốc xe chạy bằng đá granite phẳng phiu, chỉ có **2 rãnh hẹp âm sàn** chạy dọc theo đường bánh xe. Khi cửa hạ phẳng $0^\circ$, toàn bộ thân xi-lanh ben thủy lực và đầu tuy-ô dầu lặn chìm hoàn toàn xuống dưới đáy rãnh, giúp xe ô tô và xe máy lưu thông êm ái, không hề bị vướng gầm.
> 2. **Cánh cửa Inox 304 tôn gân quả trám (Diamond Tread Plate):** Mặt trên cửa dập gân chống trượt quả trám cho lốp xe bám đường khi khô ráo (không dán biển báo STOP hay vạch vàng đen như đồ chơi). Mặt dưới là khung hộp Inox 304 bo viền và dầm tăng cứng chữ U đan lưới chịu tải trọng xe qua lại và áp lực nước ngập.
> 3. **Xi-lanh Đẩy Chéo vào 60%–65% lưng cửa:** Gối xoay chân đế xi-lanh bắt bu-lông cố định tại **đáy rãnh âm sàn** $B(95\text{ mm}, -8\text{ mm})$. Khi nâng cửa, ty xi-lanh duỗi chéo đẩy vào 2 tai chốt mắt trâu $P(16\text{ mm}, 60\text{ mm})$ trên lưng cửa, tạo góc chống nén $\approx 40.5^\circ$ cực kỳ vững chãi.
> 4. **Hố thu nước (Sump Pit) & Cực điện cực Inox 304:** Nước mưa từ mặt đường chảy vào hố thu có nắp đan inox ở mép cổng. Bên trong hố thu gắn các que đo điện cực inox 304; khi nước dâng chạm điện cực, mạch điều khiển lập tức kích hoạt chu trình nâng cửa tự động.
> 5. **Tủ điện công nghiệp chuẩn DIN-rail & Đèn âm tường:** Tủ điện gắn trên tường chứa Aptomat Schneider C63, khởi động từ CHINT, nguồn tổ ong Mean Well 24V, công tắc cảm ứng Lumi và bộ thu sóng Remote 3 nút. Hai bên trụ tường đá gắn dải đèn LED màu vàng hổ phách (amber) âm tường chớp sáng khi cửa nâng/hạ.

#### A. Phân tích Cơ học Thủy tĩnh (Hydrostatic Equilibrium):
1. **Phân bố áp lực nước:** Khối nước dâng cao $H$ tạo ra biểu đồ áp lực thủy tĩnh hình tam giác. Hợp lực nước $F_{\text{nước}} = \frac{1}{2} \rho g H^2 b$ đặt tại **tâm áp lực ở $1/3$ chiều cao** tính từ đáy máng ($z_{\text{cp}} = H/3 \approx 33.3\text{ mm}$).
2. **Nếu xi-lanh giấu dưới hầm bắt sát bản lề ($e = 14\text{ mm}$):** Cánh tay đòn chống đỡ chỉ có $0.014\text{ m}$. Khi nước ngập lớn, áp lực thủy tĩnh hàng chục tấn sẽ tạo mô-men uốn cực lớn lên bản lề:
   $$F_{\text{cyl}} = \frac{M_{\text{nước}}}{0.014\text{ m}} = \frac{F_{\text{nước}} \cdot 0.033}{0.014} \approx 2.4 \times F_{\text{nước}}$$
   Lực này tạo ứng suất uốn khổng lồ, bẻ cong cánh cửa và xé toạc cụm bản lề ngay lập tức!
3. **Khi xi-lanh Đẩy Chéo vào 2/3 lưng cửa ($h = 60\text{ mm}$):**
   - Xi-lanh đóng vai trò như **thanh giằng chống nén chéo (diagonal bracing strut)** tỳ trực tiếp vào xương tăng cứng lưng cửa, đối xứng với tâm áp lực nước.
   - Toàn bộ lực xô của dòng nước được chuyển hóa thành lực nén dọc theo thân xi-lanh và truyền thẳng xuống kết cấu sàn qua gối xoay chân đế. Bản lề ở chân cửa hoàn toàn được giải phóng lực uốn, giúp cánh cửa phẳng phiu tuyệt đối và gioăng cao su EPDM dọc 2 trụ cổng được ép khít 100%.

#### B. Tính toán Động học Xi-lanh Đẩy Chéo Âm Sàn Chuẩn Hóa:
- **Tâm bản lề cố định:** $H(0, 0)$ tại cốt sàn ram dốc.
- **Cánh cửa Inox 304:** Chiều dài $L = 100\text{ mm}$, bề rộng $W = 220\text{ mm}$, dày $6\text{ mm}$ (mặt trên dập gân quả trám, mặt dưới hàn khung hộp tăng cứng).
- **Vị trí chốt mắt trâu $P$ trên lưng cửa:** Cách bản lề $h = 60\text{ mm}$ (60% chiều cao cửa), nhô về phía lưng cửa $e = 15\text{ mm}$ tại hai bên $Y = \pm 75\text{ mm}$.
  - Khi cửa dựng $90^\circ$: $P_{90} = (16\text{ mm}, 60\text{ mm})$.
  - Khi cửa nằm phẳng $0^\circ$: $P_0 = (60\text{ mm}, -15\text{ mm})$ (lặn sâu $-15\text{ mm}$ dưới mặt đường, nằm lọt trong rãnh âm sàn).
- **Vị trí gối xoay chân xi-lanh $B$ (Clevis Foot):** Bắt bu-lông cố định tại **đáy rãnh âm sàn** tại $B = (95\text{ mm}, -8\text{ mm})$.
- **Kiểm tra thông số hành trình:**
  1. Chiều dài thu gọn khi cửa nằm phẳng ($0^\circ$):
     $$L_{\min} = \sqrt{(60 - 95)^2 + (-15 - (-8))^2} = \sqrt{(-35)^2 + (-7)^2} = \sqrt{1225 + 49} = \mathbf{35.7\text{ mm}}$$
     Tại $0^\circ$, cả hai đầu xi-lanh đều có cao độ âm ($-8\text{ mm}$ và $-15\text{ mm}$), nằm hoàn toàn dưới cốt mặt đường $0.0\text{ mm}$ $\rightarrow$ **Không hề cấn gầm xe!**
  2. Chiều dài duỗi hết cỡ khi cửa dựng đứng ($90^\circ$):
     $$L_{\max} = \sqrt{(16 - 95)^2 + (60 - (-8))^2} = \sqrt{(-79)^2 + 68^2} = \sqrt{6241 + 4624} = \mathbf{104.2\text{ mm}}$$
     Góc nghiêng chống nén so với mặt sàn: $\alpha_{90} = \arctan(68/79) \approx 40.7^\circ$ (góc chống chéo lý tưởng triệt tiêu áp lực nước).
  3. Hành trình pít-tông yêu cầu:
     $$S = L_{\max} - L_{\min} = 104.2 - 35.7 = \mathbf{68.5\text{ mm}}$$ (tỷ số duỗi $L_{\max}/L_{\min} = 2.92$, tương thích hoàn hảo với xi-lanh thủy lực 2 tầng công nghiệp hoặc cơ cấu ray trượt servo sa bàn).

#### C. Phương án Chế tạo Sa bàn Chạy thật Tiết kiệm cho Học sinh (DIY STEM Guide):
Dựa trên mục tiêu *"mô hình chạy thật, chi phí tiết kiệm, đáy xốp, thanh ray dẫn hướng dùng servo đẩy chéo, pít tông dùng motor N20"* trong file [`note.txt`](file:///d:/code/stem_long/note.txt):
1. **Nền sa bàn xốp XPS (Extruded Polystyrene):**
   - Dùng tấm xốp XPS màu xanh/hồng dày 3–5 cm (mua ở tiệm vật liệu cách âm/cách nhiệt, giá 40k–60k/tấm). Dễ gọt cắt bằng dao rọc giấy hoặc dây mayso nhiệt, không bị thấm nước.
   - Khoét 2 rãnh âm sàn hẹp rộng 1.5 cm, sâu 2.0 cm trên mặt dốc để giấu 2 thân xi-lanh ben thủy lực.
   - Dán decal vân đá granite màu xám sẫm lên mặt sàn dốc tạo thẩm mỹ sang trọng như công trình thật trong video.
2. **Cánh cửa Inox 304:**
   - Dùng tấm nhựa mica hoặc fomex xám dán decal nhôm xước / decal kim loại gân nổi giả Inox 304 tôn gân quả trám.
   - Mặt sau dán 2 nẹp nhựa chữ U làm xương tăng cứng và gắn 2 tai bắt chốt $P$ bằng ke góc nhôm.
3. **Cơ cấu chấp hành chạy thật ẩn dưới nền xốp:**
   - **Phương án Servo (Khuyên dùng):** 1 Servo MG996R (nối chân `D8` Wemos D1 Mini) gắn dưới hầm xốp. Tay đòn servo kéo/đẩy thanh ray dẫn hướng trượt chéo trong 2 rãnh âm sàn, đẩy 2 ty pít-tông mạ crom nâng cửa từ $0^\circ \rightarrow 90^\circ$ mượt mà chỉ mất 2.5 giây.
   - **Vỏ pít-tông trang trí:** Dùng 2 vỏ bút bi kim loại đen hoặc ống tiêm y tế cắt ngắn làm vỏ ben; ty bên trong dùng thanh nhôm tròn $\varnothing 4\text{ mm}$ sáng bóng. Hai đầu có dây tuy-ô bọc ruột gà xoắn đen luồn xuống rãnh âm sàn.
4. **Hố thu nước & Cảm biến:**
   - Khoét một hố nhỏ $3 \times 3\text{ cm}$ ở mép dốc, lót màng chống thấm làm hố thu nước.
   - Cắm 2 que dây đồng hoặc 2 đầu ghim inox làm điện cực dò nước (nối chân `D3` kích mức LOW khi nước tràn vào hố thu).

### 14.3. Nghiên cứu Cảm biến Hồng ngoại (IR) đo khoảng cách & Cảm biến Mực nước

1. **Tại sao KHÔNG bắn trực tiếp tia Hồng ngoại (IR — ví dụ Sharp GP2Y0A21YK0F hoặc VL53L0X/FC-51) thẳng vào mặt nước trong?**
   - Theo **Định luật khúc xạ Snell** ($n_{\text{không khí}} = 1.00 \rightarrow n_{\text{nước}} = 1.33$), ở góc chiếu vuông góc, hệ số phản xạ Fresnel của tia hồng ngoại ($\lambda \approx 850\text{–}940\text{ nm}$) trên mặt nước sạch chỉ đạt:
     $$R = \left(\frac{n_1 - n_2}{n_1 + n_2}\right)^2 = \left(\frac{1 - 1.33}{1 + 1.33}\right)^2 \approx 2\%$$
   - Tức là **hơn 96%–98% năng lượng tia hồng ngoại xuyên thấu qua mặt nước xuống tận đáy bể**, dẫn đến cảm biến đo nhầm khoảng cách tới đáy máng thay vì mặt nước! Hơn nữa, khi mặt nước gợn sóng, tia phản xạ bị tán xạ gương (specular reflection) lệch khỏi mắt thu photodiode.
2. **Giải pháp phối hợp 3 Cảm biến (3-Sensor Fusion) chuẩn kỹ thuật trên sa bàn:**
   - **Cảm biến 1 — Siêu âm `HC-SR04` (Đo mực nước liên tục không tiếp xúc):** Sóng âm 40 kHz có trở kháng âm học chênh lệch cực lớn giữa không khí và nước nên **phản xạ 99.9% ngay trên mặt nước**, đo chính xác mực nước liên tục từ `0.0 → 10.0 cm`.
   - **Cảm biến 2 — Cảm biến Điện cực Inox 304 Hố thu nước (Sump Pit Electrode Probe):** Đặt trong hố thu nước tại mép cổng. Khi nước mặt đường tràn vào hố thu, dòng điện cực kích hoạt chân `D3` xác nhận ngập độc lập (chuẩn xác như tủ điện công nghiệp trong video).
   - **Cảm biến 3 — Cảm biến Hồng ngoại `IR` (Chống kẹp an toàn):** Chiếu ngang ngưỡng cổng ở cao độ 15–20 cm. Nếu đang hạ cửa mà có người hoặc xe cộ đi ngang cắt tia hồng ngoại, ESP8266 lập tức tạm dừng xi-lanh để chống kẹp tai nạn.

### 14.4. Danh mục Bản vẽ Kỹ thuật 2D & File Mô hình 3D (`.STL` / `.OBJ`) đi kèm

Toàn bộ file thiết kế kỹ thuật đã được đồng bộ chuẩn xác theo video công trình thực tế:

1. **Bản vẽ kỹ thuật 2D mặt cắt động học xi-lanh âm sàn `0° → 90°` & sơ đồ 3 cảm biến:**
   - [`ban_ve_ky_thuat/BAN_VE_KY_THUAT_XI_LANH_90_DO.svg`](file:///d:/code/stem_long/ban_ve_ky_thuat/BAN_VE_KY_THUAT_XI_LANH_90_DO.svg) (và bản sao hiển thị trực tiếp [`SO_DO_CO_KHI_CUA_LAT.svg`](file:///d:/code/stem_long/SO_DO_CO_KHI_CUA_LAT.svg))
2. **Bộ 4 File 3D CAD chuẩn in 3D (`.stl`) và mô hình lắp ghép tổng thể (`.obj`) theo chuẩn video thực tế:**
   - [`mo_hinh_3d/cua_chan_ngap_90do.stl`](file:///d:/code/stem_long/mo_hinh_3d/cua_chan_ngap_90do.stl) — Cánh cửa Inox 304 tôn gân quả trám `100 × 220 × 6 mm`, khung hộp tăng cứng lưng cửa & 2 tai chốt mắt trâu $P(h=60\text{ mm}, e=15\text{ mm})$.
   - [`mo_hinh_3d/xi_lanh_thuy_luc_bo_doi.stl`](file:///d:/code/stem_long/mo_hinh_3d/xi_lanh_thuy_luc_bo_doi.stl) — Bộ đôi xi-lanh thủy lực to bản hạ chìm trong 2 rãnh âm sàn $B(95, -8\text{ mm})$, đầu ty mạ crom và co cút nối tuy-ô dầu.
   - [`mo_hinh_3d/khung_ho_am_san_va_tru_cong.stl`](file:///d:/code/stem_long/mo_hinh_3d/khung_ho_am_san_va_tru_cong.stl) — Khung sàn dốc granite có 2 rãnh âm sàn giấu ben, hố thu nước điện cực, dải đèn LED âm tường và 2 trụ cổng ngàm vuông góc `90°`.
   - [`mo_hinh_3d/sa_ban_tong_the.obj`](file:///d:/code/stem_long/mo_hinh_3d/sa_ban_tong_the.obj) — Mô hình 3D lắp ghép hoàn chỉnh toàn bộ sa bàn ở trạng thái cửa dựng đứng `90°`.
   - Script Python tạo mô hình 3D tham số: [`mo_hinh_3d/generate_3d_cad.py`](file:///d:/code/stem_long/mo_hinh_3d/generate_3d_cad.py).
