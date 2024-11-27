import customtkinter as ctk
import requests

class AnimeQuotesApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Anime Wisdom Quotes")
        self.geometry("600x700")
        ctk.set_appearance_mode("light")  # Light mode for a bright, friendly look
        ctk.set_default_color_theme("blue")

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self.header_label = ctk.CTkLabel(
            self, 
            text="Anime Wisdom Quotes", 
            font=("Arial", 32),
            text_color="#2C3E50"
        )
        self.header_label.grid(row=0, column=0, pady=(20, 10), sticky="ew")
        

        # Quote Frame
        self.quote_frame = ctk.CTkFrame(
            self, 
            corner_radius=15, 
            fg_color="#ECF0F1",
            border_color="#BDC3C7",
            border_width=2
        )
        
        self.quote_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.quote_frame.grid_columnconfigure(0, weight=1)
        self.quote_frame.grid_rowconfigure(1, weight=1)

        # Quote Label
        self.quote_label = ctk.CTkLabel(
            self.quote_frame, 
            text="Click 'Get Quote' to start your anime wisdom journey!",
            font=("Comic Sans MS", 20),
            text_color="#2C3E50",
            wraplength=500,
            justify="center"
        )
        self.quote_label.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        # Character Label
        self.character_label = ctk.CTkLabel(
            self.quote_frame, 
            text="", 
            font=("Arial", 18),
            text_color="#34495E"
        )
        self.character_label.grid(row=2, column=0, padx=20, pady=(0, 10))
        
        # Anime Label
        self.anime_label = ctk.CTkLabel(
            self.quote_frame, 
            text="", 
            font=("Arial", 16),
            text_color="#7F8C8D"
        )
        self.anime_label.grid(row=3, column=0, padx=20, pady=(0, 20))

        # Buttons Frame
        self.button_frame = ctk.CTkFrame(
            self, 
            fg_color="transparent"
        )
        self.button_frame.grid(row=2, column=0, pady=(0, 20))

        # Get Quote Button
        self.get_quote_btn = ctk.CTkButton(
            self.button_frame, 
            text="Get Anime Wisdom", 
            command=self.fetch_quote,
            fg_color="#3498DB",
            hover_color="#2980B9",
            text_color="white",
            font=("Comic Sans MS", 18)
        )
        self.get_quote_btn.pack(side="left", padx=10)
        
        # Copy Quote Button
        self.copy_btn = ctk.CTkButton(
            self.button_frame,
            text="Copy Quote",  # Removed the clipboard emoji for compatibility
            command=self.copy_quote,
            fg_color="#2ECC71",
            hover_color="#27AE60",
            text_color="white",
            font=("Comic Sans MS", 18)  # Make sure the font is available
        )
        self.copy_btn.pack(side="left", padx=10)

        
        # Background Anime Doodles (optional decorative elements)
        self.create_background_doodles()
        
    def create_background_doodles(self):
        """Create cute anime-style doodles in the background"""
        # This is a placeholder. In a real app, you might want to add actual cute anime doodle images
        pass

    def fetch_quote(self):
        """Fetch a random quote from the API"""
        try:
            response = requests.get('http://localhost:5000/random-quote')
            if response.status_code == 200:
                quote_data = response.json()
                
                # Update quote labels
                self.quote_label.configure(text=f'"{quote_data["quote"]}"')
                self.character_label.configure(text=f"- {quote_data['character']}")
                self.anime_label.configure(text=f"from {quote_data['anime']}")
                
                # Optional: Add a fun transition or animation
                self.quote_frame.configure(fg_color="#F1C40F")
                self.after(200, lambda: self.quote_frame.configure(fg_color="#ECF0F1"))
            else:
                self.quote_label.configure(text="Oops! Couldn't fetch a quote. Is the API running?")
        except Exception as e:
            self.quote_label.configure(text=f"Error: {str(e)}")

    def copy_quote(self):
        """Copy the current quote to clipboard"""
        quote_text = self.quote_label.cget("text")
        character_text = self.character_label.cget("text")
        anime_text = self.anime_label.cget("text")
        
        full_quote = f"{quote_text}\n{character_text}\n{anime_text}"
        
        # Copy to clipboard
        self.clipboard_clear()
        self.clipboard_append(full_quote)
        
        # Optional: Show a temporary "Copied!" tooltip
        copy_label = ctk.CTkLabel(
            self, 
            text="📋 Quote Copied!", 
            fg_color="#2ECC71",
            text_color="white",
            corner_radius=10
        )
        copy_label.place(relx=0.5, rely=0.9, anchor="center")
        self.after(1500, copy_label.destroy)

def main():
    app = AnimeQuotesApp()
    app.mainloop()

if __name__ == "__main__":
    main()