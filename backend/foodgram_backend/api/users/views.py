from djoser.views import UserViewSet
from api.users.serializers import CustomUserSerializer
from users.models import User
from recipes.models import Follow
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from api.recipes.serializers import FollowSerializer


class CustomUserViewSet(UserViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id=None):
        user = request.user
        user_to = get_object_or_404(User, id=id)
        if request.method == 'POST':
            if user == user_to:
                return Response(
                    data={'errors': 'You cant subscribe on yourself!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if Follow.objects.filter(user=user, following=user_to).exists():
                return Response(
                    data={'errors': 'You already subscribed on this user!'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            follow = Follow.objects.create(user=user, following=user_to)
            serializer = FollowSerializer(
                follow, context={'request': request}
            )
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        if user == user_to:
            return Response(
                data={'errors': 'You cant unsubscribe yourself!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        follow = Follow.objects.filter(user=user, following=user_to)
        if not follow.exists():
            return Response(
                data={'errors': 'You already not subscribed on this user!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        follows_list = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(follows_list)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
