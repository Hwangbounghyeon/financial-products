from django.shortcuts import render 
import openai
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

openai.api_key = settings.OPENAI_API_KEY

def get_completion(prompt): 
	query = openai.chat.completions.create( 
		model="gpt-3.5-turbo",
		messages=[
        	{'role':'user','content': prompt}
    	], 
	)
	response = query.choices[0].message.content
	return response 

@csrf_exempt
def chat(request): 
    if request.method == 'POST': 
        data = json.loads(request.body)
        prompt = data.get('message')
        prompt = str(prompt)
        response = get_completion(prompt)
        return JsonResponse({'response': response}) 
    return JsonResponse({'error': 'Invalid request'}, status=400)
