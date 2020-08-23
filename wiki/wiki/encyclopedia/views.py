from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2 as md
from . import util
from django import forms
from . import views
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request,title):
    entry = util.get_entry(title.capitalize())
    if(entry is not None):
        html = md.markdown(entry)
        return render(request,"encyclopedia/renderPage.html",{
            'content':html,
            'title':title.capitalize()
        })
    else:
        return render(request,'encyclopedia/errorPage.html')

def search(request):
    title = request.POST.get('q','')
    entries = [x.lower() for x in util.list_entries()]
    matches=[]
    if(title.lower() in entries):
        return HttpResponseRedirect(reverse('page',args=[title.capitalize()]))
    else:
        for entry in entries:    
            if(title in entry):
                matches.append(entry)
        return render(request,'encyclopedia/search.html',{
            'matches':matches
        })

class NewWikiForm(forms.Form):
    title = forms.CharField(label='Title')
    desc = forms.CharField(widget=forms.Textarea)

def newPage(request):
    if(request.method=='POST'):
        form = NewWikiForm(request.POST)
        if(form.is_valid()):
            title = form.cleaned_data['title']
            desc = form.cleaned_data['desc']
            if(title not in util.list_entries()):
                util.save_entry(title,desc)
                return HttpResponseRedirect(reverse('page',args=[title.capitalize()]))
            else:
                return render(request,'encyclopedia/newPage.html',{'form':form,'valid':False})
        else:
            return render(request,'encyclopedia/newPage.html',{'form':form,'valid':True})
    
    return render(request,'encyclopedia/newPage.html',{
        'form':NewWikiForm(),'valid':True
    })

def edit(request,title):
    if(request.method=='POST'):
        form=NewWikiForm(request.POST)
        if(form.is_valid()):
            title=form.cleaned_data['title'] 
            desc = form.cleaned_data['desc']
            util.save_entry(title,desc)
            return HttpResponseRedirect(reverse('page',args=[title.capitalize()]))

    data = {'title':title,'desc':util.get_entry(title)}
    form=NewWikiForm(data)
    return render(request,'encyclopedia/editPage.html',{
        'form':form
    })

def randomPage(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    return HttpResponseRedirect(reverse('page',args=[entry.capitalize()]))
    
    
    