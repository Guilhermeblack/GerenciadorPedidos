from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField
from django.db.models import signals
from django.utils.timezone import now
# import django_signal_notifier


class Loja(models.Model):

    id = models.AutoField(primary_key=True)

    STATUS_CHOICES = (
        ("L", "Ligado"),
        ("D", "Desligado"),
    )

    movimento = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='D',
        blank=False,
        null=False
    )

    nome_loja = models.CharField(
        max_length=50,
        null=False,
        blank=False,

    )


    data = models.DateTimeField(auto_now_add=True, blank=True)

    STATUS_CHOICES = (
        ("G", "Gold"),
        ("P", "Plat"),
    )
    porte = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default="G",
        blank=True,
        null=False
    )


    def __str__(self):
        return ' {}'.format(self.nome_loja)

    objects = models.Manager()


class Newcli(models.Model):

    id = models.AutoField(primary_key=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, null=True, blank=True)
    # def __str__(self):
    #     return ' {} _{}'.format(self.loja, self.user)

# Create your models here.


class Gerente(models.Model):

    class Meta:
        permissions = [
            ('fazer_pedido', 'incluir pedido'),
            ('ver_feed', 'visualizar o feed'),
            ('iniciar_movimento', 'iniciar o movimento'),
            ('fechar_comanda', 'fechar a comanda'),
            ('abrir_comanda', 'abrir uma nova comanda'),
            ('controlar_produtos', 'controlar produtos disponiveis'),
            ('sou_cliente', 'acesso de cliente')
        ]

        # app_label = 'gerente'

    def __str__(self):
        return self.nome

    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, null=True, blank=True, related_name="ger_loja")
    id = models.AutoField(primary_key=True),

    nome = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        default='gerente'
    ),
    senha = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    ),
    telefone = models.CharField(
        max_length=20,
        null=False,
        blank=False,

    ),
    email = models.CharField(
        max_length=35,
        null=False,
        blank=False,

    ),

    # loja = models.ForeignKey(Loja, on_delete=models.CASCADE, null=True, blank=True, related_name="new_loja")


    objects = models.Manager()


class Comanda(models.Model):

    id = models.AutoField(primary_key=True)

    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, null=True, blank=True, related_name="com_loja")

    cliente = models.ForeignKey(Newcli, on_delete=models.CASCADE, null=True, blank=True)

    nome = models.CharField(
        max_length=50,
        null=False,
        blank=False,

    )

    n_mesa = models.IntegerField(
        null=False,
        blank=False,
        unique=True
    )

    valor = models.FloatField(
        default=0.0,
        null=False,
        blank=True

    )

    data = models.DateTimeField(auto_now_add=True, blank=True)

    STATUS_CHOICES = (
        ("A", "Aberto"),
        ("F", "Fechado"),
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default="A",
        blank=True,
        null=False
    )


    def __str__(self):
        return ' {}'.format(self.nome)

    objects = models.Manager()


class Produtocad(models.Model):

    id = models.AutoField(primary_key=True)

    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, null=True, blank=True, related_name="pro_loja")

    nome = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    descricao = models.TextField(
        max_length=255,
        null=True,
        blank=True,
    )

    preco = models.FloatField(
        null=False,
        blank=False,
        default=0.0
    )
    qnt_minima = models.FloatField(
        null=True,
        blank=True,
        default=1
    )
    quantidade = models.FloatField(
        null=True,
        blank=True,
        default=1
    )

    # insumos = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    STATUS_CHOICES = (
        ("A", "Alimento"),
        ("B", "Bebida"),
        ("O", "Outro")
    )
    tipo = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        blank=False,
        null=False
    )

    UND_MED = (
        ("U", "Unidade"),
        ("K", "Kilo"),
        ("G", "Grama"),
        ("L", "Litro"),
        ("M", "Metro")
    )
    medida = models.CharField(
        max_length=1,
        choices=UND_MED,
        default="U",
        blank=False,
        null=False
    )

    cardapio = models.BooleanField(blank=True, null=False, default=False)

    img_prod = CloudinaryField(blank=True, null=True)

    # def __str__(self):
    #     return self.nome

    objects = models.Manager()

class Pedido(models.Model):

    STATUS_CHOICES = (
        ("P", "Pedido realizado"),
        ("F", "Fazendo"),
        ("S", "Saiu para entrega"),
        ("E", "Foi entregue"),
        ("C", "Cancelado")
    )

    STATUS_PGT = (
        ("P", "Pago"),
        ("R", "Resto"),
        ("N", "Não pago")
    )


    comandaref= models.ForeignKey(
        Comanda,
        null=True,
        on_delete=models.CASCADE,
        related_name="pedidoComanda"
    )

    id = models.AutoField(primary_key=True)

    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, null=True, blank=True, related_name="ped_loja")

    produtosPed= models.ManyToManyField(Produtocad, related_name='produto', blank=False)

    quantidade = models.IntegerField(
        null=False,
        blank=False,
        default= 1
    )
    observacao = models.TextField(
        max_length=50,
        null=False,
        blank=True,
        default='Sem Observações.',

    )

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        blank=False,
        null=False,
        default="P"
    )

    status_pago = models.CharField(
        max_length=1,
        choices=STATUS_PGT,
        blank=False,
        null=False,
        default="N"

    )

    valor = models.FloatField(
        default=0.0,
        null=False,
        blank=True

    )

    data = models.DateTimeField(auto_now_add=True , blank=True)

    # def __str__(self):
    #     return '{} - {}'.format( self.id, self.comandaref)

    objects = models.Manager()

class Pagamentos(models.Model):

    id = models.AutoField(primary_key=True)

    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, null=True, blank=True, related_name="pag_loja")

    pedidored = models.ManyToManyField(Pedido, related_name='pedidored', blank=True)

    STATUS_PGT = (
        ("F", "fechou comanda"),
        ("P", "pagou produto"),
        ("R", "Restante")
    )

    FORMA_PGT = (
        ("C", "Cartão"),
        ("P", "Pix"),
        ("D", "Dinheiro")
    )

    formapg = models.CharField(
        max_length=1,
        choices=FORMA_PGT,
        blank=False,
        null=False,
        default="D"
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS_PGT,
        blank=False,
        null=False,
        default="R"
    )


    valor = models.FloatField(
        default=0.0,
        null=False,
        blank=True
    )

    data = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return '{}'.format(self.id)

    objects = models.Manager()

class Insumos(models.Model):

    id = models.AutoField(primary_key=True)

    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, null=True, blank=True, related_name="ins_loja")

    quantidade_prod = models.FloatField(
        null=False,
        blank=False,
        default=0.0
    )


    insumo_prod = models.ForeignKey(Produtocad, on_delete=models.CASCADE, null=True, blank=True, related_name="insumo_prod")

    produto_prod = models.ForeignKey(Produtocad, on_delete=models.CASCADE, null=True, blank=True, related_name="produto_prod")

    objects = models.Manager()


class logform(models.Model):
    senha = models.CharField(
        max_length=80,
        null=False,
        blank=False,
    )
    nome = models.CharField(
        max_length=80,
        null=False,
        blank=False,
    )



