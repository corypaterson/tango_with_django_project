from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    #construct a dictionary to pass to the template engine as its context
    #Note the key bold message is the same as {{boldmessage}} in the template
    context_dict = {'boldmessage' : "Crunchy, creamy, cookie, candy, cupcake!"}
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    context_dict= {'aboutmessage' : "Hello, this is the...",
                   'name' : "Cory Paterson",
                   'tutorialmessage' : "This tutorial has been put together by ",
                   'catmessage' : "Here is a random picture of a cat"
                }
    return render(request, 'rango/about.html', context = context_dict)

