import unittest
import cv2
import numpy as np
import google.generativeai as genai
from PIL import Image

class TestAIIntegration(unittest.TestCase):
    def setUp(self):
        # Test için API anahtarını yapılandır
        genai.configure(api_key="YOUR_API_KEY")
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Test için örnek bir canvas oluştur
        self.test_canvas = np.zeros((720, 1280, 3), dtype=np.uint8)
        cv2.putText(self.test_canvas, "2+2", (100, 100), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        
    def test_model_initialization(self):
        """AI modelinin doğru şekilde başlatıldığını kontrol et"""
        self.assertIsNotNone(self.model)
        
    def test_image_conversion(self):
        """Canvas'ın PIL Image'a doğru şekilde dönüştürüldüğünü kontrol et"""
        pil_image = Image.fromarray(self.test_canvas)
        self.assertIsInstance(pil_image, Image.Image)
        self.assertEqual(pil_image.size, (1280, 720))
        
    def test_model_response(self):
        """Model yanıtının beklenen formatta olduğunu kontrol et"""
        pil_image = Image.fromarray(self.test_canvas)
        response = self.model.generate_content(["Solve this math problem", pil_image])
        self.assertIsNotNone(response)
        self.assertTrue(hasattr(response, 'text'))
        
    def test_empty_canvas(self):
        """Boş canvas ile model yanıtını kontrol et"""
        empty_canvas = np.zeros((720, 1280, 3), dtype=np.uint8)
        pil_image = Image.fromarray(empty_canvas)
        response = self.model.generate_content(["Solve this math problem", pil_image])
        self.assertIsNotNone(response)

if __name__ == '__main__':
    unittest.main() 