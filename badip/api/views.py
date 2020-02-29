from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from api.models import Ip_list, User_code


def index(request):
    input_code = request.GET.get('code', False)  # Входящий код  на проверку
    input_ip = request.GET.get('ip', False)  # Входящий Ip  на проверку
    documentation = 'doc.html'
    warning = f"""Error sending data, 
                        check out the API documentation at:<a href="{documentation}">HERE</a>
                        For all questions you can contact:
                         <b>@DoctorXR</b>"""
    if input_code == False or input_ip == False:
        return HttpResponse(warning)
    codes = User_code.objects.all()
    for code in codes:
        if input_code == code.code: #если код валидный
            if request.path.find(r"bad_ip") != -1:
                json = [{"ip": ip.ip, "type": ip.type} for ip in Ip_list.objects.filter(type=False)]
                print(json)
                return JsonResponse(json, safe=False)
            elif request.path.find(r"good_ip") != -1:
                json = [{"ip": ip.ip, "type": ip.type} for ip in Ip_list.objects.filter(type=True)]
                return JsonResponse(json, safe=False)
            elif request.path.find(r"all_ip") != -1:
                json = [{"ip": ip.ip, "type": ip.type} for ip in Ip_list.objects.filter()]
                return JsonResponse(json, safe=False)
            elif request.path.find(r"which_ip") != -1:
                for ip in Ip_list.objects.filter(type=False): # Возьмем плохие ip
                    if input_ip == ip.ip: # Если входящий плохой
                        return HttpResponse('False')
                        break
                else:
                    return HttpResponse('True')
            elif request.path.find(r"is_ip_bad") != -1:
                s = Ip_list(ip=input_ip, type=False)
                s.save()
                return HttpResponse('Your ip add in bad base')
            else:
                return HttpResponse(warning)
        else:
            pass
    else:
        return HttpResponse("доступ запрещен, неверный SecretKey")

