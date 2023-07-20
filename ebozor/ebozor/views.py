from django.http import HttpResponse
from django.shortcuts import get_object_or_404

def open_contract(request, document_id):
    # document = get_object_or_404(Document, id=document_id)
    file_path = f'/root/univer-bot/renisancebot/documents/{document_id}/shartnoma.docx'
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/docx')
        response['Content-Disposition'] = 'inline; filename="shartnoma.docx"'
        return response

def open_info(request, document_id):
    # document = get_object_or_404(Document, id=document_id)
    file_path = f'/root/univer-bot/renisancebot/documents/{document_id}/info.docx'
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/docx')
        response['Content-Disposition'] = 'inline; filename="info.docx"'
        return response

def open_uchtomonli(request, document_id):
    # document = get_object_or_404(Document, id=document_id)
    file_path = f'/root/univer-bot/renisancebot/documents/{document_id}/uchshartnoma.doc'
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/doc')
        response['Content-Disposition'] = 'inline; filename="uchshartnoma.doc"'
        return response

