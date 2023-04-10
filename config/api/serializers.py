from rest_framework import serializers
from blog.models import Article
from userAccount.models import UserAccount
# from dj_rest_auth.registration.serializers import RegisterSerializer


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'slug', 'category', 'description', 'thumbnail', 'publish_date', 'creation_date', 'update_date', 'status']



class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['first_name', 'last_name', 'username', 'email', 'password']



# class CustomRegisterSerializer(RegisterSerializer):

#     def validate(self, data):
#         if data['password1'] != data['password2']:
#             raise serializers.ValidationError(("رمزها مشابه نیستند."))
#         return data
