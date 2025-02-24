import unittest
from app import app
from defines import *


class ProducersAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_producers(self):
        # fazendo get no end point
        response = self.app.get('/producers')
        self.assertEqual(response.status_code, 200, "Resposta deveria ser 200 OK")

        # verificando se a resposta é Json
        data = response.get_json()
        self.assertIsInstance(data, dict, f"Resposta deveria ser um objeto JSON")

        # verificando se a resposta contem as chaves key_dict_min e key_dict_max
        self.assertIn(key_dict_min, data, f"resposta deveria conter a chave '{key_dict_min}'")
        self.assertIn(key_dict_max, data, f"resposta deveria conter a chave '{key_dict_max}'")

        # Ensure both keys have a list as their value
        self.assertIsInstance(data[key_dict_min], list, f"'{key_dict_min}' deveria ser uma lista")
        self.assertIsInstance(data[key_dict_max], list, f"'{key_dict_max}' deveria ser uma lista")

        # Opcional, verificando se 'min' tems os campos esperados
        if data[key_dict_min]:
            first_item = data[key_dict_max][0]
            self.assertIn(key_dict_producer, first_item,
                          f"Conteúdo de '{key_dict_min}' deveria conter chave '{key_dict_producer}'")
            self.assertIn(key_dict_interval, first_item,
                          f"Conteúdo de '{key_dict_min}' deveria conter chave '{key_dict_interval}'")
            self.assertIn(key_dict_previous_win, first_item,
                          f"Conteúdo de '{key_dict_min}' deveria conter chave '{key_dict_previous_win}'")
            self.assertIn(key_dict_following_win, first_item,
                          f"Conteúdo de '{key_dict_min}' deveria conter chave '{key_dict_following_win}' ")

        # Opcional, verificando se 'min' tems os campos esperados
        if data[key_dict_max]:
            first_item = data[key_dict_max][0]
            self.assertIn(key_dict_producer, first_item,
                          f"Conteúdo de '{key_dict_max}' deveria conter chave '{key_dict_producer}'")
            self.assertIn(key_dict_interval, first_item,
                          f"Conteúdo de '{key_dict_max}' deveria conter chave '{key_dict_interval}'")
            self.assertIn(key_dict_previous_win, first_item,
                          f"Conteúdo de '{key_dict_max}' deveria conter chave '{key_dict_previous_win}'")
            self.assertIn(key_dict_following_win, first_item,
                          f"Conteúdo de '{key_dict_max}' deveria conter chave '{key_dict_following_win}' ")


if __name__ == '__main__':
    unittest.main()
