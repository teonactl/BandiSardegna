import requests

import bs4
from bs4 import BeautifulSoup
from datetime import datetime
#from kivy.network.urlrequest import UrlRequest
#from kivymd.toast import toast
#old = {"db": {"initiated": true, "populated": true}, "upd_time": 0, "service_on": false, "fonti": {"sardegna_agricoltura": true, "sardegna_psr": true, "regione_sardegna": true}, "bandi_list": [{"link": "/index.php?xsl=2734&tdoc=&s=14&v=9&c=3613&id=102153&va=", "oggetto": "Procedura per l\u2019acquisizione di manifestazioni d\u2019interesse finalizzata all\u2019assegnazione di cinque lotti di semente certificata di categoria pre\u2013base, base e 2\u00b0 riproduzione delle variet\u00e0 di frumento duro karalis, nuraghe e shardana prodotto presso l\u2019azienda dell\u2019agenzia Agris Sardegna \u201cS. Michele\u201d di Ussana (SU).", "ente": "Agenzia per la ricerca in agricoltura (Agris Sardegna) - Servizio ricerca sui sistemi colturali erbacei", "inizio": 1667948400.0, "fine": 1668686400.0, "fonte": "sardegna_agricoltura", "color": "greenyellow"}, {"link": "/index.php?xsl=2734&tdoc=&s=14&v=9&c=3613&id=101929&va=", "oggetto": "Affidamento, mediante procedura di RDO su SardegnaCAT, dell\u2019incarico professionale di medico competente (n. 2 medici), periodo 01.02.2023 \u2013 31.12.2024, finalizzato alla sorveglianza sanitaria dei dipendenti dell\u2019agenzia Agris, secondo gli adempimenti previsti dal d. lgs. n. 81/08.", "ente": "Agenzia per la ricerca in agricoltura (Agris Sardegna) - Direzione generale", "inizio": 1666735200.0, "fine": 1668510000.0, "fonte": "sardegna_agricoltura", "color": "greenyellow"}, {"link": "/index.php?xsl=2734&tdoc=&s=14&v=9&c=3613&id=101881&va=", "oggetto": "Vendita in piedi di piante per la produzione di legna da cippare presso le aziende del Servizio ricerca sui sistemi colturali erbacei dell\u2019Agris Sardegna", "ente": "Agenzia per la ricerca in agricoltura (Agris Sardegna) - Servizio ricerca sui sistemi colturali erbacei", "inizio": 1666562400.0, "fine": 1667822400.0, "fonte": "sardegna_agricoltura", "color": "greenyellow"}, {"link": "/index.php?xsl=2734&tdoc=&s=14&v=9&c=3613&id=101880&va=", "oggetto": "Vendita di piante per la produzione di legna da cippare e da ardere presso le aziende del Servizio ricerca nell\u2019arboricoltura dell\u2019Agris Sardegna", "ente": "Agenzia per la ricerca in agricoltura (Agris Sardegna) - Servizio ricerca nell\u2019arboricoltura", "inizio": 1666562400.0, "fine": 1667822400.0, "fonte": "sardegna_agricoltura", "color": "greenyellow"}, {"link": "/index.php?xsl=2734&tdoc=&s=14&v=9&c=3613&id=101704&va=", "oggetto": "Determinazione a contrarre per la fornitura di 2 Server da rack Lenovo Think sistem SR650 e un apparato di storage Lenovo Think Sistem serie DE. Avvio della procedura negoziata tramite ricorso al MePA e al confronto concorrenziale delle offerte ricevute a seguito di R.d.O. Importo a base d\u2019asta \u20ac 55.000 + IVA 22%. CIG 9427270D4C.", "ente": "Agenzia regionale per la gestione e l'erogazione degli aiuti in agricoltura (Argea) - Servizio affari legali, amministrativi e personale", "inizio": 1665957600.0, "fine": 1667494800.0, "fonte": "sardegna_agricoltura", "color": "greenyellow"}, {"link": "/index.php?xsl=2734&tdoc=&s=14&v=9&c=3613&id=101679&va=", "oggetto": "Avviso di partecipazione delle PMI regionali alla Manifestazione fieristica Vinitaly 2023.", "ente": "Assessorato dell'agricoltura e riforma agro-pastorale - Direzione generale dell'agricoltura e riforma agro-pastorale - Servizio sviluppo delle filiere agroalimentari e dei mercati", "inizio": 1665698400.0, "fine": 1668553200.0, "fonte": "sardegna_agricoltura", "color": "greenyellow"}, {"link": "/index.php?xsl=2734&tdoc=&s=14&v=9&c=3613&id=101677&va=", "oggetto": "Indagine di mercato - Individuazione degli operatori autorizzati all\u2019esercizio della pesca subacquea professionale interessati a partecipare al piano di monitoraggio scientifico sugli effetti del fermo pesca del riccio di mare e ad attivit\u00e0 sperimentali, di monitoraggio e recupero ambientale\n", "ente": "Agenzia per la ricerca in agricoltura (Agris Sardegna) - Direzione generale", "inizio": 1665698400.0, "fine": 1667775600.0, "fonte": "sardegna_agricoltura", "color": "greenyellow"}, {"link": "/index.php?xsl=2734&tdoc=&s=14&v=9&c=3613&id=101608&va=", "oggetto": "Manifestazione di interesse finalizzata all\u2019accesso al contributo per la \u201cPartecipazione Finale Circuito Allevatoriale Mipaaf \u2013 Verona 2022.\u201d", "ente": "Agenzia per la ricerca in agricoltura (Agris Sardegna) - Servizio ricerca per la qualit\u00e0 e valorizzazione delle produzioni equine", "inizio": 1665525600.0, "fine": 1667127600.0, "fonte": "sardegna_agricoltura", "color": "greenyellow"}, {"link": "/index.php?xsl=2734&tdoc=&s=14&v=9&c=3613&id=102190&va=", "oggetto": "Affidamento, mediante procedura di RDO sul MePa, della fornitura di un'autoclave da pavimento per il laboratorio di microbiologia \u2013 Progetto \u201cBanca Germoplasma Microbico 2021\u201d", "ente": "Agenzia per la ricerca in agricoltura (Agris Sardegna) - Servizio ricerca prodotti di origine animale", "inizio": 1665525600.0, "fine": 1666821600.0, "fonte": "sardegna_agricoltura", "color": "greenyellow"}, {"oggetto": "PSR Sardegna 2014/2020 \u2013 Sottomisura 4.2 \u201cSostegno a investimenti a favore della trasformazione/commercializzazione e/o dello sviluppo dei prodotti agricoli\u201d \u2013 Annualit\u00e0 2022 \u2013 Modifica e riapertura bando 2022", "inizio": 1646262000.0, "fine": 4070905200.0, "proroga": 31532400.0, "fonte": "sardegna_psr", "link": "https://sardegnapsr.it/2022/bando/psr-sardegna-2014-2020-sottomisura-4-2-sostegno-a-investimenti-a-favore-della-trasformazione-commercializzazione-e-o-dello-sviluppo-dei-prodotti-agricoli-annualita-2022-la-domande-possono-es/", "color": "aquamarine"}, {"oggetto": "PSR Sardegna 2014/2020 \u2013 Disposizioni attuative della Misura 1 \u201cTrasferimento di conoscenze e azioni di informazione\u201d \u2013 Sottomisura 1.2 \u2013 \u201cSostegno ad attivit\u00e0 dimostrative e azioni di informazione\u201d \u2013 Tipologia di intervento 1.2.1 \u201cAttivit\u00e0 dimostrative e azioni di informazione\u201d", "inizio": 1499205600.0, "fine": 1659218400.0, "proroga": 1672441200.0, "fonte": "sardegna_psr", "link": "https://sardegnapsr.it/2022/bando/psr-sardegna-2014-2020-disposizioni-attuative-della-misura-1-trasferimento-di-conoscenze-e-azioni-di-informazione-sottomisura-1-2-sostegno-ad-attivita/", "color": "aquamarine"}, {"oggetto": "PSR Sardegna 2014/2020 \u2013 Sottomisura 3.2 \u201cSostegno per attivit\u00e0 di informazione e promozione, svolte da associazioni di produttori nel mercato interno\u201d. Bando pubblico per l\u2019ammissione ai finanziamenti \u2013 Anno 2022", "inizio": 1658268000.0, "fine": 1671058800.0, "proroga": 31532400.0, "fonte": "sardegna_psr", "link": "https://sardegnapsr.it/2022/bando/psr-sardegna-2014-2020-sottomisura-3-2-sostegno-per-attivita-di-informazione-e-promozione-svolte-da-associazioni-di-produttori-nel-mercato-interno-bando-pubblico-per-lammissione-ai-f/", "color": "aquamarine"}, {"oggetto": "PSR Sardegna 2014/2020 \u2013 Sottomisura 3.1. Sostegno alla nuova adesione a regimi di qualit\u00e0. Annualit\u00e0 2022.", "inizio": 1656453600.0, "fine": 1671058800.0, "proroga": 31532400.0, "fonte": "sardegna_psr", "link": "https://sardegnapsr.it/2022/bando/psr-sardegna-2014-2020-sottomisura-3-1-sostegno-alla-nuova-adesione-a-regimi-di-qualita-annualita-2022/", "color": "aquamarine"}, {"oggetto": "PSR Sardegna 2014/2020 \u2013 Sottomisura 4.1 Precision farming e agricoltura conservativa. Annualit\u00e0 2022 \u2013 La presentazione delle domande potr\u00e0 avvenire nel periodo compreso tra il 15/04/2022 e il 16/05/2022", "inizio": 1644447600.0, "fine": 4070905200.0, "proroga": 31532400.0, "fonte": "sardegna_psr", "link": "https://sardegnapsr.it/2022/bando/psr-sardegna-2014-2020-sottomisura-4-1-precision-farming-e-agricoltura-conservativa-annualita-2022-la-presentazione-delle-domande-potra-avvenire-nel-periodo-compreso-tra-il-15-04-2022-e-il-16-05/", "color": "aquamarine"}, {"oggetto": "PSR Sardegna 2014/2020 \u2013 Sottomisura 4.2 \u201cSostegno a investimenti a favore della trasformazione/commercializzazione e/o dello sviluppo dei prodotti agricoli\u201d \u2013 Annualit\u00e0 2022 \u2013 Modifica e riapertura bando 2022", "inizio": 1646262000.0, "fine": 4070905200.0, "proroga": 31532400.0, "fonte": "sardegna_psr", "link": "https://sardegnapsr.it/2022/bando/psr-sardegna-2014-2020-sottomisura-4-2-sostegno-a-investimenti-a-favore-della-trasformazione-commercializzazione-e-o-dello-sviluppo-dei-prodotti-agricoli-annualita-2022-la-domande-possono-es/", "color": "aquamarine"}, {"oggetto": "PSR Sardegna 2014/2020 \u2013 Disposizioni attuative della Misura 1 \u201cTrasferimento di conoscenze e azioni di informazione\u201d \u2013 Sottomisura 1.2 \u2013 \u201cSostegno ad attivit\u00e0 dimostrative e azioni di informazione\u201d \u2013 Tipologia di intervento 1.2.1 \u201cAttivit\u00e0 dimostrative e azioni di informazione\u201d", "inizio": 1499205600.0, "fine": 1659218400.0, "proroga": 1672441200.0, "fonte": "sardegna_psr", "link": "https://sardegnapsr.it/2022/bando/psr-sardegna-2014-2020-disposizioni-attuative-della-misura-1-trasferimento-di-conoscenze-e-azioni-di-informazione-sottomisura-1-2-sostegno-ad-attivita/", "color": "aquamarine"}, {"oggetto": "PSR Sardegna 2014/2020 \u2013 Sottomisura 3.2 \u201cSostegno per attivit\u00e0 di informazione e promozione, svolte da associazioni di produttori nel mercato interno\u201d. Bando pubblico per l\u2019ammissione ai finanziamenti \u2013 Anno 2022", "inizio": 1658268000.0, "fine": 1671058800.0, "proroga": 31532400.0, "fonte": "sardegna_psr", "link": "https://sardegnapsr.it/2022/bando/psr-sardegna-2014-2020-sottomisura-3-2-sostegno-per-attivita-di-informazione-e-promozione-svolte-da-associazioni-di-produttori-nel-mercato-interno-bando-pubblico-per-lammissione-ai-f/", "color": "aquamarine"}, {"oggetto": "PSR Sardegna 2014/2020 \u2013 Sottomisura 3.1. Sostegno alla nuova adesione a regimi di qualit\u00e0. Annualit\u00e0 2022.", "inizio": 1656453600.0, "fine": 1671058800.0, "proroga": 31532400.0, "fonte": "sardegna_psr", "link": "https://sardegnapsr.it/2022/bando/psr-sardegna-2014-2020-sottomisura-3-1-sostegno-alla-nuova-adesione-a-regimi-di-qualita-annualita-2022/", "color": "aquamarine"}, {"oggetto": "PSR Sardegna 2014/2020 \u2013 Sottomisura 4.1 Precision farming e agricoltura conservativa. Annualit\u00e0 2022 \u2013 La presentazione delle domande potr\u00e0 avvenire nel periodo compreso tra il 15/04/2022 e il 16/05/2022", "inizio": 1644447600.0, "fine": 4070905200.0, "proroga": 31532400.0, "fonte": "sardegna_psr", "link": "https://sardegnapsr.it/2022/bando/psr-sardegna-2014-2020-sottomisura-4-1-precision-farming-e-agricoltura-conservativa-annualita-2022-la-presentazione-delle-domande-potra-avvenire-nel-periodo-compreso-tra-il-15-04-2022-e-il-16-05/", "color": "aquamarine"}, {"oggetto": "PSR Sardegna 2014/2020 \u2013 Sottomisura 4.2 \u201cSostegno a investimenti a favore della trasformazione/commercializzazione e/o dello sviluppo dei prodotti agricoli\u201d \u2013 Annualit\u00e0 2022 \u2013 Modifica e riapertura bando 2022", "inizio": 1646262000.0, "fine": 4070905200.0, "proroga": 31532400.0, "fonte": "sardegna_psr", "link": "https://sardegnapsr.it/2022/bando/psr-sardegna-2014-2020-sottomisura-4-2-sostegno-a-investimenti-a-favore-della-trasformazione-commercializzazione-e-o-dello-sviluppo-dei-prodotti-agricoli-annualita-2022-la-domande-possono-es/", "color": "aquamarine"}, {"oggetto": "PSR Sardegna 2014/2020 \u2013 Disposizioni attuative della Misura 1 \u201cTrasferimento di conoscenze e azioni di informazione\u201d \u2013 Sottomisura 1.2 \u2013 \u201cSostegno ad attivit\u00e0 dimostrative e azioni di informazione\u201d \u2013 Tipologia di intervento 1.2.1 \u201cAttivit\u00e0 dimostrative e azioni di informazione\u201d", "inizio": 1499205600.0, "fine": 1659218400.0, "proroga": 1672441200.0, "fonte": "sardegna_psr", "link": "https://sardegnapsr.it/2022/bando/psr-sardegna-2014-2020-disposizioni-attuative-della-misura-1-trasferimento-di-conoscenze-e-azioni-di-informazione-sottomisura-1-2-sostegno-ad-attivita/", "color": "aquamarine"}, {"oggetto": "PSR Sardegna 2014/2020 \u2013 Sottomisura 3.2 \u201cSostegno per attivit\u00e0 di informazione e promozione, svolte da associazioni di produttori nel mercato interno\u201d. Bando pubblico per l\u2019ammissione ai finanziamenti \u2013 Anno 2022", "inizio": 1658268000.0, "fine": 1671058800.0, "proroga": 31532400.0, "fonte": "sardegna_psr", "link": "https://sardegnapsr.it/2022/bando/psr-sardegna-2014-2020-sottomisura-3-2-sostegno-per-attivita-di-informazione-e-promozione-svolte-da-associazioni-di-produttori-nel-mercato-interno-bando-pubblico-per-lammissione-ai-f/", "color": "aquamarine"}, {"oggetto": "PSR Sardegna 2014/2020 \u2013 Sottomisura 3.1. Sostegno alla nuova adesione a regimi di qualit\u00e0. Annualit\u00e0 2022.", "inizio": 1656453600.0, "fine": 1671058800.0, "proroga": 31532400.0, "fonte": "sardegna_psr", "link": "https://sardegnapsr.it/2022/bando/psr-sardegna-2014-2020-sottomisura-3-1-sostegno-alla-nuova-adesione-a-regimi-di-qualita-annualita-2022/", "color": "aquamarine"}, {"oggetto": "PSR Sardegna 2014/2020 \u2013 Sottomisura 4.1 Precision farming e agricoltura conservativa. Annualit\u00e0 2022 \u2013 La presentazione delle domande potr\u00e0 avvenire nel periodo compreso tra il 15/04/2022 e il 16/05/2022", "inizio": 1644447600.0, "fine": 4070905200.0, "proroga": 31532400.0, "fonte": "sardegna_psr", "link": "https://sardegnapsr.it/2022/bando/psr-sardegna-2014-2020-sottomisura-4-1-precision-farming-e-agricoltura-conservativa-annualita-2022-la-presentazione-delle-domande-potra-avvenire-nel-periodo-compreso-tra-il-15-04-2022-e-il-16-05/", "color": "aquamarine"}, {"oggetto": "PSR Sardegna 2014/2020 \u2013 Sottomisura 4.2 \u201cSostegno a investimenti a favore della trasformazione/commercializzazione e/o dello sviluppo dei prodotti agricoli\u201d \u2013 Annualit\u00e0 2022 \u2013 Modifica e riapertura bando 2022", "inizio": 1646262000.0, "fine": 4070905200.0, "proroga": 31532400.0, "fonte": "sardegna_psr", "link": "https://sardegnapsr.it/2022/bando/psr-sardegna-2014-2020-sottomisura-4-2-sostegno-a-investimenti-a-favore-della-trasformazione-commercializzazione-e-o-dello-sviluppo-dei-prodotti-agricoli-annualita-2022-la-domande-possono-es/", "color": "aquamarine"}, {"oggetto": "PSR Sardegna 2014/2020 \u2013 Disposizioni attuative della Misura 1 \u201cTrasferimento di conoscenze e azioni di informazione\u201d \u2013 Sottomisura 1.2 \u2013 \u201cSostegno ad attivit\u00e0 dimostrative e azioni di informazione\u201d \u2013 Tipologia di intervento 1.2.1 \u201cAttivit\u00e0 dimostrative e azioni di informazione\u201d", "inizio": 1499205600.0, "fine": 1659218400.0, "proroga": 1672441200.0, "fonte": "sardegna_psr", "link": "https://sardegnapsr.it/2022/bando/psr-sardegna-2014-2020-disposizioni-attuative-della-misura-1-trasferimento-di-conoscenze-e-azioni-di-informazione-sottomisura-1-2-sostegno-ad-attivita/", "color": "aquamarine"}, {"oggetto": "PSR Sardegna 2014/2020 \u2013 Sottomisura 3.2 \u201cSostegno per attivit\u00e0 di informazione e promozione, svolte da associazioni di produttori nel mercato interno\u201d. Bando pubblico per l\u2019ammissione ai finanziamenti \u2013 Anno 2022", "inizio": 1658268000.0, "fine": 1671058800.0, "proroga": 31532400.0, "fonte": "sardegna_psr", "link": "https://sardegnapsr.it/2022/bando/psr-sardegna-2014-2020-sottomisura-3-2-sostegno-per-attivita-di-informazione-e-promozione-svolte-da-associazioni-di-produttori-nel-mercato-interno-bando-pubblico-per-lammissione-ai-f/", "color": "aquamarine"}, {"oggetto": "PSR Sardegna 2014/2020 \u2013 Sottomisura 3.1. Sostegno alla nuova adesione a regimi di qualit\u00e0. Annualit\u00e0 2022.", "inizio": 1656453600.0, "fine": 1671058800.0, "proroga": 31532400.0, "fonte": "sardegna_psr", "link": "https://sardegnapsr.it/2022/bando/psr-sardegna-2014-2020-sottomisura-3-1-sostegno-alla-nuova-adesione-a-regimi-di-qualita-annualita-2022/", "color": "aquamarine"}, {"oggetto": "PSR Sardegna 2014/2020 \u2013 Sottomisura 4.1 Precision farming e agricoltura conservativa. Annualit\u00e0 2022 \u2013 La presentazione delle domande potr\u00e0 avvenire nel periodo compreso tra il 15/04/2022 e il 16/05/2022", "inizio": 1644447600.0, "fine": 4070905200.0, "proroga": 31532400.0, "fonte": "sardegna_psr", "link": "https://sardegnapsr.it/2022/bando/psr-sardegna-2014-2020-sottomisura-4-1-precision-farming-e-agricoltura-conservativa-annualita-2022-la-presentazione-delle-domande-potra-avvenire-nel-periodo-compreso-tra-il-15-04-2022-e-il-16-05/", "color": "aquamarine"}, {"link": "https://www.regione.sardegna.it/j/v/2599?s=1&v=9&c=46&c1=46&id=102185", "ente": "ASSESSORATO DEL LAVORO, FORMAZIONE PROFESSIONALE, COOPERAZIONE E SICUREZZA SOCIALE - DIREZIONE GENERALE DEL LAVORO, FORMAZIONE PROFESSIONALE, COOPERAZIONE E SICUREZZA SOCIALE - A. SERVIZIO ATTUAZIONE DELLE POLITICHE PER I CITTADINI", "inizio": 1668034800.0, "fine": 1668034800.0, "fonte": "regione_sardegna", "oggetto": " Avviso V^ edizione 2022/2023 Concorso Graziano Deiana. ", "color": "yellowgreen"}, {"link": "https://www.regione.sardegna.it/j/v/2599?s=1&v=9&c=46&c1=46&id=102160", "ente": "ASSESSORATO DELLA PUBBLICA ISTRUZIONE, BENI CULTURALI, INFORMAZIONE, SPETTACOLO E SPORT - DIREZIONE GENERALE DELLA PUBBLICA ISTRUZIONE - SERVIZIO POLITICHE SCOLASTICHE", "inizio": 1667948400.0, "fine": 1669201200.0, "fonte": "regione_sardegna", "oggetto": " Avviso pubblico per manifestazione d\u2019interesse destinato ad associazioni che si occupano di programmi di studi all\u2019estero - Annualit\u00e0 2022.", "color": "yellowgreen"}, {"link": "https://www.regione.sardegna.it/j/v/2599?s=1&v=9&c=46&c1=46&id=101851", "ente": "ASSESSORATO DEGLI ENTI LOCALI, FINANZE E URBANISTICA - DIREZIONE GENERALE ENTI LOCALI E FINANZE - SERVIZIO DEMANIO E PATRIMONIO E AUTONOMIE LOCALI DI SASSARI E OLBIA TEMPIO", "inizio": 1666562400.0, "fine": 1671192000.0, "fonte": "regione_sardegna", "oggetto": " Alienazione mediante gara pubblica con il sistema delle offerte segrete ai sensi dell\u2019art. 1 comma 5 L.R. 35/1995 e art. 73 lett. c) RD 827/1924, di n. 8 immobili di propriet\u00e0 regionale, articolata in 8 lotti ubicati nei Comuni di Sassari, Alghero ed Uri.", "color": "yellowgreen"}, {"link": "https://www.regione.sardegna.it/j/v/2599?s=1&v=9&c=46&c1=46&id=101835", "ente": "COMMISSARIO DI GOVERNO PER IL CONTRASTO DEL DISSESTO IDROGEOLOGICO NELLA REGIONE SARDEGNA", "inizio": 1666303200.0, "fine": 1666303200.0, "fonte": "regione_sardegna", "oggetto": " Procedura espropriativa preordinata all\u2019acquisizione delle aree occorrenti per l\u2019esecuzione delle \u201c20IR002/G9 - Opere di difesa idraulica della citt\u00e0 di Bosa (OR) \u2013 Primo lotto - Opere previste nella sola sponda destra del Fiume Temo\u201d.", "color": "yellowgreen"}, {"link": "https://www.regione.sardegna.it/j/v/2599?s=1&v=9&c=46&c1=46&id=101739", "ente": "ASSESSORATO DEGLI ENTI LOCALI, FINANZE E URBANISTICA - DIREZIONE GENERALE ENTI LOCALI E FINANZE - SERVIZIO DEMANIO E PATRIMONIO E AUTONOMIE LOCALI DI SASSARI E OLBIA TEMPIO", "inizio": 1666130400.0, "fine": 1668772800.0, "fonte": "regione_sardegna", "oggetto": " Bando di gara per l\u2019assegnazione in locazione ad uso commerciale per la durata di anni 7 rinnovabili per ulteriori 7 anni, mediante gara ad offerte segrete ex art. 73, lett.c) del R.D. 23/05 /1924 n. 827, dell\u2019immobile di propriet\u00e0 regionale sito in Comune di Sassari, localit\u00e0 Villa Assunta, Piazza Beata Vergine Maria n. 1, identificato al foglio 105 mappali 169 sub 2.", "color": "yellowgreen"}, {"link": "https://www.regione.sardegna.it/j/v/2599?s=1&v=9&c=46&c1=46&id=96897", "ente": "ASSESSORATO DELLA PUBBLICA ISTRUZIONE, BENI CULTURALI, INFORMAZIONE, SPETTACOLO E SPORT - DIREZIONE GENERALE DEI BENI CULTURALI, INFORMAZIONE, SPETTACOLO E SPORT - SERVIZIO LINGUA E CULTURA SARDA", "inizio": 1638226800.0, "fine": 1671534000.0, "fonte": "regione_sardegna", "oggetto": " Legge regionale 3 luglio 2018, n. 22, artt. 9 e 16 'Disciplina della politica linguistica regionale'. Avviso pubblico per la costituzione dell\u2019elenco regionale docenti di lingua sarda, catalana di Alghero, gallurese, sassarese e tabarchino per l\u2019anno scolastico 2021/2022.", "color": "yellowgreen"}]}
#default_config = {"sardegna_agricoltura": true,"sardegna_psr":false,"regione_sardegna":false}
#init_db = {"db": {"initiated": false, "populated": false},"v_mode": "sort-clock-ascending", "fonti": {"sardegna_agricoltura": false,"sardegna_psr":false,"regione_sardegna":false}, "bandi_list": []}
#from kivy.clock import mainthread

#@mainthread
#def toast_m(text):
#	toast(text)

def sardegna_agricoltura():
	#toast_m("Inizio a scaricare da Sardegna Agricoltura...")
	BANDI = []
	baseurl = "https://www.sardegnaagricoltura.it/bandi/"
	pager_url = "https://www.sardegnaagricoltura.it/index.php?xsl=2734&tdoc=&s=14&v=9&c=3501&n=10&o=&b=&va=&idcatdatelimit=4953,4939,4922&p=" #"11&f=110"
	page = requests.get(baseurl)
	soup = BeautifulSoup(page.content, "html.parser")
	#print(page.content)
	pager_container = soup.find("div", class_="paginazione-div2")
	#print("pager_container", pager_container.text.split("-")[1].split(" ")[0])
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
			#print("LINK-->", link)
			bando["link"] = "https://www.sardegnaagricoltura.it" + link
			oggetto = anc[0].text
			bando["oggetto"] = oggetto
			span = el.findChildren("span", {"class":"title10"})[0]
			ente = span.text
			bando["ente"] = ente
			datecont = el.findChildren("div", {"class": "ext-center"})[2]
			#print(datecont.text)
			basedate = datecont.text.split("Pubblicazione online: ")
			#print("BASEDATE-->", basedate[1])
			#print(basedate[1].split(" - ")[1].split(":")[1].strip())
			bando["inizio"] = datetime.strptime(basedate[1].split(" - ")[0].strip() , "%d/%m/%Y").timestamp()
			#print("inizio",bando["inizio"])
			if "Rettifica" in basedate[1]:
				#print("REtt-----__")
				#print(basedate[1].split("Rettifica:")[1])
				bando["fine"] = datetime.strptime( basedate[1].split("Rettifica:")[1].strip(), "%d/%m/%Y").timestamp()
			if len(basedate[1].split(" - ")) > 1:
				try: 
					bando["fine"] = datetime.strptime(basedate[1].split(" - ")[1].split(":")[1].strip(), "%d/%m/%Y %H").timestamp()
				except Exception :
					bando["fine"] = datetime.strptime(basedate[1].split(" - ")[1].split(":")[1].strip() , "%d/%m/%Y").timestamp()
				#print("fine", bando["fine"])
			else :
				bando["fine"]= datetime.strptime("01/01/2099",  "%d/%m/%Y").timestamp()
				
			bando["fonte"] = "sardegna_agricoltura"
			bando["color"]= "greenyellow"

			BANDI.append(bando)
	#	toast_m("Finito!")
	return BANDI







def sardegna_psr():
#	toast_m("Inizio a scaricare da PSR...!")

	BANDI = []
	baseurl = "https://sardegnapsr.it/bandi/?wpv-wpcf-stato-bando=aperto"
	url_pager = "&wpv_paged="
	page = requests.get(baseurl)

	soup = BeautifulSoup(page.content, "html.parser")
	pager_container = soup.find_all("li", class_="wpv-pagination-nav-links-item")
	#print ("PAGINE: ",len(pager_container))
	for  i in range(len(pager_container)):
		page = requests.get(baseurl+url_pager+str(i+1)+"&wpv_view_count=65")
		#print("bandi from page--> ",baseurl+url_pager+str(i+1))

		soup = BeautifulSoup(page.content, "html.parser")


		container = soup.find_all("div", class_="card-bandi")
		#print("bandi: ", len(container))
		for card in container:
			bando = {}

			#print(card.findChildren("p", {"class":"card-text"})[0].text)
			bando["oggetto"] = card.findChildren("p", {"class":"card-text"})[0].text.strip()
			for s in card.findChildren("div", {"class": "col"}):
				basedate = s.text.split("Data pubblicazione:")
				if not len(basedate)>1: continue;
				basedate = basedate[1]
				inizio = basedate.split("\n")[0].strip()  
				resto = basedate.split("\n")[1].split("/n")
				if len(resto)>=1 :
					fine = resto[0].split(":")[1].strip() if resto[0].split(":")[1].strip() != "SOSPESO" else "01/01/2099"
				proroga = basedate.split("\n")[2].split(":")[1].strip() if basedate.split("\n")[2].strip() != "" else "01/01/2099"

				#print(s)
				#print("INIZIO",inizio)
				#print("FINE",fine)
				#print("PROROGA",proroga)
			bando["inizio"] = datetime.strptime(inizio, "%d/%m/%Y").timestamp()
			bando["fine"] = datetime.strptime(fine, "%d/%m/%Y").timestamp() if datetime.strptime(fine, "%d/%m/%Y").timestamp() > datetime.now().timestamp() else datetime.strptime(proroga, "%d/%m/%Y").timestamp()
			bando ["proroga"] = datetime.strptime(proroga, "%d/%m/%Y").timestamp()
			bando["fonte"] = "sardegna_psr"

			anc = card.findChildren("a", {"class": "stretched-link"})
			#print(anc[0]["href"])
			bando["link"] = anc[0]["href"]
			bando["color"]= "aquamarine"
			BANDI.append(bando)
#	toast_m("Finito!")
	return BANDI

def regione_sardegna():
#	toast_m("Inizio a scaricare da Regione Sardegna...")
	BANDI = []
	baseurl = "https://www.regione.sardegna.it/servizi/cittadino/bandi/"
	page = requests.get(baseurl)
	soup = BeautifulSoup(page.content, "html.parser")
	container = soup.find("ul", class_="list-unstyled articlelist lined")



	for li in container.children:
		bando = {}
		if type(li) == bs4.element.NavigableString:
			continue
	#LINK
		a_tag = li.findChildren("a")
		if not a_tag == []:
			link = a_tag[0]["href"]
		#print(a_tag[0]["href"])
		bando["link"] = "https://www.regione.sardegna.it" + link
#ENTE e DATE
		ent_and_dates = li.findChildren("span")
		ente = ent_and_dates[0].text
		#print(ente)
		bando["ente"] = ente.replace("\"", "\'")

		dates = li.findChildren("div")
		inizio, fine = dates[-2].text.split("-")
		bando["inizio"] = datetime.strptime(inizio.split(":")[1].strip() , "%d/%m/%Y").timestamp()

		try: 
			bando["fine"] = datetime.strptime(fine.split(":")[1].strip(), "%d/%m/%Y %H").timestamp()
		except Exception :
			bando["fine"] = datetime.strptime(inizio.split(":")[1].strip() , "%d/%m/%Y").timestamp()
		bando["fonte"] = "regione_sardegna"

	#OGGETTO
		#print(li.text.split("Oggetto")[1].split("\n")[0][1:])
		bando["oggetto"]=li.text.split("Oggetto")[1].split("\n")[0][1:].replace("\"", "\'")
		bando["color"]= "yellowgreen"

		BANDI.append(bando)
#	toast_m("Finito!")
	return BANDI



