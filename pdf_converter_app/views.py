from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
from convert_single import convert_single_pdf
import time
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import pypdfium2 # Needs to be at the top to avoid warnings
import os
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1" # For some reason, transformers decided to use .isin for a simple op, which is not supported on MPS

import argparse
from marker.convert import convert_single_pdf
from marker.logger import configure_logging
from marker.models import load_all_models

from marker.output import save_markdown
import os
from django.core.files.storage import FileSystemStorage, default_storage
from django.conf import settings


import os
import json
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
configure_logging()

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import JsonResponse
import os
from convert_single import convert_single_pdf
from marker.convert import convert_single_pdf
from marker.logger import configure_logging
from marker.models import load_all_models
from marker.output import save_markdown

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import JsonResponse
import os
from convert_single import convert_single_pdf
from marker.convert import convert_single_pdf
from marker.logger import configure_logging
from marker.models import load_all_models
from marker.output import save_markdown

configure_logging()

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import JsonResponse
import os
from convert_single import convert_single_pdf
from marker.convert import convert_single_pdf
from marker.logger import configure_logging
from marker.models import load_all_models
from marker.output import save_markdown

configure_logging()

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

        # Validate the selected language code
        if selected_lang and selected_lang not in CODE_TO_LANGUAGE:
            raise ValueError(f"Invalid language code {selected_lang} for Surya OCR")

        # Lookup the language name
        language_name = list({i for i in CODE_TO_LANGUAGE if CODE_TO_LANGUAGE[i]==selected_lang})
        #= CODE_TO_LANGUAGE.get(selected_lang, 'Unknown Language')

        # Save the uploaded PDF to the media/input directory
        input_folder = os.path.join(settings.MEDIA_ROOT, 'input')
        fs = FileSystemStorage(location=input_folder)
        fname = fs.save(pdf_file.name, pdf_file)
        file_path = fs.path(fname)

        # Load models and convert PDF to Markdown
        model_lst = load_all_models()
        full_text = convert_single_pdf(file_path, model_lst, max_pages=10, langs=language_name, batch_multiplier=2)

        # Prepare the output Markdown filename
        fname_without_ext = os.path.splitext(os.path.basename(fname))[0]
        markdown_filename = f"{fname_without_ext}.md"
        output_folder = os.path.join(settings.MEDIA_ROOT, 'output')
        markdown_output_path = os.path.join(output_folder, markdown_filename)

        # Save the converted Markdown content
        with open(markdown_output_path, 'w') as f:
            f.write(full_text)

        # Generate the URL for the user to download the file
        file_url = os.path.join(settings.MEDIA_URL, 'output', markdown_filename)

        # Return the file URL as a JSON response
        return JsonResponse({'file_url': file_url, 'language': language_name})

    return render(request, 'pdf_converter_app/upload.html', {'languages': CODE_TO_LANGUAGE})
