from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['nickname', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        # Создаём пользователя, передавая дополнительные данные
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        instance.save()
        return instance