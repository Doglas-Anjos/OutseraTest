from models import *
from defines import *
import pandas as pd
import re
from typing import List
from copy import deepcopy


def carregar_arquivo_no_banco(caminho_do_arquivo) -> None:
    """
    Função que abre arquivos em um dado caminho
    :param caminho_do_arquivo: sting contendo o caminho arquiovo
    :return:
    """
    try:
        df_filmes = pd.read_csv(caminho_do_arquivo, delimiter=';', usecols=cabecalho_arquivo_de_importacao)
    except Exception as e:
        raise "Houve um problema na leitura do arquivo, verificar se o cabeçalho está no padrão esperado"
    df_filmes[campo_bool_vencedor] = df_filmes[campo_bool_vencedor].fillna('')
    # padroniza a coluna boolana de vencedor do premio
    df_filmes[campo_bool_vencedor] = [transforma_coluna_vencedor_em_booleano(valor)
                                      for valor in df_filmes[campo_bool_vencedor]]
    for index, row in df_filmes.iterrows():
        obj_filme = registrar_filme(row[campo_titulo], row[campo_ano], row[campo_bool_vencedor])

        lista_de_produtores = transforma_texto_em_lista(row[campo_produtor], regex_encontra_produtores)
        lista_de_studios = transforma_texto_em_lista(row[campo_studio], regex_encontra_studios)

        registrar_produtores_no_filme(lista_de_produtores, obj_filme)
        registrar_studios_no_filme(lista_de_studios, obj_filme)


def registrar_produtor(nome_produtor: str) -> Producer:
    """
    Função para inserir no banco de dados o Produtor do filme, traz o produtor caso exista
    :param nome_produtor: nome do produtor
    :return: Objeto de Producer
    """
    obj_producer, created = Producer.get_or_create(name=nome_produtor)

    return obj_producer


def registrar_studio(nome_estudio: str) -> Studio:
    """
    Função para inserir no banco de dados o Studio que produz filmes, traz o estudio caso exista
    :param nome_estudio: nome do estudio
    :return: Objeto de Studio
    """
    obj_studio, created = Studio.get_or_create(name=nome_estudio)

    return obj_studio


def registrar_filme(nome_filme: str, ano: int, booleano_ganhou: bool) -> Movie:
    """
    Função para inserir registro de filme -> Movie, traz o filme caso exista
    :param nome_filme: nome do filme
    :param ano: ano do filme
    :param booleano_ganhou: boleano para verificar se o registro é ganhador ou não
    :return:objeto de Movie
    """
    nome_filme = nome_filme.lstrip().replace(',', '')  # remove espaço em branco no inicio caso tenha
    obj_movie, created = Movie.get_or_create(movie_name=nome_filme, year=ano, bool_winner=booleano_ganhou)

    return obj_movie


def registrar_produtor_no_filme(produtor: Producer, filme: Movie) -> MovieProducer:
    """
    Função para registrar o produtor do filme, traz registro caso exista
    :param produtor: objeto de Producer
    :param filme: objeto de Movie
    :return: objeto de MovieProducer
    """
    obj_prod_movie, created = MovieProducer.get_or_create(movie=filme, producer=produtor)
    return obj_prod_movie


def registrar_studio_no_filme(studio: Studio, filme: Movie) -> MovieStudio:
    """
    Função para registrar o studio do filme, traz registro caso exista
    :param studio: objeto de Studio
    :param filme: objeto de Movie
    :return: objeto de MovieStudio
    """
    obj_prod_movie, created = MovieStudio.get_or_create(movie=filme, studio=studio)
    return obj_prod_movie


def registrar_produtores_no_filme(lista_produtores: List[str], filme: Movie) -> None:
    """
    Registra a lista de nome de produtores no filme
    :param lista_produtores: lista com os nomes dos produtores
    :param filme: objeto de Movie
    :return: None
    """
    for nome_produtor in lista_produtores:
        nome_produtor = nome_produtor.lstrip().replace(',',
                                                       '')  # remove espaço em branco no inicio da string caso contenha
        obj_produtor_do_filme = registrar_produtor(nome_produtor)
        obj_prod_movie = registrar_produtor_no_filme(obj_produtor_do_filme, filme)


def registrar_studios_no_filme(lista_estudios: list, filme: Movie) -> None:
    """
    registra a lista de nome de estudios no filme
    :param lista_estudios: lista com os nomes dos estudios
    :param filme: objeto de Movie
    :return: None
    """
    for nome_estudio in lista_estudios:
        obj_estudio = registrar_studio(nome_estudio)
        obj_estud_movie = registrar_studio_no_filme(obj_estudio, filme)


def transforma_coluna_vencedor_em_booleano(valor_a_verificar: str) -> bool:
    """
    Função para transformar coluna de vencedor do premio em booleando, se utilizou regex nessa função se pensando
    que talvez a coluna possa conter lixo, seria mais fácil mexer em um regex do que adicionar condições a um if
    :param valor_a_verificar:
    :return: booleano True para vencedor do filme, False para perdedor
    """
    valor_a_verificar = valor_a_verificar.lstrip()  #remove espaços em branco no inicio
    pattern = re.compile(regex_de_verificacao_vencerdor, re.IGNORECASE)
    if pattern.fullmatch(valor_a_verificar):
        return True
    else:
        return False


def transforma_texto_em_lista(string_texto: str, regex_pattern: str) -> list:
    """
    Função para transformar texto em lista com base em padrão regex para a quebra do texto
    :param string_texto: string de estudios
    :param regex_pattern: regex para split da string
    :return: lista feita após o split
    """
    lista_resultado = re.split(regex_pattern, string_texto)
    return lista_resultado


def encontra_todos_filmes_vencedores() -> List[Movie]:
    """
    Função para encontrar todos os filmes que ganharam o premio
    :return: lista de objetos Movie
    """
    lista_filmes_vencedores = Movie.select().where(Movie.bool_winner == True)
    return lista_filmes_vencedores


def encontra_todos_produtores_de_um_filme(obj_filme: Movie) -> List[Producer]:
    """
    Função responsável para encontrar a lista de produtores (Producer) de um filme, ela recebe o objeto de Movie
    e contra em MovieProducer a lista de produtores
    :param obj_filme: objeto de Movie
    :return: retorna lista de produtores (Producer)
    """
    lista_de_obj_filmes_produtores = MovieProducer.select().where(MovieProducer.movie == obj_filme)
    lista_produtores = list()
    for obj_filmes_produtores in lista_de_obj_filmes_produtores:
        lista_produtores.append(obj_filmes_produtores.producer)
    return lista_produtores


def processa_lista_de_filmes_e_transforma_em_produtores() -> dict:
    """
    Função principal para gerar o resultado da api, ela encontra todos os filmes vencedores e a partir disso
    encontra-se os produtores dos filmes, se encontra as listas contendo os produtores para o maior intervalo
    e para o menor intervalo, por fim se gera a partir dessas duas listas o dicionário final que irá para a api
    :return: dicionário base dicionario_base_max_min definido em defines.py com as informações sobre
    cada item dentro da lista que está contida nas chaves key_dict_min e key_dict_max é uma dicionário similar
    a dicionario_base_produtor
    """
    # lista com todos os filmes vencedores
    lista_de_filmes_vencedores = encontra_todos_filmes_vencedores()

    # dicionário que conterá todos os objetos de ProdutorIntervaloVitorias, como se percorre primeiro filmes
    # filme por filme se vai atualizando o conteudo de dict_produtores
    dict_produtores = dict()

    # loop para percorrer a lista com todos os filmes vencedores e transformar o(s) Producer(s) em um objeto de
    # ProdutorIntervaloVitorias que facilita na hora de calcular o intervalo de vitórias
    for filme_vencedor in lista_de_filmes_vencedores:
        lista_produtores = encontra_todos_produtores_de_um_filme(filme_vencedor)
        ano_vitoria_filme = filme_vencedor.year
        # nesse loop, lista todos os produtores do filme atual para atualizar dict_produtores
        for obj_produtores in lista_produtores:
            if obj_produtores in dict_produtores:
                # se caso esse objeto já entrou no dicionário é necessário atualizar o objeto
                atualiza_objeto_produtor_intervalo_vitorias(dict_produtores[obj_produtores], ano_vitoria_filme)
            else:
                # se caso esse objeto não entrou no dicionário énecessário cria-lo
                dict_produtores[obj_produtores] = cria_objeto_produtor_intervalo_vitorias(obj_produtores,
                                                                                          ano_vitoria_filme)
    # lista que conterá os objetos que de ProdutorIntervaloVitorias que possuem intervalo, ou seja, qualquer vencedor
    # premio que ganhou apenas uma vez ele não estará nessa lista
    lista_produtor_intervalo = list()

    # loop para retirar todos os produtores que ganharam apenas uma vez dessa lista (eles não serão contabilizados)
    for obj_produtor, obj_produtor_intervalo in dict_produtores.items():
        if not isNaN(obj_produtor_intervalo.maior_intervalo):
            lista_produtor_intervalo.append(obj_produtor_intervalo)

    # após os produtores tratados e filtrados encontra-se os ProdutorIntervaloVitorias que tem o maior intervalo
    # e o menor intervalo respectivamente em list_prod_intervalo_maior, list_prod_intervalo_menor.
    list_prod_intervalo_maior = processa_lista_produtor_intervalo_encontra_intervalo(lista_produtor_intervalo,
                                                                                     maior_intervalo=True)
    list_prod_intervalo_menor = processa_lista_produtor_intervalo_encontra_intervalo(lista_produtor_intervalo,
                                                                                     maior_intervalo=False)

    # com os dois dicionários contendo os objetos de ProdutorIntervaloVitorias se gera o dicionário final
    # para ser retornado para a api
    dicionario_resultado = transforma_lista_produtor_intervalo_em_dict(list_prod_intervalo_maior,
                                                                       list_prod_intervalo_menor)

    return dicionario_resultado


def processa_lista_produtor_intervalo_encontra_intervalo(lista_prod_inter: List[ProdutorIntervaloVitorias],
                                                         maior_intervalo=True) -> List[ProdutorIntervaloVitorias]:
    """
    Função para processar a lista contendo o objeto ProdutorIntervaloVitorias que se organiza a lista por meio da
    variavel maior valor, pois a depender do valor da varável se inverte a lista porém se muda a variavel do
    objeto ProdutorIntervaloVitorias sobre qual será feito o ordenamento, função retorna uma lista contendo tratada
    a depender do valor de maior_intervalo
    :param lista_prod_inter: lista de ProdutorIntervaloVitorias contendo todos os produtores que ganharam o premio
    :param maior_intervalo: booleano pra decidir qual tipo de ProdutorIntervaloVitorias será retornado
    produtores com o menor intervalo entre dois prêmios consecutivos se maior_intervalo == True
    produtores que obtveram o premio mais rápido se maior_intervalo == False
    :return: lista de ProdutorIntervaloVitorias
    """
    if maior_intervalo:
        lista_organizada_por_intervalo = sorted(lista_prod_inter, key=lambda x: x.maior_intervalo,
                                                reverse=maior_intervalo)  # ordena utilizando maior intervalo
    else:
        lista_organizada_por_intervalo = sorted(lista_prod_inter, key=lambda x: x.menor_intervalo,
                                                reverse=maior_intervalo)  # ordena utilizando menor intervalo
    sub_lista_maior_intervalo = list()
    if lista_organizada_por_intervalo:
        # o ordenamento é revertido pois nessa etatapa do código pois se considera que o valor que será procurado
        # do maior ou do menor intervalo estará sempre na primeira posição da lista
        intervalo = lista_organizada_por_intervalo[primeiro_elemento_lista]
        if maior_intervalo:
            valor_intervalo = intervalo.maior_intervalo
        else:
            valor_intervalo = intervalo.menor_intervalo
        # apos se encotrar o valor de intervalo desejado se percorre a lista contendo todos os vencedores para encontrar
        # somente os produtores com valor de intervalo igual a variavel 'intervalo'
        for obj_prod_inter_vit in lista_organizada_por_intervalo:
            if maior_intervalo:
                if obj_prod_inter_vit.maior_intervalo == valor_intervalo:
                    sub_lista_maior_intervalo.append(obj_prod_inter_vit)
                else:
                    # uma vez que a lista esta ordenada pode-se parar mais cedo nesse for pois os valores subsequentes
                    # não são mais uteis
                    break
            else:
                if obj_prod_inter_vit.menor_intervalo == valor_intervalo:
                    sub_lista_maior_intervalo.append(obj_prod_inter_vit)
                else:
                    break

    return sub_lista_maior_intervalo


def transforma_lista_produtor_intervalo_em_dict(lista_maior_intervalo: List[ProdutorIntervaloVitorias],
                                                lista_menor_intervalo: List[ProdutorIntervaloVitorias]) -> dict:
    """
    Função que monta o dicionário final, recebe dias listas contendo os objetos de ProdutorIntervaloVitorias a
    primeira com os objetos contendo os produtores com o menor intervalo entre dois prêmios consecutivos
    e a segunda com os produtores que obtveram o premio mais rápido
    :param lista_maior_intervalo: lista contendo objeto de ProdutorIntervaloVitorias para representar os produtores
     com os maiores intervalos entre dois prêmios consecutivos
    :param lista_menor_intervalo: lista contendo objeto de ProdutorIntervaloVitorias para representar os produtores
     com o menor intervalo entre dois prêmios consecutivos
    :return: retorna dicionário base dicionario_base_max_min definido em defines.py com as informações sobre
    cada item dentro da lista que está contida nas chaves key_dict_min e key_dict_max é uma dicionário similar
    a dicionario_base_produtor
    """

    dicionario_base_max_min_aux = deepcopy(dicionario_base_max_min)  # faz copia profunda pois o dicionário contem lista
    for obj_produtor_intervalo in lista_maior_intervalo:
        dict_aux = deepcopy(dicionario_base_produtor)
        dict_aux[key_dict_producer] = obj_produtor_intervalo.produtor.name
        dict_aux[key_dict_interval] = obj_produtor_intervalo.maior_intervalo
        dict_aux[key_dict_previous_win] = obj_produtor_intervalo.retorna_maior_intervalo_previous_win()
        dict_aux[key_dict_following_win] = obj_produtor_intervalo.retorna_maior_intervalo_following_win()
        dicionario_base_max_min_aux[key_dict_max].append(dict_aux)

    for obj_produtor_intervalo in lista_menor_intervalo:
        dict_aux = deepcopy(dicionario_base_produtor)
        dict_aux[key_dict_producer] = obj_produtor_intervalo.produtor.name
        dict_aux[key_dict_interval] = obj_produtor_intervalo.menor_intervalo
        dict_aux[key_dict_previous_win] = obj_produtor_intervalo.retorna_menorintervalo_previous_win()
        dict_aux[key_dict_following_win] = obj_produtor_intervalo.retorna_menor_intervalo_following_win()
        dicionario_base_max_min_aux[key_dict_min].append(dict_aux)

    return dicionario_base_max_min_aux


def cria_objeto_produtor_intervalo_vitorias(obj_produtor: Producer, ano_vitoria: int) -> ProdutorIntervaloVitorias:
    """
    Função para criar objeto de ProdutorIntervaloVitorias
    :param obj_produtor: objeto de Producer
    :param ano_vitoria: inteiro representando o ano que o produtor ganhou o filme na primeira incidência do código
    :return: objeto de ProdutorIntervaloVitorias
    """
    obj_protutor_intervalo_vitorias = ProdutorIntervaloVitorias(obj_produtor, ano_vitoria)
    return obj_protutor_intervalo_vitorias


def atualiza_objeto_produtor_intervalo_vitorias(obj_prod_inter_vit: ProdutorIntervaloVitorias,
                                                ano_vitoria: int) -> None:
    """
    Função que recebe objeto ProdutorIntervaloVitorias e atualiza com novo ano
    :param obj_prod_inter_vit: objeto de ProdutorIntervaloVitorias
    :param ano_vitoria: ano da vitoria no awards
    :return: None
    """
    obj_prod_inter_vit.processa_ano_vitoria(ano_vitoria)

