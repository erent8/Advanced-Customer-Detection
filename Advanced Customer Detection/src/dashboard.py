from dash import Dash, html, dcc, Input, Output, State, callback_context
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import xlsxwriter
import io
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import cv2
import threading
import queue
import time
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from statsmodels.tsa.seasonal import seasonal_decompose
import holidays
import calendar

from src.analytics import CustomerAnalytics
from src.logger import log_error

class CustomerDashboard:
    """Müşteri verilerini interaktif dashboard olarak görüntüleme sınıfı."""
    
    def __init__(self, analytics: CustomerAnalytics):
        """
        Args:
            analytics (CustomerAnalytics): Müşteri analiz verileri
        """
        self.analytics = analytics
        self.app = Dash(__name__, 
                       suppress_callback_exceptions=True,
                       meta_tags=[
                           {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                       ])
        self.server = self.app.server
        self.frame_queue = queue.Queue(maxsize=10)
        self.alert_threshold = 50  # Müşteri sayısı eşiği
        
        # Kamera görüntüsü için thread başlat
        self.camera_thread = threading.Thread(target=self._camera_stream, daemon=True)
        self.camera_thread.start()
        
        self._setup_layout()
        self._setup_callbacks()
        self._setup_styles()
    
    def _camera_stream(self):
        """Kamera akışı yerine örnek görüntü kullan."""
        while True:
            # Örnek bir görüntü oluştur
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            frame[:] = (200, 200, 200)  # Gri arka plan
            
            # Örnek metin ekle
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, 'Ornek Goruntu', (200, 240), font, 1, (0, 0, 0), 2)
            
            # Frame'i base64'e çevir
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode()
            
            # Kuyruğu güncelle
            if not self.frame_queue.full():
                self.frame_queue.put(jpg_as_text)
            else:
                try:
                    self.frame_queue.get_nowait()
                    self.frame_queue.put(jpg_as_text)
                except queue.Empty:
                    pass
            
            time.sleep(0.1)  # CPU kullanımını azalt
    
    def _setup_styles(self):
        """Dashboard stillerini ayarla."""
        self.app.index_string = '''
        <!DOCTYPE html>
        <html>
            <head>
                {%metas%}
                <title>Müşteri Analiz Dashboardu</title>
                {%favicon%}
                {%css%}
                <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
                <style>
                    :root {
                        /* Açık tema renkleri */
                        --light-primary-color: #2D3748;
                        --light-secondary-color: #4A5568;
                        --light-accent-color: #4299E1;
                        --light-background-color: #F7FAFC;
                        --light-card-background: #FFFFFF;
                        --light-border-color: #E2E8F0;
                        
                        /* Koyu tema renkleri */
                        --dark-primary-color: #E2E8F0;
                        --dark-secondary-color: #A0AEC0;
                        --dark-accent-color: #63B3ED;
                        --dark-background-color: #1A202C;
                        --dark-card-background: #2D3748;
                        --dark-border-color: #4A5568;
                    }
                    
                    [data-theme="light"] {
                        --primary-color: var(--light-primary-color);
                        --secondary-color: var(--light-secondary-color);
                        --accent-color: var(--light-accent-color);
                        --background-color: var(--light-background-color);
                        --card-background: var(--light-card-background);
                        --border-color: var(--light-border-color);
                    }
                    
                    [data-theme="dark"] {
                        --primary-color: var(--dark-primary-color);
                        --secondary-color: var(--dark-secondary-color);
                        --accent-color: var(--dark-accent-color);
                        --background-color: var(--dark-background-color);
                        --card-background: var(--dark-card-background);
                        --border-color: var(--dark-border-color);
                    }
                    
                    body {
                        font-family: 'Inter', sans-serif;
                        background-color: var(--background-color);
                        margin: 0;
                        padding: 20px;
                        color: var(--primary-color);
                        transition: all 0.3s ease;
                    }
                    
                    /* Tema değiştirici */
                    .theme-switcher {
                        position: fixed;
                        top: 20px;
                        right: 20px;
                        z-index: 1000;
                    }
                    
                    .theme-button {
                        background: var(--card-background);
                        border: 1px solid var(--border-color);
                        color: var(--primary-color);
                        padding: 8px 16px;
                        border-radius: 6px;
                        cursor: pointer;
                        transition: all 0.3s ease;
                    }
                    
                    .theme-button:hover {
                        background: var(--accent-color);
                        color: white;
                    }
                    
                    .dashboard-container {
                        max-width: 1400px;
                        margin: 0 auto;
                    }
                    
                    .dashboard-title {
                        font-size: 24px;
                        font-weight: 600;
                        color: var(--primary-color);
                        margin-bottom: 30px;
                        padding-bottom: 15px;
                        border-bottom: 2px solid var(--border-color);
                    }
                    
                    .controls-container {
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        gap: 20px;
                        margin-bottom: 30px;
                    }
                    
                    .control-card {
                        background: var(--card-background);
                        padding: 20px;
                        border-radius: 12px;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    }
                    
                    .control-title {
                        font-size: 16px;
                        font-weight: 500;
                        color: var(--secondary-color);
                        margin-bottom: 15px;
                    }
                    
                    .graph-grid {
                        display: grid;
                        grid-template-columns: repeat(2, 1fr);
                        gap: 20px;
                        margin-bottom: 20px;
                    }
                    
                    .graph-card {
                        background: var(--card-background);
                        padding: 20px;
                        border-radius: 12px;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    }
                    
                    .graph-title {
                        font-size: 16px;
                        font-weight: 500;
                        color: var(--secondary-color);
                        margin-bottom: 15px;
                    }
                    
                    .stats-card {
                        background: var(--card-background);
                        padding: 25px;
                        border-radius: 12px;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    }
                    
                    .stats-title {
                        font-size: 16px;
                        font-weight: 500;
                        color: var(--secondary-color);
                        margin-bottom: 20px;
                    }
                    
                    .stats-list {
                        list-style: none;
                        padding: 0;
                        margin: 0;
                    }
                    
                    .stats-list li {
                        padding: 12px 0;
                        border-bottom: 1px solid var(--border-color);
                        color: var(--secondary-color);
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }
                    
                    .stats-list li:last-child {
                        border-bottom: none;
                    }

                    .stats-label {
                        font-size: 14px;
                        color: var(--secondary-color);
                    }

                    .stats-value {
                        font-size: 16px;
                        font-weight: 600;
                        color: var(--primary-color);
                    }

                    .stats-empty, .stats-error {
                        text-align: center;
                        padding: 20px;
                        color: var(--secondary-color);
                        font-size: 14px;
                    }

                    .stats-error {
                        color: #E53E3E;
                    }

                    /* DatePicker ve Dropdown stilleri */
                    .date-picker {
                        width: 100%;
                    }

                    .view-mode-dropdown {
                        width: 100%;
                    }

                    .DateInput {
                        width: 120px;
                    }

                    .DateInput_input {
                        font-size: 14px;
                        padding: 8px 12px;
                        border-radius: 6px;
                    }

                    .SingleDatePickerInput__withBorder,
                    .DateRangePickerInput__withBorder {
                        border-color: var(--border-color);
                        border-radius: 6px;
                    }

                    .Select-control {
                        border-color: var(--border-color) !important;
                        border-radius: 6px !important;
                    }

                    /* Responsive tasarım */
                    @media (max-width: 1200px) {
                        .graph-grid {
                            grid-template-columns: 1fr;
                        }
                    }

                    @media (max-width: 768px) {
                        .controls-container {
                            grid-template-columns: 1fr;
                        }

                        body {
                            padding: 10px;
                        }

                        .dashboard-title {
                            font-size: 20px;
                        }
                    }
                    
                    /* Mobil uyumluluk */
                    @media (max-width: 768px) {
                        .dashboard-container {
                            padding: 10px;
                        }
                        
                        .controls-container {
                            grid-template-columns: 1fr;
                        }
                        
                        .graph-grid {
                            grid-template-columns: 1fr;
                        }
                        
                        .metric-card {
                            margin-bottom: 15px;
                        }
                    }
                    
                    /* Ayarlar menüsü */
                    .settings-container {
                        position: fixed;
                        top: 20px;
                        right: 20px;
                        z-index: 1000;
                    }
                    
                    .settings-button {
                        background: var(--card-background);
                        border: none;
                        border-radius: 50%;
                        width: 40px;
                        height: 40px;
                        font-size: 20px;
                        cursor: pointer;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                        transition: all 0.3s ease;
                    }
                    
                    .settings-button:hover {
                        transform: rotate(45deg);
                    }
                    
                    .settings-menu {
                        position: absolute;
                        top: 50px;
                        right: 0;
                        background: var(--card-background);
                        border-radius: 8px;
                        padding: 20px;
                        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
                        min-width: 250px;
                    }
                    
                    .settings-title {
                        margin: 0 0 10px 0;
                        color: var(--primary-color);
                    }
                    
                    .settings-item {
                        margin: 15px 0;
                    }
                    
                    .settings-item label {
                        display: block;
                        margin-bottom: 5px;
                        color: var(--secondary-color);
                    }
                    
                    .settings-dropdown {
                        width: 100%;
                        margin-top: 5px;
                    }
                    
                    .settings-checklist {
                        margin-top: 5px;
                    }
                    
                    .save-button {
                        width: 100%;
                        padding: 8px;
                        background: var(--accent-color);
                        color: white;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                        margin-top: 15px;
                    }
                    
                    .save-button:hover {
                        opacity: 0.9;
                    }
                    
                    /* Widget stilleri */
                    .widget {
                        transition: all 0.3s ease;
                    }
                    
                    .widget.dragging {
                        opacity: 0.7;
                        transform: scale(0.95);
                    }
                    
                    /* Animasyonlar */
                    @keyframes fadeIn {
                        from { opacity: 0; }
                        to { opacity: 1; }
                    }
                    
                    .fade-in {
                        animation: fadeIn 0.3s ease;
                    }
                    
                    @keyframes slideIn {
                        from { transform: translateY(-20px); opacity: 0; }
                        to { transform: translateY(0); opacity: 1; }
                    }
                    
                    .slide-in {
                        animation: slideIn 0.3s ease;
                    }
                </style>
            </head>
            <body data-theme="light">
                {%app_entry%}
                <footer>
                    {%config%}
                    {%scripts%}
                    {%renderer%}
                </footer>
                <script>
                    // Mevcut JavaScript kodları
                    
                    // Widget sürükleme işlevselliği
                    document.addEventListener('DOMContentLoaded', function() {
                        const widgets = document.querySelectorAll('.widget');
                        let draggedWidget = null;
                        
                        widgets.forEach(widget => {
                            widget.addEventListener('dragstart', function(e) {
                                draggedWidget = this;
                                this.classList.add('dragging');
                            });
                            
                            widget.addEventListener('dragend', function(e) {
                                this.classList.remove('dragging');
                            });
                            
                            widget.addEventListener('dragover', function(e) {
                                e.preventDefault();
                                if (draggedWidget !== this) {
                                    const rect = this.getBoundingClientRect();
                                    const next = (e.clientY - rect.top) / (rect.bottom - rect.top) > 0.5;
                                    this.parentNode.insertBefore(draggedWidget, next ? this.nextSibling : this);
                                }
                            });
                        });
                    });
                    
                    // Ayarlar menüsü
                    document.getElementById('settings-button').addEventListener('click', function() {
                        const menu = document.getElementById('settings-menu');
                        menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
                    });
                    
                    // Kullanıcı tercihlerini kaydet
                    document.getElementById('save-settings').addEventListener('click', function() {
                        const layout = document.getElementById('layout-preference').value;
                        const widgets = Array.from(document.getElementById('visible-widgets').selectedOptions)
                            .map(option => option.value);
                        
                        localStorage.setItem('dashboardLayout', layout);
                        localStorage.setItem('visibleWidgets', JSON.stringify(widgets));
                        
                        // Ayarları uygula
                        applySettings();
                    });
                    
                    // Sayfa yüklendiğinde ayarları uygula
                    function applySettings() {
                        const layout = localStorage.getItem('dashboardLayout') || 'standard';
                        const widgets = JSON.parse(localStorage.getItem('visibleWidgets')) || 
                            ['trend', 'heatmap', 'demographics', 'performance', 'forecasts'];
                        
                        document.body.className = layout;
                        widgets.forEach(widget => {
                            const element = document.querySelector(`[data-widget="${widget}"]`);
                            if (element) {
                                element.style.display = 'block';
                            }
                        });
                    }
                </script>
            </body>
        </html>
        '''
    
    def _setup_layout(self):
        """Dashboard düzenini oluştur."""
        self.app.layout = html.Div([
            # Ana başlık
            html.H1("Müşteri Analiz Dashboardu", className="dashboard-title"),
            
            # Filtreler
            html.Div([
                html.Div([
                    html.H3("Zaman Aralığı", className="control-title"),
                    dcc.DatePickerRange(
                        id='date-picker-range',
                        start_date=(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
                        end_date=datetime.now().strftime('%Y-%m-%d'),
                        display_format='DD/MM/YYYY',
                        className="date-picker"
                    )
                ], className="control-card"),
                
                html.Div([
                    html.H3("Görüntüleme Modu", className="control-title"),
                    dcc.Dropdown(
                        id='view-mode',
                        options=[
                            {'label': 'Saatlik Analiz', 'value': 'hourly'},
                            {'label': 'Günlük Analiz', 'value': 'daily'},
                            {'label': 'Haftalık Analiz', 'value': 'weekly'},
                            {'label': 'Aylık Analiz', 'value': 'monthly'}
                        ],
                        value='daily',
                        className="view-mode-dropdown"
                    )
                ], className="control-card")
            ], className="controls-container"),
            
            # Grafikler
            html.Div([
                # Müşteri Trendi
                html.Div([
                    html.H3("Müşteri Trendi", className="graph-title"),
                    dcc.Graph(id='customer-trend')
                ], className="graph-card"),
                
                # Yoğunluk Haritası
                html.Div([
                    html.H3("Yoğunluk Haritası", className="graph-title"),
                    dcc.Graph(id='heatmap')
                ], className="graph-card"),
                
                # Özet İstatistikler
                html.Div([
                    html.H3("Özet İstatistikler", className="stats-title"),
                    html.Div(id='statistics', className="stats-list")
                ], className="stats-card")
            ], className="graph-grid"),
            
            # Interval komponenti
            dcc.Interval(
                id='interval-component',
                interval=1*1000,  # 1 saniye
                n_intervals=0
            )
        ], className="dashboard-container")
    
    def _setup_callbacks(self):
        """Callback'leri ayarla."""
        @self.app.callback(
            [Output('customer-trend', 'figure'),
             Output('heatmap', 'figure'),
             Output('statistics', 'children')],
            [Input('date-picker-range', 'start_date'),
             Input('date-picker-range', 'end_date'),
             Input('view-mode', 'value')]
        )
        def update_graphs(start_date, end_date, view_mode):
            if not start_date or not end_date:
                return {}, {}, []
            
            # Günlük rapor al
            daily_data = self.analytics.get_daily_report(start_date, end_date)
            
            # Müşteri Trendi Grafiği
            trend_fig = go.Figure()
            dates = list(daily_data.keys())
            values = [data['toplam_musteri'] for data in daily_data.values()]
            
            trend_fig.add_trace(go.Scatter(
                x=dates,
                y=values,
                mode='lines+markers',
                name='Müşteri Sayısı',
                line=dict(color='#2D3748', width=2),
                marker=dict(size=8)
            ))
            trend_fig.update_layout(
                title='Müşteri Trendi',
                xaxis_title='Tarih',
                yaxis_title='Müşteri Sayısı',
                template='plotly_white',
                hovermode='x unified',
                showlegend=False
            )
            
            # Yoğunluk Haritası
            heatmap_data = self.analytics.get_hourly_stats(start_date, end_date)
            days = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
            hours = [f"{hour:02d}:00" for hour in range(24)]
            
            heatmap_fig = go.Figure(data=go.Heatmap(
                z=heatmap_data,
                x=days,
                y=hours,
                colorscale='Viridis',
                hoverongaps=False
            ))
            heatmap_fig.update_layout(
                title='Haftalık Yoğunluk Haritası',
                xaxis_title='Gün',
                yaxis_title='Saat',
                template='plotly_white'
            )
            
            # Özet İstatistikler
            summary_stats = self.analytics.get_summary_stats(start_date, end_date)
            if summary_stats:
                stats = html.Ul([
                    html.Li([
                        html.Span("Toplam Müşteri", className="stats-label"),
                        html.Span(f"{summary_stats['toplam_musteri']:,}", className="stats-value")
                    ]),
                    html.Li([
                        html.Span("Ortalama Müşteri", className="stats-label"),
                        html.Span(f"{summary_stats['ortalama_musteri']:,.1f}", className="stats-value")
                    ]),
                    html.Li([
                        html.Span("En Yoğun Gün", className="stats-label"),
                        html.Span(f"{summary_stats['en_yogun_gun']} ({summary_stats['en_yogun_gun_musteri']:,} müşteri)", 
                                className="stats-value")
                    ])
                ])
            else:
                stats = html.Div("Veri bulunamadı", className="stats-empty")
            
            return trend_fig, heatmap_fig, stats
    
    def _generate_pdf_report(self, sections, start_date, end_date):
        # PDF rapor oluşturma
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Başlık tablosu
        title_data = [['Müşteri Analiz Raporu'],
                      [f'Tarih Aralığı: {start_date} - {end_date}']]
        title_table = Table(title_data)
        title_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 16),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ]))
        elements.append(title_table)
        
        # Seçili bölümler için veriler
        if 'density' in sections:
            # Müşteri yoğunluğu verileri
            density_data = self.analytics.get_customer_density(start_date, end_date)
            density_table = Table([['Saat', 'Müşteri Sayısı']] + 
                                [[k, v] for k, v in density_data.items()])
            density_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(density_table)
        
        # Diğer bölümler için benzer tablolar...
        
        doc.build(elements)
        return dcc.send_bytes(buffer.getvalue(), 'rapor.pdf')
    
    def _generate_excel_report(self, sections, start_date, end_date):
        # Excel rapor oluşturma
        buffer = io.BytesIO()
        # ... Excel oluşturma kodu ...
        return dcc.send_bytes(buffer.getvalue(), 'rapor.xlsx')
    
    def _save_report_schedule(self, schedule, email, sections):
        # Rapor planlaması veritabanına kaydedilir
        pass
    
    def _send_scheduled_report(self, email, sections):
        # Planlı rapor gönderimi
        pass
    
    def run(self, debug=False, port=8050):
        """Dashboard'u çalıştır."""
        self.app.run_server(debug=debug, port=port) 