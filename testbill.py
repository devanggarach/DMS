# ls=[[1, 1601625403, 'Apple', 80.0, 12.5, 1, 70.0], [2, 16016254031, 'Apple', 80.0, 12.5, 1, 70.0]]
# GprintBill=[[1, 1601625403, 'Apple', 80.0, 25.0, 2, 140.0], [3, 1603059891, 'Hello', 200.0, 127.0, 2, 146.0]]
# GprintBillN={0:}
# ds=[1601625403,16016254031]
# decodeItem = [3, 36, 'Hello', 40.0, 200.0, 63.5, 10, 10, 1997, 1603059891, 73.0]

# decodelist=[]
# if decodeitem[9] not in decodelist:
#     decodelist.append(decodeitem[9])
#     GprintBill.append({'srno':decodedItem[0],'prodid':decodedItem[9], 'prodname':decodedItem[2], 'discount':decodedItem[4], 'discount':decodedItem[5],'qty':1, 'total':decodedItem[10]})
# if decodeitem[9] in decodelist:
#     productIndex=decodelist.index(decodeitem[9])
#     print(productIndex)
#     # GprintBill[productIndex][3]+=decodeitem[4]
#     # GprintBill[productIndex][4]+=decodeitem[5]
#     GprintBill[productIndex][5]+=1
#     GprintBill[productIndex][6]+=decodeitem[10]
# else:
#     GprintBill.append([decodedItem[0],decodedItem[9], decodedItem[2], decodedItem[4], decodedItem[5],1, decodedItem[10]])
    
  
# print(decodelist)
# print(GprintBill)

# import os
# os.system('play -nq -t alsa synth {} sin {}'.format(0.3, 700))

# GprintBill=[[1, 1601625403, 'Apple', 80.0, 25.0, 2, 140.0], [3, 1603059891, 'Hello', 200.0, 127.0, 2, 146.0]]

# for i in GprintBill:
#             for j in i:
#                 if j['srno']!=1:
#                     j['srno']-=1

billtype=True
if billtype==True:
    print("hello")
else:
    print("bye")