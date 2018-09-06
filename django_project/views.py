from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render,render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
import string
from random import *
from django.http import QueryDict
import time
from django.core.mail import send_mail
from django.test import Client
import base64
import datetime
import MySQLdb
import json
import ast
import traceback


class users:
    u_id = ''
    first_name = ''
    laat_name = ''
    email = ''
    password = ''
    dob = ''
    csrf_token = ''
    signup_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    last_login = ''
    mobile = ''


def sendmail1(subject, message, to_):
    from_ = settings.DEFAULT_FROM_EMAIL
    try:
        send_mail(subject, message, from_, to_, fail_silently=True, html_message = message)
        return True
    except:
        return False



#db config
db = MySQLdb.connect(host="localhost", user="achyuth", passwd="1234", db="django_project")
cursor = db.cursor()





@csrf_exempt
def check_login(request):
    user = users()

    data = json.loads(request.body)

    email = data['email']
    password = data['password']
    remember = data['remember']

    try:
        cursor.execute("select * from users where email = '%s' and password = '%s'" % (email,password))
    except Exception as err:
        print ('You got Error',err)
    data = cursor.fetchone()

    if data:
        user.u_id = data[0]
        user.first_name = data[1]
        user.last_name = data[2]
        user.email = data[3]
        user.password = data[4]
        user.dob = data[5]
        user.csrf_token = data[6]

        print ('inside if')
        data1 = {
            'id': user.u_id,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'email': user.email,
            'dob': user.dob,
            'status': True
        }
        try:
            cursor.execute("update users set last_login = '%s' where email = '%s'" % (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), email))
            db.commit()
            print ('hello')
        except Exception as err:
            print ('You got Error',err)

        return HttpResponse(json.dumps(data1))
    else:
        return HttpResponse(json.dumps({'status': False}))





@csrf_exempt
def check_register(request):

    #create object for user class
    user = users()

    #get data from the frontend server
    data = json.loads(request.body)

    #set all the recived data to class variables
    user.first_name = data['firstName']
    user.last_name = data['lastName']
    user.email = data['email']
    user.password = data['password']
    user.dob = data['dob']

    #check whether user already exists
    try:
        cursor.execute("select * from users where email = '%s'" % (user.email))
    except:
        print ('you got an exeption at email validation')

    data1 = cursor.fetchone()
    if data1:
        return HttpResponse(json.dumps({'status': False, 'error':'user already exists'}))
    else:
        min_char = 18
        max_char = 20
        allchar = string.ascii_letters + string.digits
        user.csrftoken = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
        subject = 'Please verify your email address for SMAC'
        message = 'Hello, You are asked for an account in SMAC. Please verify your account by clicking this link <a href="http://192.168.0.100:5000/user_activate/%s">Click Here</a>' % (user.csrftoken)
        sendmail1(subject, message, [user.email])
        try:
            cursor.execute("insert into users(firstName,lastName,email,password,dob,csrftoken,signupTime,mobile) values('%s','%s','%s','%s','%s','%s','%s','%s')" % (user.first_name, user.last_name, user.email, user.password, user.dob, user.csrftoken, user.signup_time, user.mobile))
            db.commit()
        except Exception as err:
            print ('you got database error', err)
            return HttpResponse(json.dumps({'status': False,'error': err}))
        return HttpResponse(json.dumps({'status': True}))




@csrf_exempt
def activate_user(request):
    user = users()
    data = json.loads(request.body)
    print (request.body)

    user.csrftoken = data['token']
    print (user.csrftoken)

    try:
        cursor.execute("select * from users where csrftoken = '%s'" % (user.csrftoken))
        print ('inside try block')
    except:
        print ("except block in first try")
        HttpResponse(json.loads({'status': 'error for token'}))
    data1 = cursor.fetchone()
    print (data1)
    if data1:
        print ('inside of if')
        try:
            cursor.execute("update users set csrftoken = '1' where id = '%s'" % (data[0]))
            print ('inside of try inside if')
        except:
            print ("except block in second try")
            HttpResponse(json.dumps({'status': 'update for registration failed'}))
    return HttpResponse(json.dumps({'status': 'user register sucsessfull'}))




@csrf_exempt
def edit_profile(request):
    user = users()
    data = json.loads(request.body)
    user.firstName = data['firstName']
    user.lastName = data['lastName']
    user.dob = data['dob']
    user.email = data['email']

    print (data)
    data1 = {
        'firstName': user.firstName,
        'lastName': user.lastName,
        'dob': user.dob,
        'email': user.email,
        'status': True
    }

    try:
        cursor.execute("update users set firstName = '%s', lastName = '%s', DOB = '%s' where email = '%s'" % (user.firstName, user.lastName, user.dob, user.email))
        db.commit()
        return HttpResponse(json.dumps(data1))
    except:
        return HttpResponse(json.dumps({'status': False, 'error': 'integrity error'}))






@csrf_exempt
def change_password(request):
    user = users()
    data = json.loads(request.body)
    newPassword = data['newPassword']
    confirmPassword = data['confirmPassword']
    oldPassword = data['oldPassword']
    id = data['id']
    if newPassword == confirmPassword:

        try:
            cursor.execute("select password from users where id = '%s'" % (id))
        except:
            return HttpResponse(json.dumps({'error': 'integrity error at old password retrival'}))

        results = cursor.fetchone()


        if oldPassword == results[0]:
            try:
                cursor.execute("update users set password = '%s' where id = '%s'" % (newPassword,id))
                db.commit()
            except:
                return HttpResponse(json.dumps({'status': False, 'error': 'integrity error at updation'}))
                sys.exit()
            return HttpResponse(json.dumps({'status': True}))
        else:
            return HttpResponse(json.dumps({'status': False, 'oldPasswordError': 'old password is not same'  }))

    else:
        return HttpResponse(json.dumps({'status' : False, 'confirmPasswordError': 'new password and confirm password not same'}))





@csrf_exempt
def upload_avatar(request):
    user = users()
    print ('hello')
    data = request.body
    print ('after data')
    avatar = request.FILES.get('avatar')
    print ('after avatar')
    print (type(avatar))
    id = request.POST.get('id')

    try:
        cursor.execute("update users set dp = '%s' where id = '%s'" % (avatar, id))
        db.commit()
        print ('inside try')
    except:
        traceback.print_exc()
        return HttpResponse(json.dumps({'status': False, 'error': 'integrity error at updation'}))

    return HttpResponse(json.dumps({'status': True}))






@csrf_exempt
def jaja(request):
    c = Client()
    response = c.post('/change_password/', json.loads("{'id': '7', 'oldPassword': 'some', 'newPassword': 'something'}"))
    return HttpResponse()





@csrf_exempt
def mail_test(request):
    subject = 'Hello World'
    from_email = 'achyuth.kodali@smactechlabs.com'
    to_ = ['achyuth.kodali97@gmail.com']
    message = 'hii this is also for testing'

    send_mail(subject, message, from_email, to_, fail_silently=True)
    return HttpResponse('<h1> Mail sent successfully... yeahhhhhhhh </h1>')
