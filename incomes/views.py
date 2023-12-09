from django.shortcuts import render

# Create your views here.
def history(request):
    return render(request, 'incomes/history.html')

def get_incomes_history(request):
    pass