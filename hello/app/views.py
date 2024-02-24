from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse

# def fieUpload(request):

    
#     fileObj = request.FILES['filePath']
#     print(fileObj)
#     fs = FileSystemStorage()
#     filePathName = fs.save(fileObj.name,fileObj)
#     filePathName= fs.url(filePathName)
#     filePath = '.' +filePathName
#     print(filePath)
#     return JsonResponse({'file':filePath})
from django.views.decorators.csrf import csrf_exempt
import os
import tempfile
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .resume import extract_text_from_pdf, nlp
from .serializers import ParsedResumeSerializer
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

@csrf_exempt
@api_view(['POST'])
def parse_resume(request):
    if request.method == 'POST':
        resume_file = request.FILES.get('resume')
        

        # Validate uploaded file
        if not isinstance(resume_file, UploadedFile):
            return JsonResponse({'error': 'Invalid file format'}, status=400)
        
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in resume_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name
        
        try:
            resume_text = extract_text_from_pdf(temp_file_path)
            doc = nlp(resume_text)
            entities = [(ent.text, ent.label_) for ent in doc.ents]
        except Exception as e:
            # Handle parsing errors
            os.unlink(temp_file_path)  # Delete the temporary file
            return JsonResponse({'error': f'Error parsing resume: {str(e)}'}, status=500)

        os.unlink(temp_file_path)  # Delete the temporary file
        
        if entities:
            parsed_data = {'entities': entities}
            serializer = ParsedResumeSerializer(data=parsed_data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            else:
                return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({'error': 'No entities found'}, status=400)
