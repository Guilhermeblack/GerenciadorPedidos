from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from .views import loguin, index
import os

# importa a funçao ou classe a ser testada

class testRenders(TestCase):

    def testIndex(self):
        if self.client.get(index).status_code == 200:
            return self.assertTemplateUsed('index.html')

    def testLoguin(self):
        c = Client()
        if c.login(username='garçom', password='prontogarçom'):
            return self.assertTemplateUsed('ped')

    def funcLog(self):
        if self.client.post(loguin, {'nome':'garçom', 'senha':'prontogarçom'}).status_code == 200:
            return self.assertTemplateUsed('ped')




    # cria uma classe que vai receber o TestCase
    # cria as funções que testarão o retorno da classe ou funçao importada

    # os testes podem ser chamados individualmente, pelo modulo, pelo app, ou test em geral
