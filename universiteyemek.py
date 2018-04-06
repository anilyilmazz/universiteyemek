from bs4 import BeautifulSoup
from datetime import date
import requests
import threading
import smtplib
from email.mime.text import MIMEText

def vericek():

	site  = requests.get("https://www.trakya.edu.tr/yemek-listesi/",headers={'User-Agent': 'Mozilla/5.0'})
	soup = BeautifulSoup(site.text, 'html.parser')
	sonuclar = soup.find_all('span',attrs = {'class' : 'text-nowrap'})
	metin = ""
	for i in sonuclar[0:5]:
		metin = metin + i.text +"\n"
	return metin
def mailgonder():
	mailadresleri=maiileriadreslerioku()
	konu = date.today().strftime('%d/%m/%Y') + " Tarihli Yemek Listesi "
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login("ogrencidagitimsistemi@gmail.com", "trakyauniversitesi")
	text = vericek()

	for mailler in mailadresleri:	
		fromx = 'ogrencidagitimsistemi@gmail.com'
		msg = MIMEText(text)
		msg['Subject'] = konu
		msg['From'] = fromx
		msg['To'] = mailler
		server.sendmail("ogrencidagitimsistemi@gmail.com",mailler,msg.as_string())	
	server.close()
	#threading.Timer(86400,mailgonder).start()

def maiileriadreslerioku():
	dosyaac = open("mail_listesi.txt", "r")
	mailler=dosyaac.readlines()		
	dosyaac.close()
	return mailler

mailgonder()
