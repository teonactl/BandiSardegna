import requests
import bs4
from bs4 import BeautifulSoup
from datetime import datetime
import uuid


def sardegna_agricoltura():
	BANDI = []
	baseurl = "https://www.sardegnaagricoltura.it/bandi/"
	pager_url = "https://www.sardegnaagricoltura.it/index.php?xsl=2734&tdoc=&s=14&v=9&c=3501&n=10&o=&b=&va=&idcatdatelimit=4953,4939,4922&p=" #"11&f=110"
	page = requests.get(baseurl)
	soup = BeautifulSoup(page.content, "html.parser")
	pager_container = soup.find("div", class_="paginazione-div2")
	pager_n = pager_container.text.split("-")[1].split(" ")[0]

	for p in range(int(pager_n)):
		page = p+1
		page_url = pager_url +str(page) + "&f="+str(page)+"0"   #"11&f=110"
		page_n = requests.get(page_url)
		soup = BeautifulSoup(page_n.content, "html.parser")
		container = soup.find_all("div", class_="ext-center half-lined")
		
		for el in container:
			bando = {}
			anc = el.findChildren("a")
			link = anc[0]["href"]
			bando["link"] = "https://www.sardegnaagricoltura.it" + link
			oggetto = anc[0].text
			bando["oggetto"] = oggetto
			span = el.findChildren("span", {"class":"title10"})[0]
			ente = span.text
			bando["ente"] = ente
			datecont = el.findChildren("div", {"class": "ext-center"})[2]
			basedate = datecont.text.split("Pubblicazione online: ")
			bando["inizio"] = datetime.strptime(basedate[1].split(" - ")[0].strip() , "%d/%m/%Y").timestamp()
			if "Rettifica" in basedate[1]:
				bando["fine"] = datetime.strptime( basedate[1].split("Rettifica:")[1].strip(), "%d/%m/%Y").timestamp()
			if len(basedate[1].split(" - ")) > 1:
				try: 
					bando["fine"] = datetime.strptime(basedate[1].split(" - ")[1].split(":")[1].strip(), "%d/%m/%Y %H").timestamp()
				except Exception :
					bando["fine"] = datetime.strptime(basedate[1].split(" - ")[1].split(":")[1].strip() , "%d/%m/%Y").timestamp()
			else :
				bando["fine"]= datetime.strptime("01/01/1970",  "%d/%m/%Y").timestamp()
				
			bando["fonte"] = "sardegna_agricoltura"
			bando["color"]= "greenyellow"
			bando["uid"] = str(uuid.uuid1())
			BANDI.append(bando)
	return BANDI


def sardegna_psr():
	BANDI = []
	baseurl = "https://sardegnapsr.it/bandi/?wpv-wpcf-stato-bando=aperto"
	url_pager = "&wpv_paged="
	page = requests.get(baseurl)
	soup = BeautifulSoup(page.content, "html.parser")
	pager_container = soup.find_all("li", class_="wpv-pagination-nav-links-item")
	for  i in range(len(pager_container)):
		page = requests.get(baseurl+url_pager+str(i+1)+"&wpv_view_count=65")
		soup = BeautifulSoup(page.content, "html.parser")
		container = soup.find_all("div", class_="card-bandi")
		for card in container:
			bando = {}
			bando["oggetto"] = card.findChildren("p", {"class":"card-text"})[0].text.strip()
			for s in card.findChildren("div", {"class": "col"}):
				basedate = s.text.split("Data pubblicazione:")
				if not len(basedate)>1: continue;
				basedate = basedate[1]
				inizio = basedate.split("\n")[0].strip()  
				resto = basedate.split("\n")[1].split("/n")
				if len(resto)>=1 :
					fine = resto[0].split(":")[1].strip() if resto[0].split(":")[1].strip() != "SOSPESO" else "01/01/1970"
				proroga = basedate.split("\n")[2].split(":")[1].strip() if basedate.split("\n")[2].strip() != "" else "01/01/1970"
			bando["inizio"] = datetime.strptime(inizio, "%d/%m/%Y").timestamp()
			bando["fine"] = datetime.strptime(fine, "%d/%m/%Y").timestamp() if datetime.strptime(fine, "%d/%m/%Y").timestamp() > datetime.now().timestamp() else datetime.strptime(proroga, "%d/%m/%Y").timestamp()
			bando ["proroga"] = datetime.strptime(proroga, "%d/%m/%Y").timestamp()
			bando["fonte"] = "sardegna_psr"
			anc = card.findChildren("a", {"class": "stretched-link"})
			bando["link"] = anc[0]["href"]
			bando["color"]= "aquamarine"
			bando["uid"] = str(uuid.uuid1())

			BANDI.append(bando)
	return BANDI

def regione_sardegna():
	BANDI = []
	baseurl = "https://www.regione.sardegna.it/servizi/cittadino/bandi/"
	page = requests.get(baseurl)
	soup = BeautifulSoup(page.content, "html.parser")
	container = soup.find("ul", class_="list-unstyled articlelist lined")
	for li in container.children:
		bando = {}
		if type(li) == bs4.element.NavigableString:
			continue
		a_tag = li.findChildren("a")
		if not a_tag == []:
			link = a_tag[0]["href"]
		bando["link"] = "https://www.regione.sardegna.it" + link
		ent_and_dates = li.findChildren("span")
		ente = ent_and_dates[0].text
		bando["ente"] = ente.replace("\"", "\'")
		dates = li.findChildren("div")
		inizio, fine = dates[-2].text.split("-")
		bando["inizio"] = datetime.strptime(inizio.split(":")[1].strip() , "%d/%m/%Y").timestamp()
		try: 
			bando["fine"] = datetime.strptime(fine.split(":")[1].strip(), "%d/%m/%Y %H").timestamp()
		except Exception :
			bando["fine"] = datetime.strptime(inizio.split(":")[1].strip() , "%d/%m/%Y").timestamp()
		bando["fonte"] = "regione_sardegna"
		bando["oggetto"]=li.text.split("Oggetto")[1].split("\n")[0][1:].replace("\"", "\'")
		bando["color"]= "yellowgreen"
		bando["uid"] = str(uuid.uuid1())
		BANDI.append(bando)
	return BANDI



