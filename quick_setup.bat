@echo off
echo ======================================================
echo   OpenCV Musteri Analiz Sistemi - Hizli Kurulum
echo ======================================================
echo.

echo [1/5] Sanal ortami temizleniyor...
if exist .venv (
    rmdir /s /q .venv
    echo    Eski sanal ortam silindi
)

echo [2/5] Yeni sanal ortam olusturuluyor...
python -m venv .venv
if %errorlevel% neq 0 (
    echo HATA: Python bulunamadi veya sanal ortam olusturulamadi
    pause
    exit /b 1
)

echo [3/5] Sanal ortam etkinlestiriliyor...
call .venv\Scripts\activate.bat

echo [4/5] Minimal kutuphaneler yukleniyor...
python -m pip install --upgrade pip
pip install -r requirements_minimal.txt
if %errorlevel% neq 0 (
    echo HATA: Kutuphaneler yuklenemedi
    pause
    exit /b 1
)

echo [5/5] Sistem test ediliyor...
python test_requirements.py
if %errorlevel% neq 0 (
    echo UYARI: Test sirasinda sorun olustu
)

echo.
echo =====================================================
echo   KURULUM TAMAMLANDI!
echo =====================================================
echo.
echo Sistemi baslatmak icin:
echo   python main.py
echo.
echo Yuz tanima ozelligini etkinlestirmek icin (sonradan):
echo   pip install dlib face-recognition
echo.
pause 