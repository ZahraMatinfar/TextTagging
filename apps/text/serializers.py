from rest_framework import serializers
from apps.text.models import Tag, Text
from django.utils.translation import gettext_lazy as _


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ('id', 'content', 'dataset')
        extra_kwargs = {
            "dataset": {"write_only": True},
        }


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ('user', )

    def validate(self, data):
        user = self.context['request'].user
        text = data.get('text')
        category = data.get('category')

        # Check if the text's dataset is accessible by the user
        if text.dataset not in user.datasets.all():
            raise serializers.ValidationError(_("You can only tag texts in your assigned datasets."))
        
        # Check for duplicate tags
        if user.tags.filter(text=text, category=category).exists():
            raise serializers.ValidationError(_("You have already tagged this text with this category."))
        
        return data