from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from tutorial.quickstart.serializers import GroupSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            # Allow anyone to create a user (register)
            permission_classes = [permissions.AllowAny]
        else:
            # Require authentication for other actions
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
