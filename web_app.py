"""
OpenCV Müşteri Analiz Sistemi - Modern Flask Web App
Gelişmiş web dashboard ile uzaktan erişim ve mobile support
"""

from flask import Flask, render_template, request, jsonify, Response, send_file
from flask_socketio import SocketIO, emit
import cv2
import base64
import threading
import json
import time
from datetime import datetime, timedelta
import logging
from pathlib import Path
import pandas as pd
import io
import sqlite3
import os

# Existing system imports
from src.core.camera import CameraManager
from src.core.detector import HumanDetector
from src.core.visitor_tracker import visitor_tracker
from src.models.database import db_manager
from src.utils.logger import get_logger
from src.config.settings import SETTINGS

class ModernWebApp:
    """Modern Flask Web Application for Customer Analytics"""
    
    def __init__(self):
        # Flask app setup
        self.app = Flask(__name__, 
                         template_folder='templates',
                         static_folder='static')
        self.app.config['SECRET_KEY'] = 'customer_analytics_2025_secret'
        
        # WebSocket support
        self.socketio = SocketIO(self.app, cors_allowed_origins="*", async_mode='threading')
        
        # System components
        self.camera_manager = CameraManager()
        self.human_detector = HumanDetector()
        self.is_system_running = False
        
        # Video streaming
        self.current_frame = None
        self.frame_lock = threading.Lock()
        
        # Analytics data
        self.hourly_stats = {}
        self.daily_trends = []
        
        # Logging
        self.logger = get_logger("webapp")
        
        # Setup routes and websockets
        self._setup_routes()
        self._setup_websockets()
        
        self.logger.info("🌐 Modern Web App başlatıldı")
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def dashboard():
            """Ana dashboard sayfası"""
            return render_template('modern_dashboard.html')
        
        @self.app.route('/mobile')
        def mobile_dashboard():
            """Mobile optimized dashboard"""
            return render_template('mobile_dashboard.html')
        
        @self.app.route('/analytics')
        def analytics_page():
            """Detaylı analiz sayfası"""
            return render_template('analytics.html')
        
        # API Routes
        @self.app.route('/api/system/start', methods=['POST'])
        def start_system():
            """Sistemi başlat"""
            try:
                if self.is_system_running:
                    return jsonify({'success': False, 'message': 'Sistem zaten çalışıyor'})
                
                # Kamera başlat
                if not self.camera_manager.initialize_camera():
                    return jsonify({'success': False, 'message': 'Kamera başlatılamadı'})
                
                # Detector başlat
                if not self.human_detector.initialize():
                    return jsonify({'success': False, 'message': 'AI model yüklenemedi'})
                
                # Kamera yakalamayı başlat
                self.camera_manager.start_capture()
                self.camera_manager.add_frame_callback(self._process_frame)
                
                self.is_system_running = True
                
                # WebSocket ile durumu bildir
                self.socketio.emit('system_status', {
                    'running': True, 
                    'message': 'Sistem başlatıldı'
                })
                
                return jsonify({'success': True, 'message': 'Sistem başarıyla başlatıldı'})
                
            except Exception as e:
                self.logger.error(f"Sistem başlatma hatası: {e}")
                return jsonify({'success': False, 'message': str(e)})
        
        @self.app.route('/api/system/stop', methods=['POST'])
        def stop_system():
            """Sistemi durdur"""
            try:
                if not self.is_system_running:
                    return jsonify({'success': False, 'message': 'Sistem zaten durdurulmuş'})
                
                self.camera_manager.stop_capture()
                self.human_detector.cleanup()
                self.is_system_running = False
                
                # WebSocket ile durumu bildir
                self.socketio.emit('system_status', {
                    'running': False, 
                    'message': 'Sistem durduruldu'
                })
                
                return jsonify({'success': True, 'message': 'Sistem durduruldu'})
                
            except Exception as e:
                self.logger.error(f"Sistem durdurma hatası: {e}")
                return jsonify({'success': False, 'message': str(e)})
        
        @self.app.route('/api/stats/current')
        def get_current_stats():
            """Mevcut istatistikleri getir"""
            try:
                stats = visitor_tracker.get_current_stats()
                
                # Ek istatistikler ekle
                today_visitors = db_manager.get_today_stats()
                
                response_data = {
                    'total_today': today_visitors.get('total_visitors', 0),
                    'avg_confidence': today_visitors.get('avg_confidence', 0.0),
                    'last_visit': today_visitors.get('last_visit'),
                    'system_running': self.is_system_running,
                    'current_detections': getattr(self, 'current_detections', 0),
                    'hourly_data': self._get_hourly_distribution(),
                    'weekly_trend': self._get_weekly_trend()
                }
                
                return jsonify({'success': True, 'data': response_data})
                
            except Exception as e:
                self.logger.error(f"Stats getirme hatası: {e}")
                return jsonify({'success': False, 'message': str(e)})
        
        @self.app.route('/api/stats/hourly')
        def get_hourly_stats():
            """Saatlik istatistikleri getir"""
            try:
                hourly_data = self._get_hourly_distribution()
                return jsonify({'success': True, 'data': hourly_data})
            except Exception as e:
                return jsonify({'success': False, 'message': str(e)})
        
        @self.app.route('/api/stats/weekly')
        def get_weekly_stats():
            """Haftalık istatistikleri getir"""
            try:
                weekly_data = self._get_weekly_trend()
                return jsonify({'success': True, 'data': weekly_data})
            except Exception as e:
                return jsonify({'success': False, 'message': str(e)})
        
        @self.app.route('/api/visitors/recent')
        def get_recent_visitors():
            """Son ziyaretçileri getir"""
            try:
                # Son 20 ziyaretçiyi getir
                conn = sqlite3.connect('data/musteri_analiz.db')
                query = """
                    SELECT entry_time, confidence_avg, detection_count 
                    FROM visitors 
                    WHERE confidence_avg > 0.0 
                    ORDER BY entry_time DESC 
                    LIMIT 20
                """
                df = pd.read_sql_query(query, conn)
                conn.close()
                
                visitors = []
                for _, row in df.iterrows():
                    visitors.append({
                        'time': row['entry_time'],
                        'confidence': round(row['confidence_avg'] * 100, 1),
                        'detection_count': row['detection_count']
                    })
                
                return jsonify({'success': True, 'data': visitors})
                
            except Exception as e:
                return jsonify({'success': False, 'message': str(e)})
        
        @self.app.route('/api/visitors/export')
        def export_visitors():
            """Ziyaretçi verilerini export et"""
            try:
                # Enhanced export kullan
                import subprocess
                result = subprocess.run(['python', 'enhanced_data_export.py'], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    # En son oluşturulan dosyayı bul
                    import glob
                    files = glob.glob('data/csv_backups/enhanced_visitor_data_*.csv')
                    if files:
                        latest_file = max(files, key=os.path.getctime)
                        return send_file(latest_file, as_attachment=True)
                
                return jsonify({'success': False, 'message': 'Export başarısız'})
                
            except Exception as e:
                return jsonify({'success': False, 'message': str(e)})
        
        @self.app.route('/video_feed')
        def video_feed():
            """Video stream endpoint"""
            return Response(self._generate_frames(),
                          mimetype='multipart/x-mixed-replace; boundary=frame')
        
        @self.app.route('/api/camera/snapshot')
        def camera_snapshot():
            """Anlık kamera görüntüsü"""
            try:
                if self.current_frame is not None:
                    with self.frame_lock:
                        frame = self.current_frame.copy()
                    
                    # JPEG encode
                    _, buffer = cv2.imencode('.jpg', frame)
                    
                    return Response(buffer.tobytes(), mimetype='image/jpeg')
                else:
                    return jsonify({'success': False, 'message': 'Kamera aktif değil'})
                    
            except Exception as e:
                return jsonify({'success': False, 'message': str(e)})
    
    def _setup_websockets(self):
        """Setup WebSocket events"""
        
        @self.socketio.on('connect')
        def handle_connect():
            """Client bağlandığında"""
            self.logger.info(f"Web client bağlandı: {request.sid}")
            emit('connection_status', {'status': 'connected'})
            
            # Mevcut durumu gönder
            stats = visitor_tracker.get_current_stats()
            emit('stats_update', stats)
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Client bağlantısı kesildiğinde"""
            self.logger.info(f"Web client bağlantısı kesildi: {request.sid}")
        
        @self.socketio.on('request_stats')
        def handle_stats_request():
            """İstatistik güncellemesi istendi"""
            try:
                stats = visitor_tracker.get_current_stats()
                stats['current_detections'] = getattr(self, 'current_detections', 0)
                stats['system_running'] = self.is_system_running
                emit('stats_update', stats)
            except Exception as e:
                self.logger.error(f"Stats gönderme hatası: {e}")
        
        @self.socketio.on('request_hourly_data')
        def handle_hourly_request():
            """Saatlik veri istendi"""
            try:
                hourly_data = self._get_hourly_distribution()
                emit('hourly_update', hourly_data)
            except Exception as e:
                self.logger.error(f"Hourly data gönderme hatası: {e}")
    
    def _process_frame(self, frame):
        """Frame işleme callback'i"""
        if frame is None:
            return
        
        try:
            # İnsan tespiti yap
            detections, processed_frame = self.human_detector.detect_humans(frame, draw_boxes=True)
            
            # Anlık tespit sayısını güncelle
            self.current_detections = len(detections) if detections else 0
            
            # Processed frame'i sakla
            with self.frame_lock:
                self.current_frame = processed_frame.copy()
            
            # Ziyaretçi takibi
            if detections and len(detections) > 0:
                tracking_result = visitor_tracker.process_detections(detections, datetime.now())
                
                # Yeni ziyaretçi varsa WebSocket ile bildir
                if tracking_result['new_visitors'] > 0:
                    self.socketio.emit('new_visitor', {
                        'count': tracking_result['new_visitors'],
                        'total_today': tracking_result['current_stats']['total_today']
                    })
                
                # Stats güncelle
                stats = tracking_result['current_stats']
                stats['current_detections'] = self.current_detections
                stats['system_running'] = self.is_system_running
                
                self.socketio.emit('stats_update', stats)
            
        except Exception as e:
            self.logger.error(f"Frame işleme hatası: {e}")
    
    def _generate_frames(self):
        """Video stream generator"""
        while True:
            try:
                if self.current_frame is not None:
                    with self.frame_lock:
                        frame = self.current_frame.copy()
                    
                    # JPEG encode
                    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                    
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
                else:
                    # Placeholder image
                    time.sleep(0.1)
                    
            except Exception as e:
                self.logger.error(f"Frame generation hatası: {e}")
                time.sleep(0.1)
    
    def _get_hourly_distribution(self):
        """Saatlik dağılım verilerini getir"""
        try:
            conn = sqlite3.connect('data/musteri_analiz.db')
            today = datetime.now().date()
            
            query = """
                SELECT strftime('%H', entry_time) as hour, COUNT(*) as count
                FROM visitors 
                WHERE DATE(entry_time) = ? AND confidence_avg > 0.0
                GROUP BY hour
                ORDER BY hour
            """
            
            df = pd.read_sql_query(query, conn, params=[str(today)])
            conn.close()
            
            # 24 saatlik veri hazırla
            hourly_data = {str(i).zfill(2): 0 for i in range(24)}
            
            for _, row in df.iterrows():
                hourly_data[row['hour']] = row['count']
            
            return hourly_data
            
        except Exception as e:
            self.logger.error(f"Hourly distribution hatası: {e}")
            return {}
    
    def _get_weekly_trend(self):
        """Haftalık trend verilerini getir"""
        try:
            conn = sqlite3.connect('data/musteri_analiz.db')
            
            # Son 7 günün verilerini al
            query = """
                SELECT DATE(entry_time) as date, COUNT(*) as count
                FROM visitors 
                WHERE entry_time >= date('now', '-7 days') AND confidence_avg > 0.0
                GROUP BY DATE(entry_time)
                ORDER BY date
            """
            
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            # 7 günlük veri hazırla
            weekly_data = []
            for i in range(7):
                date = (datetime.now() - timedelta(days=6-i)).date()
                date_str = str(date)
                
                count = 0
                matching_row = df[df['date'] == date_str]
                if not matching_row.empty:
                    count = matching_row.iloc[0]['count']
                
                weekly_data.append({
                    'date': date_str,
                    'day': date.strftime('%A'),
                    'count': count
                })
            
            return weekly_data
            
        except Exception as e:
            self.logger.error(f"Weekly trend hatası: {e}")
            return []
    
    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Web uygulamasını başlat"""
        self.logger.info(f"🚀 Modern Web App başlatılıyor: http://{host}:{port}")
        self.socketio.run(self.app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=True)

def main():
    """Ana fonksiyon"""
    app = ModernWebApp()
    app.run()

if __name__ == '__main__':
    main() 