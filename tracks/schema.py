import graphene
import tracks.user.schema
import graphql_jwt
import tracks.musics.schema


class Query(tracks.musics.schema.Query, tracks.user.schema.Query, graphene.ObjectType):
    pass


class Mutation(tracks.musics.schema.Mutation,
               tracks.user.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
