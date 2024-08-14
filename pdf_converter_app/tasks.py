# tasks.py
from celery import shared_task
from time import sleep
from celery_progress.backend import ProgressRecorder

@shared_task(bind=True)
def convert_pdf_to_md(self, file_path):
    progress_recorder = ProgressRecorder(self)
    total_steps = 10  # Assume 10 steps in the conversion process

    for i in range(total_steps):
        # Simulate a step in the conversion process
        sleep(1)  # Replace with actual conversion logic
        progress_recorder.set_progress(i + 1, total_steps)

    # Return the path to the converted file
    return "output/your_converted_file.md"
