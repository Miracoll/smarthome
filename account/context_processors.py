
def config_objects(request):
    from .models import Config
    if not Config.objects.all().exists():
        Config.objects.create()
    return {'config': Config.objects.get(id=1)}