from django.shortcuts import render
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import secrets

from . import util

class CreateForm(forms.Form):
    title = forms.CharField(label='Entry Title', widget=forms.TextInput(attrs={'class': 'form-control col-md-8 col-lg-8','placeholder': 'Title of the page'}))
    content = forms.CharField(label='Textarea', widget=forms.Textarea(attrs={'class': 'form-control col-lg-8','rows': 10 ,'placeholder': 'Enter Description'}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    markdownner = Markdown()
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request,'encyclopedia/error.html', {
            'message': 'The requested page was not found.',
            'entryTitle': entry
        })
    else:
        return render(request,'encyclopedia/entry.html',{
            'entry': markdownner.convert(entryPage),
            'entryTitle': entry
        })
def search(request):
    value = request.GET.get('q','')
    if (util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse('entry', kwargs={'entry':value}))
    else:
        subStringEntries = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                subStringEntries.append(entry)
        return render(request, 'encyclopedia/index.html', {
            'entries': subStringEntries,
            'search': True,
            'value': value
        })
def create(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if (util.get_entry(title) is None or form.cleaned_data['edit'] is True):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('entry', kwargs={'entry': title}))
            else:
                return render(request,'encyclopedia/create.html',{
                    'form': form, 'existing': True, 'entry': title
                    })
        else:
                return render(request,'encyclopedia/create.html',{
                    'form' : form, 'existing': False
                    })
    else:
        return render(request,'encyclopedia/create.html',{
                    'form' : CreateForm(), 'existing': False
                    })
def edit(request, entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request,'encyclopedia/nopage.html',{
            'entryTitle': entry
        })
    else:
        form = CreateForm()
        form.fields['title'].initial = entry
        form.fields['title'].widget = forms.HiddenInput()
        form.fields['content'].initial = entryPage
        form.fields['edit'].initial = True
        return render(request,'encyclopedia/create.html',{
            'form': form,
            'edit': form.fields['edit'].initial,
            'entryTitle': form.fields['title'].initial
        })
def random(request):
    entries = util.list_entries()
    randomEntry = secrets.choice(entries)
    return HttpResponseRedirect(reverse('entry', kwargs={'entry': randomEntry}))
#  its test for develeopment after this line
# class Search(forms.Form):
#     item = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Search'}))
# markdowner = Markdown()
# def searchTwo(request):
#     entries = util.list_entries()
#     searched = []
#     if request.method == "POST":
#         form = Search(request.POST)
#         if form.is_valid():
#             item = form.cleaned_data["item"]
#             for i in entries:
#                 if item in entries:
#                     page = util.get_entry(item)
#                     page_converted = markdowner.convert(page)
                    
#                     context = {
#                         'page': page_converted,
#                         'entryTitle': item,
#                         'form': Search()
#                     }

#                     return render(request, "encyclopedia/entry.html", context)
#                 if item.lower() in i.lower(): 
#                     searched.append(i)
#                     context = {
#                         'entryTitle': searched, 
#                         'form': Search()
#                     }
#                 # written by Daniel
#                 # else:
#                 #     return render(request,"encyclopedia/error.html",{
#                 #         'message': "Search text is not found"
#                 #     })
#             # return of for loop
#             return render(request, "encyclopedia/search.html", context)

#         else:
#             # if its not valid
#             return render(request, "encyclopedia/index.html", {"form": form})
#     else:
#         # if method is GET
#         return render(request, "encyclopedia/nopage.html", {
#             "entries": util.list_entries(), "form":Search()
#         })