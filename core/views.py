from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import rag_app
from .serializers import QuestionSerializer, AnswerSerializer

@api_view(["POST"])
def get_answer(request):
    # Validate the request data using the serializer
    question_serializer = QuestionSerializer(data=request.data)
    if question_serializer.is_valid():
        question = question_serializer.validated_data["question"]
        relevant_chunks = rag_app.query_documents(question)
        answer = rag_app.generate_response(question, relevant_chunks)
        
        # Serialize the response
        answer_serializer = AnswerSerializer({"answer": answer})
        return Response(answer_serializer.data, status=201)
    else:
        return Response(question_serializer.errors, status=400)