import graphene

from graphene_django import DjangoObjectType, DjangoListField
from .models import Stock
from psaw import PushshiftAPI
import datetime

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
        # Get all stokcs
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
        stock_instance = Stock(
            name=stock_data.name,
            exchange=stock_data.exchange,
            symbol=stock_data.symbol,
            is_etf=stock_data.isEtf,
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
