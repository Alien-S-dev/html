from flask import Flask, request, jsonify
from flask_cors import CORS
backend = Flask(__name__)
CORS(backend)
@backend.route('/api/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400
    print(f"收到图片: {file.filename}")
    return jsonify({
        'success': True,
        'message': '图片上传成功',
        'results': [
            {'title': '百度识图', 'url': 'https://image.baidu.com'},
            {'title': '谷歌识图', 'url': 'https://www.google.com'},
        ]
    })
if __name__ == '__main__':
    backend.run(port=3000, debug=True)
