from flask import Flask, request, render_template
import json
import re
import imageutil
import net
import chainer.functions as F
import chainer.links as L
from chainer import serializers
import numpy as np
import urllib
import netkeiba
from PIL import Image

app = Flask(__name__)

IMAGE_WIDTH = 32
IMAGE_HEIGHT = 32


def load_model():
    model = L.Classifier(net.CNN(), lossfun=F.mean_squared_error)
    model.predictor.train = False
    serializers.load_npz('model.npz', model)
    return model


def do_predict(x):
    model = load_model()
    y = model.predictor(x)
    pred = y.data
    return pred[0]


def predict_score(img):
    img = img.resize((IMAGE_WIDTH, IMAGE_HEIGHT), resample=Image.LANCZOS)
    input_img = np.asarray(img).astype(np.float32).transpose(2, 0, 1) / 255
    mean = np.load('mean.npy')
    input_img -= mean / 255.0
    score = do_predict(input_img.reshape((1,) + input_img.shape))  # 1.0-10.0
    score = (score - 1.0) / 9.0  # rescale to 0.0-1.0
    return score


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        url = request.args.get('url')
        data = request.args.get('data')
        if data:
            img = imageutil.read_image_from_base64(data)
        elif url:
            url = url.strip()  # remove spaces
            if not re.match('^http', url):
                url = "http://" + url
            try:
                img = imageutil.read_image_from_url(url)
            except urllib.error.URLError:
                return '''
                <h3>Error: Invalid url</h3>
                '''
        else:
            return '''
            <h3>Error: Invalid parameter</h3>
            '''

        score = predict_score(img)
        return render_template('result.html', score=score, image=imageutil.encode_base64(img))
    else:
        f = request.files['file']
        img = imageutil.read_image_from_file(f)
        score = predict_score(img)
        return render_template('result.html', score=score, image=imageutil.encode_base64(img))


@app.route('/predict.json', methods=['GET', 'POST'])
def predict_json():
    if request.method == 'GET':
        url = request.args.get('url')
        data = request.args.get('data')
        if data:
            img = imageutil.read_image_from_base64(data)
        elif url:
            url = url.strip()  # remove spaces
            if not re.match('^http', url):
                url = "http://" + url
            try:
                img = imageutil.read_image_from_url(url)
            except urllib.error.URLError as e:
                print(str(e.reason))
                return json.dumps({'error': str(e.reason)})
        else:
            return json.dumps({'error': 'Invalid parameter'})

        score = predict_score(img)
        return json.dumps({'score': float(score[0])})
    else:
        f = request.files['file']
        img = imageutil.read_image_from_file(f)
        score = predict_score(img)
        return json.dumps({'score': float(score[0])})


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/netkeiba/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('netkeiba_search.html')
    elif request.method == 'POST':
        name = request.form['name']

        _netkeiba = netkeiba.Netkeiba()
        html = _netkeiba.searchHorseByName(name)
        if html:
            url = _netkeiba.getHorseUrl(html)
            factor = _netkeiba.getHorseDistanceAptitude(html)
        else:
            url = None
            factor = None

        return render_template('netkeiba_search.html', name=name, url=url, factor=factor)


@app.route('/netkeiba/search.json', methods=['POST'])
def search_json():
    name = request.form['name']

    _netkeiba = netkeiba.Netkeiba()
    html = _netkeiba.searchHorseByName(name)
    if html:
        url = _netkeiba.getHorseUrl(html)
        factor = _netkeiba.getHorseDistanceAptitude(html)
    else:
        url = None
        factor = None
    return json.dumps({'name': name, 'url': url, 'score': factor})

if __name__ == '__main__':
    app.debug = True
    app.run()
