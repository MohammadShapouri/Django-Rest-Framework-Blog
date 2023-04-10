from urllib import request
from . import permissions
from blog.models import Article
from userAccount.models import UserAccount
from .serializers import ArticleSerializer, UserAccountSerializer
from django.views.generic import TemplateView
from rest_framework.viewsets import ModelViewSet
# from dj_rest_auth.registration.views import RegisterView
# from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.status import HTTP_204_NO_CONTENT
# from rest_framework.permissions import IsAuthenticated
# from django.core.exceptions import PermissionDenied
# from rest_framework.exceptions import APIException

# Create your views here.


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # permission_classes = [permissions.AuthorOnlyAccess] 
    filterset_fields = ['title', 'category', 'status', 'owner', 'owner__username']
    search_fields = ['title', 'owner__username', 'description']

    def get_queryset(self):
        queryset = None
        if self.request.user.is_superuser:
            queryset = Article.objects.all()
        else:
            status = self.request.query_params.get('status')
            owner = self.request.query_params.get('owner')
            owner__username = self.request.query_params.get('owner__username')
            if status == 'p' or status is None:
                queryset = Article.objects.filter(status='p')
            elif status in ['d', 'r']:
                    if self.request.user.is_authenticated:
                        if (owner == str(self.request.user.id) or owner == None) and (owner__username == self.request.user.username or owner__username == None):
                            queryset = Article.objects.filter(owner=self.request.user)
                        else:
                            raise permissions.AnonymousUserAccessException()
                    else:
                        raise permissions.AnonymousUserAccessException()
            else:
                # raise permissions.UnkonwnStatusFilteringParameterException(detail=f'{status} is not a valid parameter for status filter.')
                queryset = Article.objects.all()
        return queryset

    # def get_queryset(self):
    #     queryset = None
    #     if self.request.user.is_superuser:
    #         queryset = Article.objects.all()
    #     else:
    #         status = self.request.query_params.get('status')
    #         if status == 'p' or status is None:
    #             queryset = Article.objects.filter(status='p')
    #         elif status in ['d', 'r']:
    #             if self.request.user.is_authenticated:
    #                 queryset = Article.objects.filter(owner=self.request.user)
    #             else:
    #                 raise permissions.AnonymousUserAccessException()
    #         else:
    #             raise permissions.UnkonwnStatusFilteringParameterException(detail=f'{status} is not a valid parameter for status filter.')
    #     return queryset

# class ArticleList(ListCreateAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     permission_classes = [permissions.AuthorOnlyAccess]


# class ArticleDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     lookup_field = 'slug'
#     permission_classes = [permissions.AuthorOnlyAccess]




class UserViewSet(ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [permissions.AdminOnlyAccess]



# class UserAccountList(ListCreateAPIView):
#     queryset = UserAccount.objects.all()
#     serializer_class = UserAccountSerializer
#     permission_classes = [permissions.AdminOnlyAccess]


# class UserAccountDetail(RetrieveUpdateDestroyAPIView):
#     queryset = UserAccount.objects.all()
#     serializer_class = UserAccountSerializer
#     lookup_field = 'username'
#     permission_classes = [permissions.AdminOnlyAccess]





# class RevokeToken(APIView):
#     permission_classes = [IsAuthenticated]

#     def delete(self, request):
#         request.auth.delete()
#         return Response(status=HTTP_204_NO_CONTENT)


class AccountConfirmEmail(TemplateView):
    template_name = 'account_confirm_email.html'


# class CustomRegisterView(RegisterView):
#     serializer_class = CustomRegisterSerializer