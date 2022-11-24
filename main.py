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



from kivy.uix.image import Image


from kivy.storage.jsonstore import JsonStore


from datetime import datetime
import threading

from kivy.utils import platform
from kivymd.toast import toast

from kivy.clock import mainthread




from scraper import *

if platform == "linux":
    from kivy.core.window import Window
    Window.size = (450, 740)



Builder.load_file("screen1.kv")
Builder.load_file("screen2.kv")
Builder.load_file("screen3.kv")


store = JsonStore('db.json')


class MyCard(MDCard):
    date_str = StringProperty()
    oggetto = StringProperty()
    link = StringProperty()
    color = StringProperty("red")#random valid color , needed for initialization of param
    fonte = StringProperty()
    img = StringProperty()
   
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
            o["date_str"] = "Inizio: "+datetime.fromtimestamp(b["inizio"]).strftime("%d/%m/%Y")+"\n"+ "Scadenza: "+datetime.fromtimestamp(b["fine"]).strftime("%d/%m/%Y")
            o["oggetto"] = b["oggetto"]
            o["color"] =b["color"]
            o["fonte"] = b["fonte"].replace("_", " ").title()
            o["link"] = b["link"]
            o["img"] = b["fonte"]
            bl.append(o)
        self.data = bl
        self.scroll_y=1


class BandiApp(MDApp):
    def build(self):
        self.theme_cls.material_style = "M3"  
        self.store = store 
        #self.theme_cls.theme_style = "Dark"
        return MainScreen()

    def on_start(self):
        if not store["db"]["initiated"]:
            print("Not Initiated, going to Fonti Page")
            self.populate_fonti()
            self.root.ids.screen_manager.current="fonti_scr"
            self.root.ids.topbar.disabled = True

        else: 
            self.root.ids.screen_manager.current="bandi_scr"


    def populate_fonti(self):
        #print(self.root.ids.fonti_scr.ids)
        main_box = self.root.ids.fonti_scr.ids.fonti_list
        main_box.clear_widgets()
        desc_row = MDBoxLayout(orientation="horizontal", size_hint =(1,.4))
        desc = MDLabel(text="Scegli le fonti dei bandi ed aggiorna per scaricare nuovi bandi.")
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
        conf_button = MDFlatButton( text = "Aggiorna i bandi", on_release=self.wait_fonti, pos_hint={"center_y": .5 ,"center_x": .5})
        f_l.add_widget(conf_button)
        main_box.add_widget(f_l)
        store["db"]["initiated"]= True
        store.store_sync()

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
  

    def aggiorna_fonti(self, b, fonti_dic):
        bandi_list = []
        for k in fonti_dic:
            if fonti_dic[k]==True:
                self.toast_m("Scaricando da "+ k.replace("_", " ").title()+"...")
                #print("UPD")
                #print(f"fonte {k}-->" ,eval(f"{k}()"))
                bandi_list =  bandi_list +  eval(f"{k}()")
        #bandi_list = sorted( bandi_list, key=lambda but: but['fine'],reverse = False) 
        store.store_put("bandi_list", [])
        store.store_put("bandi_list",bandi_list)
        store.store_sync()
        print(f"{len(store['bandi_list'])} Bandi in -->")
        self.root.ids.topbar.disabled = False
        self.root.ids.bandi_scr.ids.scroller.update()
        self.change_scr("bandi_scr")

    def change_mode(self):
        self.root.ids.screen_manager.current = "wait_scr"

        store.store_load()
        #print("sort-clock-descending", str(b.icon) == "sort-clock-descending")
        if store["v_mode"] == "sort-clock-descending":
            #print("ifff")
            store.store_put("v_mode", "sort-clock-ascending")
            store.store_sync()

            bandi_list = sorted( self.store["bandi_list"], key=lambda but: but['inizio'],reverse = True) 


        else:
            #print("else-")
            store.store_put("v_mode", "sort-clock-descending")
            store.store_sync()

            bandi_list = sorted( self.store["bandi_list"], key=lambda but: but['fine'],reverse = False) 
        store.store_put("bandi_list", bandi_list)
        store.store_sync()
        self.root.ids.bandi_scr.ids.scroller.update()
        self.root.ids.screen_manager.current = "bandi_scr"




    def delete_item(self, item):
        print("delete_item-->",item)

BandiApp().run()