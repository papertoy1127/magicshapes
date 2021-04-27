import json
import os
import PIL.Image
import requests

from flask import Flask, send_file

app = Flask(__name__)

content = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Magicshapes</title>
    <script src="script.js"></script>
    <style>
        body {{font-family: "나눔스퀘어";}}
        .title {{text-align: center;}}
        .shape {{width: 60%; height: 128px; border: 1px solid black; margin: 0 auto;}}
        .crop {{width: 128px; height: 128px; overflow: hidden; margin: 0; border-right: 1px solid black; float: left;}}
        .author {{line-height: 0.5em; font-size: 2em; padding-left: 140px ; margin: 28px 10px; text-align:left; font-weight: 600}}
        .desc {{line-height: 0.5em; font-size: 1.5em; padding-left: 140px ; margin: 12px 10px;}}
        .id {{line-height: 3em; font-size: 0.8em; padding-left: 140px ; margin: 12px 10px; color: #999999}}
        .download {{float: right}}
        .link {{text-align:center; display: block; padding-top: 50px; padding-right: 10px}}
    </style>
</head>
<body>
    <h1 class="title">마법진 공유소</h1>
    {body}
</body>
</html>"""

shapeTemplate = """
    <div class="shape">
        <div class="crop">
            <img class="img" src="{img}" style="line-height: 0.5em; font-size: 1.5em; float: left; margin: 0; margin-left: -{offset}px; height: 100%;  height: 128px; width: auto;">
        </div>
        <div class="download"><a class="link" href="./magicshapes/{id}">download</a></div>
        <p class="author">by {author}</p>
        <p class="desc">Tags: {Tiles}{tags}</p>
        <p class="id">ID: {id}</p>
    </div><br>"""


@app.route('/')
@app.route('/magicshape')
def home():
    global content, shapeTemplate
    shapes = ""
    filenames = os.listdir("magicshapes")
    for i in filenames:
        data = json.loads(open("magicshapes/" + i + "/" + i + ".json").read())
        img = data["img"]
        image = PIL.Image.open(requests.get(img, stream=True).raw)
        width, height = image.size
        offset = ((width - height) / height) * 64
        author = data["author"]
        tiles = data["tiles"]
        taglist = data["tags"]
        tags = ""
        for t in taglist:
            tags += ", " + t;
        shapes += shapeTemplate.format(offset=offset, img=img, author=author, Tiles=tiles, tags=tags, id=i)
    body = content.format(body=shapes)
    return body


@app.route('/magicshapes/<filename>')
def download(filename):
    path = app.root_path + "\\magicshapes\\" + filename + '\\' + filename + ".adofai"
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=80)
