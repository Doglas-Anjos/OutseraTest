from models import *
from defines import *
import pandas as pd
import re


def carregar_arquivo_no_banco(caminho_do_arquivo):
    """
    Função que abre arquivos
    :param caminho_do_arquivo:
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


def registrar_produtores_no_filme(lista_produtores: list, filme: Movie) -> None:
    """
    Registra a lista de nome de produtores no filme
    :param lista_produtores: lista com os nomes dos produtores
    :param filme: objeto de Movie
    :return: None
    """
    for nome_produtor in lista_produtores:
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
    pattern = re.compile(regex_de_verificacao_vencerdor, re.IGNORECASE)
    if pattern.fullmatch(valor_a_verificar):
        return True
    else:
        return False


def transforma_texto_em_lista(string_texto: str, regex_pattern: str) -> list:
    """
    Função para transformar texto contendo os studios em uma lista com o nome dos studios
    :param string_texto: string de estudios
    :param regex_pattern: regex para split da string
    :return: lista feita após o split
    """
    lista_resultado = re.split(regex_pattern, string_texto)
    return lista_resultado


if __name__ == '__main__':
    carregar_arquivo_no_banco(path_arquivo_importacao)
