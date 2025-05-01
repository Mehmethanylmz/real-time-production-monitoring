
from flask import Flask, render_template, request, Response, url_for, flash
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
import cv2
from ultralytics import YOLO
import mysql.connector
import time
from mysql.connector import Error

app = Flask(__name__)  


model_talep = joblib.load('saved_models/retail_store_inventory_model.pkl')
scaler = joblib.load('saved_models/retail_store_inventory_scaler.pkl')


data = pd.read_csv('datasets/retail_store_inventory.csv')
le_category = LabelEncoder().fit(data['Category'])
le_region = LabelEncoder().fit(data['Region'])
le_weather = LabelEncoder().fit(data['Weather Condition'])
le_seasonality = LabelEncoder().fit(data['Seasonality'])


model_yolo = YOLO('saved_models/best.pt')
camera = cv2.VideoCapture(0)


db = mysql.connector.connect(
    host="localhost",       
    user="root",             
    password="password",  
    database="urun_tespit"     
)
cursor = db.cursor()


def calculate_defect_ratio(result, frame_shape):
    total_area = frame_shape[0] * frame_shape[1]
    defect_area = 0
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        defect_area += (x2 - x1) * (y2 - y1)
    if total_area == 0:
        return 0
    return (defect_area / total_area) * 100
def generate_frames():
    baslangic_zamani = time.time()  
    son_kayit_zamani = baslangic_zamani

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            results = model_yolo.predict(source=frame, conf=0.5, save=False, verbose=False)

            annotated_frame = frame.copy()
            deformasyon_orani = 0

            for result in results:
                deformasyon_orani = calculate_defect_ratio(result, frame.shape)

                boxes = result.boxes.xyxy.cpu().numpy()
                confs = result.boxes.conf.cpu().numpy()
                classes = result.boxes.cls.cpu().numpy()

                for box, conf, cls in zip(boxes, confs, classes):
                    x1, y1, x2, y2 = map(int, box)
                    label = f"leke {conf:.2f}"
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.putText(annotated_frame, label, (x1, max(y1 - 10, 0)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            
            cv2.putText(annotated_frame, f"Deformasyon: %{deformasyon_orani:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            
            simdiki_zaman = time.time()
            if simdiki_zaman - son_kayit_zamani >= 10:  
                try:
                    sql = "INSERT INTO deformasyon_kayitlari (deformasyon_orani) VALUES (%s)"
                    val = (float(deformasyon_orani),)  
                    cursor.execute(sql, val)
                    db.commit()
                    print(f"✅ {time.strftime('%H:%M:%S')} - % {deformasyon_orani:.2f} kaydedildi.")
                    son_kayit_zamani = simdiki_zaman  
                except mysql.connector.Error as err:
                    print(f"❌ MySQL Hatası: {err}")

            
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def home():
    
    hatali_oran = 0
    toplam_veri = 0

    try:
        cursor = db.cursor(dictionary=True)
        sql1 = "SELECT AVG(deformasyon_orani) AS ortalama FROM deformasyon_kayitlari;"
        cursor.execute(sql1)
        result = cursor.fetchone()

        if result and result['ortalama'] is not None:
            hatali_oran = round(result['ortalama'], 2)

        
        cursor.execute("SELECT COUNT(*) AS toplam FROM deformasyon_kayitlari;")
        result2 = cursor.fetchone()
        if result2:
            toplam_veri = result2['toplam']

    except Error as e:
        flash(f"Veri tabanı hatası: {e}", "danger")
    finally:
        cursor.close()

    return render_template('index.html', hatali_oran=hatali_oran, toplam_veri=toplam_veri)


@app.route('/tahmin', methods=['POST'])
def tahmin():
    if request.method == 'POST':
        store = request.form['firma']
        product = request.form['urun']
        category = 0
        region = request.form['bolge']
        inventory_level = int(request.form['stok_seviyesi'])
        units_sold = int(request.form['satilan_birimler'])
        units_ordered = int(request.form['siparis_edilen_birimler'])
        price = float(request.form['satis_fiyati'])
        discount = float(request.form['indirim'])
        weather = request.form['hava_durumu']
        holiday_promotion = 0
        competitor_pricing = float(request.form['rakip_fiyat'])
        seasonality = request.form['sezon']

        input_data = np.array([
            store,
            product,
            category,
            region,
            inventory_level,
            units_sold,
            units_ordered,
            price,
            discount,
            weather,
            holiday_promotion,
            competitor_pricing,
            seasonality,
        ]).reshape(1, -1)

        input_scaled = scaler.transform(input_data)

        forecast = model_talep.predict(input_scaled)[0]

        forecast = round(forecast)

        return render_template('stok-ekle.html', forecast=forecast)

@app.route('/tedarik')
def tedarik():
    return render_template('tedarik.html')

@app.route('/uretim')
def uretim():
    return render_template('uretim.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stok-yonetimi')
def stok_yonetimi():
    return render_template('stok-yonetimi.html')

@app.route('/lojistik')
def lojistik():
    return render_template('lojistik.html')

@app.route('/insan-kaynaklari')
def insan_kaynaklari():
    return render_template('insan-kaynaklari.html')

@app.route('/musteri-destek')
def musteri_destek():
    return render_template('musteri-destek.html')

@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)