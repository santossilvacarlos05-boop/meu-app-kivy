import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.clock import Clock
from kivy.utils import platform

from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivymd.uix.card import MDCard

from plyer import camera, storagepath

# Interface KV embutida
KV = '''
ScreenManager:
    LoginScreen:
    HomeScreen:
    CameraScreen:
    HistoryScreen:

<LoginScreen>:
    name: 'login'
    MDFloatLayout:
        md_bg_color: 0.1, 0.1, 0.12, 1

        MDCard:
            size_hint: 0.85, 0.7
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            elevation: 4
            padding: 20
            spacing: 20
            orientation: 'vertical'
            md_bg_color: 0.15, 0.15, 0.18, 1

            MDIconButton:
                icon: 'lock-check'
                user_font_size: '64sp'
                pos_hint: {'center_x': 0.5}
                theme_text_color: 'Custom'
                text_color: 0, 0.8, 0.8, 1

            MDLabel:
                text: 'Fechadura Inteligente'
                font_style: 'H5'
                halign: 'center'
                theme_text_color: 'Custom'
                text_color: 1, 1, 1, 1

            MDTextField:
                id: pin_input
                hint_text: 'Digite o PIN (Ex: 1234)'
                password: True
                max_text_length: 6
                input_filter: 'int'
                pos_hint: {'center_x': 0.5}
                theme_text_color: 'Custom'
                text_color_normal: 1, 1, 1, 1

            MDRaisedButton:
                text: 'ENTRAR'
                pos_hint: {'center_x': 0.5}
                md_bg_color: 0, 0.6, 0.8, 1
                on_release: root.verify_pin()

            MDRoundFlatIconButton:
                text: 'Biometria / Digital'
                icon: 'fingerprint'
                pos_hint: {'center_x': 0.5}
                on_release: root.authenticate_biometrics()

<HomeScreen>:
    name: 'home'
    MDFloatLayout:
        md_bg_color: 0.1, 0.1, 0.12, 1

        MDTopAppBar:
            title: 'Painel de Controle'
            pos_hint: {'top': 1}
            right_action_items: [['logout', lambda x: root.logout()]]
            md_bg_color: 0.15, 0.15, 0.18, 1

        MDIconButton:
            id: lock_button
            icon: 'lock'
            user_font_size: '100sp'
            pos_hint: {'center_x': 0.5, 'center_y': 0.6}
            theme_text_color: 'Custom'
            text_color: 0.9, 0.2, 0.2, 1
            on_release: root.toggle_lock()

        MDLabel:
            id: status_label
            text: 'PORTA TRANCADA'
            font_style: 'H6'
            halign: 'center'
            pos_hint: {'center_y': 0.42}
            theme_text_color: 'Custom'
            text_color: 0.9, 0.2, 0.2, 1

        MDRaisedButton:
            text: 'Capturar Foto de Acesso'
            icon: 'camera'
            pos_hint: {'center_x': 0.5, 'center_y': 0.25}
            md_bg_color: 0, 0.6, 0.8, 1
            on_release: app.root.current = 'camera'

        MDRoundFlatIconButton:
            text: 'Histórico de Acessos'
            icon: 'history'
            pos_hint: {'center_x': 0.5, 'center_y': 0.15}
            on_release: app.root.current = 'history'

<CameraScreen>:
    name: 'camera'
    MDFloatLayout:
        md_bg_color: 0, 0, 0, 1

        MDLabel:
            text: 'Câmera do Dispositivo'
            halign: 'center'
            pos_hint: {'center_y': 0.6}
            theme_text_color: 'Custom'
            text_color: 1, 1, 1, 1

        MDRaisedButton:
            text: 'Tirar Foto'
            icon: 'camera-iris'
            pos_hint: {'center_x': 0.5, 'center_y': 0.3}
            on_release: root.take_picture()

        MDRoundFlatButton:
            text: 'Voltar'
            pos_hint: {'center_x': 0.5, 'center_y': 0.15}
            on_release: app.root.current = 'home'

<HistoryScreen>:
    name: 'history'
    MDFloatLayout:
        md_bg_color: 0.1, 0.1, 0.12, 1

        MDTopAppBar:
            title: 'Histórico'
            pos_hint: {'top': 1}
            left_action_items: [['arrow-left', lambda x: setattr(app.root, 'current', 'home')]]
            md_bg_color: 0.15, 0.15, 0.18, 1

        MDScrollView:
            pos_hint: {'top': 0.88}
            MDList:
                id: history_list
'''

class LoginScreen(Screen):
    def verify_pin(self):
        pin = self.ids.pin_input.text
        if pin == "1234":
            self.manager.current = 'home'
            self.ids.pin_input.text = ""
        else:
            Snackbar(text="PIN Incorreto! Tente 1234").open()

    def authenticate_biometrics(self):
        if platform == 'android':
            try:
                from jnius import autoclass
                Snackbar(text="Aguardando leitor biométrico...").open()
            except Exception as e:
                Snackbar(text="Biometria não disponível no emulador").open()
        else:
            Snackbar(text="Biometria simulada com sucesso!").open()
            self.manager.current = 'home'

class HomeScreen(Screen):
    is_unlocked = False

    def toggle_lock(self):
        self.is_unlocked = not self.is_unlocked
        if self.is_unlocked:
            self.ids.lock_button.icon = 'lock-open'
            self.ids.lock_button.text_color = (0.2, 0.8, 0.2, 1)
            self.ids.status_label.text = 'PORTA DESTRANCADA'
            self.ids.status_label.text_color = (0.2, 0.8, 0.2, 1)
            Snackbar(text="Porta destrancada!").open()
        else:
            self.ids.lock_button.icon = 'lock'
            self.ids.lock_button.text_color = (0.9, 0.2, 0.2, 1)
            self.ids.status_label.text = 'PORTA TRANCADA'
            self.ids.status_label.text_color = (0.9, 0.2, 0.2, 1)
            Snackbar(text="Porta trancada!").open()

    def logout(self):
        self.manager.current = 'login'

class CameraScreen(Screen):
    def take_picture(self):
        try:
            filename = os.path.join(storagepath.get_pictures_dir(), "acesso_doorlock.jpg")
            camera.take_picture(filename=filename, on_complete=self.camera_callback)
        except Exception as e:
            Snackbar(text="Simulando foto tirada com sucesso!").open()
            self.manager.current = 'home'

    def camera_callback(self, filepath):
        Snackbar(text=f"Foto salva em: {filepath}").open()
        self.manager.current = 'home'

class HistoryScreen(Screen):
    def on_enter(self):
        self.ids.history_list.clear_widgets()
        logs = [
            ("Acesso por PIN", "10:15 - Sucesso", "key"),
            ("Tentativa de Acesso", "09:30 - PIN Incorreto", "alert-circle"),
            ("Acesso Biométrico", "Ontem 22:00 - Sucesso", "fingerprint")
        ]
        for title, subtitle, icon in logs:
            item = OneLineIconListItem(text=f"{title} ({subtitle})")
            item.add_widget(IconLeftWidget(icon=icon))
            self.ids.history_list.add_widget(item)

class PremiumDoorLockApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        Builder.load_string(KV)
        return ScreenManager()

if __name__ == '__main__':
    PremiumDoorLockApp().run()