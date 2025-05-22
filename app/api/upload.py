import os
from flask import jsonify, request, current_app
from . import bp
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
import uuid

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': '没有文件'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': '没有选择文件'}), 400
        
    if file and allowed_file(file.filename):
        # 生成安全的文件名
        filename = secure_filename(file.filename)
        # 使用UUID作为文件名前缀
        unique_filename = f"{str(uuid.uuid4())}_{filename}"
        
        # 确保上传目录存在
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            
        # 保存文件
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        
        # 返回文件URL
        file_url = f"/uploads/{unique_filename}"
        return jsonify({
            'url': file_url,
            'filename': unique_filename
        })
        
    return jsonify({'message': '不支持的文件类型'}), 400