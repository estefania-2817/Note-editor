from django.http import HttpResponse
from django.shortcuts import redirect, render
import markdown2
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):      # i added
    if util.get_entry(title) is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    else:
        html_content = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })   
    
def search(request):     # i added
    query = request.GET.get('q')
    if query:
        entries = util.list_entries()
        exact_match = [entry for entry in entries if query.lower() == entry.lower()]
        matching_entries = [entry for entry in entries if query.lower() in entry.lower()]        
        if exact_match:
            entry_content = util.get_entry(exact_match[0])
            if entry_content:
                entry_content = markdown2.markdown(entry_content)
                return render(request, "encyclopedia/entry.html", {
                    "title": exact_match[0],
                    "content": entry_content
                })
        else:
            return render(request, "encyclopedia/search.html", {
                "query": query,
                "entries": matching_entries
            })
    else:
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "entries": []
        })

def randompage(request): 
    entries = util.list_entries()
    size_entries = len(entries)
    random_integer = random.randint(0, size_entries-1)
    entry_content = util.get_entry(entries[random_integer])
    entry_content = markdown2.markdown(entry_content)
    return render(request, "encyclopedia/entry.html", {
        "title": entries[random_integer],
        "content": entry_content
    })

    
def newPage(request):
    return render(request, "encyclopedia/newPage.html", {
    })

def saveEntry(request):
    entries = util.list_entries()
    if request.method == 'POST':
        input_title = request.POST.get('inputTitle')
        # input_content = request.POST.get('inputContent')
        input_content = request.POST.get('inputContent')


        exact_match = [entry for entry in entries if input_title.lower() == entry.lower()]
        if not exact_match:
            if input_title and input_content: 
                util.save_entry(input_title, input_content)
                title = input_title
                html_content = markdown2.markdown(util.get_entry(title))
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "content": html_content
                })   
            else:
                return HttpResponse("Both title and content are required.")
        else:
            return HttpResponse("ERROR: Entry with title already exists.")

    
    return render(request, 'encyclopedia/index.html')

def editButton(request):
    input_title = request.GET.get('inputTitle')
    entry = util.get_entry(input_title)
    readContent = entry
    return render(request, "encyclopedia/editPage.html", {
        "title": input_title,
        "editableContent": readContent 
    })

def saveEntry2(request):
    entries = util.list_entries()
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        exact_match = [entry for entry in entries if title.lower() == entry.lower()]
        if exact_match:
            existingContent = util.get_entry(title)
            if content == existingContent:
                return HttpResponse("Content has not been changed. Nothing new has been saved.")  
            else:
                util.save_entry(title, content)
                html_content = markdown2.markdown(util.get_entry(title))
                # return redirect('index')
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "content": html_content
                })   
        else:
            return HttpResponse("ERROR: Entry does not exist.")
    
    return render(request, 'encyclopedia/index.html')