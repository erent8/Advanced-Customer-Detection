import cv2
import mediapipe as mp
import pyautogui
import math

# Mediapipe modüllerini başlat
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Kamera çözünürlüğü(optimize olanı seçin.)
cam_width, cam_height = 1920, 480

# Kamera erişim hatasını yönetmek için try-except bloğu ekleyelim
try:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Kamera başlatılamadı!")
except Exception as e:
    print(f"Hata: {e}")
    exit()
cap.set(3, cam_width)  # Genişlik
cap.set(4, cam_height)  # Yükseklik

# Kamera çözünürlük ayarlarını kontrol et
def check_camera_resolution():
    actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    if actual_width != cam_width or actual_height != cam_height:
        print(f"Uyarı: İstenen çözünürlük ({cam_width}x{cam_height}) ayarlanamadı.")
        print(f"Mevcut çözünürlük: {actual_width}x{actual_height}")
    
    return actual_width, actual_height

# Kamera başlatıldıktan sonra çağır
actual_width, actual_height = check_camera_resolution()

# MediaPipe başlatma hatası yönetimi
try:
    hands = mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )
except Exception as e:
    print(f"MediaPipe başlatılamadı: {e}")
    exit()

# Ekran boyutunu al (pyautogui ile fare kontrolü için)
screen_width, screen_height = pyautogui.size()

# Yakınlaştırma/uzaklaştırma için başlangıç ölçeği
zoom_scale = 1.0

# PyAutoGUI güvenlik ayarları
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1  # İşlemler arası minimum bekleme süresi

def calculate_distance(point1, point2):
    """İki nokta arasındaki mesafeyi hesaplar."""
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

# Program sonlandırma işlemlerini düzgün yapma
def cleanup():
    try:
        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"Temizleme sırasında hata: {e}")

# Ana döngüde
try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Çerçeveyi aynalayarak daha kullanıcı dostu bir deneyim yarat
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Mediapipe ile işleme
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            hand_distances = []

            for hand_landmarks in results.multi_hand_landmarks:
                # Ekranda el izlerini çiz
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # El parmak uçlarını al
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]

                # Fare hareketi için işaret parmağı koordinatlarını kullan
                screen_x = int(index_tip.x * screen_width)
                screen_y = int(index_tip.y * screen_height)
                pyautogui.moveTo(screen_x, screen_y)

                # Tıklama işlemleri
                if calculate_distance(thumb_tip, index_tip) < 0.05:
                    pyautogui.click()  # Sol tık
                elif calculate_distance(thumb_tip, middle_tip) < 0.05:
                    pyautogui.rightClick()  # Sağ tık
                elif calculate_distance(thumb_tip, ring_tip) < 0.05:
                    pyautogui.doubleClick()  # Çift tık

                # Yakınlaştırma/Uzaklaştırma (iki el ile)
                hand_distances.append(thumb_tip)
            
            if len(results.multi_hand_landmarks) == 2:  # İki el varsa
                thumb_1 = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.THUMB_TIP]
                thumb_2 = results.multi_hand_landmarks[1].landmark[mp_hands.HandLandmark.THUMB_TIP]
                distance = calculate_distance(thumb_1, thumb_2)

                if distance > 0.15:  # Uzaksa yakınlaştır
                    zoom_scale = min(zoom_scale + 0.02, 2.0)  # Maksimum 2x
                elif distance < 0.1:  # Yakınsa uzaklaştır
                    zoom_scale = max(zoom_scale - 0.02, 1.0)  # Minimum 1x

        # Yakınlaştırma/uzaklaştırma işlemleri
        height, width, _ = frame.shape
        center_x, center_y = width // 2, height // 2
        new_width = int(width * zoom_scale)
        new_height = int(height * zoom_scale)

        # Çerçeveyi yakınlaştırma oranına göre yeniden boyutlandır
        resized_frame = cv2.resize(frame, (new_width, new_height))
        cropped_frame = resized_frame[
            (new_height - height) // 2 : (new_height + height) // 2,
            (new_width - width) // 2 : (new_width + width) // 2,
        ]
        frame = cropped_frame

        # OpenCV ile ekran göster
        cv2.imshow("AI Virtual Mouse", frame)

        # Çıkış işlemi
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            cleanup()
            break
except KeyboardInterrupt:
    print("\nProgram kullanıcı tarafından sonlandırıldı.")
    cleanup()
except Exception as e:
    print(f"Beklenmeyen hata: {e}")
    cleanup()
