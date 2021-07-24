from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from googletrans import Translator
from .models import BookMst, TranslationBookMap, InputLanguage
from booktranslate import text_translate
from cp2.settings import MEDIA_URL
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, inch
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors, fonts
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, _baseFontName
#from reportlab.rl_config import canvas_basefontname as _baseFontName
from django.core.files import File
from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
import io
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.
#def index(request):
#    return render(request, 'testindex.html')


#def home(request):
#    if request.method == "POST":
#        text = request.POST["translate"]
#        language = request.POST["language"]
#        translator= Translator(to_lang=language)
#        translation = translator.translate(text)
#        return HttpResponse(translation)

def login(request):
    if request.method== 'POST':
        username = request.POST['login_username']
        password = request.POST['login_password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            #messages.info(request,'LogIn Successful')
            return redirect("/home/")
        else:
            messages.info(request,'Invalid credentials')
            return redirect('/home/')

    else:
        return render(request,'testindex.html')

def logout(request):
    auth.logout(request)
    return redirect('/home/')

def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        reg_username = request.POST['reg_username']
        reg_password= request.POST['reg_password']
        reg_confirm_password = request.POST['reg_confirm_password']
        
        if reg_password == reg_confirm_password:
            if User.objects.filter(username=reg_username).exists():
                messages.info(request,'USERNAME ALREADY EXISTS, PLEASE CHOOSE ANOTHER ONE')
            else:
                user = User.objects.create_user(first_name=name, username=reg_username, password=reg_password)
                user.save()    
                messages.info(request,'SIGN UP SUCCESSFUL')
        else:
            messages.info(request,'PASSWORD DOES NOT MATCH')
        return redirect('/home/')
    else:
        return render(request,'testindex.html')

def profile(request):
    if request.user.is_authenticated:
        books = BookMst.objects.filter(created_by=request.user.id)
        return render(request, 'profile.html', {'books': books.all})
    else:
        messages.info(request, "Please login first!!!")
        return redirect('/home/')


def pTranslate(request):
    if request.method == 'POST':
        from_lang = request.POST['inputlang']
        to_lang = request.POST['outputlang']
        input_text = request.POST['input_para']
        translator = Translator()
        translation = translator.translate(input_text, dest=to_lang, src=from_lang)
        return render(request, 'testindex.html', {'input_para': input_text, 'output_para': translation.text, 'input_lang': from_lang})
    return render(request, 'testindex.html')

def bookTranslate(request):
    if request.method == 'POST':
        if request.user.id: 
            from_lang = convertToLangEnum(request.POST['pdfInputLang'])
            to_lang = convertToLangEnum(request.POST['pdfOutputLang'])
            if request.POST.get('isPrivate', False) == 'on':
                privateFLag = 1
            else:
                privateFLag = 0
            pdf = request.FILES['myFile']

            #book = BookMst.objects.filter(book_name=pdf.name, input_language=from_lang, output_language=to_lang, created_by=request.user.id)
            #if book is not None:
            #    messages.info(request, "Book Already translated")
            #    return redirect('/home/')
            bookMst = BookMst(book_name=pdf.name, book_path=pdf, input_language=from_lang, output_language=to_lang, is_private=privateFLag, created_by=request.user.id)
            bookMst.save()
            
            
            #translatedText = text_translate.translateFromPath(path=bookMst.book_path.path, input_lang=request.POST['pdfInputLang'], output_lang=request.POST['pdfOutputLang'])
            
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, bottomup=0)
            pdfmetrics.registerFont(TTFont('hindi-light', r"C:\Users\Teerth Patel\sem6cp\Hind\Hind-Light.ttf"))
            addMapping('hindi-light', 0, 0, r"C:\Users\Teerth Patel\sem6cp\Hind\Hindi-Light.ttf")
            pdfmetrics.registerFont(TTFont('arabic', r"C:\Users\Teerth Patel\sem6cp\Hind\arabic-Light.ttf"))
            addMapping('arabic', 0, 0, r"C:\Users\Teerth Patel\sem6cp\Hind\arabic-Light.ttf")
            pdfmetrics.registerFont(TTFont('chinese', r"C:\Users\Teerth Patel\sem6cp\Hind\chinese.ttf"))
            addMapping('chinese', 0, 0, r"C:\Users\Teerth Patel\sem6cp\Hind\chinese.ttf")
            #pdfmetrics.registerFont(TTFont('japanesee', r"C:\Users\Teerth Patel\sem6cp\Hind\japanesee.ttf"))
            #addMapping('japanesee', 0, 0, r"C:\Users\Teerth Patel\sem6cp\Hind\japanesee.ttf")
            pdfmetrics.registerFont(TTFont('bengali', r"C:\Users\Teerth Patel\sem6cp\Hind\bengali-Light.ttf"))
            addMapping('bengali', 0, 0, r"C:\Users\Teerth Patel\sem6cp\Hind\bengali-Light.ttf")
            pdfmetrics.registerFont(TTFont('japanese', r"C:\Users\Teerth Patel\sem6cp\Hind\japanesee.ttf"))
            addMapping('japanese', 0, 0, r"C:\Users\Teerth Patel\sem6cp\Hind\japanesee.ttf")
            styles = getSampleStyleSheet()
            styleN = styles["BodyText"]
            styleN.wrapOn = 'CJK'
            styleN.alignment = TA_LEFT
            styleN.fontName=_baseFontName

            if to_lang == InputLanguage.ENGLISH:
                styleN.fontName=_baseFontName
            if to_lang == InputLanguage.CHINESE:
                styleN.fontName="chinese"
            if to_lang == InputLanguage.SPANISH:
                styleN.fontName=_baseFontName
            if to_lang == InputLanguage.HINDI:
                styleN.fontName="hindi-light"
            if to_lang == InputLanguage.ARABIC:
                styleN.fontName="arabic"
            if to_lang == InputLanguage.BENGALI:
                styleN.fontName="bengali"
            if to_lang == InputLanguage.PORTUGUESE:
                styleN.fontName=_baseFontName
            if to_lang == InputLanguage.RUSSIAN:
                styleN.fontName="hindi-light"
            if to_lang == InputLanguage.JAPANESE:
                styleN.fontName="japanese"
            if to_lang == InputLanguage.INDONESIAN:
                styleN.fontName=_baseFontName

            #description = Paragraph(translatedText.text, styleN)
            description = Paragraph("घ-hindi,\n 你好-chinese ,\n مرحبا - arabic \n Hola  ñ - spanish,\n Здравствуйте, как поживаете russian, \n Olá-portugese, \n হ্যালো, আপনি কেমন আছেন -bengali, \n こんにちは - japanese, \n Halo apa kabarmu - indonesian, \n these letters are for font testing.  Here is bookMst id -  " + str(bookMst.id), styleN)
            
            
            
            #p.setFont('Hindi-Light', 14)
            data = [[description]]
            table = Table(data)
            #table.setStyle(TableStyle([
                        #('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        #('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        #]))
            #p.drawString(1.5*cm, 28.2*cm, translatedText.text)

            # Close the PDF object cleanly, and we're done.
            w, h = table.wrap(550, 800)
            table.wrapOn(p, 550, 800)
            table.drawOn(p, 0.5*cm, 2*cm-h)
            #draw_paragraph(p, table, x=0.5*cm, y=0.5*cm, max_width=550, max_height=800)
            #table.drawOn(p, 0.5*cm,0.5*cm)

            p.setTitle(to_lang+"_"+bookMst.book_name)
            p.showPage()
            p.save()

            # FileResponse sets the Content-Disposition header so that browsers
            # present the option to save the file.
            buffer.seek(0)
            translatedBook = TranslationBookMap(book_id=bookMst.id, translated_language=to_lang, translated_book_path=File(buffer, name=to_lang+"_"+bookMst.book_name))
            translatedBook.save()
            return FileResponse(translatedBook.translated_book_path, as_attachment=True, filename=to_lang+"_"+bookMst.book_name)
        else:
            messages.info(request, "Please log in to use this feature")
            return redirect('/home/')
    return render(request, 'testindex.html')
    

def convertToLangEnum(lang):
    if lang == "en":
        return InputLanguage.ENGLISH
    if lang == "zh-cn":
        return InputLanguage.CHINESE
    if lang == "es":
        return InputLanguage.SPANISH
    if lang == "hi":
        return InputLanguage.HINDI
    if lang == "ar":
        return InputLanguage.ARABIC
    if lang == "bn":
        return InputLanguage.BENGALI
    if lang == "pt":
        return InputLanguage.PORTUGUESE
    if lang == "ru":
        return InputLanguage.RUSSIAN
    if lang == "ja":
        return InputLanguage.JAPANESE
    if lang == "id":
        return InputLanguage.INDONESIAN
    raise Exception("Invalid input/output language selected. Not Supported!!!")