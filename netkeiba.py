# encoding: utf-8
from bs4 import BeautifulSoup
import urllib
import chardet
import traceback


class Netkeiba:

    URL = "http://db.netkeiba.com/"

    def fetchPage(self, url):
        res = urllib.request.urlopen(url)
        body = res.read()
        guess_enc = chardet.detect(body)
        try:
            unicode_html = body.decode(guess_enc['encoding'])
        except UnicodeDecodeError:
            print(url, guess_enc)
            print(traceback.format_exc())
            unicode_html = None

        if not unicode_html:
            try:
                unicode_html = body.decode('shift_jisx0213')
                print('Decoding in shift_jisx0213 is successful.')
            except UnicodeDecodeError:
                print(traceback.format_exc())
                unicode_html = body

        return unicode_html

    def searchHorseByName(self, name):
        params = [('pid', 'horse_list'), ('under_age', 2), ('sort', 'birthyear'), ('list', 20), ('word', name.encode('euc-jp')), ('match', 1)]
        data = urllib.parse.urlencode(params).encode(encoding='ascii')
        res = urllib.request.urlopen(url=self.URL, data=data)
        body = res.read()

        guess_enc = chardet.detect(body)
        try:
            unicode_html = body.decode(guess_enc['encoding'])
        except UnicodeDecodeError:
            print(name)
            print(traceback.format_exc())
            return None

        soup = BeautifulSoup(unicode_html, "html.parser")
        title = soup.select('div.horse_title')
        if title:
            return unicode_html
        else:
            # check if 'not found'
            h2 = soup.select('div.search_result_box div.cate_bar h2')
            if h2 and h2[0].string.find(u'は見つかりませんでした') >= 0:
                return None

            # in case of multiple horse found
            table_tr = soup.select("form table tr")
            url = table_tr[1].select("td a")[0]['href']
            url = self.URL[0:-1] + url
            html = self.fetchPage(url)
            return html

    def getHorseUrl(self, html):
        soup = BeautifulSoup(html, "html.parser")
        url = soup.select("meta[property='og:url']")
        return url[0]['content']

    def getHorseDistanceAptitude(self, html):
        soup = BeautifulSoup(html, "html.parser")

        tekisei_table = soup.select("table.tekisei_table")[0]
        distance = tekisei_table.select("tr")[1]
        imgs = distance.select("img")
        short_val = imgs[1]['width']
        long_val = imgs[3]['width']
        factor = float(long_val) / (int(short_val) + int(long_val))
        return factor
