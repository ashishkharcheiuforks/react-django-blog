from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Tags
from tags import serializers
from blog_permissions.permissions import IsOwnerOrStaffUser, UserCanCreateOwnObject


# Create your views here.
class TagsViewSet(viewsets.ModelViewSet):

    """Base viewset for user owned recipe attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrStaffUser, UserCanCreateOwnObject)

    """Manage tags in the database"""
    queryset = Tags.objects.all()
    serializer_class = serializers.TagsSerializer

    def get_queryset(self):
        """
        In listing page, return what you have access to
        """
        user = self.request.user

        if user.is_staff:
            return Tags.objects.all()
        else:
            return Tags.objects.filter(user=user.id)

    def get_serializer(self, *args, **kwargs):
        """
        This enables creating multiple tags at once!
        :param args:
        :param kwargs:
        :return: serializer
        """
        if "data" in kwargs:
            data = kwargs["data"]

            if isinstance(data, list):
                kwargs["many"] = True

        return super(TagsViewSet, self).get_serializer(*args, **kwargs)
