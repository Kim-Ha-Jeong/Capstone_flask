ALLOWED_EXTENSIONS = set(['mp4', 'avi', 'mkv', 'flv', 'wmv', 'mov'])
def allowed_file(value):
    return '.' in value and value.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS