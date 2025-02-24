
campo_ano = 'year'
campo_titulo = 'title'
campo_studio = 'studios'
campo_produtor = 'producers'
campo_bool_vencedor = 'winner'

cabecalho_arquivo_de_importacao = [campo_ano, campo_titulo, campo_studio, campo_produtor, campo_bool_vencedor]

path_arquivo_importacao = 'movielist.csv'

regex_de_verificacao_vencerdor = r'^\s*yes\s*$'

regex_encontra_studios = r',?\s+and\s+|,\s*'
regex_encontra_produtores = regex_encontra_studios

key_dict_producer = 'producer'
key_dict_interval = 'interval'
key_dict_previous_win = 'previousWin'
key_dict_following_win = 'followingWin'
key_dict_max = 'max'
key_dict_min = 'min'

dicionario_base_produtor = {key_dict_producer: '', key_dict_interval: 0, key_dict_previous_win : 0,
                            key_dict_following_win: 0}

dicionario_base_max_min = {key_dict_max: list(), key_dict_min: list()}
