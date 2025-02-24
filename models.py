from peewee import *
from math import nan as NaN
from math import isnan as isNaN

db = SqliteDatabase('outsera_test.db')
quantidade_minima_para_processamento_de_lista = 1
primeiro_elemento_lista = 0
segundo_elemento_lista = 1
ultimo_elemento_lista = -1


class BaseModel(Model):
    class Meta:
        database = db


class Producer(BaseModel):
    name = CharField(max_length=200, unique=True, null=False)


class Studio(BaseModel):
    name = CharField(max_length=200, unique=True, null=False)


class Movie(BaseModel):
    movie_name = CharField(max_length=200, null=False)
    year = IntegerField(null=False)
    bool_winner = BooleanField(null=False)

    class Meta:
        indexes = (
            (('movie_name', 'year'), True),
        )


class MovieProducer(BaseModel):
    movie = ForeignKeyField(Movie, null=False, backref='film_award_producer')
    producer = ForeignKeyField(Producer, null=False, backref='film_award_producer')

    class Meta:
        indexes = (
            (('movie', 'producer'), True),
        )


class MovieStudio(BaseModel):
    movie = ForeignKeyField(Movie, null=False, backref='film_award_studio')
    studio = ForeignKeyField(Studio, null=False, backref='film_award_studio')

    class Meta:
        indexes = (
            (('movie', 'studio'), True),
        )


class ProdutorIntervaloVitorias:
    """
    Objeto criado para simplifcar o manejo de Producer e a relação entre os produtores e os
    intervalos de vitórias
    """
    def __init__(self, produtor: Producer, ano_vitoria: int):
        """
        Init do objeto
        :param produtor: é objeto de Produtor
        :param ano_vitoria: primeiro ano da vitória encontrado

        Attributes
        ----------
        produtor: objeto de Producer
            guarda o produtor na forma de model
        maior_intervalo: float
            maior_intervalo só será diferente de NaN quando o produtor ganhar mais 2 filmes ou mais, variável
            contem o valor com o maior intervalo qua o produtor tem entre vitórias do prêmio.
        menor_intervalo: float
            menor_intervalo só será diferente de NaN quando o produtor ganhar mais 2 filmes ou mais, variável
            contem o valor com o maior intervalo qua o produtor tem entre vitórias do prêmio.
        lista_vitorias: list
            lista com todos os anos de vitórias do produtor
        _ano_maior_intervalo_vitoria_prev: int -> privado
            menor ano de vitória do produtor quando for maior intervalo
        _ano_maior_intervalo_vitoria_prox: int -> privado
            maior ano de vitória do produtor quando for maior intervalo
        _ano_menor_intervalo_vitoria_prev: int -> privado
            maior ano de vitória do produtor quando for maior intervalo
        _ano_menor_intervalo_vitoria_prox: int -> privado
            maior ano de vitória do produtor quando for maior intervalo
        """
        self.produtor = produtor
        self.maior_intervalo = NaN
        self.menor_intervalo = NaN
        self.lista_vitorias = [ano_vitoria]
        self._ano_maior_intervalo_vitoria_prev = 0
        self._ano_maior_intervalo_vitoria_prox = 0
        self._ano_menor_intervalo_vitoria_prev = 0
        self._ano_menor_intervalo_vitoria_prox = 0

    def _adiciona_ano_vitoria(self, ano_vitoria: int) -> None:
        """
        Função privada para se adicionar o ano da vitória
        :param ano_vitoria: ano da vitória do produtor
        :return:  None
        """
        if ano_vitoria not in self.lista_vitorias:
            self.lista_vitorias.append(ano_vitoria)

    def processa_ano_vitoria(self, ano_vitoria: int):
        """
        Função que processa o ano da vitória, ela atualiza a lista de vitória do produtor
        e calcula o menor intervalo considerando o novo ano adicionado
        :param ano_vitoria:
        :return:
        """
        self._adiciona_ano_vitoria(ano_vitoria)

        if len(self.lista_vitorias) > quantidade_minima_para_processamento_de_lista:
            self.lista_vitorias.sort()
            self._calcula_menor_intervalor_vitoria()
            self._calcula_maior_intervalor_vitoria()

    def _calcula_menor_intervalor_vitoria(self) -> None:
        """
        Calcula o menor intervalo de vitória do produtor e atualiza as variáveis privadas
        _ano_menor_intervalo_vitoria_prev e _ano_menor_intervalo_vitoria_prox para função funcionar corretamente
        é necessário se realizar antes uma ORDENAÇÃO DA LISTA DE VITÓRIAS lista_vitorias
        :return: None
        """
        intervalo_aux = self.menor_intervalo
        for index in range(len(self.lista_vitorias) - 1):
            elemento_atual = index
            elemento_proximo = index + 1
            intervalo_atual = self.lista_vitorias[elemento_proximo] - self.lista_vitorias[elemento_atual]
            if not isNaN(intervalo_aux):
                if intervalo_atual < intervalo_aux:
                    intervalo_aux = intervalo_atual
                    self._ano_menor_intervalo_vitoria_prev = self.lista_vitorias[elemento_atual]
                    self._ano_menor_intervalo_vitoria_prox = self.lista_vitorias[elemento_proximo]
            else:
                self._ano_menor_intervalo_vitoria_prev = self.lista_vitorias[elemento_atual]
                self._ano_menor_intervalo_vitoria_prox = self.lista_vitorias[elemento_proximo]
                intervalo_aux = intervalo_atual
        self.menor_intervalo = intervalo_aux

    def _calcula_maior_intervalor_vitoria(self) -> None:
        """
        Calcula o menor intervalo de vitória do produtor e atualiza as variáveis privadas
        _ano_menor_intervalo_vitoria_prev e _ano_menor_intervalo_vitoria_prox para função funcionar corretamente
        é necessário se realizar antes uma ORDENAÇÃO DA LISTA DE VITÓRIAS lista_vitorias
        :return: None
        """
        intervalo_aux = self.maior_intervalo
        for index in range(len(self.lista_vitorias) - 1):
            elemento_atual = index
            elemento_proximo = index + 1
            intervalo_atual = self.lista_vitorias[elemento_proximo] - self.lista_vitorias[elemento_atual]
            if not isNaN(intervalo_aux):
                if intervalo_atual > intervalo_aux:
                    intervalo_aux = intervalo_atual
                    self._ano_maior_intervalo_vitoria_prev = self.lista_vitorias[elemento_atual]
                    self._ano_maior_intervalo_vitoria_prox = self.lista_vitorias[elemento_proximo]
            else:
                intervalo_aux = intervalo_atual
                self._ano_maior_intervalo_vitoria_prev = self.lista_vitorias[elemento_atual]
                self._ano_maior_intervalo_vitoria_prox = self.lista_vitorias[elemento_proximo]
        self.maior_intervalo = intervalo_aux

    def retorna_maior_intervalo_previous_win(self) -> int:
        """
        Função para retornar o valor de _ano_maior_intervalo_vitoria_prev
        :return: valor de _ano_maior_intervalo_vitoria_prev
        """
        return self._ano_maior_intervalo_vitoria_prev

    def retorna_maior_intervalo_following_win(self) -> int:
        """
        Função para retornar o valor de _ano_maior_intervalo_vitoria_prox
        :return: valor de _ano_maior_intervalo_vitoria_prox
        """
        return self._ano_maior_intervalo_vitoria_prox

    def retorna_menorintervalo_previous_win(self) -> int:
        """
        Função para retornar o valor de _ano_menor_intervalo_vitoria_prev
        :return: valor de _ano_menor_intervalo_vitoria_prev
        """
        return self._ano_menor_intervalo_vitoria_prev

    def retorna_menor_intervalo_following_win(self) -> int:
        """
        Função para retornar o valor de _ano_menor_intervalo_vitoria_prox
        :return: valor de _ano_menor_intervalo_vitoria_prox
        """
        return self._ano_menor_intervalo_vitoria_prox


db.connect()
db.create_tables([Producer, Studio, Movie, MovieProducer, MovieStudio])
