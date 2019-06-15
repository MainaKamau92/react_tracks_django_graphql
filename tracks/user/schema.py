import graphene
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType
from datetime import datetime
from graphql import GraphQLError


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return User.objects.all()

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')
        try:
            return User.objects.get(pk=id)
        except:
            raise GraphQLError("User does not exist")


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        date_joined = graphene.DateTime(default_value=datetime.now())

    def mutate(self, info, **kwargs):
        user = get_user_model()(
            username=kwargs.get('username'),
            email=kwargs.get('email'),
        )
        user.set_password(kwargs.get('password'))
        user.save()
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()