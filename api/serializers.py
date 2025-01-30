from rest_framework import serializers
from django.utils import timezone
import random
from scraper.models import News, Comment

class NewsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['title', 'url', 'author', 'text', 'type']
        read_only_fields = [
            'id', 'score', 'descendants', 'kids', 'is_posted', 
            'dead', 'deleted', 'date_created'
        ]

    def validate(self, data):
        """
        Validate 'type' and 'url' fields.
        """
        # Validate the 'type' field
        item_type = data.get('type', '')
        if item_type not in ['story', 'job']:
            raise serializers.ValidationError({"error": "Type must be either 'story' or 'job'"})

        # Validate the 'url' field
        url = data.get('url', '')
        if url and not url.startswith(('http://', 'https://')):
            raise serializers.ValidationError({"error": "URL must start with 'http://' or 'https://'"})

        return data

    def create(self, validated_data):
        """
        Add additional fields and create the object.
        """
        validated_data['is_posted'] = True
        validated_data['date_created'] = timezone.now()
        validated_data['score'] = random.randint(1, 100)  # Assign a random score
        return super().create(validated_data)

class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class NewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = [
            'item_id', 'deleted', 'dead', 'kids', 'descendants', 
            'is_posted', 'score', 'date_created'
        ]
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
