
campo_ano = 'year'
campo_titulo = 'title'
campo_studio = 'studios'
campo_produtor = 'producers'
campo_bool_vencedor = 'winner'

cabecalho_arquivo_de_importacao = [campo_ano, campo_titulo, campo_studio, campo_produtor, campo_bool_vencedor]

path_arquivo_importacao = 'movielist.csv'

regex_de_verificacao_vencerdor = '^yes$'

regex_encontra_studios = r',\s*|\s+and\s+'
regex_encontra_produtores = regex_encontra_studios