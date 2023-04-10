from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import APIException
from rest_framework import status




class AdminOnlyAccess(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        return False





class AuthorOnlyAccess(BasePermission):
    """
    Authors are registered users.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated or request.method in SAFE_METHODS:
            return True
        return False


    def object_owner(self, obj, user):
        if obj.author == user:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and self.object_owner(obj, request.user) == True or request.method in SAFE_METHODS:
            return True
        return False



class AnonymousUserAccessException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'For accessing returned and drafted articles of other users, you must be admin; for accessing yours, please login.'
    default_code = 'error'

class UnkonwnStatusFilteringParameterException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Filter parameter doesn\'t exists.'
    default_code = 'error'
