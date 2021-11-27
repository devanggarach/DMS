def printIntoPdf():
	# s=product.objects.filter(id=sid)
	# Tall_products = product.objects.values().order_by('pname')
	# d = {'Tall_products': Tall_products, 'hd': headerData()}
	from fpdf import FPDF
	import sys
	pdf = FPDF(orientation='P',unit='mm',format='A4')
	# from PIL import Image
	# from io import  BytesIO
	# list_im = ['Test1.jpg','Test2.jpg','Test3.jpg']
	# buffer=BytesIO()

	import cv2
	import numpy as np
	img1 = cv2.imread('Orange1KG_1600408263.png')
	space = cv2.imread('space.png')
	# img2 = cv2.imread('Orange1KG_1600408263.png')
	pdf.set_margins(3,5)
	h_img = cv2.hconcat([img1, img1, img1, img1])
	# h_img = cv2.hconcat([img1, img1])
	ls=[]
	n=56
	rem=n//4
	v_img = cv2.vconcat([space,h_img,space, h_img,space, h_img,space, h_img,space,h_img])
	cv2.imwrite('demo.png',v_img)
	while rem>0:
		if rem<5:
			for i in range(rem):
				ls.append(space)
				ls.append(h_img)
				# print(ls)
			v_img = cv2.vconcat(ls)
			cv2.imwrite('demo1.png',v_img)
			pdf.add_page()
			pdf.image("demo1.png")
			# print("rem="+str(rem))
		else:
			pdf.add_page()
			pdf.image("demo.png")
			# print("rem="+str(rem))
		rem-=5
	pdf.output('labels.pdf','F')

printIntoPdf()