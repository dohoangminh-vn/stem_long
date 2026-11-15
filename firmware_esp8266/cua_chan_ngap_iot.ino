/*
 * ============================================================================
 * ĐỀ TÀI NCKHKT & STEM: HỆ THỐNG CỬA CHẮN NGẬP THỦY LỰC THÔNG MINH (0° -> 90°)
 * Vi điều khiển: Wemos D1 Mini (ESP8266)
 *
 * CẬP NHẬT KỸ THUẬT:
 * 1. Góc nâng cánh cửa đạt chuẩn vuông góc 90° (ép kín gioăng cao su EPDM).
 * 2. Hợp nhất 3 cảm biến (3-Sensor Fusion):
 *    - Cảm biến siêu âm HC-SR04 (TRIG=D1, ECHO=D2): Đo mực nước liên tục (cm).
 *    - Cảm biến mực nước tiếp xúc / Phao (D3): Xác nhận ngập khẩn cấp tại ngưỡng 5 cm.
 *    - Cảm biến Hồng ngoại IR (D0): Chống kẹp an toàn khi có người/xe trên cửa.
 * 3. Hỗ trợ song song cả Servo (D8) và Motor N20 + Driver TB6612FNG (D5, D6).
 * 4. Phát Wi-Fi nội bộ "SaBan_ChongNgap_IoT" (MK: 12345678, IP: 192.168.4.1)
 *    đồng bộ thời gian thực với Web App 3D Digital Twin & Giọng nói tiếng Việt.
 * ============================================================================
 */

#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <Servo.h>

// -------------------- CẤU HÌNH WI-FI SOFT-AP --------------------
const char* AP_SSID = "SaBan_ChongNgap_IoT";
const char* AP_PASS = "12345678";

ESP8266WebServer server(80);
Servo gateServo;

// -------------------- SƠ ĐỒ CHÂN WEMOS D1 MINI --------------------
const int PIN_TRIG        = D1; // GPIO5  - Xung kích HC-SR04
const int PIN_ECHO        = D2; // GPIO4  - Xung thu HC-SR04 (qua cầu chia áp 2.2k/3.3k)
const int PIN_WATER_PROBE = D3; // GPIO0  - Cảm biến điện cực Hố thu nước Inox 304 (Sump Pit, LOW = Chạm nước)
const int PIN_IR_OBSTACLE = D0; // GPIO16 - Cảm biến Hồng ngoại IR chống kẹp (LOW = Có vật cản)
const int PIN_MOTOR_AIN1  = D5; // GPIO14 - Chiều nâng cửa (TB6612FNG AIN1)
const int PIN_MOTOR_AIN2  = D6; // GPIO12 - Chiều hạ cửa   (TB6612FNG AIN2)
const int PIN_ALARM_LED   = D7; // GPIO13 - Đèn LED hổ phách âm tường + Rơ-le còi (Flush Amber LED / Relay)
const int PIN_SERVO       = D8; // GPIO15 - Servo kéo/đẩy xi-lanh 0° -> 90°
const int PIN_LIMIT_LOW   = A0; // Analog - Công tắc hành trình cửa nằm ngang 0°

// -------------------- THÔNG SỐ KỸ THUẬT & NGƯỠNG --------------------
const float SENSOR_HEIGHT_CM   = 22.0; // Chiều cao gắn cảm biến HC-SR04 so với đáy máng (cm)
const float WATER_CLOSE_CM     = 5.0;  // Ngưỡng nước dâng tự động nâng cửa 90° (cm)
const float WATER_OPEN_SAFE_CM = 2.0;  // Ngưỡng nước rút an toàn cho phép hạ cửa (cm)

// Góc Servo tương ứng với cơ cấu tai lệch tâm P(r=55mm, e=14mm) đẩy cửa đúng 0° -> 90°
const int SERVO_ANGLE_HORIZ  = 10;  // Khi cửa nằm phẳng âm sàn 0.0°
const int SERVO_ANGLE_RAISED = 100; // Khi cửa dựng đứng vuông góc 90.0° (hành trình đúng 90°)

const unsigned long MOTOR_MAX_RUN_MS = 8000; // Bảo vệ quá thời gian chạy motor N20 (8 giây)

// -------------------- BIẾN TRẠNG THÁI HỆ THỐNG --------------------
enum GateState {
  STATE_HORIZONTAL = 0, // 0° - Nằm phẳng mặt sàn
  STATE_RAISING    = 1, // Đang nâng lên 90°
  STATE_RAISED     = 2, // 90° - Đã dựng đứng vuông góc (ép kín gioăng EPDM)
  STATE_LOWERING   = 3, // Đang hạ xuống 0°
  STATE_PAUSED_IR  = 4  // Tạm dừng khẩn cấp do cảm biến Hồng ngoại IR phát hiện vật cản
};

GateState gateState = STATE_HORIZONTAL;
GateState stateBeforeIRPause = STATE_HORIZONTAL;

bool autoMode      = true;
bool alarmActive   = false;
bool contactWet    = false;
bool irObstacle    = false;

float distanceCm   = 20.0;
float waterLevelCm = 2.0;
float gateAngleDeg = 0.0;

int highWaterCount = 0;
unsigned long motorStartMs    = 0;
unsigned long lastMeasureMs   = 0;
unsigned long lastBlinkMs     = 0;
bool ledBlinkState            = false;

// -------------------- HÀM ĐO SIÊU ÂM HC-SR04 (LỌC TRUNG VỊ) --------------------
float measureDistanceOnce() {
  digitalWrite(PIN_TRIG, LOW);
  delayMicroseconds(3);
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);

  long duration = pulseIn(PIN_ECHO, HIGH, 25000); // Timeout 25ms (~4m)
  if (duration <= 0) return -1.0;
  float cm = duration * 0.0343f / 2.0f;
  if (cm < 2.0f || cm > 100.0f) return -1.0;
  return cm;
}

void updateSensors() {
  // 1. Đọc cảm biến siêu âm HC-SR04
  float d = measureDistanceOnce();
  if (d > 0) {
    distanceCm = 0.7f * distanceCm + 0.3f * d; // Lọc thông thấp chống nhiễu gợn sóng
    waterLevelCm = SENSOR_HEIGHT_CM - distanceCm;
    if (waterLevelCm < 0.0f) waterLevelCm = 0.0f;
    if (waterLevelCm > 12.0f) waterLevelCm = 12.0f;
  }

  // 2. Đọc cảm biến mực nước tiếp xúc (LOW khi nước chạm cực kim loại hoặc phao đóng)
  contactWet = (digitalRead(PIN_WATER_PROBE) == LOW) || (waterLevelCm >= WATER_CLOSE_CM);

  // 3. Đọc cảm biến Hồng ngoại IR chống kẹp (Module IR FC-51 xuất LOW khi có vật cản phản xạ)
  irObstacle = (digitalRead(PIN_IR_OBSTACLE) == LOW);
}

// -------------------- ĐIỀU KHIỂN CƠ CẤU CHẤP HÀNH (SERVO + N20) --------------------
void stopMotor() {
  digitalWrite(PIN_MOTOR_AIN1, LOW);
  digitalWrite(PIN_MOTOR_AIN2, LOW);
}

void startRaiseGate90() {
  if (irObstacle) {
    stateBeforeIRPause = STATE_RAISING;
    gateState = STATE_PAUSED_IR;
    stopMotor();
    return;
  }
  gateState = STATE_RAISING;
  motorStartMs = millis();
  alarmActive = true;
  // Quay motor N20 chiều nâng
  digitalWrite(PIN_MOTOR_AIN1, HIGH);
  digitalWrite(PIN_MOTOR_AIN2, LOW);
  // Quay Servo tới góc dựng đứng 90°
  gateServo.write(SERVO_ANGLE_RAISED);
}

void startLowerGate0() {
  if (irObstacle) {
    stateBeforeIRPause = STATE_LOWERING;
    gateState = STATE_PAUSED_IR;
    stopMotor();
    return;
  }
  gateState = STATE_LOWERING;
  motorStartMs = millis();
  // Quay motor N20 chiều hạ
  digitalWrite(PIN_MOTOR_AIN1, LOW);
  digitalWrite(PIN_MOTOR_AIN2, HIGH);
  // Đưa Servo về góc phẳng 0°
  gateServo.write(SERVO_ANGLE_HORIZ);
}

void updateGateKinematics() {
  // Bảo vệ chống kẹp bằng cảm biến Hồng ngoại IR
  if (irObstacle && (gateState == STATE_RAISING || gateState == STATE_LOWERING)) {
    stateBeforeIRPause = gateState;
    gateState = STATE_PAUSED_IR;
    stopMotor();
    alarmActive = true;
    return;
  }

  // Tự động tiếp tục hành trình khi vật cản IR đã rời khỏi mặt cửa
  if (!irObstacle && gateState == STATE_PAUSED_IR) {
    if (stateBeforeIRPause == STATE_RAISING) startRaiseGate90();
    else if (stateBeforeIRPause == STATE_LOWERING) startLowerGate0();
    else gateState = STATE_HORIZONTAL;
  }

  // Cập nhật góc cửa ước tính (0° -> 90°) và kiểm tra hoàn tất hành trình
  if (gateState == STATE_RAISING) {
    unsigned long elapsed = millis() - motorStartMs;
    float progress = (float)elapsed / 2500.0f; // 2.5 giây lên hết 90°
    if (progress >= 1.0f || elapsed >= MOTOR_MAX_RUN_MS) {
      gateAngleDeg = 90.0f;
      gateState = STATE_RAISED;
      stopMotor();
    } else {
      gateAngleDeg = progress * 90.0f;
    }
  } else if (gateState == STATE_LOWERING) {
    unsigned long elapsed = millis() - motorStartMs;
    float progress = (float)elapsed / 2500.0f;
    bool limitLowHit = (analogRead(PIN_LIMIT_LOW) < 200);
    if (progress >= 1.0f || limitLowHit || elapsed >= MOTOR_MAX_RUN_MS) {
      gateAngleDeg = 0.0f;
      gateState = STATE_HORIZONTAL;
      stopMotor();
      if (!contactWet && waterLevelCm < WATER_CLOSE_CM) {
        alarmActive = false;
      }
    } else {
      gateAngleDeg = 90.0f * (1.0f - progress);
    }
  }
}

// -------------------- GIAO DIỆN REST API ĐỒNG BỘ WEB APP 3D --------------------
void sendCorsHeaders() {
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.sendHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  server.sendHeader("Access-Control-Allow-Headers", "Content-Type");
}

String getGateStateString() {
  switch (gateState) {
    case STATE_HORIZONTAL: return "HORIZONTAL_0_DEG";
    case STATE_RAISING:    return "RAISING_TO_90_DEG";
    case STATE_RAISED:     return "RAISED_90_DEG";
    case STATE_LOWERING:   return "LOWERING_TO_0_DEG";
    case STATE_PAUSED_IR:  return "PAUSED_IR_OBSTACLE";
    default:               return "UNKNOWN";
  }
}

void handleApiStatus() {
  sendCorsHeaders();
  String json = "{";
  json += "\"water_cm\":" + String(waterLevelCm, 1) + ",";
  json += "\"distance_cm\":" + String(distanceCm, 1) + ",";
  json += "\"gate_angle_deg\":" + String(gateAngleDeg, 1) + ",";
  json += "\"gate_state\":\"" + getGateStateString() + "\",";
  json += "\"auto_mode\":" + String(autoMode ? "true" : "false") + ",";
  json += "\"alarm\":" + String(alarmActive ? "true" : "false") + ",";
  json += "\"contact_wet\":" + String(contactWet ? "true" : "false") + ",";
  json += "\"sump_pit_wet\":" + String(contactWet ? "true" : "false") + ",";
  json += "\"ir_obstacle\":" + String(irObstacle ? "true" : "false");
  json += "}";
  server.send(200, "application/json", json);
}

void handleApiCmd() {
  sendCorsHeaders();
  String action = server.arg("action");
  if (action.length() == 0) action = server.arg("cmd");
  if (action == "raise") {
    startRaiseGate90();
  } else if (action == "lower") {
    startLowerGate0();
  } else if (action == "auto_on") {
    autoMode = true;
  } else if (action == "auto_off") {
    autoMode = false;
  } else if (action == "alarm_on") {
    alarmActive = true;
  } else if (action == "alarm_off") {
    alarmActive = false;
    digitalWrite(PIN_ALARM_LED, LOW);
  }
  handleApiStatus();
}

void handleRoot() {
  sendCorsHeaders();
  String html = "<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>";
  html += "<title>ESP8266 Cửa Chắn Ngập Thủy Lực 90°</title>";
  html += "<style>body{background:#0f172a;color:#f8fafc;font-family:sans-serif;padding:20px;text-align:center}";
  html += ".card{max-width:480px;margin:auto;background:#1e293b;padding:20px;border-radius:12px;border:1px solid #38bdf8}";
  html += "button{margin:6px;padding:12px 18px;border:none;border-radius:8px;font-weight:bold;cursor:pointer;background:#0284c7;color:#fff}</style></head><body>";
  html += "<div class='card'><h2>SA BÀN CỬA CHẮN NGẬP 90° (ESP8266)</h2>";
  html += "<p>Mực nước HC-SR04: <b>" + String(waterLevelCm, 1) + " cm</b> | Góc cửa: <b>" + String(gateAngleDeg, 1) + "° / 90°</b></p>";
  html += "<p>Cảm biến tiếp xúc: <b>" + String(contactWet ? "CHẠM NƯỚC" : "KHÔ") + "</b> | Hồng ngoại IR: <b>" + String(irObstacle ? "CÓ VẬT CẢN!" : "THÔNG THOÁNG") + "</b></p>";
  html += "<p><a href='/api/cmd?action=raise'><button>NÂNG CỬA 90°</button></a>";
  html += "<a href='/api/cmd?action=lower'><button style='background:#475569'>HẠ CỬA 0°</button></a></p>";
  html += "<p style='font-size:13px;color:#94a3b8'>Mở file web_app_3d/index.html trên điện thoại/máy tính để điều khiển 3D Digital Twin & Giọng nói AI.</p></div></body></html>";
  server.send(200, "text/html", html);
}

// -------------------- SETUP & LOOP --------------------
void setup() {
  Serial.begin(115200);

  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  pinMode(PIN_WATER_PROBE, INPUT_PULLUP);
  pinMode(PIN_IR_OBSTACLE, INPUT);
  pinMode(PIN_MOTOR_AIN1, OUTPUT);
  pinMode(PIN_MOTOR_AIN2, OUTPUT);
  pinMode(PIN_ALARM_LED, OUTPUT);

  stopMotor();
  digitalWrite(PIN_ALARM_LED, LOW);

  gateServo.attach(PIN_SERVO);
  gateServo.write(SERVO_ANGLE_HORIZ);

  WiFi.mode(WIFI_AP);
  WiFi.softAP(AP_SSID, AP_PASS);
  Serial.print("AP IP address: ");
  Serial.println(WiFi.softAPIP());

  server.on("/", HTTP_GET, handleRoot);
  server.on("/api/status", HTTP_GET, handleApiStatus);
  server.on("/api/cmd", HTTP_GET, handleApiCmd);
  server.on("/api/cmd", HTTP_OPTIONS, []() {
    sendCorsHeaders();
    server.send(204);
  });
  server.on("/api/command", HTTP_GET, handleApiCmd);
  server.on("/api/command", HTTP_OPTIONS, []() {
    sendCorsHeaders();
    server.send(204);
  });
  server.begin();
}

void loop() {
  server.handleClient();

  unsigned long now = millis();
  if (now - lastMeasureMs >= 250) {
    lastMeasureMs = now;
    updateSensors();

    // Logic tự động nâng cửa lên 90° khi (HC-SR04 >= 5cm HOẶC Cảm biến tiếp xúc báo ngập)
    if (autoMode) {
      if (waterLevelCm >= WATER_CLOSE_CM || contactWet) {
        highWaterCount++;
        if (highWaterCount >= 3 && gateState == STATE_HORIZONTAL && !irObstacle) {
          startRaiseGate90();
        }
      } else {
        highWaterCount = 0;
      }
    }
  }

  updateGateKinematics();

  // Nháy đèn LED cảnh báo & còi khi có ngập hoặc có vật cản IR
  if (alarmActive || irObstacle) {
    if (now - lastBlinkMs >= 300) {
      lastBlinkMs = now;
      ledBlinkState = !ledBlinkState;
      digitalWrite(PIN_ALARM_LED, ledBlinkState ? HIGH : LOW);
    }
  } else {
    digitalWrite(PIN_ALARM_LED, LOW);
  }
}

