from django.http import HttpResponse
from django.shortcuts import get_object_or_404

def open_contract(request, document_id):
    # document = get_object_or_404(Document, id=document_id)
    file_path = f'/root/univer-bot/renisancebot/documents/{document_id}/contract.pdf'
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="contract.pdf"'
        return response
    
def open_info(request, document_id):
    # document = get_object_or_404(Document, id=document_id)
    file_path = f'/root/univer-bot/renisancebot/documents/{document_id}/info.pdf'
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="info.pdf"'
        return response

