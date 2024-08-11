import os
import json


def get_subfolder_path(out_folder, fname):
    subfolder_name = fname.rsplit('.', 1)[0]
    subfolder_path = os.path.join(out_folder, subfolder_name)
    return subfolder_path


def get_markdown_filepath(out_folder, fname):
    subfolder_path = get_subfolder_path(out_folder, fname)
    out_filename = fname.rsplit(".", 1)[0] + ".md"
    out_filename = os.path.join(subfolder_path, out_filename)
    return out_filename


def markdown_exists(out_folder, fname):
    out_filename = get_markdown_filepath(out_folder, fname)
    return os.path.exists(out_filename)


def save_markdown(out_folder, fname, full_text):
    subfolder_path = get_subfolder_path(out_folder, fname)
    os.makedirs(subfolder_path, exist_ok=True)

    markdown_filepath = get_markdown_filepath(out_folder, fname)
    

    with open(markdown_filepath, "w+", encoding='utf-8') as f:
        f.write(full_text)
  

  
    return subfolder_path