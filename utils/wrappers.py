from django.http import JsonResponse

def handle_data_check(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            code = e.args[0]
            if code == 1062:
                return JsonResponse({'status': 1})
            else:
                return JsonResponse({'status': -1})
    return wrapper