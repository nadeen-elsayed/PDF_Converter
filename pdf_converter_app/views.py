

import os
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1" # For some reason, transformers decided to use .isin for a simple op, which is not supported on MPS

from django.core.files.storage import FileSystemStorage, default_storage
from django.conf import settings

from django.http import JsonResponse
from django.shortcuts import render

from django.http import HttpResponse

import fitz  # PyMuPDF
from markdownify import markdownify as md

CODE_TO_LANGUAGE = {
    'af': 'Afrikaans',
    'am': 'Amharic',
    'ar': 'Arabic',
    'as': 'Assamese',
    'az': 'Azerbaijani',
    'be': 'Belarusian',
    'bg': 'Bulgarian',
    'bn': 'Bengali',
    'br': 'Breton',
    'bs': 'Bosnian',
    'ca': 'Catalan',
    'cs': 'Czech',
    'cy': 'Welsh',
    'da': 'Danish',
    'de': 'German',
    'el': 'Greek',
    'en': 'English',
    'eo': 'Esperanto',
    'es': 'Spanish',
    'et': 'Estonian',
    'eu': 'Basque',
    'fa': 'Persian',
    'fi': 'Finnish',
    'fr': 'French',
    'fy': 'Western Frisian',
    'ga': 'Irish',
    'gd': 'Scottish Gaelic',
    'gl': 'Galician',
    'gu': 'Gujarati',
    'ha': 'Hausa',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'hr': 'Croatian',
    'hu': 'Hungarian',
    'hy': 'Armenian',
    'id': 'Indonesian',
    'is': 'Icelandic',
    'it': 'Italian',
    'ja': 'Japanese',
    'jv': 'Javanese',
    'ka': 'Georgian',
    'kk': 'Kazakh',
    'km': 'Khmer',
    'kn': 'Kannada',
    'ko': 'Korean',
    'ku': 'Kurdish',
    'ky': 'Kyrgyz',
    'la': 'Latin',
    'lo': 'Lao',
    'lt': 'Lithuanian',
    'lv': 'Latvian',
    'mg': 'Malagasy',
    'mk': 'Macedonian',
    'ml': 'Malayalam',
    'mn': 'Mongolian',
    'mr': 'Marathi',
    'ms': 'Malay',
    'my': 'Burmese',
    'ne': 'Nepali',
    'nl': 'Dutch',
    'no': 'Norwegian',
    'om': 'Oromo',
    'or': 'Oriya',
    'pa': 'Punjabi',
    'pl': 'Polish',
    'ps': 'Pashto',
    'pt': 'Portuguese',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sa': 'Sanskrit',
    'sd': 'Sindhi',
    'si': 'Sinhala',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'so': 'Somali',
    'sq': 'Albanian',
    'sr': 'Serbian',
    'su': 'Sundanese',
    'sv': 'Swedish',
    'sw': 'Swahili',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'tl': 'Tagalog',
    'tr': 'Turkish',
    'ug': 'Uyghur',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'uz': 'Uzbek',
    'vi': 'Vietnamese',
    'xh': 'Xhosa',
    'yi': 'Yiddish',
    'zh': 'Chinese',
}
def upload_pdf(request):
    if request.method == 'POST' and request.FILES.get('pdf'):
        pdf_file = request.FILES['pdf']
        selected_lang = request.POST.get('language', None)

        # Save the uploaded PDF to the media/input directory
        input_folder = os.path.join(settings.MEDIA_ROOT, 'input')
        fs = FileSystemStorage(location=input_folder)
        fname = fs.save(pdf_file.name, pdf_file)
        file_path = fs.path(fname)
 
        # Prepare the output Markdown filename
        fname_without_ext = os.path.splitext(os.path.basename(fname))[0]
        markdown_filename = f"{fname_without_ext}.md"
        output_folder = os.path.join(settings.MEDIA_ROOT, 'output')
        markdown_output_path = os.path.join(output_folder, markdown_filename)

       # Open the PDF file
        pdf_document = fitz.open(file_path)
        text_content = ""

        # Extract text from each page
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            text_content += page.get_text()
        
        # Convert the extracted text to Markdown
        markdown_content = md(text_content)
        

        # Return the file URL and markdown content as a JSON response
        return JsonResponse({
            'file_url': 'placeholder',
            'markdown_content': markdown_content,  # This will populate the text editor
            'language': None
        })

    return render(request, 'pdf_converter_app/upload.html', {'languages': CODE_TO_LANGUAGE})


def favicon(request):
    return HttpResponse(status=204)
