from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import rag_app
from .serializers import QuestionSerializer, AnswerSerializer, ImageSerializer
from PIL import Image
import pytesseract

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

@api_view(['POST'])
def parse_image(request):
    serializer = ImageSerializer(data=request.data)

    if serializer.is_valid():
        image_file = serializer.validated_data['image']
        try:
            image = Image.open(image_file)
            extracted_text = pytesseract.image_to_string(image, lang='nep')
            instance = serializer.save(extracted_text=extracted_text)
            return Response({'extracted_text': extracted_text}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    else:
        return Response(serializer.errors, status=400)
    