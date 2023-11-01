from .forms import UploadFormFile

ulopad_file_form_ = UploadFormFile()

def upload_file_form(request):
    context ={'upload_file_form': ulopad_file_form_}
    return context