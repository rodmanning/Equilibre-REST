from django.contrib.auth.models import User
from rest_framework import serializers
from transactions.models import Account, Balance, Category, Transaction


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category objects."""
    class Meta:
        model = Category
        fields = ("id", "name",)
        read_only_fields = fields


class AccountSerializer(serializers.ModelSerializer):
    """Serializer for Account objects."""
    icon = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = (
            "id",
            "name",
            "abbreviation",
            "icon",
        )
        read_only_fields = (
            "id",
            "name",
            "abbreviation",
            "icon",
        )


    def get_icon(self, obj):
        return obj.icon.url


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User objects."""
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
    """Serializer for Transaction objects."""
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    account = AccountSerializer(read_only=True)
    account_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    created_by = serializers.SerializerMethodField(read_only=True)
    updated_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Transaction
        fields = (
            "id",
            "user", "user_id",
            "account", "account_id",
            "date",
            "action", "amount",
            "category", "category_id",
            "description",
            "tax_deduction",
            "created", "created_by",
            "updated", "updated_by"
        )
        read_only_fields = (
            "user",
            "account",
            "created",
            "created_by",
            "updated",
            "updated_by"
        )

    def __init__(self, *args, **kwargs):
        """Override __init__ method to set custom validation messages."""
        super(TransactionSerializer, self).__init__(*args, **kwargs)
        self.fields["category_id"].error_messages["invalid"] = "You must select a category."
        self.fields["account_id"].error_messages["invalid"] = "You must select an account."
        self.fields["amount"].error_messages["invalid"] = "You must enter a valid amount."
        self.fields["action"].error_messages["invalid_choice"] = "Select an action."
        self.fields["date"].error_messages["invalid"] = "You must enter a valid date (try YYYY-MM-DD)."

    def get_created_by(self, obj):
        """Return the value for the `created_by` field."""
        return obj.created_by.username

    def get_updated_by(self, obj):
        """Return the value for the `updated_by` field."""
        return obj.created_by.username

    def _handle_related_fields(self, validated_data):
        """Handle fields for writable related objects.

        :account_id: The `pk` of the related account

        :category_id: The `pk` of the related category.

        :return: The `validated_data` object, with the values `account` and
                 `category` fields replaced by the applicable related objects.

        """
        validated_data["account"] = Account.objects.get(
            id=validated_data["account_id"])
        validated_data["category"] = Category.objects.get(
            id=validated_data["category_id"])
        validated_data["user"] = User.objects.get(id=1)

        return validated_data


    def create(self, validated_data):
        """Custom `create()` method to set the `created_by` value."""
        _data = self._handle_related_fields(validated_data)
        instance = Transaction(**_data)
        instance.created_by = self.context['request'].user
        instance.updated_by = self.context['request'].user
        instance.save()

        return instance


    def update(self, instance, validated_data):
        """Custom `update()` method to set the `updated_by` value."""

        _data = self._handle_related_fields(validated_data)
        for attr, val in _data.items():
            setattr(instance, attr, val)
        instance.updated_by = self.context['request'].user
        instance.save()

        return instance


class BalanceSerializer(serializers.ModelSerializer):
    """Read-only serializer for account Balance objects."""
    account = AccountSerializer(read_only=True)

    class Meta:
        model = Balance
        fields = "__all__"
