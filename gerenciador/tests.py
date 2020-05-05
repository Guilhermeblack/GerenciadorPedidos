from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .views import loguin, saveproduto, index
import os

# importa a funçao ou classe a ser testada

class testRenders(TestCase):

    def testIndex(self):
        if self.client.get(index).status_code == 200:
            return self.assertTemplateUsed('index.html')

#
# class testImage(TestCase):
#
#     def testUploadImagem(self):
#         # newPhoto = Photo()
#         # print(open('media/prod.jpg','rb')
#         newPhoto = SimpleUploadedFile(name='prod.jpg', content=open('website/static/media/prod.jpg', 'rb').read())
#         if self.client.post(saveproduto, {
#             'produto': 'testproduto',
#             'modelo': 'modeloproduto',
#             'quabtidade': 100,
#             'preco': 10,
#             'img_prod': newPhoto,
#             'descrocao': 'testDescricao'
#         }):
#             if 'prod.jpg' in os.listdir('website/static/media/image/'):
#                 return self.assertEqual(response.status_code, 200)

    # cria uma classe que vai receber o TestCase
    # cria as funções que testarão o retorno da classe ou funçao importada

    # os testes podem ser chamados individualmente, pelo modulo, pelo app, ou test em geral
