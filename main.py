# %%
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


loginurl = ('https://131.101.120.134/dms2/Login.jsp')
main = ('https://131.101.120.134/dms2/main/main.jsp')

EDR1 = ('https://131.101.120.134/dms2/systemsetting/DeviceInformation_BACnet.jsp?address=11.13.01&deviceType=indoor')
EDR2 = ('https://131.101.120.134/dms2/systemsetting/DeviceInformation_BACnet.jsp?address=11.13.05&deviceType=indoor')
EDR3 = ('https://131.101.120.134/dms2/systemsetting/DeviceInformation_BACnet.jsp?address=11.13.04&deviceType=indoor')
# IDF1 = ('https://131.101.120.134/dms2/systemsetting/DeviceInformation_BACnet.jsp?address=11.13.00&deviceType=indoor')
# IDF2 = ('https://131.101.120.134/dms2/systemsetting/DeviceInformation_BACnet.jsp?address=11.13.03&deviceType=indoor')
# IDF3 = ('https://131.101.120.134/dms2/systemsetting/DeviceInformation_BACnet.jsp?address=11.13.02&deviceType=indoor')
#MDF = ('https://131.101.120.134/dms2/systemsetting/DeviceInformation_BACnet.jsp?address=11.02.04&deviceType=indoor')
equipos = [EDR1, EDR2, EDR3]

#%% envio de correo condicional
sender = 'pythonMonitor@teradyne.com'
receivers = ['maycol.saenz@teradyne.com']

message = """From: pythonMonitor <pythonMonitor@teradyne.com>
To: Usuario <maycol.saenz@teradyne.com>
Subject: ALTA TEMPERATURA en {} 
Temperatura ambiente en grados celsius es de: {} 

Requiere atension inmediata
Contacte a Facilities


"""


 
#%% Llamando variables
session = requests.Session()
jar = requests.cookies.RequestsCookieJar() 
jar.set('JSESSIONID','byghu61ro7cl121fmjwtzvz89')
session.cookies = jar

for i in range(1):
    for e in equipos:
        r = session.get(e, verify = False).text
        soup = BeautifulSoup(r,'html.parser')
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S ")
        Addr = soup.find('label', class_ = 'b fontSize12').text.replace(' ','')
        nombre = soup.find('td', id = 'OBJ_NAME').text.replace(' ','')
        valor = soup.find('td', class_ = 'ACenter', id = 'A_VALUE_0').text.replace('[°C]','')
        setpoint = soup.find('td', class_ = 'ACenter', id = 'A_VALUE_1').text.replace('[°C]','').strip()
        salida = [str(i)+' ', current_time,Addr,nombre +' ', setpoint +' ', valor]
        with open('historial.txt','a') as f:
            for salidas in salida:
                f.write(salidas)
                print(salida)
        if(int(valor)>=22):
            try:
                smtpObj = smtplib.SMTP('192.168.150.92')
                smtpObj.sendmail(sender, receivers, message.format(nombre, valor))         
                print ("Successfully sent email")
            except SMTPException:
                print ("Error: unable to send email")
        
    time.sleep(10)


# %%
