from django.shortcuts import render
# from django.http import HttpResponse
from django.http import HttpResponse
from warnings import filterwarnings  # Qr code reade
from pyzbar.pyzbar import decode  # Qr code reade
import os
from django.contrib import auth  # authenticate


# from django.contrib.auth import logout
import cv2
import numpy as np
import pyqrcode
import png #Qr generate
from pyqrcode import QRCode #Qr generate
import datetime #Qr generate time setting for expiry date and mrf date
from io import  BytesIO #Qr generate
from  PIL import Image, ImageDraw, ImageFont #Qr generate
import os
from pybeep.pybeep import PyBeep

from datetime import *
import calendar
import time

# model include
from .models import product,customer,invoice, gst, User
# from django.db.models import Sum

# Create your views here.
filterwarnings('ignore')

# global variable
Guid = []
GbillingProducts = []
GprintBill = []
GbillTotal = []
decodelist=[]
gstval=[]
gst_type={'billtype':True}

#  function view
def headerData():
    today = date.today()
    dt = today.strftime("%Y-%m-%d")
    print(dt)
    notification_products = product.objects.filter(pexpirydt__lt=dt)
    return {"nfexpire": notification_products, "nfcount": len(notification_products)}

# function template

# login, register, index________________________________________________________
def login(request):
    return render(request, 'MegaMart/login.html')


def logout(request):
    auth.logout(request)
    return render(request, 'MegaMart/login.html')


def submitLogin(request):
    vusername = request.GET['username']
    vpassword = request.GET['password']
    user = auth.authenticate(username=vusername, password=vpassword)

    if user is not None:
        auth.login(request, user)
        current_user = request.user
        request.session['uid'] = current_user.id
        # Guser['name'] = current_user.username
        d = {'hd': headerData()}
        return render(request, 'MegaMart/index.html', context=d)
    else:
        return render(request, 'MegaMart/login.html', context={'loginmessage': 'Username or Password invalid !.....'})


def index(request):
    d = {'hd': headerData()}
    return render(request, 'MegaMart/index.html', context=d)


#  products ____{% csrf_token %}____________________________________________________
def addProduct(request):
    dditeam = []
    Tall_hsn = gst.objects.all()
    Tall_products = product.objects.all()
    uiteam = product.objects.all().distinct('pname').values_list('pname')

    for x in uiteam:
        dditeam.append(x[0])
    d = {'Tall_products': Tall_products, 'Tall_hsn': Tall_hsn, 'dditeam': dditeam, 'hd': headerData()}
    return render(request, 'MegaMart/addProduct.html',
                  context=d)


def saveProduct(request):
    vname = request.GET['name']
    vspihsncode = request.GET['hsncode']
    vcost = request.GET['cost']
    vmrp = request.GET['mrp']
    vsellingprice = request.GET['sellingprice']
    vdiscount = request.GET['discount']
    vpackingdt = request.GET['packingdt']
    vexpirydt = request.GET['expirydt']
    vquantity = request.GET['quantity']
    vqrcode = calendar.timegm(time.gmtime())
    

    vexpirydt = datetime.strptime(vexpirydt, '%d-%m-%Y')
    vpackingdt = datetime.strptime(vpackingdt, '%d-%m-%Y')

    insPro = product(pname=vname, id=User.objects.get(id=request.session.get('uid')), phsncode=gst.objects.get(ghsncode=vspihsncode), pcost=vcost, pmrp=vmrp,psellingprice=vsellingprice, pdiscount=vdiscount, ppackingdt=vpackingdt, pexpirydt=vexpirydt, pstock=vquantity, pquantity=vquantity, pqrcode=vqrcode)
    insPro.save()
    Tall_products = product.objects.all()

    d = {'Tall_products': Tall_products, 'urlback': 1, 'hd': headerData()}

    return render(request, 'MegaMart/addProduct.html', context=d)


# Display products ________________________________________________________
def showProduct(request):
    Tall_products = product.objects.values().order_by('pname')
    d = {'Tall_products': Tall_products, 'hd': headerData()}
    return render(request, 'MegaMart/showproduct.html', context=d)

def showProductSingle(request):
    Tall_products = product.objects.exclude(pquantity__lt=1).order_by('pname')
    print(Tall_products)
    d = {'Tall_products': Tall_products, 'hd': headerData()}
    return render(request, 'MegaMart/showproduct.html', context=d)

def printqr(request):
    Tall_products = product.objects.values().order_by('pname')
    d = {'Tall_products': Tall_products, 'hd': headerData()}
    return render(request, 'MegaMart/printqr.html', context=d)

def printIntoPdf(request,sid):
    s=product.objects.get(pid=sid)
    n=int(request.GET["nval"])
    Tall_products = product.objects.values().order_by('pname')
    d = {'Tall_products': Tall_products, 'hd': headerData()}
    from fpdf import FPDF
    import sys
    pdf = FPDF(orientation='P',unit='mm',format='A4')
    # from PIL import Image
    # from io import  BytesIO
    # list_im = ['Test1.jpg','Test2.jpg','Test3.jpg']
    # buffer=BytesIO()
    url = pyqrcode.create(s.pqrcode)
    fname = f'{s.pname}_{s.pqrcode}.png'
    vcode=str(s.pqrcode)
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
    vmrp="MRP. Rs "+str(s.pmrp)+"/-"
    vsellingprice="Sp. Rs " +str(s.psellingprice)+"/-"
    w,h  =MRPfont.getsize(vmrp)
    w1,h1=Productfont.getsize(s.pname)
    w2,h2=SPPricefont.getsize(vsellingprice)

    draw.text(((bg_w-w)/2, 2),vmrp,(0,0,0),font=MRPfont)
    draw.text(((bg_w-w1)/2, 8),s.pname,(0,0,0),font=Productfont)#10

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
    w3,h3=ExpireDatefont.getsize("EXP."+s.pexpirydt.strftime("%d-%m-%Y"))
    w4,h4=MFDatefont.getsize("MFR."+s.ppackingdt.strftime("%d-%m-%Y"))
    vexpirydt = "EXP."+s.pexpirydt.strftime("%d-%m-%Y")
    vpackingdt ="MFR."+s.ppackingdt.strftime("%d-%m-%Y")
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
    img_rotate_90.save("tempqrcode.png")
    
    img1 = cv2.imread('tempqrcode.png')
    space = cv2.imread('space.png')
    # img2 = cv2.imread('Orange1KG_1600408263.png')
    pdf.set_margins(3,5)
    h_img = cv2.hconcat([img1, img1, img1, img1])
    # h_img = cv2.hconcat([img1, img1])
    
    ls=[]
    # n=64
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
    # import webbrowser as wb
    # wb.open_new(r'labels.pdf')

    from django.http import FileResponse, Http404
    with open('labels.pdf','rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=DMS_labels.pdf'
        return response
    
    return render(request, 'MegaMart/printqr.html',context=d)

# not used _____________________________________________________________________
def addItem(request):
    print("addItem")
    capture = cv2.VideoCapture(0)
    # start_time = time.time()
    recieved_data = None
    i = 0
    decodedItem = [len(GbillingProducts) + 1]
    while i < 1:
        # reading frame from the camera
        _, frame = capture.read()
        # print("1test:",capture.read())
        # Decoding the QR Code
        decoded_data = decode(frame)
        # print("2test:",decoded_data)
        try:
            data = decoded_data[0][0]
            if data != recieved_data:
                recieved_data = data
                scanneditem = data.decode('ascii')
                # print(scanneditem,type(scanneditem))
                Titem = product.objects.filter(pqrcode=scanneditem).values_list(
                    'pid', 'pname', 'pcost', 'pmrp', 'pdiscount', 'ppackingdt',
                    'pexpirydt', 'pquantity', 'pqrcode','phsncode_id','psellingprice')
                # print("\n", data.decode('ascii'), "\n")
                # print(Titem)
                # decodedItem.clear()
                for item in Titem:
                    for x in item:
                        decodedItem.append(x)
                        # print(x)

                i = 1
                recieved_data = None
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break
                # end_time = time.time()
                # elapsed = end_time - start_time
                # if elapsed > 1:
                #     capture.release()
                #     cv2.destroyAllWindows()
                    
        except:
            pass
        cv2.imshow("QR CODE Scanner", frame)
        # To exit press Esc Key.
        cv2.waitKey(1)
        # print(type(key),key)
        # if key == 27:
        #     break
    # print(decodedItem)
    hscd=decodedItem[10]
    print(hscd,type(hscd))
    gstv = [gst.objects.filter(ghsncode=hscd).values_list('ghsncode','gsgst','gcgst','gigst')]
    for item in gstv:
        for x in item:
            gstval.append(x)
    print("Guid:",Guid,"GbillingProducts:",GbillingProducts,"GprintBill:",GprintBill,"GbillTotal:",GbillTotal,"gstval:",gstval)
    # gstval=gst.objects.filter(ghsncode=decodedItem[9])
    # print("gstval:",gstval,gstval[0],gstval[1],gstval[2],gstval[3])#gstval[0],gstval[1],gstval[2],gstval[3]
    GbillingProducts.append(decodedItem)
    
    # print("decodedItem",decodedItem)
    # print("Test0",GprintBill,decodelist)
    print("Test0 gstval:",gstval)
    print("Test0 decodelist:",decodelist)
    print("Test0 GprintBill:",GprintBill)
    print("Test0 decodeItem:",decodedItem)
    # Original Cost = GST Inclusive Price x 100/(100+GST Rate)
    OriginalCost=decodedItem[11]*100/(100+round(decodedItem[11]*gstval[len(GprintBill)][3]/(100+(gstval[len(GprintBill)][3])),2))

    # GST Amount =  GST Inclusive Price x GST Rate/(100+GST Rate)
    GSTAmount=decodedItem[11]*round(gstval[len(GprintBill)][3],2)/(100+round(gstval[len(GprintBill)][3],2))
    SCGSTAmount=GSTAmount/2
    
    # Discount= (MRP - (Selling Price - GST Amount)) / MRP x 100
    Discount=(decodedItem[4]-(decodedItem[11]-GSTAmount))/decodedItem[4]*100
    
    if decodedItem[9] not in decodelist:
        # print("Test01 gstval:",gstval)
        # print("Test01 decodelist:",decodelist)
        # print("Test01 GprintBill:",GprintBill)
        # print("Test01 decodeItem:",decodedItem)
        
        decodelist.append(decodedItem[9])

        GprintBill.append({'srno':len(GprintBill)+1,'hsncode':decodedItem[10],'prodid':decodedItem[9],'prodname':decodedItem[2], 
        'rate':decodedItem[4],'amt': decodedItem[4],'discount':round(Discount,2),'qty':1, 'total':decodedItem[11],'temp':decodedItem[11],
        'cgstval':round(SCGSTAmount,2),'sgstval':round(SCGSTAmount,2),
        'igstval':round(GSTAmount,2),'gstrate':gstval[len(GprintBill)][3]})
        #'cgstval':gstval[1],'sgstval':gstval[2],'igstval':gstval[3]
        # print("Test11 gstval:",gstval)
        # print("Test11 decodelist:",decodelist)
        # print("Test11 GprintBill:",GprintBill)
        # print("Test11 decodeItem:",decodedItem)
    elif decodedItem[9] in decodelist:
        productIndex=decodelist.index(decodedItem[9])
        # print(Test02 productIndex)
        # print("Test02 gstval:",gstval)
        # print("Test02 decodelist:",decodelist)
        # print("Test02 GprintBill:",GprintBill)
        # print("Test02 decodeItem:",decodedItem)
        GprintBill[productIndex]['amt']+=decodedItem[4]
        GprintBill[productIndex]['qty']+=1
        GprintBill[productIndex]['total']+=decodedItem[11]
        GprintBill[productIndex]['cgstval']+=round(decodedItem[11]*gstval[len(GprintBill)][1]/(100+(gstval[len(GprintBill)][1])),2)
        GprintBill[productIndex]['sgstval']+=round(decodedItem[11]*gstval[len(GprintBill)][2]/(100+(gstval[len(GprintBill)][2])),2)
        GprintBill[productIndex]['igstval']+=round(decodedItem[11]*gstval[len(GprintBill)][3]/(100+(gstval[len(GprintBill)][3])),2)

        # GprintBill[productIndex][cgst]
        # print("Test22 gstval:",gstval)
        # print("Test22 decodelist:",decodelist)
        # print("Test22 GprintBill:",GprintBill)
        # print("Test22 decodeItem:",decodedItem)
    else:
        GprintBill.append({'srno':len(GprintBill)+1,'hsncode':decodedItem[10],'prodid':decodedItem[9],'prodname':decodedItem[2], 
        'rate':decodedItem[4],'amt': decodedItem[4],'discount':decodedItem[5],'qty':1, 'total':decodedItem[11],'temp':decodedItem[11],
        'cgstval':round(decodedItem[11]*gstval[1]/(100+(gstval[1])),2),'sgstval':round(decodedItem[11]*gstval[2]/(100+(gstval[2])),2),
        'igstval':round(decodedItem[11]*gstval[3]/(100+(gstval[3])),2),'gstrate':gstval[3]})
        # 'cgstval':gstval[1],'sgstval':gstval[2],'igstval':gstval[3]
    #     print("Test03 gstval:",gstval)
    #     print("Test03 decodelist:",decodelist)
    #     print("Test03 GprintBill:",GprintBill)
    #     print("Test03 decodeItem:",decodedItem)
    # print("Test31 gstval:",gstval)
    # print("Test31 decodelist:",decodelist)
    # print("Test31 GprintBill:",GprintBill)
    # print("Test31 decodeItem:",decodedItem)
    totalsum=0
    cgstsum=0
    sgstsum=0
    igstsum=0
    if gst_type['billtype']==True:
        for i in GprintBill:
            totalsum+=i['total']
            cgstsum+=i['cgstval']
            sgstsum+=i['sgstval']
    else:
        for i in GprintBill:
            totalsum+=i['total']
            igstsum+=i['igstval']
    x = ("% 12.2f" % (totalsum))
    a = ("% 12.2f" % (cgstsum))
    b = ("% 12.2f" % (sgstsum))
    c = ("% 12.2f" % (igstsum))
    if gst_type['billtype']==True:
        shscgst='background-color: rgb(233, 233, 245);'
        shigst=''
    else:
        shscgst=''
        shigst='background-color: rgb(233, 233, 245);'
    # d={pprintBill:GprintBill}
    d = {'pprintBill':GprintBill, 'billTotal': x,'cgsttotal':a,'sgsttotal':b,'igsttotal':c,'shscgst':shscgst,'shigst':shigst}
    os.system('play -nq -t alsa synth {} sin {}'.format(0.3, 700))  
    return render(request, 'MegaMart/home.html',context=d)

def clearBill(request):
# 	GbillingProducts.clear()
    GprintBill.clear()
    decodelist.clear()
    gstval.clear()
    
    if gst_type['billtype']==True:
        shscgst='background-color: rgb(233, 233, 245);'
        shigst=''
    else:
        shscgst=''
        shigst='background-color: rgb(233, 233, 245);'
# 	GbillTotal.clear()
    os.system('play -nq -t alsa synth {} sin {}'.format(0.3, 700))
    return render(request,'MegaMart/home.html',context={'shscgst':shscgst,'shigst':shigst})

def qtyPlus(request,sid):
    if sid in decodelist:
        # print("qtyPlus:")
        # print("Test1 gstval:",gstval)
        # print("Test1 decodelist:",decodelist)
        # print("Test1 GprintBill:",GprintBill)
        # print("Test1 decodelist:",decodelist)
        
        productIndex=decodelist.index(sid)
        # print(productIndex)
        GprintBill[productIndex]['amt']+=GprintBill[productIndex]['rate']
        GprintBill[productIndex]['qty']+=1
        GprintBill[productIndex]['total']+=GprintBill[productIndex]['temp']
        GprintBill[productIndex]['cgstval']+=round(GprintBill[productIndex]['temp']*gstval[productIndex][1]/(100+(gstval[productIndex][1])),2)
        GprintBill[productIndex]['sgstval']+=round(GprintBill[productIndex]['temp']*gstval[productIndex][2]/(100+(gstval[productIndex][2])),2)
        GprintBill[productIndex]['igstval']+=round(GprintBill[productIndex]['temp']*gstval[productIndex][3]/(100+(gstval[productIndex][3])),2)

    totalsum=0
    cgstsum=0
    sgstsum=0
    igstsum=0
    if gst_type['billtype']==True:
        for i in GprintBill:
            totalsum+=i['total']
            cgstsum+=i['cgstval']
            sgstsum+=i['sgstval']
    else:
        for i in GprintBill:
            totalsum+=i['total']
            igstsum+=i['igstval']
    x = ("% 12.2f" % (totalsum))
    a = ("% 12.2f" % (cgstsum))
    b = ("% 12.2f" % (sgstsum))
    c = ("% 12.2f" % (igstsum))
    d = {'pprintBill':GprintBill, 'billTotal': x,'cgsttotal':a,'sgsttotal':b,'igsttotal':c}
    os.system('play -nq -t alsa synth {} sin {}'.format(0.3, 700))
    return render(request, 'MegaMart/home.html', context=d)
def qtyMinus(request,sid):
    if sid in decodelist:
        print("qtyMinus:")
        print("Test1 gstval:",gstval)
        print("Test1 decodelist:",decodelist)
        print("Test1 GprintBill:",GprintBill)
        print("Test1 decodelist:",decodelist)
        productIndex=decodelist.index(sid)
        print(productIndex)
        if GprintBill[productIndex]['qty']!=1:
            # print("Test21:",GprintBill,productIndex,decodelist)
            GprintBill[productIndex]['amt']-=GprintBill[productIndex]['rate']
            GprintBill[productIndex]['qty']-=1
            GprintBill[productIndex]['total']-=GprintBill[productIndex]['temp']
            GprintBill[productIndex]['cgstval']-=round(GprintBill[productIndex]['temp']*gstval[productIndex][1]/(100+(gstval[productIndex][1])),2)
            GprintBill[productIndex]['sgstval']-=round(GprintBill[productIndex]['temp']*gstval[productIndex][2]/(100+(gstval[productIndex][2])),2)
            GprintBill[productIndex]['igstval']-=round(GprintBill[productIndex]['temp']*gstval[productIndex][3]/(100+(gstval[productIndex][3])),2)
            print("Test2 gstval:",gstval)
            print("Test2 decodelist:",decodelist)
            print("Test2 GprintBill:",GprintBill)
            print("Test2 decodelist:",decodelist)
            # print("Test22:",GprintBill,productIndex,decodelist)
        else:
            # print("Test23:",GprintBill,productIndex,decodelist)
            if productIndex!=len(GprintBill)-1:
                print("if",len(GprintBill))
                del GprintBill[productIndex]
                del decodelist[productIndex]
                del gstval[productIndex]
                for i in GprintBill:
                    if (i['srno']!=1) and (i['srno']!=len(GprintBill)-1):
                        i['srno']-=1
            else:
                print("else",len(GprintBill))
                for i in GprintBill:
                    if (i['srno']!=1) and (i['srno']!=len(GprintBill)-1):
                        i['srno']-=1
                del GprintBill[productIndex]
                del decodelist[productIndex]
                del gstval[productIndex]
            print("Test3 gstval:",gstval)
            print("Test3 decodelist:",decodelist)
            print("Test3 GprintBill:",GprintBill)
            print("Test3 decodelist:",decodelist)
            # print("Test24:",GprintBill,productIndex,decodelist)
    totalsum=0
    cgstsum=0
    sgstsum=0
    igstsum=0
    if gst_type['billtype']==True:
        for i in GprintBill:
            totalsum+=i['total']
            cgstsum+=i['cgstval']
            sgstsum+=i['sgstval']
    else:
        for i in GprintBill:
            totalsum+=i['total']
            igstsum+=i['igstval']
    x = ("% 12.2f" % (totalsum))
    a = ("% 12.2f" % (cgstsum))
    b = ("% 12.2f" % (sgstsum))
    c = ("% 12.2f" % (igstsum))
    d = {'pprintBill':GprintBill, 'billTotal': x,'cgsttotal':a,'sgsttotal':b,'igsttotal':c}
    os.system('play -nq -t alsa synth {} sin {}'.format(0.3, 700))
    return render(request, 'MegaMart/home.html', context=d)
def deleteProd(request,sid):
    if sid in decodelist:
        productIndex=decodelist.index(sid)
        for i in GprintBill:
            if (i['srno']!=1) and (i['srno']!=len(GprintBill)-1):
                i['srno']-=1
        del GprintBill[productIndex]
        del decodelist[productIndex]
        del gstval[productIndex]
    totalsum=0
    cgstsum=0
    sgstsum=0
    igstsum=0
    if gst_type['billtype']==True:
        for i in GprintBill:
            totalsum+=i['total']
            cgstsum+=i['cgstval']
            sgstsum+=i['sgstval']
    else:
        for i in GprintBill:
            totalsum+=i['total']
            igstsum+=i['igstval']
    x = ("% 12.2f" % (totalsum))
    a = ("% 12.2f" % (cgstsum))
    b = ("% 12.2f" % (sgstsum))
    c = ("% 12.2f" % (igstsum))
    d = {'pprintBill':GprintBill, 'billTotal': x,'cgsttotal':a,'sgsttotal':b,'igsttotal':c}
    os.system('play -nq -t alsa synth {} sin {}'.format(0.3, 700))
    return render(request, 'MegaMart/home.html', context=d)

def showigst(request):
    gst_type['billtype']=False
    totalsum=0
    cgstsum=0
    sgstsum=0
    igstsum=0
    if gst_type['billtype']==True:
        for i in GprintBill:
            totalsum+=i['total']
            cgstsum+=i['cgstval']
            sgstsum+=i['sgstval']
    else:
        for i in GprintBill:
            totalsum+=i['total']
            igstsum+=i['igstval']
    x = ("% 12.2f" % (totalsum))
    a = ("% 12.2f" % (cgstsum))
    b = ("% 12.2f" % (sgstsum))
    c = ("% 12.2f" % (igstsum))
    d = {'pprintBill':GprintBill, 'billTotal': x,'cgsttotal':a,'sgsttotal':b,'igsttotal':c,'shigst':'background-color: rgb(233, 233, 245);'}
    os.system('play -nq -t alsa synth {} sin {}'.format(0.3, 700))
    return render(request, 'MegaMart/home.html', context=d)

def showscgst(request):
    gst_type['billtype']=True
    totalsum=0
    cgstsum=0
    sgstsum=0
    igstsum=0
    if gst_type['billtype']==True:
        for i in GprintBill:
            totalsum+=i['total']
            cgstsum+=i['cgstval']
            sgstsum+=i['sgstval']
    else:
        for i in GprintBill:
            totalsum+=i['total']
            igstsum+=i['igstval']
    x = ("% 12.2f" % (totalsum))
    a = ("% 12.2f" % (cgstsum))
    b = ("% 12.2f" % (sgstsum))
    c = ("% 12.2f" % (igstsum))
    d = {'pprintBill':GprintBill, 'billTotal': x,'cgsttotal':a,'sgsttotal':b,'igsttotal':c,'shscgst':'background-color: rgb(233, 233, 245);'}
    os.system('play -nq -t alsa synth {} sin {}'.format(0.3, 700))
    return render(request, 'MegaMart/home.html', context=d)

def insertInvoiceRecord(request):
    # cust_nm=request.GET["cust_nm"]
    # cust_mob=request.GET["cust_mob"]
    # cust_email=request.GET["cust_email"]
    # cust_addr=request.GET["cust_addr"]
    # cust_st=request.GET["cust_st"]
    # cust_cty=request.GET["cust_cty"]
    # cust_pcode=request.GET["cust_pcode"]
    # data=customer(customer_name=cust_nm)
    # data.save()
    
    # cust_id=customer.objects.filter(customer_mobile=cust_mob)
    # print("cust_id:",cust_id)
    # for cust in cust_id:
    #     print("cust:",cust)
    #     custid = cust.customer_id
    # print("printing cust_id:",custid)
    r=clearBill(request)
    return HttpResponse(r)


# def cancleScanne(request):
# 	return render(request, 'MegaMart/home.html')


# ____________________________________________________
# product= 	pid,pname,pcost,pselling,pdiscount,ppackingdt,pexpirydt,pquantity,pqrcode,pqrimage
# sub – subtraction
# mul – multiplication
# div – division
# abs – absolute value
# mod – modulo
