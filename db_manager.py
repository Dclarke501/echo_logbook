import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_file='echo_reports.db'):
        self.db_file = db_file
        self.setup_database()

    def setup_database(self):
        """Create the database and tables if they don't exist"""
        with sqlite3.connect(self.db_file) as conn:
            with open('schema.sql', 'r') as schema_file:
                conn.executescript(schema_file.read())

    def save_report(self, report_data):
        """Save a new report to the database"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            
            # Convert the report data dictionary to SQL insert
            placeholders = ', '.join('?' * len(report_data))
            columns = ', '.join(report_data.keys())
            sql = f"INSERT INTO reports ({columns}) VALUES ({placeholders})"
            
            cursor.execute(sql, list(report_data.values()))
            conn.commit()
            return cursor.lastrowid

    def get_scans_completed(self):
        """Get total number of scans completed"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM reports")
            return cursor.fetchone()[0]

    def get_scans_remaining(self, target=75):
        """Calculate remaining scans needed"""
        completed = self.get_scans_completed()
        return max(0, target - completed)

    def get_pathology_summary(self):
        """Get summary of pathological findings"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            query = """
            SELECT 
                COUNT(CASE WHEN lv_size != 'normal' OR lv_function != 'normal' THEN 1 END) as lv_abnormal,
                COUNT(CASE WHEN rv_size != 'normal' OR rv_function != 'normal' THEN 1 END) as rv_abnormal,
                COUNT(CASE WHEN av_status != 'normal' THEN 1 END) as av_abnormal,
                COUNT(CASE WHEN mv_status != 'normal' THEN 1 END) as mv_abnormal,
                COUNT(CASE WHEN tv_status != 'normal' THEN 1 END) as tv_abnormal,
                COUNT(CASE WHEN aortic_root = 'dilated' THEN 1 END) as aortic_root_dilated,
                COUNT(CASE WHEN pericardial_fluid IN ('significant', 'trivial') THEN 1 END) as pericardial_effusion,
                COUNT(CASE WHEN pleural_effusion = 'Present' THEN 1 END) as pleural_effusion
            FROM reports
            """
            cursor.execute(query)
            return dict(zip([
                'LV abnormality', 'RV abnormality', 'AV abnormality',
                'MV abnormality', 'TV abnormality', 'Dilated aortic root',
                'Pericardial effusion', 'Pleural effusion'
            ], cursor.fetchone()))

    def get_quality_trends(self):
        """Get scan quality trends"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            query = """
            SELECT 
                strftime('%Y-%m', date_created) as month,
                scan_quality,
                COUNT(*) as count
            FROM reports
            GROUP BY month, scan_quality
            ORDER BY month
            """
            cursor.execute(query)
            return cursor.fetchall()
        