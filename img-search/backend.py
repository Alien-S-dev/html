import os
import uuid
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
from PicImageSearch import Network, SauceNAO

backend = Flask(__name__)
CORS(backend)

# 从云端的环境变量里读取 Key，如果本地测试没有配置，就用后面的空字符串代替
SAUCENAO_API_KEY = os.environ.get("SAUCENAO_API_KEY", "")

@backend.route('/api/upload', methods=['POST'])
def upload_image():
    file = request.files.get('image')
    if not file:
        return jsonify({"success": False, "error": "没有收到图片！"}), 400

    file_ext = os.path.splitext(file.filename)[1] if '.' in file.filename else '.png'
    temp_filename = f"temp_{uuid.uuid4().hex}{file_ext}"
    temp_filepath = os.path.join(os.getcwd(), temp_filename)
    
    file.save(temp_filepath)
    print(f"🔥 收到图片，正在呼叫 SauceNAO...")

    try:
        results = asyncio.run(search_saucenao(temp_filepath))
        return jsonify({"success": True, "message": "SauceNAO 搜索完成", "results": results})
    except Exception as e:
        print(f"❌ 搜索出错: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)

async def search_saucenao(file_path):
    async with Network() as client:
        # 使用你填写的 Key 初始化
        saucenao = SauceNAO(client=client, api_key=SAUCENAO_API_KEY)
        resp = await saucenao.search(file=file_path)
        
        # 打印看看拿到几个结果
        print("SauceNAO 搜到了", len(resp.raw), "个结果")
        
        parsed_results = []
        for item in resp.raw:
            parsed_results.append({
                "title": item.title or "未知标题",
                "similarity": f"{item.similarity}%",
                "author": item.author or "未知作者",
                "url": item.url or "无链接",
                "source": item.source or "未知来源"
            })
        return parsed_results
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    backend.run(host="0.0.0.0", port=port)