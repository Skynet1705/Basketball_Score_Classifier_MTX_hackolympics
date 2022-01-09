from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponsePermanentRedirect, JsonResponse
from .detections import detectVideo
from django.views.decorators.csrf import csrf_exempt
import base64
from xgboost import XGBClassifier
import numpy as np
import matplotlib.pyplot as plt
import cv2


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
    video = cv2.VideoCapture("video.mp4")
    duration = video.get(cv2.CAP_PROP_FRAME_COUNT)
    detections = detectVideo("video.mp4")
    print(detections)
    if duration <= 60:
        model = XGBClassifier()
        model.load_model('basketball/model/final_classifier.txt')
        scored = model.predict([detections])
        print(scored)
        probab = model.predict_proba([detections])
        probab1 = 0.0
        if scored[0] == 0:
            probab1 = probab[0][0]
        else:
            probab1 = probab[0][1]
        print(probab1)
        return JsonResponse({'success': True, 'msg': 'Hello', 'prob': str(probab1), 'isLong': False, 'scored': str(scored[0])})
    else:
        model = XGBClassifier()
        model.load_model('basketball/model/final_classifier.txt')
        basket = detections[0:int(duration)*4]
        basketball = detections[int(duration)*4:]
        x = []
        y = []
        i = 0
        count = 0
        print(len(basket))
        while i <= (len(basket) - 240):
            sliding_window_basket = basket[i:i+240]
            sliding_window_basketball = basketball[i:i+240]
            row = []
            row.append(sliding_window_basket)
            row.append(sliding_window_basketball)
            print(row)
            probab = model.predict_proba(row)
            x.append(count)
            y.append(probab[0][1])
            count += 1
            i += 40
        fig = plt.plot(x, y)
        plt.xlabel("Time")
        plt.ylabel("probability Of score")
        plt.savefig('example.png')
        plt.show()
        return JsonResponse({'success': True, 'msg': 'Hello', 'prob': str(0.0), 'isLong': True, 'scored': str(1)})
