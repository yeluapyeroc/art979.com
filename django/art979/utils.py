## Callables for FileField upload_to variables
def image_path(instance, filename):
    return "user/%s/img/%s" % (instance.user.username, filename)

def audio_path(instance, filename):
    return "user/%s/audio/%s" % (instance.user.username, filename)

def video_path(instance, filename):
    return "user/%s/video/%s" % (instance.user.username, filename)

def doc_path(instance, filename):
    return "user/%s/doc/%s" % (instance.user.username, filename)
