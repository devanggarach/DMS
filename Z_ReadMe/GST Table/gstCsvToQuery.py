import pandas as pd

df = pd.read_csv('01 GST_01092020.csv')

l=df.values.tolist()
for x in range(0,len(l)):
	a='INSERT INTO public."MegaMart_gst"(ghsncode, gdescription, gcgst, gsgst, gigst, gtimestamp)VALUES ('
	b= "'"+str(l[x][0])+"','"+str(l[x][1])+"','"+str(l[x][2])+"','"+str(l[x][3])+"','"+str(l[x][4])+"'"
	c=',NOW()::timestamp);\n'
	print(a+b+c)



