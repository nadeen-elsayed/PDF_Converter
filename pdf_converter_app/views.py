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

configure_logging()
def upload_pdf(request):
    if request.method == 'POST' and request.FILES['pdf']:
        pdf_file = request.FILES['pdf']
        fs = FileSystemStorage(location='input')
        fname = fs.save(pdf_file.name, pdf_file)
        file_path = fs.path(fname)
        model_lst = load_all_models()
        start = time.time()
        full_text, images, out_meta = convert_single_pdf(file_path, model_lst, max_pages=10, langs=None, batch_multiplier=2)
        fname = os.path.basename(fname)
        #fname = os.path.basename(fname)
        output_file_path = save_markdown('output', fname, full_text)
        # Run your PDF to Markdown conversion code here
         # Your conversion function
        
        # Save the output file in the output folder
        #fs_out = FileSystemStorage(location='output')
        markdown_foldername = os.path.basename(output_file_path)
        markdown_filename = f"{markdown_foldername}.md"
        #fs_out.save(markdown_filename, open(output_file_path, 'rb'))
        # Return the output file to the user
        file_url = default_storage.url(f'output/{markdown_foldername}/{markdown_filename}')
        return render(request, 'pdf_converter_app/result.html', {'file_url': file_url})
        # Return the output file to the user
        return render(request, 'pdf_converter_app/result.html', {'file_url': fs_out.url(markdown_filename)})

    return render(request, 'pdf_converter_app/upload.html')
