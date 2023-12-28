from controllers.qr_controller import update_status_qr
from controllers.qr_controller import generate_qr
from controllers.qr_controller import download_qr
from controllers.qr_controller import download_one_qr
from controllers.qr_controller import input_qr
from flask import Blueprint

blueprint_qr=Blueprint('blueprint_qr',__name__)

blueprint_qr.route('/update_status_qr/<string:qr_data>', methods=['GET', 'POST'])(update_status_qr)
blueprint_qr.route('/generate_qr', methods=['GET','POST'])(generate_qr)
blueprint_qr.route('/download_qr', methods=['GET','POST'])(download_qr)
blueprint_qr.route('/input_qr/<string:zip>', methods=['GET','POST'])(download_one_qr)
blueprint_qr.route('/input_qr', methods=['GET','POST'])(input_qr)



