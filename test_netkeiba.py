import unittest
import netkeiba


class TestNetkeiba(unittest.TestCase):

    def test_getHorseUrl(self):
        _netkeiba = netkeiba.Netkeiba()
        name = 'オルフェーヴル'
        html = _netkeiba.searchHorseByName(name)
        url = _netkeiba.getHorseUrl(html)
        self.assertEqual(url, "http://db.netkeiba.com/horse/2008102636/")

    def test_getHorseDistanceAptitude(self):
        _netkeiba = netkeiba.Netkeiba()
        name = 'オルフェーヴル'
        html = _netkeiba.searchHorseByName(name)
        factor = _netkeiba.getHorseDistanceAptitude(html)
        self.assertEqual(factor, 0.6293103448275862)

if __name__ == "__main__":
    unittest.main()
