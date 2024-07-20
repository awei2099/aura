import tkinter as tk
from tktooltip import ToolTip
import customtkinter as ctk
from tkinter import END
from .Client2Server import Client #.Client2Server when runing run.py
from PIL import Image
import tkinter.font as tkFont
import json
import ast

class ChatbotGUI(ctk.CTkToplevel):

    def __init__(self, name, ai):
        
        super().__init__()
        self.title(f"{name}'s Corner")
        
        self.geometry("600x600") 
        self.minsize(600, 600)   
        ctk.set_appearance_mode("Dark") 
        
        
        self.client = ai

        #padding grids
        self.rowconfigure(0, weight=1)    
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)    
        self.rowconfigure(4, weight=1)

        self.columnconfigure(0,weight=1)

        self.columnconfigure(1,weight=13)
        self.columnconfigure(2,weight=1)
        
        bgColor = "#2a2b2b"

        # Create main frame
        self.scroll_frame = ctk.CTkScrollableFrame(self, border_width= 3, fg_color=bgColor, border_color="#5c5b5b")
        self.scroll_frame.grid(row=1,column=1, sticky="nsew")
        
        
        self.canvas = tk.Canvas(self.scroll_frame, bg =bgColor, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Input frame
        self.input_frame = ctk.CTkFrame(self, fg_color = bgColor, border_width= 3, border_color="#5c5b5b")
        self.input_frame.grid(row=3,column=1, sticky="nsew")

        # Entry box
        self.entry = ctk.CTkEntry(self.input_frame, width = 395)
        self.entry.xview_scroll(4, tk.UNITS)
        self.entry.pack(side = "left", pady=10, padx=10, expand=True , fill = "x")
        self.entry.bind("<Return>", self.send_message)

        #Load Prev Convo Button
        load_image = ctk.CTkImage(Image.open("src/images/white_reload_sign.png"))
        self.load_prev_convo= ctk.CTkButton(self.input_frame, text="", image= load_image, command=self.load_prev_convo, width=50)
        self.load_prev_convo.pack(side = "right", padx=10)
        tooltip_font = tkFont.Font(family="Space Grotesk", size=13, weight="bold")
        ToolTip(self.load_prev_convo, msg="Loads Previous Convos", y_offset=40, font=tooltip_font)
        

        # Send button
        self.send_button = ctk.CTkButton(self.input_frame, text="Send", command=self.send_message, width=75)
        self.send_button.pack(side = "right", padx=5)

    
    #New entry
       # self.entry = ctk.CTkTextbox(self.input_frame, height=20, wrap = 'word')
       # self.entry.pack(side = "left", pady=10, padx=10, expand=True, fill = "x")
       # self.entry.bind("<Return>", self.send_message)

    def send_message(self, event=None):
        user_message = self.entry.get()#1.0, END for text box
        #self.entry.delete(1.0, END) for text box
        if user_message.strip() != "":
            self.create_speech_bubble(user_message, "right")
            self.entry.delete(0, END)
            self.update()
            response = self.client.sendData(sys="Question", message=user_message)
            bot_response = response.get('answer')
            self.create_speech_bubble(bot_response, "left")
            # self.update()
            # os.remove(self.client.tts(bot_response))

    def create_speech_bubble(self, message, side):
        bubble_frame = ctk.CTkFrame(self.canvas, corner_radius=15, fg_color="#5c5b5b", width=360)
        bubble_label = ctk.CTkLabel(bubble_frame, text=message, wraplength=250, justify="left" if side == "left" else "right")
        bubble_label.pack(padx=10, pady=5)

        if side == "left":
            bubble_frame.pack(anchor="w", padx=10, pady=5)
        else:
            bubble_frame.pack(anchor="e", padx=10, pady=5)
        self.update_idletasks()
        self.scroll_frame._parent_canvas.yview_moveto(1.0)

    def load_prev_convo(self):
        with open("src/Temp/previous_convos.txt", "r") as f:
            convo = f.read()
        if convo != "":
            self.client.sendData("Set Convo", convo)
            convo = ast.literal_eval(convo) 
            for m in convo:
                if m.get('role') == "user":
                    self.create_speech_bubble(m.get("content"), "1 LV 80085")
                elif m.get('role') == "assistant":
                    self.create_speech_bubble(m.get("content"), "left")
                self.update()

if __name__ == "__main__":
    app = ChatbotGUI("Jerry", ai = Client("hello")) #ai = Client(), ai = None
    app.mainloop()
