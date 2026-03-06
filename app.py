from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

# ইউটিউব ডাউনলোড ইঞ্জিন আপডেট করা
def update_ytdlp():
    try:
        subprocess.run(["yt-dlp", "-U"], check=True)
    except Exception as e:
        print(f"Update failed: {e}")

@app.route('/get-link', methods=['GET'])
def get_link():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    # প্রতি রিকোয়েস্টে আপডেট চেক
    update_ytdlp()
    
    # --no-playlist: ভিডিও ফাস্ট করবে
    # -g: ডাইরেক্ট ডাউনলোড লিংক দেবে
    # --user-agent: ইউটিউবকে ধোঁকা দেওয়ার জন্য ব্রাউজারের ছদ্মবেশ
    command = f"yt-dlp --no-playlist --no-check-certificate --user-agent 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' -g {url}"
    
    try:
        result = subprocess.check_output(command, shell=True).decode().strip()
        # সব ফরম্যাট না পাঠিয়ে শুধু বেস্ট কোয়ালিটি লিংক দিচ্ছি
        return jsonify({"url": result.split('\n')[0]})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
