from django.shortcuts import render, get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskSerializer
from .models import Task

@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def tasks(request):
    """
    List all tasks or create a new task.
    """
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
@parser_classes([JSONParser])
def task_detail(request, pk):
    """
    Retrieve, update, or delete a task by id.
    """
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
