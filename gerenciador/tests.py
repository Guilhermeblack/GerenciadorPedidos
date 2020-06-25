from django.test import TestCase
from django.contrib.auth.hashers import make_password, check_password, pbkdf2

from .views import loguin, index, adm


# importa a funçao ou classe a ser testada

class testRenders(TestCase):

    def testIndex(self):
        if self.client.get(index).status_code == 200:
            return self.assertTemplateUsed('index.html')

    def testLog(self):
        if self.client.post(loguin, {
            'nome':'gerente',

            'senha': make_password('prontoadmin', salt=None, hasher='pbkdf2_sha256')
        }).status_code == 200:
            return self.assertTemplateUsed('adm')

class statusMovimento(TestCase):

    #teste do ajax
    def alteraMov(self):
        pass

    # cria uma classe que vai receber o TestCase
    # cria as funções que testarão o retorno da classe ou funçao importada

    # os testes podem ser chamados individualmente, pelo modulo, pelo app, ou test em geral
