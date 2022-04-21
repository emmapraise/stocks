import graphene
import alpaca_trade_api as tradeapi
from graphene_django import DjangoObjectType, DjangoListField
from .models import Stock
from psaw import PushshiftAPI
import datetime
from django.conf import settings

api_url = settings.ALAPA_MARKET_URL
api_key_id = settings.ALAPA_MARKET_API_KEY
api_secret_key = settings.ALAPA_MARKET_SECRET_KEY


api = PushshiftAPI()
start_time = int(datetime.datetime(2021, 1, 30).timestamp())

list(
    api.search_submissions(
        after=start_time,
        subreddit="wallstreetbets",
        filter=["url", "author", "title", "subreddit"],
        limit=10,
    )
)


class StockType(DjangoObjectType):
    class Meta:
        model = Stock
        fields = "__all__"


class Query(graphene.ObjectType):
    all_stocks = graphene.List(StockType)
    stock = graphene.Field(StockType, stock_id=graphene.Int())

    def resolve_all_stocks(self, info, **kwargs):
        """Get all Stocks"""
        return Stock.objects.all()

    def resolve_stock(self, info, stock_id):
        """Get a stock with id"""
        return Stock.objects.get(pk=stock_id)


class StockInput(graphene.InputObjectType):
    name = graphene.String()
    symbol = graphene.String()
    exchange = graphene.String()
    isEtf = graphene.Boolean()


class CreateStock(graphene.Mutation):
    class Arguments:
        stock_data = StockInput(required=True)

    stock = graphene.Field(StockType)

    @staticmethod
    def mutate(root, info, stock_data=None):

        api = tradeapi.REST(api_key_id, api_secret_key, base_url=api_url)
        assets = api.list_assets()

        for asset in assets:
            stock_instance = Stock(
                name=asset.name,
                exchange=asset.exchange,
                symbol=asset.symbol,
                # is_etf=stock_data.isEtf,
            )
            stock_instance.save()

        return CreateStock(stock=stock_instance)


class UpdateStock(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        stock_data = StockInput(required=True)

    stock = graphene.Field(StockType)

    @staticmethod
    def mutate(root, info, id=None, stock_data=None):

        stock_instance = Stock.objects.get(pk=id)

        if stock_instance:
            stock_instance.name = stock_data.name
            stock_instance.exchange = stock_data.exchange
            stock_instance.symbol = stock_data.symbol
            stock_instance.is_etf = stock_data.isEtf
            stock_instance.save()

            return UpdateStock(stock=stock_instance)
        return UpdateStock(stock=None)


class DeleteStock(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    stock = graphene.Field(StockType)

    @staticmethod
    def mutate(root, info, id):
        stock_instance = Stock.objects.get(pk=id)
        stock_instance.delete()

        return None


class Mutation(graphene.ObjectType):
    create_stock = CreateStock.Field()
    update_stock = UpdateStock.Field()
    delete_stock = DeleteStock.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
