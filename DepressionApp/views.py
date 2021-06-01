from django.shortcuts import render
from .Responses import motivationPost

# Create your views here.
from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import datetime
import joblib
import PIL.Image
import pytesseract
import matplotlib.pyplot as plt
import re
import numpy as np
import speech_recognition as sr

# Create your views here.


allUsers = []

svm_classifier = joblib.load("svmClassifier.pkl")


def index(request):
    if request.method == "GET":
        return render(request, "index.html", {})


def UploadPost(request):
    if request.method == "GET":
        return render(request, "UploadPost.html", {})


def Register(request):
    if request.method == "GET":
        return render(request, "Register.html", {})


def Admin(request):
    if request.method == "GET":
        return render(request, "Admin.html", {})


def Login(request):
    if request.method == "GET":
        return render(request, "Login.html", {})


def Logout(request):
    if request.method == "GET":
        return render(request, "Logout.html", {})


def SendMotivatedPost(request):
    if request.method == "GET":
        return render(request, "SendMotivatedPost.html", {})


def predict(textdata, classifier):
    text_processed = textdata
    X = [text_processed]
    sentiment = classifier.predict(X)
    return sentiment[0]


def predictSentiment(textdata):
    result = predict(textdata, svm_classifier)
    predicts = ""
    if result == 0:
        predicts = "Negative"
    if result == 1:
        predicts = "Positive"
    return predicts


def SendMotivatedPostData(request):
    result = motivationPost()
    if request.method == "POST":
        username = request.POST.get("t1", False)
        time = request.POST.get("t2", False)
        quote = result["quote"]
        book = result["book"]
        song = result["song"]
        db_connection = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="depression",
            charset="utf8",
        )
        db_cursor = db_connection.cursor()
        student_sql_query = (
            "update postdata set motivate_post='Not Pending', quote =\""
            + quote
            + '", song = "'
            + song
            + '", book = "'
            + book
            + '"where username= "'
            + username
            + '" and post_time="'
            + time
            + "\" and motivate_post='Pending'"
        )
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        context = {"data": "Your motivated text sent to user " + username}
        return render(request, "SendMotivatedPost.html", context)


def UploadPostData(request):
    if request.method == "POST" and request.FILES["t1"]:
        output = ""
        myfile = request.FILES["t1"]
        fs = FileSystemStorage()
        name = str(myfile)
        # if name.lower().endswith(('.txt')):
        # name = 'text.txt'
        # elif name.lower().endswith(('.png', '.jpg', '.jpeg', 'gif')):
        # name = 'img.jpg'
        filename = fs.save(name, myfile)
        if name.lower().endswith((".txt")):
            with open(name, "r") as file:
                for line in file:
                    line = line.strip("\n")
                    output += line + " "
        elif name.lower().endswith((".png", ".jpg", ".jpeg", "gif", "jfif")):
            output = pytesseract.image_to_string(PIL.Image.open(name))
            output = output.replace("\n", " ")
        elif name.lower().endswith((".wav")):
            r = sr.Recognizer()
            with sr.WavFile(name) as source:
                audio = r.record(source)
        try:
            output = r.recognize_google(audio)
        except:
            pass
        user = ""
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip("\n")
        now = datetime.datetime.now()
        option = "Pending"
        output = re.sub("\W+", " ", output)
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        sentiment = predictSentiment(output.lower())
        db_connection = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="depression",
            charset="utf8",
        )
        db_cursor = db_connection.cursor()
        student_sql_query = (
            "INSERT INTO postdata(username,post_data,post_time,depression,motivate_post) VALUES('"
            + user
            + "','"
            + output
            + "','"
            + current_time
            + "','"
            + sentiment
            + "','"
            + option
            + "')"
        )
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            context = {"data": "Detected Depression From Uploaded File : " + sentiment}
            return render(request, "UploadPost.html", context)
        else:
            context = {"data": "Error in signup process"}
            return render(request, "UploadPost.html", context)


def ViewUsers(request):
    if request.method == "GET":
        strdata = "<table border=1 align=center width=100%><tr><th>Username</th><th>Password</th><th>Contact No</th><th>Email ID</th><th>Address</th></tr><tr>"
        con = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="depression",
            charset="utf8",
        )
        with con:
            cur = con.cursor()
            cur.execute("select * FROM users")
            rows = cur.fetchall()
            for row in rows:
                sampleDict = {}
                strdata += (
                    "<td>"
                    + row[0]
                    + "</td><td>"
                    + row[1]
                    + "</td><td>"
                    + row[2]
                    + "</td><td>"
                    + str(row[3])
                    + "</td><td>"
                    + str(row[4])
                    + "</td></tr>"
                )
                sampleDict["user"] = str(row[0])
                sampleDict["contact_no"] = str(row[2])
                sampleDict["email_id"] = str(row[3])
                sampleDict["Address"] = str(row[4])
                allUsers.append(sampleDict)
    context = {"data": strdata, "allUsers": allUsers}
    return render(request, "ViewUsers.html", context)


def ViewPosts(request):
    if request.method == "GET":
        positive = 0
        negative = 0
        strdata = "<table border=1 align=center width=100%><col style=width:10%><col style=width:30%><col style=width:10%><col style=width:10%><col style=width:40%><tr><th>Username</th><th>Post Data</th><th>Post Time</th><th>Depression</th><th>Motivated Post</th></tr><tr>"
        con = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="depression",
            charset="utf8",
        )
        with con:
            cur = con.cursor()
            cur.execute("select * FROM postdata")
            rows = cur.fetchall()
            for row in rows:
                if row[3] == "Negative":
                    negative = negative + 1
                else:
                    positive = positive + 1
                strdata += (
                    "<td>"
                    + row[0]
                    + "</td><td>"
                    + row[1]
                    + "</td><td>"
                    + str(row[2])
                    + "</td><td>"
                    + str(row[3])
                    + "</td><td>"
                )
                if row[4] == "Pending":
                    strdata += str(row[4])
                else:
                    strdata += (
                        '<article class="media content-section">'
                        + '<div class="media-body">'
                        + "<fieldset>"
                        + "<legend><u>Quote:</u></legend>"
                        + "<label><b>"
                        + row[5]
                        + "</b></label>"
                        + "</fieldset>  <br>"
                        + '<div class="article-metadata">'
                        + "<p><u> Listen to this wonder Track : </u></p>"
                        + "<h2 class = mr-2>"
                        + row[6]
                        + "</h2> <br>"
                        + "</div>"
                        + '<div class="article-metadata">'
                        + "<p><u> Read this Book : </u></p>"
                        + "<h2 class = mr-2>"
                        + row[7]
                        + "</h2>"
                        + "</div>"
                        + "</div>"
                        + "</article>"
                    )
                strdata += "</td></tr>"
                # article = {"quote": row[5], "song": row[6], "book": row[7]}
    height = [positive, negative]
    bars = ("Non Depression Posts", "Depression Post")
    y_pos = np.arange(len(bars))
    # plt.bar(y_pos, height)
    # plt.xticks(y_pos, bars)
    # plt.show()
    context = {"data": strdata}
    return render(request, "ViewPosts.html", context)


def BlogPosts(request):
    allPosts = []
    con = pymysql.connect(
        host="127.0.0.1",
        port=3308,
        user="root",
        password="root",
        database="depression",
        charset="utf8",
    )
    with con:
        cur = con.cursor()
        cur.execute("select * FROM postdata")
        rows = cur.fetchall()

        for row in rows:
            sampleDict = {}
            sampleDict["username"] = str(row[0])
            sampleDict["post_data"] = str(row[1])
            sampleDict["post_time"] = str(row[2])
            sampleDict["depression"] = str(row[3])
            sampleDict["motivated_post"] = str(row[4])
            allPosts.append(sampleDict)
            allPosts = allPosts[::-1]
    context = {"posts": allPosts}
    return render(request, "BlogPosts.html", context)


def MotivatedText(request):
    if request.method == "GET":
        user = ""
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip("\n")
        strdata = "<table border=1 align=center width=100%><col style=width:10%><col style=width:30%><col style=width:10%><col style=width:10%><col style=width:40%><tr><th>Username</th><th>Post Data</th><th>Post Time</th><th>Depression</th><th>Motivated Post</th></tr><tr>"
        con = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="depression",
            charset="utf8",
        )
        with con:
            cur = con.cursor()
            cur.execute("select * FROM postdata")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == user:
                    strdata += (
                        "<td>"
                        + row[0]
                        + "</td><td>"
                        + row[1]
                        + "</td><td>"
                        + str(row[2])
                        + "</td><td>"
                        + str(row[3])
                        + "</td><td>"
                    )
                    if row[4] == "Pending":
                        strdata += str(row[4])
                    else:
                        strdata += (
                            '<article class="media content-section">'
                            + '<div class="media-body">'
                            + "<fieldset>"
                            + "<legend><u>Quote:</u></legend>"
                            + "<label><b>"
                            + row[5]
                            + "</b></label>"
                            + "</fieldset>  <br>"
                            + '<div class="article-metadata">'
                            + "<p><u> Listen to this wonder Track : </u></p>"
                            + "<h2 class = mr-2>"
                            + row[6]
                            + "</h2> <br>"
                            + "</div>"
                            + '<div class="article-metadata">'
                            + "<p><u> Read this Book : </u></p>"
                            + "<h2 class = mr-2>"
                            + row[7]
                            + "</h2>"
                            + "</div>"
                            + "</div>"
                            + "</article>"
                        )
                    strdata += "</td></tr>"
                # article = {"quote": row[5], "song": row[6], "book": row[7]}
    context = {"data": strdata}
    return render(request, "MotivatedText.html", context)


def ViewMotivatedPost(request):
    if request.method == "GET":
        strdata = "<table border=1 align=center width=100%><col style=width:10%><col style=width:30%><col style=width:10%><col style=width:10%><col style=width:40%><tr><th>Username</th><th>Post Data</th><th>Post Time</th><th>Depression</th><th>Motivated Post</th></tr><tr>"
        con = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="depression",
            charset="utf8",
        )
        with con:
            cur = con.cursor()
            cur.execute("select * FROM postdata")
            rows = cur.fetchall()
            for row in rows:
                strdata += (
                    "<td>"
                    + row[0]
                    + "</td><td>"
                    + row[1]
                    + "</td><td>"
                    + str(row[2])
                    + "</td><td>"
                    + str(row[3])
                    + "</td><td>"
                )
                if row[4] == "Pending":
                    strdata += str(row[4])
                else:
                    strdata += (
                        '<article class="media content-section">'
                        + '<div class="media-body">'
                        + "<fieldset>"
                        + "<legend><u>Quote:</u></legend>"
                        + "<label><b>"
                        + row[5]
                        + "</b></label>"
                        + "</fieldset>  <br>"
                        + '<div class="article-metadata">'
                        + "<p><u> Listen to this wonder Track : </u></p>"
                        + "<h2 class = mr-2>"
                        + row[6]
                        + "</h2> <br>"
                        + "</div>"
                        + '<div class="article-metadata">'
                        + "<p><u> Read this Book : </u></p>"
                        + "<h2 class = mr-2>"
                        + row[7]
                        + "</h2>"
                        + "</div>"
                        + "</div>"
                        + "</article>"
                    )
                strdata += "</td></tr>"
                # article = {"quote": row[5], "song": row[6], "book": row[7]}
    context = {"data": strdata}
    return render(request, "ViewMotivatedPost.html", context)


def SearchFriends(request):
    if request.method == "GET":
        user = ""
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip("\n")
        strdata = "<table border=1 align=center width=100%><tr><th>Username</th><th>Contact No</th><th>Email ID</th><th>Address</th></tr><tr>"
        con = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="depression",
            charset="utf8",
        )
        with con:
            cur = con.cursor()
            cur.execute("select * FROM users")
            rows = cur.fetchall()
            for row in rows:
                if row[0] != user:
                    strdata += (
                        "<td>"
                        + row[0]
                        + "</td><td>"
                        + row[2]
                        + "</td><td>"
                        + row[3]
                        + "</td><td>"
                        + str(row[4])
                        + "</td></tr>"
                    )

    context = {"data": strdata}
    return render(request, "SearchFriends.html", context)


def UserLogin(request):
    if request.method == "POST":
        username = request.POST.get("t1", False)
        password = request.POST.get("t2", False)
        index = 0
        con = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="depression",
            charset="utf8",
        )
        with con:
            cur = con.cursor()
            cur.execute("select * FROM users")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and password == row[1]:
                    index = 1
                    break
        if index == 1:
            file = open("session.txt", "w")
            file.write(username)
            file.close()
            context = {"data": "welcome " + username}
            return render(request, "UserScreen.html", context)
        else:
            context = {"data": "login failed"}
            return render(request, "Login.html", context)


def Signup(request):
    if request.method == "POST":
        username = request.POST.get("t1", False)
        password = request.POST.get("t2", False)
        contact = request.POST.get("t3", False)
        email = request.POST.get("t4", False)
        address = request.POST.get("t5", False)
        db_connection = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="depression",
            charset="utf8",
        )
        db_cursor = db_connection.cursor()
        student_sql_query = (
            "INSERT INTO users(username,password,contact_no,email,address) VALUES('"
            + username
            + "','"
            + password
            + "','"
            + contact
            + "','"
            + email
            + "','"
            + address
            + "')"
        )
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            context = {"data": "Signup Process Completed"}
            return render(request, "Register.html", context)
        else:
            context = {"data": "Error in signup process"}
            return render(request, "Register.html", context)


def AdminLogin(request):
    if request.method == "POST":
        username = request.POST.get("t1", False)
        password = request.POST.get("t2", False)
        if username == "admin" and password == "admin":
            context = {"data": "welcome " + username}
            return render(request, "AdminScreen.html", context)
        else:
            context = {"data": "login failed"}
            return render(request, "Admin.html", context)
