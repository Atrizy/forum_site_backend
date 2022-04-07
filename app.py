from email.policy import default
import json
from flask import Flask, request, Response
import dbinteractions as db

app = Flask(__name__)

@app.get("/api/post")
def get_forum_posts():
    try:
        forum_id = request.args["forum_id"]
        success, posts = frp.get_forum_post(forum_id)
        if(success):
            posts_json = json.dumps(posts, default=str)
            return Response(posts_json, mimetype="plain/text", status=200)
        else:
            return Response("Please try again", mimetype="plain/text", status=400)
    except:
        return Response("Sorry Please try again", mimetype="plain/text", status=500)