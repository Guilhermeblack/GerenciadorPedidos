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
        max_length=255,
        null=False,
        blank=False
    )
    senha = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )
    senha_rep = models.CharField(
        max_length=255,
        null=False,
        blank=False,

    )
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
        max_length=255,
        null=False,
        blank=False,
        default="garçom"
    )
    senha = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )
    senha_rep = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )
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
        max_length=255,
        null=False,
        blank=False
    )
    senha = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )
    senha_rep = models.CharField(
        max_length=255,
        null=False,
        blank=False,

    )
    objects = models.Manager()


class Comanda(models.Model):

    def __str__(self):
        return self.id

    id = models.AutoField(primary_key=True),
    total = models.FloatField(
        max_length=6,
        null=False,
        blank=False
    ),
    pedidos = models.TextField(
        max_length=200,
        null=False,
        blank=False
    )
    objects = models.Manager()


class Produto(models.Model):

    def __str__(self):
        return self.nome

    id = models.AutoField(primary_key=True),

    nome = models.TextField(
        max_length=255,
        null=False,
        blank=False
    ),
    descricao= models.TextField(
        max_length=255,
        null=False,
        blank=False
    ),
    preco = models.FloatField(
        max_length=6,
        null=False,
        blank=False
    )

    comanda = models.ForeignKey(
        Comanda,
        on_delete=models.CASCADE
    )
    objects = models.Manager()


class Pedido(models.Model):

    STATUS_CHOICES = (
        ("P", "Pedido realizado"),
        ("F", "Fazendo"),
        ("E", "Saiu para entrega"),
    )

    def __str__(self):
        return self.id

    id = models.AutoField(primary_key=True),

    item = models.TextField(
        max_length=255,
        null=False,
        blank=False
    ),
    quantidade= models.IntegerField(
        max_length=6,
        null=False,
        blank=False
    ),
    valor = models.FloatField(
        max_length=6,
        null=False,
        blank=False,
        default=0
    )
    produtos = models.ManyToManyField(Produto)
    comanda = models.ForeignKey(
        Comanda,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        blank=False,
        null=False,
        default="P"
    )
    objects = models.Manager()



# Create your models here.
