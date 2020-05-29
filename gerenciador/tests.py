from django.test import TestCase

from .views import loguin, index


# importa a funçao ou classe a ser testada

class testRenders(TestCase):

    def testIndex(self):
        if self.client.get(index).status_code == 200:
            return self.assertTemplateUsed('index.html')

    def testLog(self):
        if self.client.post(loguin, {'nome':'garçom', 'senha':'prontogarçom'}).status_code == 200:
            return self.assertTemplateUsed('ped')




    # cria uma classe que vai receber o TestCase
    # cria as funções que testarão o retorno da classe ou funçao importada

    # os testes podem ser chamados individualmente, pelo modulo, pelo app, ou test em geral
