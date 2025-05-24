from rest_framework import serializers
from .models import Image

class QuestionSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=500)

class AnswerSerializer(serializers.Serializer):
    answer = serializers.CharField(max_length=500)

class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
    class Meta:
        model = Image
        fields = ['image', 'extracted_text']

    def create(self, validated_data):
        # Create and save an ImageText instance
        return Image.objects.create(
            image=validated_data['image'],
            extracted_text=validated_data.get('extracted_text', '')
        )