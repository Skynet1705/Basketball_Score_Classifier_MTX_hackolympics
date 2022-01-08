from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponsePermanentRedirect, JsonResponse
from .detections import detectVideo
from django.views.decorators.csrf import csrf_exempt
import base64
from xgboost import XGBClassifier
import numpy as np


# Create your views here.


def show_app_home(request):
    context = {}
    context['page_nav_title'] = 'MTX Hackolympics-2.0'
    context['page'] = 'MTX Hackolympics-2.0'
    return render(request, 'index.html', context)


def show_app_features(request):
    context = {}
    context['page_nav_title'] = 'MTX Hackolympics-2.0'
    context['page'] = 'MTX Hackolympics-2.0'
    return render(request, 'features.html', context)


def show_app_about(request):
    context = {}
    context['page_nav_title'] = 'MTX Hackolympics-2.0'
    context['page'] = 'MTX Hackolympics-2.0'
    return render(request, 'about.html', context)


@csrf_exempt
def classify_video(request):
    url = request.POST.get('video')
    fh = open("video.mp4", "wb")
    fh.write(base64.b64decode(url[21:]))
    fh.close()
    detections = detectVideo("video.mp4")
    print(str(detections))
    # print("CameBack"+str(detections))
    # detections = [[252, 2, 63, 62, 240, 5, 55, 65, 234, 3, 59, 63, 226, 2, 61, 63, 219, 5, 62, 65, 99999, 99999, 0, 0, 99999, 99999, 0, 0, 99999, 99999, 0, 0, 99999, 99999, 0, 0, 99999,
    #               99999, 0, 0, 181, 8, 72, 52, 99999, 99999, 0, 0, 99999, 99999, 0, 0, 99999, 99999, 0, 0, 99999, 99999, 0, 0, 99999, 99999, 0, 0, 99999, 99999, 0, 0, 99999, 99999, 0, 0, 99999, 99999, 0, 0, 99999, 99999, 0, 0, 99999, 99999, 0, 0, 99999, 99999, 0, 0, 99999, 99999, 0, 0, 99999, 99999, 0, 0, 99999, 99999, 0, 0, 99999, 99999, 0, 0, 1254, 157, 62, 27, 1245, 159, 58, 35, 1232, 160, 53, 40, 1224, 160, 58, 45, 1212, 162, 55, 54, 1205, 163, 56, 39, 1199, 166, 55, 40, 1187, 167, 55, 47, 1181, 168, 51, 39, 1173, 168, 53, 41, 1162, 171, 51, 47, 1157, 170, 51, 39, 1152, 171, 52, 39, 1150, 174, 48, 45, 1135, 175, 49, 49, 1132, 174, 49, 40, 1128, 175, 49, 40, 1124, 177, 50, 41, 1117, 179, 50, 45, 1109, 178, 52, 42, 1106, 180, 50, 41, 1102, 181, 48, 44, 1100, 184, 47, 41, 1099, 183, 49, 40, 1093, 185, 47, 46, 1086, 186, 48, 50, 1084, 185, 48, 41, 1083, 185, 48, 40, 1082, 187, 47, 40, 1079, 188, 47, 42, 1075, 187, 49, 43, 1076, 188, 49, 42, 1074, 190, 48, 42, 1070, 190, 48, 43, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0, -99999, -99999, 0, 0]]
    model = XGBClassifier()
    model.load_model('basketball/model/final_classifier.txt')
    scored = model.predict([detections])
    print(scored)
    # print("yeah")
    probab = model.predict_proba([detections])
    probab1 = 0.0
    # print("reached")
    if scored[0] == 0:
        probab1 = probab[0][0]
    else:
        probab1 = probab[0][1]
    score = 0
    # if scored[0] == 0:
    #     score = 0
    # else:
    #     score = 1
    print(probab1)
    # isLong = False
    # graph = [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]
    # prob = detectVideo(request.POST.get('video'))
    return JsonResponse({'success': True, 'msg': 'Hello', 'prob': str(probab1), 'isLong': False, 'scored': str(scored[0])})
