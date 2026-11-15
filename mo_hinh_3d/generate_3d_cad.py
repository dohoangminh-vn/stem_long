# -*- coding: utf-8 -*-
"""
Script tạo bộ file mô hình 3D kỹ thuật (.STL và .OBJ) cho Sa bàn Cửa chắn ngập Thủy lực 90 độ.
ĐƯỢC CHUẨN HÓA 100% THEO CÔNG TRÌNH THỰC TẾ (Video Cửa_chống_ngập_tự_động_thủy_lực_cao_cấp_inox_304.mp4):
1. Cánh cửa Inox 304 dập gân nhám quả trám (Diamond Tread Plate) mặt trước, khung dầm hộp đan lưới mặt sau.
2. Sàn ram dốc khoét 2 RÃNH ÂM SÀN CHỮ NHẬT (Floor Pockets) - thân xi-lanh lặn chìm dưới rãnh khi cửa hạ phẳng.
3. Chân gối xi-lanh B bắt chìm dưới đáy rãnh âm sàn, ty vươn lên tỳ vào tai U ở 2/3 lưng cánh cửa.
4. Có HỐ THU NƯỚC (Sump Pit) bên hông với 3 cọc cảm biến điện cực Inox tự động báo ngập.
5. Trạm nguồn bơm thủy lực công nghiệp và tủ điện điều khiển DIN-rail.
Đơn vị CAD: milimét (mm).
"""
import math
import os
import struct

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT_DIR, exist_ok=True)


def make_box(x0, y0, z0, x1, y1, z1):
    """Trả về danh sách các tam giác (v0, v1, v2) của hình hộp chữ nhật từ (x0,y0,z0) đến (x1,y1,z1)."""
    p000 = (x0, y0, z0)
    p100 = (x1, y0, z0)
    p110 = (x1, y1, z0)
    p010 = (x0, y1, z0)
    p001 = (x0, y0, z1)
    p101 = (x1, y0, z1)
    p111 = (x1, y1, z1)
    p011 = (x0, y1, z1)

    return [
        # Bottom (z0)
        (p000, p110, p100), (p000, p010, p110),
        # Top (z1)
        (p001, p101, p111), (p001, p111, p011),
        # Front (y0)
        (p000, p100, p101), (p000, p101, p001),
        # Back (y1)
        (p010, p111, p110), (p010, p011, p111),
        # Left (x0)
        (p000, p001, p011), (p000, p011, p010),
        # Right (x1)
        (p100, p110, p111), (p100, p111, p101),
    ]


def make_cylinder_along_segment(pA, pB, radius, segments=20):
    """Tạo hình trụ dọc theo đoạn thẳng nối từ pA đến pB."""
    ax, ay, az = pA
    bx, by, bz = pB
    dx, dy, dz = bx - ax, by - ay, bz - az
    length = math.sqrt(dx * dx + dy * dy + dz * dz)
    if length < 1e-6:
        return []
    ux, uy, uz = dx / length, dy / length, dz / length

    if abs(ux) < 0.8:
        vx, vy, vz = 0.0, -uz, uy
    else:
        vx, vy, vz = -uz, 0.0, ux
    vlen = math.sqrt(vx * vx + vy * vy + vz * vz)
    vx, vy, vz = vx / vlen, vy / vlen, vz / vlen

    wx = uy * vz - uz * vy
    wy = uz * vx - ux * vz
    wz = ux * vy - uy * vx

    tris = []
    for i in range(segments):
        a0 = 2.0 * math.pi * i / segments
        a1 = 2.0 * math.pi * (i + 1) / segments
        c0, s0 = math.cos(a0) * radius, math.sin(a0) * radius
        c1, s1 = math.cos(a1) * radius, math.sin(a1) * radius

        pa0 = (ax + c0 * vx + s0 * wx, ay + c0 * vy + s0 * wy, az + c0 * vz + s0 * wz)
        pa1 = (ax + c1 * vx + s1 * wx, ay + c1 * vy + s1 * wy, az + c1 * vz + s1 * wz)
        pb0 = (bx + c0 * vx + s0 * wx, by + c0 * vy + s0 * wy, bz + c0 * vz + s0 * wz)
        pb1 = (bx + c1 * vx + s1 * wx, by + c1 * vy + s1 * wy, bz + c1 * vz + s1 * wz)

        tris.append((pa0, pa1, pb1))
        tris.append((pa0, pb1, pb0))
        tris.append(((ax, ay, az), pa1, pa0))
        tris.append(((bx, by, bz), pb0, pb1))
    return tris


def compute_normal(v0, v1, v2):
    ux, uy, uz = v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2]
    vx, vy, vz = v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2]
    nx = uy * vz - uz * vy
    ny = uz * vx - ux * vz
    nz = ux * vy - uy * vx
    nl = math.sqrt(nx * nx + ny * ny + nz * nz)
    if nl < 1e-9:
        return (0.0, 0.0, 1.0)
    return (nx / nl, ny / nl, nz / nl)


def write_binary_stl(filepath, triangles, header_text="STEM Floodgate Video Realism CAD"):
    header = header_text.encode("ascii", errors="ignore")[:80].ljust(80, b" ")
    with open(filepath, "wb") as f:
        f.write(header)
        f.write(struct.pack("<I", len(triangles)))
        for v0, v1, v2 in triangles:
            n = compute_normal(v0, v1, v2)
            f.write(struct.pack("<12fH", n[0], n[1], n[2],
                                v0[0], v0[1], v0[2],
                                v1[0], v1[1], v1[2],
                                v2[0], v2[1], v2[2], 0))


def write_obj(filepath, groups):
    """groups: list of (group_name, triangles)"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# Sa Ban Cua Chan Ngap Thuy Luc - Chuan Video Thuc Te Gia Tung (mm)\n")
        v_idx = 1
        for gname, tris in groups:
            f.write(f"g {gname}\n")
            for v0, v1, v2 in tris:
                f.write(f"v {v0[0]:.3f} {v0[1]:.3f} {v0[2]:.3f}\n")
                f.write(f"v {v1[0]:.3f} {v1[1]:.3f} {v1[2]:.3f}\n")
                f.write(f"v {v2[0]:.3f} {v2[1]:.3f} {v2[2]:.3f}\n")
                f.write(f"f {v_idx} {v_idx+1} {v_idx+2}\n")
                v_idx += 3


def build_gate_90deg():
    """
    1. CÁNH CỬA CHẮN NGẬP INOX 304 CHUẨN BIỆT THỰ (Đúng video thực tế):
       - Tấm mặt chính Inox gân chống trượt (Diamond Tread Plate): cao Z 0..100 mm, rộng Y -110..110 mm (220mm), dày X -5..0 mm.
       - Trục bản lề xoay đáy H(0, y, 0).
       - Khung dầm hộp Inox đan lưới mặt sau (hộp 6x6mm):
         + Khung viền chu vi bao quanh (trái, phải, đỉnh).
         + 2 Dầm dọc chính tại Y = -75 mm và Y = +75 mm (nơi truyền lực đẩy xi-lanh).
         + 2 Dầm ngang tăng cứng tại Z = 30 mm và Z = 60 mm.
       - 2 Tai kẹp chữ U bắt chốt mắt trâu xi-lanh ở độ cao 60% (Z = 60 mm), nhô ra lưng X = +15 mm tại Y = ±75 mm.
    """
    tris = []
    # Tấm Inox chính mặt trước
    tris.extend(make_box(-5, -110, 0, 0, 110, 100))

    # Gân nhám chống trượt mặt trước (mô phỏng vân quả trám diamond tread plate)
    for z_tread in range(10, 95, 12):
        for y_tread in range(-100, 105, 20):
            tris.extend(make_box(-5.8, y_tread - 4, z_tread - 1.5, -5.0, y_tread + 4, z_tread + 1.5))

    # Ống trục bản lề đáy H(0, y, 0)
    tris.extend(make_cylinder_along_segment((0, -110, 0), (0, 110, 0), 4.0, 20))

    # Khung dầm hộp Inox đan lưới mặt sau lưng cửa (X từ 0..6 mm)
    # Khung viền đỉnh và 2 bên
    tris.extend(make_box(0, -110, 94, 6, 110, 100)) # Dầm mép đỉnh
    tris.extend(make_box(0, -110, 0, 6, -104, 94))  # Dầm viền mép trái
    tris.extend(make_box(0, 104, 0, 6, 110, 94))    # Dầm viền mép phải

    # 2 Dầm dọc chính chịu lực xi-lanh tại Y = ±75 mm
    for y_pos in (-75.0, 75.0):
        tris.extend(make_box(0, y_pos - 4, 0, 8, y_pos + 4, 94))

    # 2 Dầm ngang giằng chịu áp lực nước tại Z = 30 mm và Z = 60 mm
    tris.extend(make_box(0, -104, 26, 6, 104, 34))
    tris.extend(make_box(0, -104, 56, 6, 104, 64))

    # 2 Tai kẹp chữ U bắt chốt mắt trâu xi-lanh tại Y = ±75 mm, Z = 60 mm, nhô X = +16 mm
    for y_pos in (-75.0, 75.0):
        tris.extend(make_box(0, y_pos - 6, 52, 16, y_pos - 2, 68))
        tris.extend(make_box(0, y_pos + 2, 52, 16, y_pos + 6, 68))
        # Chốt xỏ ngang qua mắt trâu
        tris.extend(make_cylinder_along_segment((16, y_pos - 8, 60), (16, y_pos + 8, 60), 2.8, 16))

    return tris


def build_twin_hydraulic_cylinders():
    """
    2. BỘ ĐÔI XI-LANH THỦY LỰC ĐẶT CHÌM TRONG RÃNH ÂM SÀN (Đúng video thực tế):
       - Chân đế gối xoay B(95, y, -8) đặt chìm dưới đáy rãnh âm sàn ram dốc.
       - Ty pít-tông vươn chéo lên tỳ vào tai U cánh cửa P(16, y, 60).
       - Thân ben Inox sáng bóng phi 12mm, ty crom phi 6mm, cút nối ren góc 90 độ và ống tuy-ô dầu đen.
    """
    tris = []
    for y_pos in (-75.0, 75.0):
        pB = (95.0, y_pos, -8.0)   # Chân đế xoay nằm chìm dưới đáy rãnh âm sàn
        pP = (16.0, y_pos, 60.0)  # Chốt mắt trâu trên lưng cửa ở 2/3 chiều cao
        
        dx, dy, dz = pP[0] - pB[0], pP[1] - pB[1], pP[2] - pB[2]
        length = math.sqrt(dx * dx + dy * dy + dz * dz)
        
        # Điểm nối giữa vỏ xi-lanh và ty pít-tông (55% chiều dài)
        t_split = 0.55
        pMid = (pB[0] + dx * t_split, pB[1] + dy * t_split, pB[2] + dz * t_split)

        # 2.1. Khớp xoay chân đế Clevis Foot bắt chặt vào đáy rãnh bê tông
        tris.extend(make_box(86.0, y_pos - 6.0, -15.0, 104.0, y_pos + 6.0, -11.0)) # Bản mã đế bắt sàn
        tris.extend(make_box(89.0, y_pos - 5.5, -11.0, 101.0, y_pos - 2.0, -3.0))   # Má kẹp trái
        tris.extend(make_box(89.0, y_pos + 2.0, -11.0, 101.0, y_pos + 5.5, -3.0))   # Má kẹp phải
        # Trục chốt xoay ngang chân xi-lanh
        tris.extend(make_cylinder_along_segment((95.0, y_pos - 7.0, -8.0), (95.0, y_pos + 7.0, -8.0), 2.5, 16))

        # 2.2. Vỏ xi-lanh ben thủy lực Inox 304 to bản (phi 12mm)
        tris.extend(make_cylinder_along_segment(pB, pMid, 6.0, 24))
        # Nắp bích đầu xi-lanh (phi 14mm)
        pCapA = (pMid[0] - dx / length * 3.5, pMid[1], pMid[2] - dz / length * 3.5)
        tris.extend(make_cylinder_along_segment(pCapA, pMid, 7.0, 24))

        # 2.3. Ty pít-tông Inox mạ crom sáng bóng (phi 6.4mm)
        tris.extend(make_cylinder_along_segment(pMid, pP, 3.2, 20))

        # 2.4. Khớp mắt trâu tròn ở đầu ty lồng vào tai kẹp chữ U của cửa
        tris.extend(make_cylinder_along_segment((pP[0], y_pos - 2.0, pP[2]), (pP[0], y_pos + 2.0, pP[2]), 4.5, 20))

        # 2.5. Cút nối ren 90 độ và ống tuy-ô thủy lực đen chạy dưới rãnh âm sàn
        pHosePort = (pB[0] - 6.0, y_pos, pB[2] + 6.0)
        tris.extend(make_cylinder_along_segment((pB[0] - 4.0, y_pos, pB[2] + 4.0), pHosePort, 2.0, 12)) # Cút nối góc
        # Tuy-ô mềm uốn lượn chạy men theo rãnh ngang
        pH1 = (pHosePort[0] + 12.0, y_pos - 8.0, -10.0)
        pH2 = (pH1[0] + 20.0, y_pos - 5.0, -10.0)
        pH3 = (130.0, y_pos, -10.0)
        tris.extend(make_cylinder_along_segment(pHosePort, pH1, 1.8, 12))
        tris.extend(make_cylinder_along_segment(pH1, pH2, 1.8, 12))
        tris.extend(make_cylinder_along_segment(pH2, pH3, 1.8, 12))

    return tris


def build_pit_and_portal_frame():
    """
    3. KHUNG SÀN RAM DỐC LÁT ĐÁ VỚI 2 RÃNH ÂM SÀN CHỮ NHẬT + HỐ THU NƯỚC (Đúng video thực tế):
       - Sàn ram dốc lát đá granite xám, bằng phẳng 100%.
       - 2 Rãnh chữ nhật âm sàn (Floor Slots) tại Y = -75 và Y = +75 (rộng 22mm, dài 90mm, sâu 15mm).
       - Hố thu nước bên hông dốc (Sump Pit) có 3 cọc cảm biến điện cực Inox.
       - Hai vách tường hầm ốp đá granite xám có đèn LED vàng hổ phách gắn chìm.
       - Tủ điện điều khiển chuẩn công nghiệp gắn tường.
    """
    tris = []
    # 3.1. Đế sa bàn tổng thể (nền xốp cứng XPS)
    tris.extend(make_box(-220, -130, -35, 165, 130, -25))

    # 3.2. Máng thử nghiệm ngập nước phía trước cửa (X < 0) như trong video công nhân test
    tris.extend(make_box(-220, -125, -25, -6, -115, 85))  # Vách máng bên trái
    tris.extend(make_box(-220, 115, -25, -6, 125, 85))   # Vách máng bên phải
    tris.extend(make_box(-220, -125, -25, -212, 125, 85)) # Vách máng mặt trước
    tris.extend(make_box(-212, -115, -25, -6, 115, -6))   # Đáy bê tông máng nước

    # 3.3. SÀN RAM DỐC LÁT ĐÁ GRANITE (X = 0..165) CÓ 2 RÃNH ÂM SÀN CHỮ NHẬT
    # Mặt sàn chính (cao Z = 0) chia làm các mảng bao quanh 2 rãnh âm sàn
    # Mảng sàn giữa 2 rãnh (Y từ -64..+64)
    tris.extend(make_box(0, -64, -25, 165, 64, 0))
    # Mảng sàn cánh trái (Y từ -125..-86)
    tris.extend(make_box(0, -125, -25, 165, -86, 0))
    # Mảng sàn cánh phải (Y từ 86..125, trừ hố thu nước)
    tris.extend(make_box(0, 86, -25, 90, 125, 0))
    tris.extend(make_box(130, 86, -25, 165, 125, 0))

    # 2 RÃNH ÂM SÀN CHỮ NHẬT (Floor Pockets) tại Y = [-86..-64] và Y = [64..86]
    # Đáy rãnh âm sàn sâu Z = -15 mm (X từ 20..115 mm)
    for y_cen in (-75.0, 75.0):
        # Đáy rãnh âm sàn bê tông
        tris.extend(make_box(15, y_cen - 11, -25, 115, y_cen + 11, -15))
        # Vách rãnh phía trước và phía sau
        tris.extend(make_box(15, y_cen - 11, -15, 20, y_cen + 11, 0))
        tris.extend(make_box(110, y_cen - 11, -15, 115, y_cen + 11, 0))
        # Rãnh ngang gom ống dầu tuy-ô tại X = 115..130
        tris.extend(make_box(115, y_cen - 6, -25, 135, y_cen + 6, -12))

    # 3.4. HỐ THU NƯỚC (SUMP PIT) BÊN HÔNG RAM DỐC (X = 90..130, Y = 86..125, sâu Z = -25 mm)
    # Đáy hố thu nước
    tris.extend(make_box(90, 86, -30, 130, 125, -22))
    # Vách hố thu nước
    tris.extend(make_box(90, 86, -22, 94, 125, 0))
    tris.extend(make_box(126, 86, -22, 130, 125, 0))
    tris.extend(make_box(94, 86, -22, 126, 90, 0))
    # 3 CỌC CẢM BIẾN MỰC NƯỚC ĐIỆN CỰC INOX (Stainless Steel Probes) cắm thẳng đứng vào hố thu
    for y_probe, z_tip in ((96.0, -18.0), (105.0, -12.0), (114.0, -6.0)):
        tris.extend(make_cylinder_along_segment((110.0, y_probe, 5.0), (110.0, y_probe, z_tip), 1.4, 12))
        # Đầu nối dây cảm biến màu vàng
        tris.extend(make_cylinder_along_segment((110.0, y_probe, 5.0), (110.0, y_probe, 8.0), 2.2, 12))

    # 3.5. HAI VÁCH TƯỜNG HẦM ỐP ĐÁ GRANITE (không dùng 2 cột trụ độc lập kiểu cũ)
    # Vách tường bên trái hầm
    tris.extend(make_box(-15, -128, 0, 140, -112, 110))
    # Vách tường bên phải hầm
    tris.extend(make_box(-15, 112, 0, 140, 128, 110))

    # Đèn LED cảnh báo màu vàng hổ phách gắn chìm âm tường (Flush Amber LED Beacons)
    for y_wall in (-112.5, 112.5):
        tris.extend(make_box(5, y_wall - 1.5, 30, 15, y_wall + 1.5, 55)) # Hốc đèn LED chìm âm tường

    # 3.6. TỦ ĐIỆN ĐIỀU KHIỂN CHUẨN CÔNG NGHIỆP GẮN TƯỜNG (như frame 45s trong video)
    # Tủ điện gắn trên vách tường phải tại X = 40..85, Z = 45..105
    tris.extend(make_box(40, 128, 45, 85, 145, 105)) # Vỏ tủ điện IP65
    # Cánh tủ điện có nắp kính trong suốt
    tris.extend(make_box(42, 145, 47, 83, 147, 103))

    return tris


def main():
    gate_tris = build_gate_90deg()
    cyl_tris = build_twin_hydraulic_cylinders()
    frame_tris = build_pit_and_portal_frame()

    p1 = os.path.join(OUT_DIR, "cua_chan_ngap_90do.stl")
    p2 = os.path.join(OUT_DIR, "xi_lanh_thuy_luc_bo_doi.stl")
    p3 = os.path.join(OUT_DIR, "khung_ho_am_san_va_tru_cong.stl")
    p4 = os.path.join(OUT_DIR, "sa_ban_tong_the.obj")

    write_binary_stl(p1, gate_tris, "Cua Inox 304 gan qua tram + Khung dam hop")
    write_binary_stl(p2, cyl_tris, "Bo doi xi lanh Inox chim duoi 2 ranh am san")
    write_binary_stl(p3, frame_tris, "San ram doc 2 ranh am san + Ho thu nuoc")
    write_obj(p4, [
        ("Cua_Inox_Gan_Chong_Truot", gate_tris),
        ("Xi_Lanh_Chim_Ranh_Am_San", cyl_tris),
        ("San_Ram_Doc_Ho_Thu_Nuoc", frame_tris),
    ])

    for p in (p1, p2, p3, p4):
        print(f"[OK] Generated {os.path.basename(p)} ({os.path.getsize(p)} bytes)")


if __name__ == "__main__":
    main()
