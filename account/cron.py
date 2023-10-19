from .models import Config, Test

def autoUpdate():
    config = Config.objects.get(id=1)
    # Check if config.acknowledge_request is false
    if not config.acknowledge_request:
        config.acknowledge_request = True       # Assign true to acknowledge_request
        config.save()
    elif config.acknowledge_request:
        config.connection_status = False
        config.save()

    # Test.objects.create(name='hiii')
    # print('hiiii')