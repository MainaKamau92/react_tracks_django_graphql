import graphene
from graphql import GraphQLError
from django.db.models import Q
from tracks.user.schema import UserType
from .models import Track, Likes
from graphene_django import DjangoObjectType


class TrackType(DjangoObjectType):
    class Meta:
        model = Track


class LikesType(DjangoObjectType):
    class Meta:
        model = Likes


class Query(graphene.ObjectType):
    tracks = graphene.List(TrackType, search=graphene.String())
    likes = graphene.List(LikesType)

    def resolve_tracks(self, info, search=None):
        filter = (
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(url__icontains=search) |
            Q(posted_by__username__icontains=search)
        )
        if search:
            return Track.objects.filter(filter)
        return Track.objects.all()

    def resolve_likes(self, info):
        return Likes.objects.all()


class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in to create a track")
        track = Track(title=kwargs.get('title'),
                      description=kwargs.get('description'), url=kwargs.get('url'), posted_by=user)
        track.save()
        return CreateTrack(track=track)


class UpdateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, **kwargs):
        track_id = kwargs.get('track_id')
        title = kwargs.get('title')
        description = kwargs.get('description')
        url = kwargs.get('url')
        user = info.context.user
        track = Track.objects.get(pk=track_id)
        if user.is_anonymous or track.posted_by != user:
            raise GraphQLError("Unauthorized edit")
        track.title = title
        track.description = description
        track.url = url
        track.save()
        return UpdateTrack(track=track)


class DeleteTrack(graphene.Mutation):
    track_id = graphene.Int(required=True)

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        user = info.context.user
        track_id = kwargs.get('track_id')
        if user.is_anonymous:
            raise GraphQLError("You need be logged in")
        track = Track.objects.get(pk=track_id)
        if user != track.posted_by:
            raise GraphQLError("Unauthorized delete")
        track.delete()
        return DeleteTrack(track_id=track_id)


class CreateLike(graphene.Mutation):
    user = graphene.Field(UserType)
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        user = info.context.user
        track_id = kwargs.get('track_id')
        try:
            track = Track.objects.get(pk=track_id)
        except:
            raise GraphQLError("No track of that id exists")
        if user.is_anonymous:
            raise GraphQLError("You must be logged in to like track")

        Likes.objects.create(
            user=user,
            track=track
        )
        return CreateLike(track=track, user=user)


class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()
    update_track = UpdateTrack.Field()
    delete_track = DeleteTrack.Field()
    create_like = CreateLike.Field()
