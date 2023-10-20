from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import timezone
from .models import ChatSchema
import openai


openAiKey= 'please add your Open Ai key'
openai.api_key = openAiKey

def askOpenAI(message):
    response = openai.Completion.create(
        model= 'text-davinci-003',
        prompt=message,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    answer = response.choices[0].text.strip()
    return answer

def chatbotAi(request):  
    user_chats = ChatSchema.objects.filter(user = request.user)
    if request.method =='POST':
        message = request.POST.get('message')
        res =askOpenAI(message)
        conversation = ChatSchema(user=request.user, message= message, response=res, timeOfMessage=timezone.now())
        conversation.save()
        return JsonResponse({'message':message,'response':res})
    
    return render(request,'chatbot.html', {'chats': user_chats}) 

def login(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('chatbot')
         
        else:
            err_msg= 'invalid username or password'
            return render(request,'chatbot.html',{'error_message':err_msg})
    else:

        return render(request,'login.html')
 

def logout(request):
    auth.logout(request)
    return redirect('login')


def newUser(request):
       
    if request.method =='POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            try:
                user =User.objects.create_user(username,email,password1)
                user.save()
                auth.login(request,user)
                return redirect('chatbot')
            except:
                error_msg = 'error while creating user'
                return render(request,'register.html', {'error_message': error_msg})
        
        else:
            mess= 'Passwords do not match'
            return render(request,'register.html',{'error_message': mess})
        
    return render(request,'register.html')