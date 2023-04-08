from io import BytesIO
from PyPDF4 import PdfFileMerger, PdfFileReader
from flask import send_file


def combine_pdfs(filename, top_pdf, second_pdf=None, third_pdf=None, bulk_pdfs=None):
    merger = PdfFileMerger()

    if top_pdf:
        try:
            top_pdf_data = top_pdf.read()
            top_pdf_reader = PdfFileReader(BytesIO(top_pdf_data))
            merger.append(top_pdf_reader)
        except Exception as e:
            print(f"Error while reading {top_pdf.filename}: {str(e)}")

    if second_pdf:
        try:
            second_pdf_data = second_pdf.read()
            second_pdf_reader = PdfFileReader(BytesIO(second_pdf_data))
            merger.append(second_pdf_reader)
        except Exception as e:
            print(f"Error while reading {second_pdf.filename}: {str(e)}")

    if third_pdf:
        try:
            third_pdf_data = third_pdf.read()
            third_pdf_reader = PdfFileReader(BytesIO(third_pdf_data))
            merger.append(third_pdf_reader)
        except Exception as e:
            print(f"Error while reading {third_pdf.filename}: {str(e)}")

    if bulk_pdfs:
        for file in bulk_pdfs:
            if file.filename == "":
                break
            try:
                pdf_data = file.read()
                pdf_reader = PdfFileReader(BytesIO(pdf_data))
                merger.append(pdf_reader)
            except Exception as e:
                print(f"Error while reading {file.filename}: {str(e)}")

    output_stream = BytesIO()
    merger.write(output_stream)

    # reset the file pointer to the beginning of the stream
    output_stream.seek(0)

    return send_file(output_stream, download_name=f'{filename}.pdf', as_attachment=True)
