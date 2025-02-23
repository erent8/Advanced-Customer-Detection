import unittest
import numpy as np
from main import getHandInfo

class TestGestureRecognition(unittest.TestCase):
    def setUp(self):
        # Test için örnek el landmark verileri
        self.sample_hand = {
            "lmList": [[0, 100, 100] for _ in range(21)],  # 21 landmark noktası
            "type": "Right"
        }
        
    def test_writing_mode(self):
        """Yazma modu el hareketini test et (işaret parmağı yukarıda)"""
        # İşaret parmağı yukarıda, diğerleri aşağıda
        self.sample_hand["lmList"][8][1] -= 50  # İşaret parmağı yukarı
        fingers = [0, 1, 0, 0, 0]  # Beklenen parmak durumu
        result = getHandInfo(self.sample_hand)
        self.assertEqual(result, fingers)
        
    def test_erasing_mode(self):
        """Silme modu el hareketini test et (başparmak yukarıda)"""
        # Başparmak yukarıda, diğerleri aşağıda
        self.sample_hand["lmList"][4][1] -= 50  # Başparmak yukarı
        fingers = [1, 0, 0, 0, 0]  # Beklenen parmak durumu
        result = getHandInfo(self.sample_hand)
        self.assertEqual(result, fingers)
        
    def test_solution_mode(self):
        """Çözüm modu el hareketini test et (dört parmak yukarıda)"""
        # Dört parmak yukarıda (serçe hariç)
        for i in [4, 8, 12, 16]:  # Dört parmak landmark'ları
            self.sample_hand["lmList"][i][1] -= 50
        fingers = [1, 1, 1, 1, 0]  # Beklenen parmak durumu
        result = getHandInfo(self.sample_hand)
        self.assertEqual(result, fingers)

if __name__ == '__main__':
    unittest.main() 