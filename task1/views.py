from django.http.response import HttpResponse
from task1.models import uploadfiles
from django.shortcuts import render,redirect
import os
import datetime
from os import listdir
from fpdf import FPDF 
from docx2pdf import convert
import re
import xlwt
from django.http import HttpResponse
from .models import uploadfiles
from io import StringIO
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
from pdfminer3.layout import LAParams
from django.core.files.storage import FileSystemStorage
from pdfminer3.pdfpage import PDFPage

# function to convert text to pdf
def texttopdf(file):
    pdf = FPDF()      
    # Add a page 
    pdf.add_page()  
    # set style and size of font  
    # that you want in the pdf 
    pdf.set_font("Arial", size = 15)
    # open the text file in read mode 
    f = open(file, "r") 
    # insert the texts in pdf 
    for x in f: 
        pdf.cell(50,5, txt = x, ln = 1, align = 'C') 
    # save the pdf with name .pdf 
    file1=file.split('/')
    name=file1[-1]
    name1=name.split('.')
    name1[-1]='.pdf'
    final=''.join(name1)
    final1='./media/'+final
    pdf.output(final1)

#function to convert docx to pdf
def docxtopdf(file):
    convert(file)

#function to get email and pfn no
def get_cv_email_and_phn(cv_path):
        pagenums = set()
        output = StringIO()
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, laparams=LAParams())
        interpreter = PDFPageInterpreter(manager, converter)
        infile = open(cv_path, 'rb')
        for page in PDFPage.get_pages(infile, pagenums):
            interpreter.process_page(page)
        infile.close()
        converter.close()
        text = output.getvalue()
        output.close()  
        pattern=['^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$','[\+\d]?(\d{2,3}[-\.\s]??\d{2,3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})']
        for i in pattern:

            match = re.search(i, text)  
            if match:
                break         
        phn_no=match.group(0)           
        pattern=[r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+",r"[a-z0-9\.\-+_]+@.[a-z0-9\.\-+_]+\.[a-z]+"]
        for i in pattern:
            match1 = re.search(i, text)
            if match1:
                
                break
        if match1:
            email = match1.group(0)
        else:email=None  
        print(phn_no,email,cv_path)
        return phn_no,email,cv_path


#function to convertfiles in the directory
def convertorfordirectory(listdir):
    
    try:
        x=listdir.split('.')
        if x[-1]=='txt':
            texttopdf(listdir)

        elif x[-1]=='docx':
            convert(listdir)
        
    except:
        pass


# Create your views here.
def input(request):
    return render(request,'input.html')
def upload(request):
    type_file=request.POST.get('type')
    fs=FileSystemStorage()
    fileobj=(request.FILES.getlist('upload'))
    for i in fileobj:
        fs.save(i.name,i)
    listdir=[]
    path='./media/'
    list1=os.listdir('./media/')
    listdir=[]
    
    for i in list1:
        x=os.path.join(path,i)
        listdir.append(x)
    for i in listdir:
        convertorfordirectory(i)
        
    for i in list1:
        try:
            
                x=i.split('.')
                if x[-1]!='pdf':
                    p=os.path.join('./media/',i)
                    os.remove(p)
        except:
            pass
    list1=os.listdir('./media/')
    for i in list1:
        upf=uploadfiles()
        x=os.path.join('./media/',i)
        p,e,l=get_cv_email_and_phn(x)
        print(p,e,l,'-------------------------------------------------')
        upf.email=e
        upf.phn=p
        upf.file=x
        upf.save()
        
    return redirect(output)
def output(request):
    upf=uploadfiles.objects.all()
    return render(request,'output.html',{'upf':upf})


def download(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachement;filename=Output'+\
        str(datetime.datetime.now())+'.xls'
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Output')
    row_num=0
    font_style=xlwt.XFStyle()
    font_style.font.bold=True
    columns=['Email','Phone Number','Location']
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)
    font_style=xlwt.XFStyle()
    rows=uploadfiles.objects.values_list('email','phn','file')
    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)
    wb.save(response)
    return response
        
   
        

