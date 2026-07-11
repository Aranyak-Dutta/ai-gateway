from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


#importing libraries/modules
import os
import time
from openai import OpenAI

#importing of models
from .models import RequestLog

#use OPENAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

#the features
from . import prompt_inj



@api_view(['POST'])
def call_it(request):
    messages = request.data.get('messages')

    is_sus = prompt_inj.check_prompt(messages)
    if is_sus:
        RequestLog.objects.create(
            request_body=messages,
            response_body=None,
            latency_ms=0,
            status="blocked"
        )
        return Response(
            {"error": f"Request blocked: potential prompt injection detected!."},
            status=400
        )
    start_time = time.time()
    try:
        #give it to open ai
        completion = client.chat.completions.create(
            model = 'gpt-4o',
            messages=messages
        )
        reply = completion.choices[0].message.content
        elapsed_ms = int((time.time() - start_time) * 1000)
            

        RequestLog.objects.create(
            request_body = messages,
            response_body = {'reply': reply},
            latency_ms = elapsed_ms,
            status = 'success!'
        )

        return Response({'reply': reply})
        
    except Exception as e:
        elapsed_ms = int((time.time() - start_time) * 1000)
        RequestLog.objects.create(
            request_body=messages,
            response_body=None,
            latency_ms=elapsed_ms,
            status="error"
        )

        return Response({'error': str(e)}, status = 500)