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

configure_logging()
def upload_pdf(request):
    if request.method == 'POST' and request.FILES['pdf']:
        pdf_file = request.FILES['pdf']
        fs = FileSystemStorage(location='input')
        fname = fs.save(pdf_file.name, pdf_file)
        file_path = fs.path(fname)

        # Assume `load_all_models` and `convert_single_pdf` are defined elsewhere
        model_lst = load_all_models()
        full_text, images, out_meta = convert_single_pdf(file_path, model_lst, max_pages=10, langs=None, batch_multiplier=2)

        # Generate the output markdown file path
        fname_without_ext = os.path.splitext(os.path.basename(fname))[0]
        output_file_path = save_markdown('output', fname_without_ext, full_text)

        # Ensure the file is saved with a .md extension
        markdown_filename = f"{fname_without_ext}.md"
        markdown_output_path = os.path.join(settings.MEDIA_ROOT, 'output', markdown_filename)

        # Save the markdown content to the output directory
        with open(markdown_output_path, 'w') as f:
            f.write(full_text)

        # Generate the URL to download the file
        file_url = os.path.join(settings.MEDIA_URL, 'output', markdown_filename)

        return render(request, 'pdf_converter_app/result.html', {'file_url': file_url})

    return render(request, 'pdf_converter_app/upload.html')