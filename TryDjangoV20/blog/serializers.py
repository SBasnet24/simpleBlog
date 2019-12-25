from rest_framework.serializers import (ModelSerializer, HyperlinkedIdentityField, SerializerMethodField)

from .models import UserBlog


class UserBlogListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='blogapp:blog_api_detail',
        lookup_field='pk'
    )
    user = SerializerMethodField()

    class Meta:
        model = UserBlog
        fields = ['title',
                  'user',
                  'url',
                  ]


    def get_user(self, obj):
        return str(obj.user.username)


class UserBlogDetailSerializer(ModelSerializer):
    user = SerializerMethodField()
    image = SerializerMethodField()

    class Meta:
        model = UserBlog
        fields = "__all__"

    def get_user(self, obj):
        return str(obj.user.username)

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image
