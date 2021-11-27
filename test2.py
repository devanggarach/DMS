
decodedItem = [3, 36, 'Hello', 40.0, 200.0, 63.5, 10, 10, 1997, 1603059891, 73.0]

GprintBill=[]
# print(GprintBill[0]['srno'])

# {'srno':len(GprintBill)+1,'prodid':decodedItem[9],'prodname':decodedItem[2], 'price':decodedItem[4], 'discount':decodedItem[5],'qty':1, 'total':decodedItem[10]}
decodelist=[]
if decodedItem[9] not in decodelist:
    decodelist.append(decodedItem[9])
    GprintBill.append({'srno':len(GprintBill)+1,'prodid':decodedItem[9],'prodname':decodedItem[2], 'price':decodedItem[4], 'discount':decodedItem[5],'qty':1, 'total':decodedItem[10]})
    # print(decodelist)
elif decodedItem[9] in decodelist:
    productIndex=decodelist.index(decodedItem[9])
    # print(productIndex)
    # GprintBill[productIndex][3]+=decodedItem[4]
    # GprintBill[productIndex][4]+=decodedItem[5]
    GprintBill[productIndex]['qty']+=1
    GprintBill[productIndex]['total']+=decodedItem[10]
else:
    GprintBill.append([decodedItem[0],decodedItem[9], decodedItem[2], decodedItem[4], decodedItem[5],1, decodedItem[10]])
# print(GprintBill,decodelist)