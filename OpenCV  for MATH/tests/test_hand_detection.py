import unittest
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

class TestHandDetection(unittest.TestCase):
    def setUp(self):
        self.detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.7, minTrackCon=0.5)
        # Test için boş bir görüntü oluştur
        self.test_image = np.zeros((720, 1280, 3), dtype=np.uint8)
        
    def test_detector_initialization(self):
        """El detektörünün doğru şekilde başlatıldığını kontrol et"""
        self.assertIsNotNone(self.detector)
        self.assertEqual(self.detector.maxHands, 1)
        self.assertEqual(self.detector.detectionCon, 0.7)
        
    def test_find_hands_empty_image(self):
        """Boş görüntüde el algılama testi"""
        hands, img = self.detector.findHands(self.test_image, draw=False)
        self.assertEqual(len(hands), 0)
        
    def test_image_dimensions(self):
        """Görüntü boyutlarının doğru olduğunu kontrol et"""
        height, width = self.test_image.shape[:2]
        self.assertEqual(height, 720)
        self.assertEqual(width, 1280)
        
if __name__ == '__main__':
    unittest.main() 