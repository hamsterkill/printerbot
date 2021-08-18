import img2pdf
import os
from PIL import Image

def convert_img_to_pdf(img_path):
	image = Image.open(img_path)
	if(img_path.endswith('.png')):
		image = image.convert('RGB')
		image.save('img.jpg')
		img_path = img_path.replace(".png", ".jpg")
		image = Image.open('img.jpg')
	pdf_bytes = img2pdf.convert(image.filename)
	file = open('converted.pdf', "wb")
	file.write(pdf_bytes)
	image.close()
	file.close()
