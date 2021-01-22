from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
import json
from datetime import datetime
from django.contrib.auth.decorators import login_required

# importing Models
from .models import *
# Create your views here.

def index(request):
  return render (request, "progress/index.html")

def login_view(request):
  if request.method == "POST":
    # Attempt to sign user in
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    # Check if authentication successful
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "progress/login.html", {
            "message": "Invalid username and/or password."
        })
  else:
    return render(request, "progress/login.html")

def logout_view(request):
  logout(request)
  return HttpResponseRedirect(reverse("index"))

def register(request):
  if request.method == "POST":
      username = request.POST["username"]
      email = request.POST["email"]

      # Ensure password matches confirmation
      password = request.POST["password"]
      confirmation = request.POST["confirmation"]
      if password != confirmation:
          return render(request, "progress/register.html", {
              "message": "Passwords must match."
          })

      # Attempt to create new user
      try:
          user = User.objects.create_user(username, email, password)
          user.save()
      except IntegrityError:
          return render(request, "progress/register.html", {
              "message": "Username already taken."
          })
      login(request, user)
      return HttpResponseRedirect(reverse("index"))
  else:
      return render(request, "progress/register.html")

#  Started table drop stage saving function
@login_required
def startedNew_stage(request):
    if request.method == "PUT":
        # json.loads loading from javascript
        data = json.loads(request.body.decode('utf-8'))
        # print(f'data:', data)

        # slength is for started
        slength = int(data["slength"])
        # print(f'slength:', slength)

        modifiedDate = datetime.now()
        # print(modifiedDate)

        started_data = data["started"]
        # print(f'started_data:', started_data)

        # true/false value to delete/stay decision
        stfnew_value = data["stfnew_value"]
        # print(stfnew_value)

        # save started records to db
        started = Started(started=started_data, user = request.user, modifiedDate=modifiedDate, stfnew_value=stfnew_value)
        started.save()
        # to delete started old values
        Started.objects.filter(stfnew_value=False).delete()
        # print("deleted started values at new_stage")
         
        return JsonResponse({
            "started result": True
        },status=200)
    else:
        return index(request) 

#  Proceeding table drop stage saving function
@login_required
def proceedingNew_stage(request):
    if request.method == "PUT":
        # json.loads loading from javascript
        data = json.loads(request.body.decode('utf-8'))
        # print(f'data:', data)

        # plength is for proceeding
        plength = int(data["plength"])
        # print(f'plength:', plength)

        modifiedDate = datetime.now()
        # print(modifiedDate)

        proceeding_data = data["proceeding"]
        # print(f'proceeding_data:', proceeding_data)

        # true/false value to delete/stay decision
        ptfnew_value = data["ptfnew_value"]
        # print(ptfnew_value)

        # save proceeding records to db
        proceeding = Proceeding(proceeding=proceeding_data, user = request.user, modifiedDate=modifiedDate, ptfnew_value=ptfnew_value)
        proceeding.save()
        # to delete proceeding old values
        Proceeding.objects.filter(ptfnew_value=False).delete()
        # print("deleted proceeding values at new_stage")
         
        return JsonResponse({
            "proceeding result": True
        },status=200)
    else:
        return index(request) 

#  completed table drop stage saving function
@login_required
def completedNew_stage(request):
    if request.method == "PUT":
        # json.loads loading from javascript
        data = json.loads(request.body.decode('utf-8'))
        # print(f'data:', data)

        # colength is for completed
        colength = int(data["colength"])
        # print(f'colength:', colength)

        modifiedDate = datetime.now()
        # print(modifiedDate)

        # data of completed
        completed_data = data["completed"]
        # print(f'completed_data:', completed_data)

        # true/false value to delete/stay decision
        cotfnew_value = data["cotfnew_value"]
        # print(cotfnew_value)

        # save completed records to db
        completed = Completed(completed=completed_data, user = request.user, modifiedDate=modifiedDate, cotfnew_value=cotfnew_value)
        completed.save()
        # to delete completed old values
        Completed.objects.filter(cotfnew_value=False).delete()
        # print("deleted completed values at new_stage")
         
        return JsonResponse({
            "completed result": True
        },status=200)
    else:
        return index(request) 


#  cancelled table drop stage saving function
@login_required
def cancelledNew_stage(request):
    if request.method == "PUT":
        # json.loads loading from javascript
        data = json.loads(request.body.decode('utf-8'))
        # print(f'data:', data)

        # calength is for cancelled
        calength = int(data["calength"])
        # print(f'calength:', calength)

        modifiedDate = datetime.now()
        # print(modifiedDate)

        # data of cancelled
        cancelled_data = data["cancelled"]
        # print(f'cancelled_data:', cancelled_data)

        # true/false value to delete/stay decision
        catfnew_value = data["catfnew_value"]
        # print(catfnew_value)

        # save cancelled records to db
        cancelled = Cancelled(cancelled=cancelled_data, user = request.user, modifiedDate=modifiedDate, catfnew_value=catfnew_value)
        cancelled.save()
        # to delete cancelled old values
        Cancelled.objects.filter(catfnew_value=False).delete()
        # print("deleted cancelled values at new_stage")
         
        return JsonResponse({
            "cancelled result": True
        },status=200)
    else:
        return index(request) 
    

# loading datas from db
@login_required
def load_stage(request):
    # filtering started True values to make is False so they become old values
    filtered_true = Started.objects.all().filter(stfnew_value=True).values('stfnew_value')
    # print(f'filtered_true at load_stage:', filtered_true)
    # updating true values to False in started table
    filtered_true.update(stfnew_value=False)
    # filtering new started values
    filtered_false = Started.objects.all().filter(stfnew_value=False).values('stfnew_value')
    # print(f'filtered_false updated at load_stage:', filtered_false)


    # filtering proceeding True values to make is False so they become old values
    filtered_true = Proceeding.objects.all().filter(ptfnew_value=True).values('ptfnew_value')
    # print(f'filtered_true at load_stage:', filtered_true)
    # updating true values to False in proceeding table
    filtered_true.update(ptfnew_value=False)
    # filtering new proceeding values
    filtered_false = Proceeding.objects.all().filter(ptfnew_value=False).values('ptfnew_value')
    # print(f'filtered_false updated at load_stage:', filtered_false)

    # filtering completed True values to make is False so they become old values
    filtered_true = Completed.objects.all().filter(cotfnew_value=True).values('cotfnew_value')
    # print(f'filtered_true at load_stage:', filtered_true)
    # updating true values to False in completed table
    filtered_true.update(cotfnew_value=False)
    # filtering new completed values
    filtered_false = Completed.objects.all().filter(cotfnew_value=False).values('cotfnew_value')
    # print(f'filtered_false updated at load_stage:', filtered_false)

    # filtering cancelled True values to make is False so they become old values
    filtered_true = Cancelled.objects.all().filter(catfnew_value=True).values('catfnew_value')
    # print(f'filtered_true at load_stage:', filtered_true)
    # updating true values to False in cancelled table
    filtered_true.update(catfnew_value=False)
    # filtering new cancelled values
    filtered_false = Cancelled.objects.all().filter(catfnew_value=False).values('catfnew_value')
    # print(f'filtered_false updated at load_stage:', filtered_false)

    user = request.user.username
    started = Started.objects.all()
    proceeding = Proceeding.objects.all()
    completed = Completed.objects.all()
    cancelled = Cancelled.objects.all()
    return JsonResponse({
        "started" : [startedx.serialize(user) for startedx in started],
        "proceeding": [proceedingx.serialize(user) for proceedingx in proceeding],
        "completed": [completedx.serialize(user) for completedx in completed],
        "cancelled": [cancelledx.serialize(user) for cancelledx in cancelled]
    }, status=200)

@login_required
def new_item_save(request):
    if request.method == "PUT":
        # json.loads loading from javascript
        data = json.loads(request.body.decode('utf-8'))
        # print(f'data:', data)

        modifiedDate = datetime.now()
        # print(modifiedDate)

        # data of new Item that coming from JSs
        newItem_data = data["data"]
        # print(f'newItem_data:', newItem_data)


        # true/false value to delete/stay decision
        # written harccode

        # save new Item records to db
        # hardcoded

        itemcolumn = (int(data["column"]))
        if (itemcolumn == 0):
            # print("itemcolumn: 0")
            started = Started(started=newItem_data, user = request.user, modifiedDate=modifiedDate, stfnew_value=True)
            started.save()
            return load_stage(request)
        elif (itemcolumn == 1):
            # print("itemcolumn: 1")
            proceeding = Proceeding(proceeding=newItem_data, user = request.user, modifiedDate=modifiedDate, ptfnew_value=True)
            proceeding.save()
            return load_stage(request)
        elif (itemcolumn == 2):
            # print("itemcolumn: 2")
            completed = Completed(completed=newItem_data, user = request.user, modifiedDate=modifiedDate, cotfnew_value=True)
            completed.save()
            return load_stage(request)
        else:
            # print("itemcolumn: 3")
            cancelled = Cancelled(cancelled=newItem_data, user = request.user, modifiedDate=modifiedDate, catfnew_value=True)
            cancelled.save()
            return load_stage(request)      
    else:
        return index(request) 
    return load_stage(request)
