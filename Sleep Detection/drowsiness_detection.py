import cv2
import dlib
import pygame
import numpy as np
from scipy.spatial import distance
from datetime import datetime

# Pygame başlatma ve ses dosyasını yükleme
pygame.mixer.init()
pygame.mixer.music.load("alarm.wav")

# Yüz ve landmark dedektörlerini başlatma
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Göz kırpma oranı hesaplama fonksiyonu
def calculate_EAR(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Göz noktalarını alma fonksiyonu
def get_eye_points(facial_landmarks, start, end):
    points = []
    for i in range(start, end):
        point = (facial_landmarks.part(i).x, facial_landmarks.part(i).y)
        points.append(point)
    return points

def main():
    cap = cv2.VideoCapture(0)
    
    # Değişkenler
    EAR_THRESHOLD = 0.25  # Göz kapalı kabul edilecek EAR değeri
    CONSECUTIVE_FRAMES = 20  # Kaç frame boyunca göz kapalı kalırsa uyarı verilecek
    counter = 0
    alarm_on = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            landmarks = predictor(gray, face)
            
            # Sol ve sağ göz noktalarını alma
            left_eye = get_eye_points(landmarks, 42, 48)
            right_eye = get_eye_points(landmarks, 36, 42)
            
            # Göz kırpma oranlarını hesaplama
            left_ear = calculate_EAR(np.array(left_eye))
            right_ear = calculate_EAR(np.array(right_eye))
            
            # Ortalama EAR değeri
            ear = (left_ear + right_ear) / 2.0
            
            # Gözleri çizme
            cv2.polylines(frame, [np.array(left_eye)], True, (0, 255, 0), 1)
            cv2.polylines(frame, [np.array(right_eye)], True, (0, 255, 0), 1)

            # EAR değeri threshold'un altındaysa sayaç artırılır
            if ear < EAR_THRESHOLD:
                counter += 1
                if counter >= CONSECUTIVE_FRAMES:
                    if not alarm_on:
                        alarm_on = True
                        pygame.mixer.music.play(-1)  # Sürekli çalma
                    cv2.putText(frame, "UYARI! UYKULU SURUCU!", (10, 30),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                counter = 0
                if alarm_on:
                    alarm_on = False
                    pygame.mixer.music.stop()

            # EAR değerini ekranda gösterme
            cv2.putText(frame, f"EAR: {ear:.2f}", (300, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        cv2.imshow("Drowsiness Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main() 