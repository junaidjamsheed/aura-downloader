from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/get-link', methods=['GET'])
def get_link():
    url = request.args.get('url')
    # --no-playlist দিলে সার্ভার খুব ফাস্ট হবে
    # --get-url শুধু ডাউনলোডের ডাইরেক্ট লিংকটা দেবে
    command = f"yt-dlp --no-playlist -g {url}"
    try:
        result = subprocess.check_output(command, shell=True).decode().strip()
        # রেজাল্ট থেকে শুধু প্রথম লিংকটি নিচ্ছি
        return jsonify({"url": result.split('\n')[0]})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
