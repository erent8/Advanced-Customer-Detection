import unittest
import cv2
import numpy as np
from drowsiness_detection import calculate_EAR, get_eye_points

class TestDrowsinessDetection(unittest.TestCase):
    def setUp(self):
        # Test için yapay landmark noktaları oluşturma
        class MockLandmark:
            def __init__(self, x, y):
                self.x = x
                self.y = y
            def part(self, index):
                return self

        self.mock_landmarks = MockLandmark(0, 0)
        
    def test_calculate_EAR(self):
        # Test için yapay göz noktaları
        eye_points = np.array([
            (0, 0),    # P1
            (1, 2),    # P2
            (2, 2),    # P3
            (3, 0),    # P4
            (2, -2),   # P5
            (1, -2)    # P6
        ])
        
        # EAR hesaplama
        ear = calculate_EAR(eye_points)
        
        # EAR değerinin makul bir aralıkta olduğunu kontrol etme
        self.assertTrue(0 < ear < 1, f"EAR değeri ({ear}) makul aralıkta değil")
        
    def test_get_eye_points(self):
        # Test için göz noktalarını alma
        eye_points = get_eye_points(self.mock_landmarks, 36, 42)
        
        # Doğru sayıda nokta döndürüldüğünü kontrol etme
        self.assertEqual(len(eye_points), 6, "Göz noktaları sayısı yanlış")
        
        # Her noktanın (x,y) koordinatları içerdiğini kontrol etme
        for point in eye_points:
            self.assertEqual(len(point), 2, "Nokta koordinatları eksik")
            
    def test_eye_aspect_ratio_threshold(self):
        # Açık göz için test noktaları
        open_eye = np.array([
            (0, 0),
            (1, 2),
            (2, 2),
            (3, 0),
            (2, -2),
            (1, -2)
        ])
        
        # Kapalı göz için test noktaları
        closed_eye = np.array([
            (0, 0),
            (1, 0.2),
            (2, 0.2),
            (3, 0),
            (2, -0.2),
            (1, -0.2)
        ])
        
        # EAR değerlerini hesaplama
        open_ear = calculate_EAR(open_eye)
        closed_ear = calculate_EAR(closed_eye)
        
        # Kapalı gözün EAR değerinin açık gözden küçük olduğunu kontrol etme
        self.assertLess(closed_ear, open_ear, "Kapalı göz EAR değeri açık gözden büyük")
        
    def test_invalid_input(self):
        # Boş nokta listesi için test
        with self.assertRaises(Exception):
            calculate_EAR([])
            
        # Yanlış sayıda nokta için test
        with self.assertRaises(Exception):
            calculate_EAR(np.array([(0,0), (1,1)]))

if __name__ == '__main__':
    unittest.main() 