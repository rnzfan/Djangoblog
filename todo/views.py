from django.shortcuts import render
from django.http import HttpResponseRedirect 
from .models import ToDoListItem
from django.contrib.auth.decorators import login_required

@login_required
def todoView(request):
    all_todo_items = ToDoListItem.objects.all()
    return render(request, 'todo/todolist.html', {'all_items': all_todo_items, 'title': 'To Do List'})

@login_required
def addToDoView(request):
    item = request.POST['content']
    new_item = ToDoListItem(content = item, creator = request.user)
    new_item.save()
    return HttpResponseRedirect('/todo/')

@login_required
def doneToDoView(request, pk):
    doneitem = ToDoListItem.objects.get(id=pk)
    doneitem.delete()
    return HttpResponseRedirect('/todo/')