from .forms import UploadFormFile, RegisterTransactionForm

ulopad_file_form_ = UploadFormFile()
register_transaction_form_ = RegisterTransactionForm()

def portfolio_context(request):
    context ={
        'upload_file_form': ulopad_file_form_,
        'register_transaction_form': register_transaction_form_,
    }
    return context
