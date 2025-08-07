from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine, Table, Column, MetaData, NVARCHAR, DateTime, Float
from datetime import datetime
import os

app = Flask(__name__)
metadata = MetaData()

# Tên bảng theo CSDL của bạn
attendance_table = Table('HR_GPS_Attendance', metadata,
    Column('EmployeeId', NVARCHAR(50)),
    Column('EmployeeName', NVARCHAR(50)),
    Column('CheckInTime', DateTime, default=datetime.now),
    Column('Latitude', Float),
    Column('Longitude', Float)
)

# Thông tin kết nối lấy từ biến môi trường (khuyên dùng trên Render)
DB_SERVER = os.getenv("DESKTOP-LF6CHGA\SQLEXPRESS")     # ex: 192.168.1.5 hoặc tên server
DB_NAME   = os.getenv("Sun_Database")       # ex: Sun_Database
DB_USER   = os.getenv("render_user")                # ex: sa
DB_PASS   = os.getenv("StrongPassword123!")            # ex: 123456
# Kết nối với SQL Server bằng pytds
DB_URL = f"mssql+pytds://{DB_USER}:{DB_PASS}@{DB_SERVER}/{DB_NAME}"
engine = create_engine(DB_URL)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/checkin", methods=["POST"])
def checkin():
    data = request.get_json()
    try:
        with engine.begin() as conn:
            conn.execute(attendance_table.insert().values(
                EmployeeId=data['EmployeeId'],
                EmployeeName=data['EmployeeName'],
                CheckInTime=datetime.now(),
                Latitude=data['Latitude'],
                Longitude=data['Longitude']
            ))
        return jsonify({"status": "success", "message": "Chấm công thành công"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run()
