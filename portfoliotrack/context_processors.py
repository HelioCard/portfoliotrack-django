import datetime

WEEK_DAYS = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]

def get_date(request):
    today = datetime.date.today()
    week_day = WEEK_DAYS[datetime.datetime.now().weekday()]
    
    context = {
        'weekday': week_day,
        'today': today,
    }
    return context