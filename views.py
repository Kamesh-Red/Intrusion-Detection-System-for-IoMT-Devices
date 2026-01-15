from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


from django.shortcuts import render
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
global scaler








def HomePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('home')
@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')

def getPredictions(a,b,c,d,e,f,g,h,i,j):
    model = pickle.load(open('RF.pkl', 'rb'))
    new_data = {'Date':a,
            'Time':b,
            'Source IP Address':c,
            'Destination IP Address':d,
             'Source Port':e,
            'Destination Port':f,
            'Protocol':g,
            'Traffic Type':h,
            'Anomaly Scores':i,
            'Severity Level':j
           }
    new_df = pd.DataFrame([new_data])
    prediction = model.predict(new_df)
    return (prediction)


def result(request):
    if request.method == 'POST':
        a = request.POST.get('Date')
        b = request.POST.get('Time')
        c = request.POST.get('Source_IP')
        d = request.POST.get('Destination_IP')
        e = request.POST.get('Source_Port')
        f = request.POST.get('Destination_Port')
        g = request.POST.get('Protocol')
        h = request.POST.get('Traffic_Type')
        i = request.POST.get('Anomaly_Scores')
        j = request.POST.get('Severity_Level')
        
        result = getPredictions(a, b, c, d, e, f, g, h, i, j)
        
        return render(request, 'result.html', {'result': result[0]})
    else:
        return render(request, 'error.html', {'message': 'Invalid request method'})