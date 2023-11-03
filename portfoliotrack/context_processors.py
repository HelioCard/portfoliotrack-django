from django.utils import timezone

WEEK_DAYS = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]

def get_date(request):
    today = timezone.datetime.today().date()
    week_day = WEEK_DAYS[timezone.datetime.now().weekday()]
    
    context = {
        'weekday': week_day,
        'today': today,
    }
    return context