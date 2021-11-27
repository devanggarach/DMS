from django.db import models
import qrcode #Qr generate
from io import  BytesIO #Qr generate
from  django.core.files import File #Qr generate
from  PIL import Image, ImageDraw, ImageFont #Qr generate
from django.contrib.auth.models import User
import pyqrcode #Qr generate
import png #Qr generate
from pyqrcode import QRCode #Qr generate
import datetime #Qr generate time setting for expiry date and mrf date
from django.core.validators import MaxValueValidator
# python manage.py makemigrations MegaMart
# python manage.py sqlmigrate MegaMart 0001
# python manage.py migrate




# Create your models here.



class gst(models.Model):
	ghsncode = models.IntegerField(primary_key=True)
	gdescription = models.TextField()
	gcgst = models.FloatField()	
	gsgst = models.FloatField()	
	gigst = models.FloatField()
	gtimestamp = models.DateTimeField(auto_now_add=True)

class customer(models.Model):
	customer_id= models.AutoField(primary_key=True)
	customer_name= models.TextField(max_length=30)
	customer_mobile= models.PositiveIntegerField(default=0,validators=[])
	customer_email= models.TextField(default="notknown@gmail.com", max_length=70)
	customer_address=models.TextField(default="no", max_length=200)
	customer_state=models.TextField(default="Gujarat", max_length=30)
	customer_city=models.TextField(default="Rajkot", max_length=30)
	customer_pincode=models.PositiveIntegerField(default=360007,validators=[MaxValueValidator(999999)])
	customer_timestamp= models.DateTimeField(auto_now_add=True)

class invoice(models.Model):
	invoice_no= models.AutoField(primary_key=True)
	cust_id= models.IntegerField(default=None)
	product_id= models.IntegerField()
	sp= models.FloatField()
	qty= models.FloatField()
	total_amount= models.FloatField()
	cgst= models.FloatField()
	sgst= models.FloatField()
	igst= models.FloatField()
	timestamp= models.DateTimeField(auto_now_add=True)

class product(models.Model):
	pid = models.AutoField(primary_key=True)
	id = models.ForeignKey(User, on_delete=models.CASCADE)
	pname = models.CharField(max_length=50)
	phsncode= models.ForeignKey(gst, on_delete=models.CASCADE)
	pcost = models.FloatField()
	pmrp = models.FloatField()
	psellingprice = models.FloatField()
	pdiscount = models.FloatField()
	ppackingdt = models.DateField()
	pexpirydt = models.DateField()
	pstock = models.IntegerField()
	pquantity = models.IntegerField()
	pqrcode = models.IntegerField()
	pqrimage = models.ImageField(upload_to='', blank=True)
	ptimestamp = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return str(self.pname)

	def save(self, *args, **kwargs):
		url = pyqrcode.create(self.pqrcode)
		fname = f'{self.pname}_{self.pqrcode}.png'
		vcode=str(self.pqrcode)
		buffer = BytesIO()
		businessname="MegaMart"
		buffer = BytesIO()
		url.png(buffer, scale = 4)
		img=Image.open(buffer,'r')
		img_w, img_h = img.size
		background = Image.new('RGBA', (144, 144), (255, 255, 255, 255))#244
		bg_w, bg_h = background.size
		offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
		background.paste(img, offset)
		draw = ImageDraw.Draw(background)
	
		MRPfont     = ImageFont.truetype("/usr/share/fonts/truetype/freefont/Saira_Bold.ttf",7) #12
		Productfont = ImageFont.truetype("/usr/share/fonts/truetype/freefont/Saira_Bold.ttf",11)#18
		SPPricefont = ImageFont.truetype("/usr/share/fonts/truetype/freefont/Saira_Bold.ttf",14)#22
		productcodefont  = ImageFont.truetype("/usr/share/fonts/truetype/freefont/Saira_Bold.ttf",8)#12
		vmrp="MRP. Rs "+str(self.pmrp)+"/-"
		vsellingprice="Sp. Rs " +str(self.psellingprice)+"/-"
		w,h  =MRPfont.getsize(vmrp)
		w1,h1=Productfont.getsize(self.pname)
		w2,h2=SPPricefont.getsize(vsellingprice)

		draw.text(((bg_w-w)/2, 2),vmrp,(0,0,0),font=MRPfont)
		draw.text(((bg_w-w1)/2, 8),self.pname,(0,0,0),font=Productfont)#10

		draw.rectangle((0,bg_h-h2,bg_w,bg_h), fill='black')
		draw.text(((bg_w-w2) // 2, bg_h-(h2+1)),vsellingprice, (255,255,255), font=SPPricefont)#5
		
		buffer=BytesIO()
		# background.show()
		background.save(buffer,'PNG')

		img=Image.open(buffer,'r')
		# img.show()
		img_rotate_270  = img.transpose(Image.ROTATE_270)
		
		buffer=BytesIO()
		img_rotate_270.save(buffer,'PNG')

		img=Image.open(buffer,'r')
		img_w, img_h = img.size
		draw = ImageDraw.Draw(img)
		BusinessNamefont = ImageFont.truetype("/usr/share/fonts/truetype/freefont/Saira_Bold.ttf",17)#22
		ExpireDatefont   = ImageFont.truetype("/usr/share/fonts/truetype/freefont/Saira_Bold.ttf",7)#11
		MFDatefont   = ImageFont.truetype("/usr/share/fonts/truetype/freefont/Saira_Bold.ttf",7)#11
		w,h  =BusinessNamefont.getsize(businessname)
		w2,h2=productcodefont.getsize(vcode)
		w3,h3=ExpireDatefont.getsize("EXP."+self.pexpirydt.strftime("%d-%m-%Y"))
		w4,h4=MFDatefont.getsize("MFR."+self.ppackingdt.strftime("%d-%m-%Y"))
		vexpirydt = "EXP."+self.pexpirydt.strftime("%d-%m-%Y")
		vpackingdt ="MFR."+self.ppackingdt.strftime("%d-%m-%Y")
		draw.text((((bg_w-w)/2)+0, 0),businessname,(0,0,0),font=BusinessNamefont)#12
		draw.text((24, bg_h-(h2+2)*2),vcode,(0,0,0),font=productcodefont)#3  
		draw.text((24+w3+3, bg_h-(h3+5)),vexpirydt,(0,0,0),font=ExpireDatefont)#3
		draw.text((24, bg_h-(h3+5)),vpackingdt,(0,0,0),font=MFDatefont)#3
		buffer=BytesIO()
		# img.show()
		img.save(buffer,'PNG')

		img=Image.open(buffer,'r')
		img_rotate_90  = img.transpose(Image.ROTATE_90)
		
		buffer=BytesIO()
		# img_rotate_90.show()
		img_rotate_90.save(buffer,'PNG')
		
		self.pqrimage.save(fname,File(buffer), save=False)
		super().save(*args, **kwargs)
		

		

		



