import unittest
import sys
import os

# Test dizinini Python path'ine ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test dosyalarını yükle
from tests.test_hand_detection import TestHandDetection
from tests.test_gesture_recognition import TestGestureRecognition
from tests.test_ai_integration import TestAIIntegration

def run_tests():
    # Test suite oluştur
    test_suite = unittest.TestSuite()
    
    # Testleri suite'e ekle
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestHandDetection))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGestureRecognition))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestAIIntegration))
    
    # Test sonuçlarını ayrıntılı göster
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1) 