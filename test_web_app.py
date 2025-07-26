"""
Web App Test Scripti
Flask uygulamasının çalışıp çalışmadığını kontrol eder
"""

import requests
import json
import time
from datetime import datetime

def test_web_app():
    """Web app'i test et"""
    base_url = "http://127.0.0.1:5000"
    
    print("🧪 Web App Test Başlıyor...")
    print("=" * 50)
    
    # 1. Ana sayfa testi
    print("1. 🏠 Ana sayfa testi...")
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("   ✅ Ana sayfa erişilebilir")
        else:
            print(f"   ❌ Ana sayfa hatası: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Ana sayfa bağlantı hatası: {e}")
    
    # 2. Mobile sayfa testi
    print("2. 📱 Mobile sayfa testi...")
    try:
        response = requests.get(f"{base_url}/mobile", timeout=5)
        if response.status_code == 200:
            print("   ✅ Mobile sayfa erişilebilir")
        else:
            print(f"   ❌ Mobile sayfa hatası: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Mobile sayfa bağlantı hatası: {e}")
    
    # 3. Stats API testi
    print("3. 📊 Stats API testi...")
    try:
        response = requests.get(f"{base_url}/api/stats/current", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Stats API çalışıyor")
            print(f"   📈 Data: {json.dumps(data, indent=2)}")
        else:
            print(f"   ❌ Stats API hatası: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Stats API bağlantı hatası: {e}")
    
    # 4. Sistem başlatma API testi
    print("4. 🚀 Sistem başlatma API testi...")
    try:
        response = requests.post(f"{base_url}/api/system/start", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Start API yanıt verdi")
            print(f"   📝 Sonuç: {data}")
        else:
            print(f"   ❌ Start API hatası: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Start API bağlantı hatası: {e}")
    
    # 5. Video feed testi
    print("5. 🎬 Video stream testi...")
    try:
        response = requests.get(f"{base_url}/video_feed", timeout=5, stream=True)
        if response.status_code == 200:
            print("   ✅ Video stream endpoint erişilebilir")
        else:
            print(f"   ❌ Video stream hatası: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Video stream bağlantı hatası: {e}")
    
    # 6. Today visitors API testi
    print("6. 👥 Today visitors API testi...")
    try:
        response = requests.get(f"{base_url}/api/visitors/today", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Visitors API çalışıyor")
            print(f"   👤 Data: {json.dumps(data, indent=2)}")
        else:
            print(f"   ❌ Visitors API hatası: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Visitors API bağlantı hatası: {e}")
    
    print("=" * 50)
    print("✅ Test tamamlandı!")
    
    # Manuel test talimatları
    print("\n🎯 MANUEL TEST TALİMATLARI:")
    print(f"1. Tarayıcıda açın: {base_url}")
    print(f"2. Mobile test: {base_url}/mobile")
    print("3. 'Başlat' butonuna basın")
    print("4. Video stream'in çalıştığını kontrol edin")
    print("5. Stats panelinin güncellendiğini kontrol edin")

if __name__ == "__main__":
    test_web_app() 