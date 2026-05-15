from flask import Flask, request, jsonify
import instaloader
import os
import re

app = Flask(__name__)

L = instaloader.Instaloader(
    download_pictures=False,
    download_videos=False,
    download_video_thumbnails=False,
    save_metadata=False,
    compress_json=False
)

# favicon fix
@app.route('/favicon.ico')
def favicon():
    return '', 204

# home route
@app.route("/")
def home():
    return jsonify({
        "status": True,
        "owner": "Xeon Vro",
        "message": "Instagram API Running"
    })

# insta downloader
@app.route("/insta")
def insta():

    url = request.args.get("url")

    if not url:
        return jsonify({
            "status": False,
            "owner": "Xeon Vro",
            "message": "No URL provided"
        }), 400

    try:

        # clean URL
        url = url.split("?")[0]

        # get shortcode safely
        match = re.search(r"(?:reel|p|tv)/([^/?]+)", url)

        if not match:
            return jsonify({
                "status": False,
                "owner": "Xeon Vro",
                "message": "Invalid Instagram URL"
            }), 400

        shortcode = match.group(1)

        # fetch post
        post = instaloader.Post.from_shortcode(
            L.context,
            shortcode
        )

        # video
        if post.is_video:
            media = post.video_url
            media_type = "video"

        # image
        else:
            media = post.url
            media_type = "image"

        return jsonify({
            "status": True,
            "owner": "Xeon Vro",
            "type": media_type,
            "media": media
        })

    except Exception as e:
        return jsonify({
            "status": False,
            "owner": "Xeon Vro",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
