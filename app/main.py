from flask import Flask, request, send_file, render_template, jsonify
import os
import yt_dlp
import time

app = Flask(__name__, template_folder='templates')

DOWNLOAD_DIR = '/tmp/downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')

    if not url or 'youtube.com' not in url:
        return jsonify({'success': False, 'error': '无效的 YouTube 链接'}), 400

    filename = f"video_{int(time.time())}.mp4"
    output_path = os.path.join(DOWNLOAD_DIR, filename)

    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({'success': True, 'file': f"/download/{filename}"})
    except Exception as e:
        return jsonify({'success': False, 'error': f'下载失败: {str(e)}'}), 500

@app.route('/download/<filename>')
def serve_file(filename):
    file_path = os.path.join(DOWNLOAD_DIR, filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
