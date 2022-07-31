from django import forms
from django.contrib.auth import get_user
from . import models
import cloudinary

class autForm(forms.ModelForm):

    class Meta:
        model = models.logform
        fields = ('nome', 'senha')

    nome = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'nome'}), help_text="Insira o nome ou identificação do usuário")
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'senha'}), help_text="Insira a senha do usuário")


class produto(forms.ModelForm):

    class Meta:
        model = models.Produtocad
        fields = 'nome','descricao','preco','tipo','img_prod','quantidade','medida','cardapio','qnt_minima'

        widgets = {
            'descricao' : forms.Textarea(attrs={'rows': 3, 'cols': 27})

            # 'nome' : forms.CharField(help_text="Este campo representa o nome do produto"),
            # 'preco' : forms.FloatField(help_text="Insira o preço do produto neste campo"),
            # 'tipo' : forms.CharField(help_text="Escolha se o produto é um alimento ou uma bebida"),
            # 'quantidade' : forms.IntegerField(widget=forms.PasswordInput(attrs={'min_value':1, 'width':15, 'require': False}) )
            # 'medida' : forms.CharField(help_text="Escolha a unidade de medida do produto"),
            # 'cardapio' : forms.BooleanField(help_text="Defina se o produto irá aparecer no cardápio"),
            # 'qnt_minima' : forms.FloatField(help_text="Defina qual a quantidade minima do produto a loja poderá ter em estoque antes de ser alertada")
        }

class pedidos(forms.ModelForm):




    class Meta:
        model = models.Pedido
        fields = 'comandaref','observacao','quantidade','produtosPed','valor'
        name= 'soupedido'

    widgets = {
        'observacao': forms.TextInput(attrs={'rows': 3, 'cols': 8})
        # 'produtosPed': forms.HiddenInput(),
    #     # 'quantidade': forms.IntegerField(help_text="Insira a quantidade do produto que será pedido"),
    #     # 'comandaref': forms.SelectMultiple(help_text="Insira a quantidade do produto que será pedido"),
    }

    def __init__(self, *args, **kwargs):
        super(pedidos, self).__init__(*args, **kwargs)
        self.fields['produtosPed'].label =''



class comandas(forms.ModelForm):


    nome = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'cliente'}), help_text="Insira o nome da nova comanda"),
    # n_mesa = forms.IntegerField(help_text="Insira o nome da nova comanda")
    # valor= forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = models.Comanda
        fields = 'nome',"n_mesa"
        name = 'soucomanda'






class Newloja(forms.ModelForm):



    class Meta:
        model = models.Loja
        fields = 'nome_loja',"porte"
        name = 'souloja'

    nome_loja: forms.CharField(help_text="Defina o Nome da Loja",
                               widget=forms.Textarea(attrs={'class': 'form-input form-group mx-5', 'placeholder': 'Nome da loja'}))
    porte: forms.ChoiceField( widget= forms.Select(attrs={"name": "select_0","class": "form-control"}))


class Newcli(forms.ModelForm):





    class Meta:
        model = models.User
        fields = 'username', 'password', 'email', 'first_name', 'last_name'
        name = 'sounovocli'

    username : forms.CharField(help_text="Defina o Nome de Usuário",widget=forms.Textarea(attrs={'class': 'form-input', 'placeholder':'Nome de acesso'}))
    password : forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input p-2 mr-4'}))
    # email : forms.EmailField(help_text="Defina o email")
    first_name : forms.CharField(help_text="Defina o Nome",widget=forms.Textarea(attrs={'class': 'form-input', 'placeholder':'Seu nome'}))
    last_name : forms.CharField(help_text="Defina o segundo nome",label="Telefone",widget=forms.Textarea(attrs={'class': 'form-input', 'placeholder':'Numero Telefone'}))

    def __init__(self, *args, **kwargs):
        super(Newcli, self).__init__(*args, **kwargs)
        self.fields['last_name'].label ='Telefone'