import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model

from .models import Operation


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class OperationType(DjangoObjectType):
    class Meta:
        model = Operation

class Query(graphene.ObjectType):
    all_Operation = graphene.List(OperationType)

    def resolve_all_operation(self, info):
        return Operation.objects.select_related('user').all()
        
schema = graphene.Schema(query=Query)