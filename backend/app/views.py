from django.views.decorators.csrf import csrf_exempt
import os
import tempfile
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .resume import extract_text_from_pdf, nlp
from .serializers import ParsedResumeSerializer
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from .models import Parse  # Import the Parse model

@csrf_exempt
@api_view(['POST','GET'])
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
            entities = [[ent.label_,ent.text] for ent in doc.ents]
        except Exception as e:
            # Handle parsing errors
            os.unlink(temp_file_path)  # Delete the temporary file
            return JsonResponse({'error': f'Error parsing resume: {str(e)}'}, status=500)

        os.unlink(temp_file_path)  # Delete the temporary file
        if entities:
    # Save extracted data to Parse model instance
    
            name = ""
            college_name = ""
            skills = ""
            companies = ""
            experience = ""
            certification = ""
            for entity in entities:
                  if entity[0] == 'Name':
                      name = entity[1]
                  elif entity[0] == 'College Name':
                      college_name = entity[1]
                  elif entity[0] == 'Skills':
                      skills = entity[1]
                  elif entity[0] == 'Companies worked at':
                      companies = entity[1]
                  elif entity[0] == 'Years of experience':
                      experience = entity[1]
                  elif entity[0] == 'Degree' or entity[0] == 'Certification':
                      certification = entity[1]
            print("Name:", name)
            print("College Name:", college_name)
            print("Skills:", skills)
            print("Years of experience:", experience)
            print("Companies worked at:", companies)
            print("Degree/Certification:", certification)
                                
                
            
        parse_instance = Parse.objects.create(name =name ,college_name=college_name,skills=skills, experience=experience, companies = companies, certification=certification, extracted_data=entities)
            
        return JsonResponse({'success': 'Data extracted and saved successfully', 'id': parse_instance.id})
            
    else:
        return JsonResponse({'error': 'No entities found'}, status=400)


@csrf_exempt
@api_view(['GET'])   
def get_parsed_data(request):
    if request.method == 'GET':
        # Retrieve all stored parsed data
        parsed_data = Parse.objects.all()
        data_list = [{'id': item.id, 'name': item.name, 'skills':item.skills, 'college_name':item.college_name, 'experience':item.experience, 'companies':item.companies, 'certification':item.certification,'extracted_data': item.extracted_data,} for item in parsed_data]
        print(data_list)
        return JsonResponse({'parsed_data': data_list})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
