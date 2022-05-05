from django.db import models


class common(models.Model):
    createat = models.DateTimeField(auto_now_add=True, null=True)
    updateat = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class Stock(common):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=100)
    exchange = models.CharField(max_length=100)
    is_etf = models.BooleanField(default=0)

    def __str__(self):
        return self.name


class Mention(common):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    source = models.CharField(max_length=200)  # Wallstreetsbet twitter etc
    url = models.URLField()

    def __str__(self):
        return f"The source is ({self.source}) and the url is ({self.url})"


class Stock_price(common):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateTimeField()
    open = models.DecimalField(decimal_places=2, max_digits=10)
    high = models.DecimalField(decimal_places=2, max_digits=10)
    low = models.DecimalField(decimal_places=2, max_digits=10)
    close = models.DecimalField(decimal_places=2, max_digits=10)
    volume = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f"Stock opened at ({self.open}) and close at ({self.close})"


class Etf_holdings(common):
    etf_id = models.IntegerField()
    holding_id = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    shares = models.IntegerField()
    weight = models.IntegerField()

    def __str__(self):
        return f"Etf Id ({self.etf_id}) with holding id ({self.holding_id})"
