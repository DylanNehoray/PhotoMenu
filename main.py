import ocr
import kivy
import os
kivy.require('2.2.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.clock import Clock

class PhotoMenu(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        self.camera_layout = BoxLayout(orientation='vertical', spacing=10)
        
        self.camera = Camera(resolution=(640, 480), play=True)
        self.camera_layout.add_widget(self.camera)
        
        self.capture_button = Button(text='Capture Photo', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5})
        self.capture_button.bind(on_press=self.capture_photo)
        self.camera_layout.add_widget(self.capture_button)
        
        self.layout.add_widget(self.camera_layout)
        
        self.list_images_button = Button(text='List Images', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5})
        self.list_images_button.bind(on_press=self.show_image_list)
        self.layout.add_widget(self.list_images_button)
        
        self.image_display_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        self.scroll_view.add_widget(self.image_display_layout)
        
        self.camera_visible = True  # To track whether the camera is visible
        
        return self.layout
        
        
    def capture_photo(self, instance):
        loading_popup = Popup(title='Capturing Photo', content=Label(text='Please wait...'), auto_dismiss=False)
        loading_popup.open()

        def capture_complete(dt):
            photo_filename = os.path.join(os.path.dirname(__file__), 'in', 'photo.png')
            self.camera.export_to_png(photo_filename)
            
            #Perfomes the OCR and Google Images API on the menu
            res=ocr.getItems("./in/menu.png")
            print(res)
            ocr.obtainImages(res)
            
            loading_popup.dismiss()

        # Schedule the capture_complete function to run after a short delay
        Clock.schedule_once(capture_complete, 1.0)  # Adjust the delay as needed
    
        
    def show_image_list(self, instance):
        if self.camera_visible:
            self.layout.remove_widget(self.camera_layout)
            self.layout.remove_widget(self.list_images_button)
            self.layout.add_widget(self.scroll_view)
            self.camera_visible = False
            
            images_folder = os.path.join(os.path.dirname(__file__), 'out')
            image_files = [f for f in os.listdir(images_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
            
            self.image_display_layout.clear_widgets()
            
            for image_file in image_files:
                image_path = os.path.join(images_folder, image_file)
                image_widget = Image(source=image_path, size_hint=(None, None), size=(400, 300), pos_hint={'center_x': 0.5})
                base_name, _ = os.path.splitext(image_file)
                label_widget = Label(text=base_name, size_hint=(None, None), size=(400, 30), font_size='30sp', pos_hint={'center_x': 0.5})
                
                self.image_display_layout.add_widget(label_widget)
                self.image_display_layout.add_widget(image_widget)
            
            back_button = Button(text='Back to Camera',padding=10, size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5})
            back_button.bind(on_press=self.show_camera)
            self.image_display_layout.add_widget(back_button)
            
            self.image_display_layout.height = (len(image_files) * 330) + 300  # Adjusted height with extra padding
    
    def show_camera(self, instance):
        self.layout.remove_widget(self.scroll_view)
        self.layout.add_widget(self.camera_layout)
        self.layout.add_widget(self.list_images_button)
        self.camera_visible = True



if __name__ == '__main__':
    PhotoMenu().run()