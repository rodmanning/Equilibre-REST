from django.contrib.auth.models import User
from rest_framework import serializers
from transactions.models import Category, Account, Transaction


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category objects.

    """
    class Meta:
        model = Category
        fields = ("name",)
        read_only_fields = fields


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for Account objects.

    """

    icon = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = (
            "name",
            "abbreviation",
            "icon",
        )
        read_only_fields = (
            "name",
            "abbreviation",
            "icon",
        )


    def get_icon(self, obj):
        return obj.icon.path


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User objects.

    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
        )
        read_only_fields = (
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
        )



    def get_full_name(self, obj):
        return obj.get_full_name()


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Transaction objects.

    """

    user = UserSerializer()
    account = AccountSerializer()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = (
            "user",
            "account",
            "created",
            "created_by",
            "updated",
            "updated_by"
        )


    def get_created_by(self, obj):
        return obj.created_by.username


    def get_updated_by(self, obj):
        return obj.created_by.username


    def to_internal_value(self, data):
        data["user"] = User.objects.get(id=data["user"])

        data["account"] = Account.objects.get(
            id=data["account"])

        data["category"] = Category.objects.get(
            id=data["category"])

        return data


    def create(self, validated_data):
        """
        Custom `create()` method to set the `created_by` value.

        """
        #self.handle_writable_nested_fields(validated_data)
        instance = Transaction(**validated_data)
        instance.created_by = self.context['request'].user
        instance.updated_by = self.context['request'].user
        instance.save()

        return instance


    def update(self, instance, **validated_data):
        """
        Custom `update()` method to set the `updated_by` value

        """
        for key,val in validated_data.items():
            instance[key] = val
        instance.updated_by = self.request.user
        instance.save()

        return instance
