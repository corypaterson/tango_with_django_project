from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm

# Create your views here.
def index(request):

    #Query the database for a list of ALL categories currently stored
    #Order the categories by no. likes in descending order
    #Retrieved the top 5 only - or all if less than 5
    #Place the list in the context_dict dictionary, which is then passed to the template engine
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    #construct a dictionary to pass to the template engine as its context
    #Note the key bold message is the same as {{boldmessage}} in the template
    context_dict = {'categories' : category_list, 'pages': page_list}
    
    return render(request, 'rango/index.html', context=context_dict)



def about(request):
    context_dict= {'aboutmessage' : "Hello, this is the...",
                   'name' : "Cory Paterson",
                   'tutorialmessage' : "This tutorial has been put together by ",
                   'catmessage' : "Here is a random picture of a cat"
                }
    return render(request, 'rango/about.html', context = context_dict)

def  show_category(request, category_name_slug):

    context_dict = {}

    try:
        #Can we find a category name slug with the given name?
        #If not, the get() method raises a do not exist exception
        #So the get() method returns one model instance or raises an execption
        category =  Category.objects.get(slug=category_name_slug)

        #retirieve all the associated pages
        #Note that the filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category=category)

        #adds our results list to the template context under name pages
        context_dict['pages'] = pages

        #we also add the category to the object from the database to the context dictionary
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                # probably better to use a redirect here.
            return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form':form, 'category': category}

    return render(request, 'rango/add_page.html', context_dict)

