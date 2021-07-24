# -*- coding: utf-8 -*-

from pdf2image import convert_from_path
import easyocr
import numpy as np
import PIL
from PIL import ImageDraw, Image, ImageEnhance
import spacy
import googletrans
from googletrans import Translator
from pdf2image.exceptions import(
  PDFInfoNotInstalledError,
  PDFPageCountError,
  PDFSyntaxError
)

def translateFromPath(path, input_lang, output_lang):
  reader = easyocr.Reader([input_lang], gpu=False)
  import tempfile
  with tempfile.TemporaryDirectory() as outputpath:
    images = convert_from_path(path, output_folder=outputpath)
    
    text = ''
    for i, image in enumerate(images):
      bounds = reader.readtext(np.array(image))
      for i in range(len(bounds)):
        text = text + bounds[i][1] + "\n"
        
    translator = Translator()
    return translator.translate(text, dest=output_lang, src=input_lang)
