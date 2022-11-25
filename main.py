from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.recycleview import RecycleView

from kivymd.uix.button import  MDFlatButton
from kivy.properties import  StringProperty
from kivymd.uix.card import MDCardSwipe, MDCard

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout

from kivymd.uix.label import MDLabel

from kivymd.uix.selectioncontrol import MDCheckbox

from kivymd.uix.dialog import MDDialog


from kivy.uix.image import Image


from kivy.storage.jsonstore import JsonStore


from datetime import datetime
import threading

from kivy.utils import platform
from kivymd.toast import toast

from kivy.clock import mainthread

import webbrowser


from scraper import *

if platform == "linux":
    from kivy.core.window import Window
    Window.size = (450, 740)

welcome_string = """
    Questa App ti può aiutare a tenere sotto controllo lo stato dei Bandi promossi dalla [b]Regione Sardegna [/b] e dalle sue agenzie.

    Come prima cosa imposta da quali fonti vuoi scaricare una lista di bandi salvati come "in corso".

    Dopo aver scaricato i [b]bandi[/b], potrai trovarli nella pagina Bandi, accessibile dal menù in alto a sinistra.

    Se non trovi la tua fonte preferita manda un email con l'indirizzo web che vorresti monitorare a teonactl@hotmail.it specificando l'oggetto FONTE_BANDI.


"""
info_string = """
[b]Autore[/b] teonactl
[b]Mail[/b] teonactl@hotmail.it
[b]Source[/b] https://github.com/teonactl/BandiSardegna
"""
Builder.load_file("screen1.kv")
Builder.load_file("screen2.kv")
Builder.load_file("screen3.kv")


store = JsonStore('db.json')

class Content(MDBoxLayout):
    pass
class Welcome(MDBoxLayout):
    text = StringProperty(welcome_string)

class Info(MDBoxLayout):
    text = StringProperty(info_string)

class MyCard(MDCard):
    date_str = StringProperty()
    oggetto = StringProperty()
    link = StringProperty()
    color = StringProperty("red")#random valid color , needed for initialization of param
    fonte = StringProperty()
    img = StringProperty()
    uid = StringProperty()
   
class MyButt(MDFlatButton):
    link = StringProperty()


class MainScreen(MDScreen):
    pass

class RecycleViewer(RecycleView):
    def __init__(self, **kwargs):
        super(RecycleViewer, self).__init__(**kwargs)
        #self.data = store["bandi_list"]
        self.update()
    def update(self):
        bl = []
        for  b in store["bandi_list"] :
            o = {}
            scadenza = datetime.fromtimestamp(b["fine"]).strftime("%d/%m/%Y") if datetime.fromtimestamp(b["fine"]).strftime("%d/%m/%Y") != "01/01/2099" else "[b]SOSPESO[/b]"
            o["date_str"] = "Inizio: "+datetime.fromtimestamp(b["inizio"]).strftime("%d/%m/%Y")+"\n"+ "Scadenza: "+scadenza
            o["oggetto"] = b["oggetto"]
            o["color"] =b["color"]
            o["fonte"] = b["fonte"].replace("_", " ").title()
            o["link"] = b["link"]
            o["img"] = b["fonte"]
            o["uid"] =b["uid"]
            bl.append(o)
        self.data = bl
        self.scroll_y=1
        if len(bl):
            store["db"]["initiated"]= True
            store.store_sync()
            #print("new-data upd-->",len(self.data))

    def update_from_data(self, mydata):

        bl = []
        for  b in mydata :
            o = {}
            scadenza = datetime.fromtimestamp(b["fine"]).strftime("%d/%m/%Y") if datetime.fromtimestamp(b["fine"]).strftime("%d/%m/%Y") != "01/01/2099" else "[b]SOSPESO[/b]"
            o["date_str"] = "Inizio: "+datetime.fromtimestamp(b["inizio"]).strftime("%d/%m/%Y")+"\n"+ "Scadenza: "+scadenza
            o["oggetto"] = b["oggetto"]
            o["color"] =b["color"]
            o["fonte"] = b["fonte"].replace("_", " ").title()
            o["link"] = b["link"]
            o["img"] = b["fonte"]
            o["uid"] =b["uid"]

            bl.append(o)
        self.data = bl
        #print("new-data upd-data-->",len(self.data))
        self.scroll_y=1


    def on_touch_down(self, touch):
        if touch.y > 679.0:
            return False
        return super(RecycleView, self).on_touch_down(touch) #pass the touch on



class BandiApp(MDApp):
    def __init__(self, **kwargs):
        super(BandiApp, self).__init__(**kwargs)
#        self.theme_cls.theme_style = store["style"]

    def build(self):
        self.theme_cls.material_style = "M3"  
        self.store = store 
        self.wb = webbrowser.open
        self.theme_cls.primary_palette = "LightGreen"
        self.theme_cls.primary_hue = "100"
        self.theme_cls.accent_palette = "Green"
        self.s_dialog = None
        self.i_dialog = None
        self.w_dialog = None
        return MainScreen()

    def change_light(self):
        #BUGGED!!!
        store.store_load()
        print("change_light")

        if store["style"] == "Light":
            self.theme_cls.theme_style = "Dark"
            store.store_put("style","Dark")
        else:
            self.theme_cls.theme_style = "Light"
            store.store_put("style","Light")
        store.store_sync()
        self.root.ids.bandi_scr.ids.scroller.update()


    def on_start(self):
        if not store["db"]["initiated"]:
            #print("Not Initiated, going to Fonti Page")
            self.populate_fonti()
            self.root.ids.screen_manager.current="fonti_scr"
            self.root.ids.topbar.disabled = True
            self.root.ids.nav_id.children[0].children[0].children[0].children[2].disabled = True
            self.welcome_dialog()

        else: 
            self.root.ids.screen_manager.current="bandi_scr"
 
    def open_web(self, but):
        webbrowser.open(but.link.strip())
    def openmenu(self):
        #print("pressedMENUUU")
        self.root.ids.nav_drawer.set_state("open")
        return True

    def populate_fonti(self):
        #print(self.root.ids.fonti_scr.ids)
        main_box = self.root.ids.fonti_scr.ids.fonti_list
        main_box.clear_widgets()
        desc_row = MDBoxLayout(orientation="horizontal", size_hint =(1,.4))
        desc = MDLabel(text="Scegli le fonti dei bandi ed aggiorna per scaricarli.")
        desc_row.add_widget(desc)
        main_box.add_widget(desc_row)
        for f  in store["fonti"]:
            row = MDBoxLayout( id=f"{f}_box", orientation="horizontal", size_hint =(1,.2))
            fonte_name = MDLabel(text= f.replace("_"," ").title())
            fonte_check = MDCheckbox(id=f"{f}_check", active=store["fonti"][f])
            row.add_widget(fonte_name)
            row.add_widget(fonte_check)
            main_box.add_widget(row)
        f_l = MDFloatLayout()
        conf_button = MDFlatButton(line_color= self.theme_cls.primary_light, text = "Aggiorna i bandi", on_release=self.wait_fonti, pos_hint={"center_y": .5 ,"center_x": .5})
        f_l.add_widget(conf_button)
        main_box.add_widget(f_l)


    def wait_fonti(self,b):
        #print("BUTTON??-->",b)
        fonti_dic = {}
        for item in b.parent.parent.children:
            for c in item.children:
                #print("C-->",c)
                if isinstance(c, MDCheckbox):
                    fonti_dic[c.id[0:-6]]= False if c.state == "normal" else True
        #print("Fonti_dic =",fonti_dic)
        if sum([fonti_dic[i] for i in fonti_dic])==0:
            toast("Seleziona almeno una fonte!")
            return

        store["fonti"]=fonti_dic
        store.store_sync()

        self.root.ids.screen_manager.current = "wait_scr"
        threading.Thread(target=self.aggiorna_fonti, args=(b,fonti_dic,)).start()

    @mainthread
    def change_scr(self,scr_name):
        self.root.ids.screen_manager.current = scr_name
    @mainthread
    def toast_m(self,text):
        toast(text)
    @mainthread
    def prepare_graphics(self):

        self.root.ids.nav_id.children[0].children[0].children[0].children[2].disabled = False
        self.root.ids.topbar.disabled = False
        self.root.ids.bandi_scr.ids.scroller.update()
        self.change_scr("bandi_scr")

    def aggiorna_fonti(self, b, fonti_dic):
        bandi_list = []
        for k in fonti_dic:
            if fonti_dic[k]==True:
                self.toast_m("Scaricando da "+ k.replace("_", " ").title()+"...")
                bandi_list =  bandi_list +  eval(f"{k}()")
        store.store_put("bandi_list", [])
        store.store_put("bandi_list",bandi_list)
        store.store_sync()
        #print(f"{len(store['bandi_list'])} Bandi in -->")
        self.prepare_graphics()

    def change_mode(self):
        self.root.ids.screen_manager.current = "wait_scr"

        store.store_load()
        #print("sort-clock-descending", str(b.icon) == "sort-clock-descending")
        if store["v_mode"] == "sort-clock-descending":
            #print("ifff")
            store.store_put("v_mode", "sort-clock-ascending")
            store.store_sync()
            bandi_list = sorted( self.store["bandi_list"], key=lambda bando: bando['inizio'],reverse = True) 
        #print(self.root.ids.topbar.title)


        else:
            #print("else-")
            store.store_put("v_mode", "sort-clock-descending")
            store.store_sync()

            bandi_list = sorted( self.store["bandi_list"], key=lambda bando: bando['fine'],reverse = False) 
        store.store_put("bandi_list", bandi_list)
        store.store_sync()
        self.root.ids.bandi_scr.ids.scroller.update()
        self.root.ids.screen_manager.current = "bandi_scr"




    def delete_item(self, item):
        #print("delete_item-->",item.uid)
        self.root.ids.screen_manager.current = "wait_scr"

        store.store_load()
        bl = []
        for b in store["bandi_list"]:
            if not b["uid"] == item.uid:
                bl.append(b)
        store.store_put("bandi_list", bl)
        store.store_sync()

        self.root.ids.bandi_scr.ids.scroller.update()
        self.root.ids.screen_manager.current = "bandi_scr"
        #print(self.root.ids.topbar.title)
        self.root.ids.topbar.title = f"{len(store['bandi_list'])} Bandi"
    

    def filtra_bandi(self, but):
        self.root.ids.screen_manager.current = "wait_scr"
        query = but.parent.parent.parent.parent.children[0].children[2].children[0].children[0].text
        store.store_load()
        bl = [] 
        for b in store["bandi_list"]:
            if query.strip().lower() in b["oggetto"].lower():
                bl.append(b)
        bl = sorted( bl, key=lambda bando: bando['fine'],reverse = True if store["v_mode"] == "sort-clock-ascending" else False ) 
        self.s_dialog.dismiss()
        self.root.ids.bandi_scr.ids.scroller.update_from_data(bl)
        n_finding = len(bl)
        store.store_sync()

        self.root.ids.screen_manager.current = "bandi_scr"
        #print(self.root.ids.topbar.title)
        if query != "":
            self.root.ids.topbar.title = f"{n_finding} / {len(store['bandi_list'])} Bandi"


    def search_dialog(self):
        if not self.s_dialog:
            self.s_dialog = MDDialog(
                title="Inserisci una parola chiave per cercare tra i bandi",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="Cerca",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release = self.filtra_bandi
                    ),
                ],
            )
        self.s_dialog.open()

    def welcome_dialog(self):
        #print(self.root.size)
        if not self.w_dialog:
            self.w_dialog = MDDialog(
                title="Benvenuto",
                type="custom",
                size= self.root.size,
                content_cls=Welcome(),
                buttons=[],
            )
        self.w_dialog.open()
    def info(self):
        if not self.i_dialog:
            self.i_dialog = MDDialog(
                title="Informazioni",
                type="custom",
                size= self.root.size,
                content_cls=Info(),
                buttons=[],
            )
        self.i_dialog.open()


if __name__ == "__main__":
    BandiApp().run()