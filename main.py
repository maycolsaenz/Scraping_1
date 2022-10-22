# %%
from bs4 import BeautifulSoup
import requests

loginurl = ('https://131.101.120.134/dms2/Login.jsp')
navigate = ('https://131.101.120.134/dms2/systemsetting/DeviceInformation_BACnet.jsp?address=11.13.04&deviceType=indoor')
main = ('https://131.101.120.134/dms2/main/main.jsp')
session = requests.Session()

jar = requests.cookies.RequestsCookieJar() 
jar.set('JSESSIONID','kdtept3bdgvj7ar3e7gh6w1f')

session.cookies = jar
r = session.get(navigate, verify = False).text

#%% Encontrando direccion
soup = BeautifulSoup(r,'lxml')
Addr = soup.find('label', class_ = 'b fontSize12').get_text()


#%% Encontrando nombre
nombre = soup.find('td', id = 'OBJ_NAME').get_text()

#%% Encontrando valor
valor = soup.find('td', class_ = 'ACenter', id = 'A_VALUE_0').get_text()

#%% Encontrando setpoint
setpoint = soup.find('td', class_ = 'ACenter', id = 'A_VALUE_1').get_text()

#%% Encontrando EDR #1 en main
#EDR1 = soup.find('div', class_ = 'indoorBackground', id = 'indoorBackground')

#%% Resultados
print(Addr)
print("Nombre = "+ nombre)
print("Setpoint = " + setpoint)
print("Valor actual = " + valor)


# %%
