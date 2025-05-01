from rest_framework import serializers

class QuestionSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=500)

class AnswerSerializer(serializers.Serializer):
    answer = serializers.CharField(max_length=500)