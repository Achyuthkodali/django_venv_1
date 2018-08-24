from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.http import QueryDict
import time
import datetime
import MySQLdb
import json
import ast


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
            'DOB': user.dob,
            'status': True
        }
        try:
            cursor.execute("update  users set last_login = '%s' where email = '%s'" % (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), email))
            db.commit()
            print ('hello')
        except Exception as err:
            print ('You got Error',err)

        return HttpResponse(json.dumps(data1))
    else:
        return HttpResponse(json.dumps({'status': False}))

@csrf_exempt

def check_register(request):
    user = users()
    data = json.loads(request.body)
    user.first_name = data['firstName']
    user.last_name = data['lastName']
    user.email = data['email']
    user.password = data['password']
    user.dob = data['dob']


    try:
        cursor.execute("insert into users(firstName,lastName,email,password,dob,csrftoken,signupTime,mobile) values('%s','%s','%s','%s','%s','%s','%s','%s')" % (user.first_name, user.last_name, user.email, user.password, user.dob, user.csrf_token, user.signup_time, user.mobile))
        db.commit()
        return HttpResponse(json.dumps({'status': True}))
    except Exception as err:
        print ('you got error', err)
        return HttpResponse(json.dumps({'status': False,'error': err}))
