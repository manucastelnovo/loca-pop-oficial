from datetime import datetime
from io import BytesIO
import os
import secrets
import zipfile
from flask_login import current_user
import qrcode
from flask import render_template, request, send_file
from sqlalchemy import and_
from models.qr import QR
from services.database_service import db


def update_status_qr(qr_data):
    token=qr_data
    qr_updated='False'
    # TODO HACER QUE SEA SOLO PARA EL CURRENT USER
    qr_row= QR.query.filter_by(qr_data=token).first()
    if qr_row:
        if qr_row.is_used==True:
            qr_updated='Used'
            return render_template('update_status.html',qr_updated=qr_updated)
        qr_row.is_used=True
        db.session.commit()
        qr_updated='True'
    return render_template('update_status.html',qr_updated=qr_updated)


def generate_qr():
    data = f'{request.url_root}/update_status_qr/'
    num_qr = int(request.form.get('num_qr', 1))  # Número de QRs, por defecto 1
    party_name=request.form['party_name']
    is_first=True
    timestamp = datetime.now()
    timestamp = timestamp.strftime("%Y-%m-%d_%H-%M-%S")
    zip_filename = f"entradas-qr-{timestamp}.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for i in range(1, num_qr + 1):
            if i!=1:
                is_first=False
            # Generar un token único para cada QR
            token = secrets.token_urlsafe(16)
            # Crear el código QR
            qr_data = f"{data}/{token}_{i}"
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)

            new_qr=QR(qr_data=f'{token}_{i}',is_used=False,user_id=current_user.id,party_name=party_name,timestamp=timestamp,is_first=is_first,file_zip_name=zip_filename)
            db.session.add(new_qr)
            db.session.commit()

            # Crear una imagen PIL desde el código QR
            img = qr.make_image(fill_color="black", back_color="white")

            # Guardar la imagen en un archivo temporal
            img_bytes = BytesIO()
            img.save(img_bytes)
            img_bytes.seek(0)

            # Crear un archivo temporal para cada QR
            temp_filename = f"Entrada_numero_{party_name}_{i}.png"
            with open(temp_filename, 'wb') as temp_file:
                temp_file.write(img_bytes.read())

            # Agregar el archivo al zip
            zip_file.write(temp_filename, os.path.basename(temp_filename))

            # Eliminar el archivo temporal
            os.remove(temp_filename)

    # Enviar el archivo zip como una descarga
    return send_file(f'{zip_filename}', as_attachment=True, download_name=zip_filename)



def download_qr():
    list_of_all_qr = QR.query.filter(and_(QR.user_id == current_user.id, QR.is_first == True)).all()
    
    
    return render_template('download_qr.html',list_of_all_qr=list_of_all_qr)


def download_one_qr(zip):
    zip_file = zip
    return send_file(f'{zip_file}', as_attachment=True, download_name=zip_file)

def input_qr():
    return render_template('input_qr.html')

