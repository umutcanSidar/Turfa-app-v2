from home.models import Settings, ServiceModel

def get_setting_items(request):
    context = {}
    if "/candidate/" in request.get_full_path():
        context['setting_item'] = Settings.objects.filter(role=False).first()
    else:
        context['setting_item'] = Settings.objects.filter(role=True).first()

    return context

def get_service_items(request):
    context={}

    if "/candidate/" in request.get_full_path():
        context['service_items'] = ServiceModel.objects.filter(role=False)
    else:
        context['service_items'] = ServiceModel.objects.filter(role=True)

    return context