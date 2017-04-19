from PIL import Image
import base64
# http://stackoverflow.com/questions/11914472/stringio-in-python3
from io import BytesIO
# http://stackoverflow.com/questions/2792650/python3-error-import-error-no-module-name-urllib2
import urllib.request
import re
import numpy as np


def read_image_from_file(file):
    return Image.open(BytesIO(file.read()))


def read_image_from_data(data):
    return Image.open(BytesIO(data))


def read_image_from_url(url):
    img = urllib.request.urlopen(url).read()
    return Image.open(BytesIO(img))


def read_image_from_base64(data):
    data = re.sub(r'^data:.+;base64,', '', data)
    decoded = base64.b64decode(data)
    return Image.open(BytesIO(decoded))


def encode_base64(img):
    buf = BytesIO()
    img.save(buf, format="JPEG")
    encoded = base64.encodestring(buf.getvalue())
    # return 'data:image/jpeg;base64,' + encoded  # Python2
    return 'data:image/jpeg;base64,' + encoded.decode('utf8')


def to_np_data_array(img):
    if img.mode != "RGB":
        img = img.convert("RGB")
    return (np.asarray(img).astype(np.float32) / 255).transpose(2, 0, 1)


def to_pil_image(np_img):
    # np_img dimension: (height, width, channel)
    return Image.fromarray((np_img * 255).astype(np.uint8))


def fft_spectrum(img):
    img_gray = img.convert('L')
    fimage = np.fft.fft2(img_gray)
    fimage = np.fft.fftshift(fimage)
    fimage = np.log(np.abs(fimage) + 1)
    fimage = fimage / np.amax(fimage) * 255
    return fimage


def fft_and_resize(img, width, height):
    img_fft = fft_spectrum(img)
    pilImg = Image.fromarray(np.uint8(img_fft))
    pilImg = pilImg.resize((width, height), resample=Image.LANCZOS)
    img_resize = np.asarray(pilImg).astype(np.float32) / 255.0
    img_resize = img_resize.reshape(-1, height, width).transpose(1, 2, 0)
    return img_resize
