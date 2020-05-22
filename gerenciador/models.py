from django.db import models


class Gerente(models.Model):
    class Meta:
        permissions = [
            ('fazer_pedido', 'incluir pedido'),
            ('ver_feed', 'visualizar o feed'),
            ('iniciar_movimento', 'iniciar o movimento'),
            ('fechar_comanda', 'fechar a comanda'),
            ('abrir_comanda', 'abrir uma nova comanda'),
            ('controlar_produtos', 'controlar produtos disponiveis')
        ]

    def __str__(self):
        return self.nome

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
    senha_rep = models.CharField(
        max_length=50,
        null=False,
        blank=False,

    ),
    objects = models.Manager()

class Garçom(models.Model):
    class Meta:
        permissions = [
            ('fazer_pedido', 'incluir pedido'),
            ('pedido_entregue', 'pedido foi entregue'),
            ('ver_feed', 'visualizar o feed'),
            ('abrir_comanda', 'abrir uma nova comanda')
        ]

    def __str__(self):
        return self.nome

    id = models.AutoField(primary_key=True),
    nome = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        default="garçom",
    ),
    senha = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    ),
    senha_rep = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    ),
    objects = models.Manager()

class Cozinha(models.Model):
    class Meta:
        permissions = [
            ('pedido_pronto', 'pedido pronto'),
            ('ver_feed', 'visualizar o feed')
        ]

    def __str__(self):
        return self.nome

    id = models.AutoField(primary_key=True),
    nome = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        default='cheff',
    )
    senha = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )
    senha_rep = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )
    objects = models.Manager()


class Comanda(models.Model):

    id = models.AutoField(primary_key=True)

    nome = models.TextField(
        max_length=50,
        null=False,
        blank=False,
        # default='sôzé'
    )
    total = models.FloatField(
        max_length=6,
        null=False,
        blank=False,
        # default=1.00
    )
    pedidos = models.TextField(
        max_length=255,
        null=False,
        blank=False,
        default=''
    )

    def __str__(self):
        return '{}- {}'.format(self.id, self.nome)

    objects = models.Manager()


class Produtocad(models.Model):

    id = models.AutoField(primary_key=True)

    nome = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    descricao = models.TextField(
        max_length=255,
        null=False,
        blank=False
    )
    preco = models.FloatField(
        max_length=6,
        null=False,
        blank=False
    )

    def __str__(self):
        return self.nome

    objects = models.Manager()


class Pedido(models.Model):

    STATUS_CHOICES = (
        ("P", "Pedido realizado"),
        ("F", "Fazendo"),
        ("E", "Saiu para entrega")
    )



    id = models.AutoField(primary_key=True)

    produtosPedido = models.ManyToManyField(Produtocad)

    item = models.TextField(
        max_length=125,
        null=False,
        blank=False
    )
    quantidade = models.IntegerField(
        null=False,
        blank=False
    )
    observacao = models.TextField(
        max_length=200,
        null=False,
        blank=True
    )

    comanda = models.ForeignKey(
        Comanda,
        on_delete=models.CASCADE,
        default=0
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        blank=False,
        null=False,
        default="P"
    )

    def __str__(self):
        return self.id

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

# Create your models here.
