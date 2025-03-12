import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

def generate_sample_visualizations(output_dir='results'):
    # Çıktı dizinini oluştur
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Saatlik Yoğunluk Analizi
    hours = range(24)
    customers = [25, 15, 10, 5, 3, 2, 5, 15, 35, 45, 50, 55,
                60, 58, 45, 40, 38, 42, 47, 40, 35, 30, 25, 20]
    
    plt.figure(figsize=(12, 6))
    plt.plot(hours, customers, marker='o')
    plt.title('Saatlik Müşteri Yoğunluğu')
    plt.xlabel('Saat')
    plt.ylabel('Müşteri Sayısı')
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'hourly_distribution.png'))
    plt.close()

    # 2. Isı Haritası
    weekly_data = np.array([
        [10, 15, 20, 25, 30, 25, 20],
        [12, 18, 22, 28, 32, 27, 22],
        [15, 20, 25, 30, 35, 30, 25],
        [18, 25, 30, 35, 40, 35, 30],
        [20, 30, 35, 40, 45, 40, 35],
        [15, 25, 30, 35, 40, 35, 30]
    ])
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(weekly_data, 
                xticklabels=['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
                yticklabels=['10:00', '12:00', '14:00', '16:00', '18:00', '20:00'],
                annot=True, fmt='d', cmap='YlOrRd')
    plt.title('Haftalık Müşteri Yoğunluğu Isı Haritası')
    plt.savefig(os.path.join(output_dir, 'heatmap.png'))
    plt.close()

    # 3. Ziyaret Süresi Dağılımı
    visit_durations = np.random.normal(25, 10, 1000)  # Ortalama 25 dakika
    plt.figure(figsize=(10, 6))
    plt.hist(visit_durations, bins=30, edgecolor='black')
    plt.title('Müşteri Ziyaret Süresi Dağılımı')
    plt.xlabel('Ziyaret Süresi (Dakika)')
    plt.ylabel('Müşteri Sayısı')
    plt.savefig(os.path.join(output_dir, 'visit_duration.png'))
    plt.close()

    # 4. Haftalık Karşılaştırma
    weeks = ['Hafta 1', 'Hafta 2', 'Hafta 3', 'Hafta 4']
    total_customers = [1200, 1350, 1180, 1420]
    avg_duration = [22, 25, 23, 24]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    
    ax1.bar(weeks, total_customers)
    ax1.set_title('Haftalık Toplam Müşteri Sayısı')
    ax1.set_ylabel('Müşteri Sayısı')
    
    ax2.plot(weeks, avg_duration, marker='o')
    ax2.set_title('Haftalık Ortalama Ziyaret Süresi')
    ax2.set_ylabel('Dakika')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'weekly_comparison.png'))
    plt.close()
    
    print(f"Görsel sonuçlar '{output_dir}' dizininde oluşturuldu:")
    print("1. hourly_distribution.png - Saatlik müşteri yoğunluğu")
    print("2. heatmap.png - Haftalık ısı haritası")
    print("3. visit_duration.png - Ziyaret süresi dağılımı")
    print("4. weekly_comparison.png - Haftalık karşılaştırmalar")

# Örnek sonuçları 'results' dizininde oluştur
generate_sample_visualizations() 