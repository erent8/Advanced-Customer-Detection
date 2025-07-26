# OpenCV Müşteri Analiz Sistemi - Hızlı Kurulum (PowerShell)

Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "  OpenCV Müşteri Analiz Sistemi - Hızlı Kurulum" -ForegroundColor Cyan  
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host ""

try {
    Write-Host "[1/5] Sanal ortamı temizleniyor..." -ForegroundColor Yellow
    if (Test-Path ".venv") {
        Remove-Item -Recurse -Force ".venv"
        Write-Host "    ✅ Eski sanal ortam silindi" -ForegroundColor Green
    }

    Write-Host "[2/5] Yeni sanal ortam oluşturuluyor..." -ForegroundColor Yellow  
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        throw "Python bulunamadı veya sanal ortam oluşturulamadı"
    }
    Write-Host "    ✅ Sanal ortam oluşturuldu" -ForegroundColor Green

    Write-Host "[3/5] Sanal ortam etkinleştiriliyor..." -ForegroundColor Yellow
    .\.venv\Scripts\Activate.ps1
    Write-Host "    ✅ Sanal ortam etkinleştirildi" -ForegroundColor Green

    Write-Host "[4/5] Minimal kütüphaneler yükleniyor..." -ForegroundColor Yellow
    Write-Host "    📦 Pip güncelleniyor..." -ForegroundColor Gray
    python -m pip install --upgrade pip | Out-Null
    
    Write-Host "    📦 Temel kütüphaneler yükleniyor (dlib hariç)..." -ForegroundColor Gray
    pip install -r requirements_minimal.txt
    
    if ($LASTEXITCODE -ne 0) {
        throw "Kütüphaneler yüklenemedi"
    }
    Write-Host "    ✅ Kütüphaneler yüklendi" -ForegroundColor Green

    Write-Host "[5/5] Sistem test ediliyor..." -ForegroundColor Yellow
    python test_requirements.py

    Write-Host ""
    Write-Host "=====================================================" -ForegroundColor Green
    Write-Host "  🎉 KURULUM BAŞARIYLA TAMAMLANDI!" -ForegroundColor Green
    Write-Host "=====================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Sistemi başlatmak için:" -ForegroundColor White
    Write-Host "  python main.py" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Yüz tanıma özelliğini etkinleştirmek için (sonradan):" -ForegroundColor Gray
    Write-Host "  pip install dlib face-recognition" -ForegroundColor Gray
    Write-Host ""

} catch {
    Write-Host ""
    Write-Host "❌ HATA: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔧 Manuel kurulum için:" -ForegroundColor Yellow
    Write-Host "1. deactivate" -ForegroundColor Gray
    Write-Host "2. Remove-Item -Recurse -Force .venv" -ForegroundColor Gray  
    Write-Host "3. python -m venv .venv" -ForegroundColor Gray
    Write-Host "4. .\.venv\Scripts\Activate.ps1" -ForegroundColor Gray
    Write-Host "5. pip install -r requirements_minimal.txt" -ForegroundColor Gray
}

Read-Host "Devam etmek için Enter'a basın" 