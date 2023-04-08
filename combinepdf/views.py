from flask import Blueprint, request, send_file, render_template
from . import tasks

bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@bp.route('/')
def index():
    return render_template('home.html')


@bp.post('/merge-pdfs')
def merge_pdf():
    filename = request.form['filename']
    top_pdf = request.files['top-pdf']
    second_pdf = request.files['second-pdf']
    third_pdf = request.files['third-pdf']
    bulk_pdfs = request.files.getlist('bulk-pdf[]')

    combined_pdf = tasks.combine_pdfs(filename, top_pdf, second_pdf, third_pdf, bulk_pdfs)

    return combined_pdf


@bp.get('/download/<task_id>')
def download_pdf(task_id):
    task, filename = merge_pdf.AsyncResult(task_id)
    if task.state == 'SUCCESS':
        output_pdf = task.result
        with open(f'{filename}.pdf', 'wb') as f:
            output_pdf.write(f)
        return send_file(output_pdf, download_name=f'{filename}.pdf', as_attachment=True)
