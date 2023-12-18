import sqlite3
import csv
import pandas as pd
from django.http import HttpResponse
from django.conf import settings
from io import BytesIO, StringIO
from fakebook.sqlqueries import get_query
import zipfile
import os

# This file acts as a utility file in order to provide the streams that will be downloaded.
# All download files are in memory (BytesIO), so that they need not be stored before downloaded

def get_csv(list_display, queryset, filename):
    f = StringIO()  
    writer = csv.writer(f)
    writer.writerow(list_display)
    for item in queryset:
        line = []
        for i in range(len(list_display)):
            line.append(str(getattr(item, list_display[i])))
        writer.writerow(line)
    f.seek(0)
    response = HttpResponse(f, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename='+filename
    return response


def get_xlsx_file_from_database(selected_tables):
    db_path = settings.DATABASES['default']['NAME']
    conn = sqlite3.connect(db_path)
    excel_file = BytesIO()
    xlsxwriter = pd.ExcelWriter(excel_file)
    print(selected_tables)
    for table in selected_tables:
        sqlquery = get_query(table)
        dbfile = pd.read_sql(sqlquery, conn)
        dbfile.to_excel(xlsxwriter, index = False, sheet_name = table, encoding="utf-16")

    xlsxwriter.save()
    xlsxwriter.close()
    excel_file.seek(0)

    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="database.xlsx"'
    return response

def get_database():
    db_path = settings.DATABASES['default']['NAME']
    with open(db_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.sqlite3")
        response['Content-Disposition'] = 'attachment; filename="database.sqlite3"'
        return response

def get_zip_file(selected_archives):
    media_path = settings.MEDIA_ROOT
    zip_file = BytesIO()
    for i, archive in enumerate(selected_archives):
        selected_archives[i] = media_path + '/' + archive
    print(media_path)
    print(selected_archives)
    with zipfile.ZipFile(zip_file, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for dirname, subdirs, files in os.walk(media_path):
            if dirname in selected_archives: 
                zf.write(dirname)
                for filename in files:
                    zf.write(os.path.join(dirname, filename))
    
    zip_file.seek(0)
    response = HttpResponse(zip_file.read(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="media.zip"'
    return response
