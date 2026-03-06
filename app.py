from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/get-link', methods=['GET'])
def get_link():
    url = request.args.get('url')
    # প্রথমবার আপডেট নিশ্চিত করা
    subprocess.run(["yt-dlp", "-U"], capture_output=True)
    
    # -g এবং --no-check-certificate দিয়ে ট্রাই করছি
    command = f"yt-dlp --no-check-certificate -g {url}"
    try:
        result = subprocess.check_output(command, shell=True).decode().strip()
        return jsonify({"url": result.split('\n')[0]})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
