from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator


#um, this is to make the models run simultaneously
import concurrent.futures


#importing libraries/modules
import os
import time
from openai import OpenAI

#importing of models
from .models import RequestLog, APIKey

#use OPENAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

#the features
from . import prompt_inj, output_scan, jailbreak_scan




@api_view(['POST'])
@ratelimit(key = 'ip', rate = '10/m', block = False)
def chat_gateway(request):

    '''
    Auth Check first
    '''
    provided_key = request.headers.get('X-API-Key')
    if not provided_key or not APIKey.objects.filter(key=provided_key, is_active=True).exists():
        return Response({"error": "Invalid or missing API key."}, status=401)



    '''
    Rate limited to 10 request per sec
    '''
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        RequestLog.objects.create(
            request_body=request.data.get('messages'),
            response_body=None,
            latency_ms=0,
            status="rate_limited"
        )
        return Response(
            {"error": "Rate limit exceeded. Try again shortly."},
            status=429
    )
    messages = request.data.get('messages')


    '''
    Check for prompt injection and jailbreak
    '''

    def run_input_scans(messages):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            injection_future = executor.submit(prompt_inj.check_prompt, messages)
            jailbreak_future = executor.submit(jailbreak_scan.check_jailbreak, messages)

            is_suspicious = injection_future.result()
            is_jailbreak = jailbreak_future.result()
            return is_suspicious, is_jailbreak

    is_sus, is_jailbreak = run_input_scans(messages)


    
    is_sus = prompt_inj.check_prompt(messages)
    is_jailbreak= jailbreak_scan.check_jailbreak(messages)

    if is_sus or is_jailbreak:
        RequestLog.objects.create(
            request_body=messages,
            response_body=None,
            latency_ms=0,
            status="blocked"
        )
        return Response(
            {"error": "Request blocked: potential prompt injection or jailbreak attempt detected."},
            status=400
        )
    

    '''
    Transferring the prompt to openAi
    '''
    start_time = time.time()
    try:
        #give it to open ai
        completion = client.chat.completions.create(
            model = 'gpt-4o',
            messages=messages
        )

        reply = completion.choices[0].message.content
        elapsed_ms = int((time.time() - start_time) * 1000)

        '''
        Scanning the output
        '''


        is_unsafe = output_scan.check_output(reply)
        if is_unsafe:
            RequestLog.objects.create(
                request_body=messages,
                response_body={"reply": reply},
                latency_ms=elapsed_ms,
                status="output_blocked"
            )
            return Response(
                {"error": "Response withheld: flagged content in AI output."},
                status=502
            )

    
        RequestLog.objects.create(
            request_body=messages,
            response_body={"reply": reply},
            latency_ms=elapsed_ms,
            status="success"
        )
        return Response({"reply": reply})
        

        
    except Exception as e:
        elapsed_ms = int((time.time() - start_time) * 1000)
        RequestLog.objects.create(
            request_body=messages,
            response_body=None,
            latency_ms=elapsed_ms,
            status="error"
        )

        return Response({'error': str(e)}, status = 500)