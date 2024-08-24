import tkinter as tk
from tkinter import messagebox, PhotoImage
from database import init_db, add_barcode_info, get_barcode_info
from config import THEME_FILE, LAST_LANGUAGE, DATABASE_PATH
import os
import json
import sqlite3

current_theme = "light"
current_language = "en"
button_images = {}
translations = {}

def load_language():
    if os.path.exists(LAST_LANGUAGE):
        with open(LAST_LANGUAGE, "r") as file:
            return file.read().strip()
    return "en"

def save_language(lang):
    with open(LAST_LANGUAGE, "w") as file:
        file.write(lang)



def load_translations(language_code):
    global translations
    try:
        with open(f"locales/{language_code}.json", "r", encoding="utf-8") as file:
            translations = json.load(file)
    except FileNotFoundError:
        translations = {}


def translate(key):
    return translations.get(key, key)

def load_theme():
    if os.path.exists(THEME_FILE):
        with open(THEME_FILE, "r") as file:
            return file.read().strip()
    return "light"

def save_theme(theme):
    with open(THEME_FILE, "w") as file:
        file.write(theme)

def apply_theme(theme):
    global current_theme
    
    bg_color, fg_color, btn_bg_color = ("white", "black", "lightgray") if theme == "light" else ("black", "white", "gray30")
    
    root.config(bg=bg_color)
    button_frame.config(bg=bg_color)
    
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg=bg_color, fg=fg_color)
        elif isinstance(widget, tk.Button):
            widget.config(bg=btn_bg_color, fg=fg_color)
    
    for button in button_frame.winfo_children():
        button.config(bg=btn_bg_color, fg=fg_color)

    current_theme = theme

def submit_barcode():
    barcode = barcode_entry.get().strip()
    if not barcode:
        messagebox.showwarning(translate("input_error"), translate("please_scan_or_enter_barcode"))
        return
    
    info = get_barcode_info(barcode)
    
    if info:
        name, price, details, amount = info
        result_text.set(f"{translate('product_name')}: {name}\n{translate('price')}: {price}\n{translate('details')}: {details}\n{translate('amount')}: {amount}")
    else:
        result_text.set(translate("product_not_found"))
        show_add_product_frame(True)

def show_add_product_frame(show):
    if show:
        add_frame.pack(pady=10)
    else:
        add_frame.pack_forget()

def add_product_info():
    def save_product_info():
        barcode = barcode_entry.get().strip()
        name = name_entry.get()
        try:
            price = float(price_entry.get())
        except ValueError:
            messagebox.showwarning(translate("input_error"), translate("please_enter_valid_price"))
            return
        details = details_entry.get()
        try:
            amount = int(amount_entry.get())
        except ValueError:
            messagebox.showwarning(translate("input_error"), translate("please_enter_valid_amount"))
            return
        
        add_barcode_info(barcode, name, price, details, amount)
        messagebox.showinfo(translate("success"), translate("product_added_successfully"))
        
        clear_window()
        open_add_product()

    save_button.config(command=save_product_info)

def open_product_query():
    clear_window()
    
    tk.Label(root, text=translate("scan_or_enter_barcode")).pack(pady=10)
    
    global barcode_entry, result_text, add_frame, name_entry, price_entry, details_entry, amount_entry, save_button
    
    barcode_entry = tk.Entry(root, width=30)
    barcode_entry.pack(pady=5)
    
    submit_button = tk.Button(root, text=translate("submit"), command=submit_barcode)
    submit_button.pack(pady=10)
    
    result_text = tk.StringVar()
    result_label = tk.Label(root, textvariable=result_text, wraplength=300, justify="left")
    result_label.pack(pady=10)
    
    add_frame = tk.Frame(root)
    
    show_add_product_frame(False)
    
    add_go_back_button()
    apply_theme(current_theme)

def open_sell():
    clear_window()

    products_sold = []
    total_price = 0.0

    def add_product_to_sell():
        nonlocal total_price

        barcode = barcode_entry.get().strip()
        if not barcode:
            messagebox.showwarning(translate("input_error"), translate("please_scan_or_enter_barcode"))
            return
        
        info = get_barcode_info(barcode)
        barcode_entry.delete(0, tk.END)

        if info:
            name, price, details, amount = info
            
            product_label = tk.Label(sell_frame, text=f"{translate('product_name')}: {name}\n"
                                                      f"Barcode: {barcode}\n"
                                                      f"{translate('details')}: {details}\n"
                                                      f"{translate('price')}: {price}",
                                                      justify="left", anchor="w")
            product_label.pack(anchor="w", padx=10, pady=5)

            total_price += price
            total_price_label.config(text=f"{translate('total_price')}: {total_price:.2f}")
            
            products_sold.append((barcode, amount))
        else:
            messagebox.showwarning(translate("product_not_found"), translate("product_not_found"))

    def finalize_sale():
        nonlocal total_price

        for barcode, amount_sold in products_sold:
            current_info = get_barcode_info(barcode)
            if current_info:
                name, price, details, amount = current_info
                new_amount = amount - 1
                if new_amount >= 0:
                    conn = sqlite3.connect(DATABASE_PATH)
                    cursor = conn.cursor()
                    cursor.execute("UPDATE barcodes SET amount=? WHERE barcode=?", (new_amount, barcode))
                    conn.commit()
                    conn.close()

        clear_window()
        products_sold.clear()
        total_price = 0.0
        go_back_to_main_menu()

    tk.Label(root, text=translate("scan_or_enter_barcode")).pack(pady=10)

    global barcode_entry
    barcode_entry = tk.Entry(root, width=30)
    barcode_entry.pack(pady=5)

    submit_button = tk.Button(root, text=translate("submit"), command=add_product_to_sell)
    submit_button.pack(pady=10)

    global sell_frame
    sell_frame = tk.Frame(root)
    sell_frame.pack(pady=10)

    global total_price_label
    total_price_label = tk.Label(root, text=f"{translate('total_price')}: 0.00")
    total_price_label.pack(pady=10)

    finish_button = tk.Button(root, text=translate("finish_sale"), command=finalize_sale)
    finish_button.pack(pady=20)

    add_go_back_button()
    apply_theme(current_theme)


def open_settings():
    clear_window()
    
    def toggle_theme():
        new_theme = "dark" if load_theme() == "light" else "light"
        apply_theme(new_theme)
        save_theme(new_theme)
    
    def change_language(language_code):
        save_language(language_code)
        global current_language
        load_translations(language_code)
        current_language = language_code
        apply_theme(current_theme)
        clear_window()
        open_settings()

    tk.Label(root, text=translate("settings")).pack(pady=10)
    
    tk.Button(root, text=translate("toggle_theme"), command=toggle_theme).pack(pady=10)
    
    language_var = tk.StringVar(value=current_language)
    language_dropdown = tk.OptionMenu(root, language_var, "en", "es", "de", "tr", command=change_language)
    language_dropdown.pack(pady=10)
    
    add_go_back_button()
    apply_theme(current_theme)

def update_price_for_barcode():
    def update_price():
        barcode = barcode_entry.get().strip()
        try:
            new_price = float(new_price_entry.get())
        except ValueError:
            messagebox.showwarning(translate("input_error"), translate("please_enter_valid_price"))
            return
        
        info = get_barcode_info(barcode)
        if not info:
            messagebox.showwarning(translate("product_not_found"), translate("product_not_found"))
            return
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE barcodes SET price=? WHERE barcode=?", (new_price, barcode))
        conn.commit()
        conn.close()

        messagebox.showinfo(translate("success"), translate("price_updated_successfully"))
        clear_window()
        open_renew_prices()
    
    clear_window()
    tk.Label(root, text=translate("enter_barcode_to_update_price")).pack(pady=10)

    global barcode_entry, new_price_entry

    barcode_entry = tk.Entry(root, width=30)
    barcode_entry.pack(pady=5)

    tk.Label(root, text=translate("enter_new_price")).pack(pady=10)

    new_price_entry = tk.Entry(root, width=30)
    new_price_entry.pack(pady=5)

    update_button = tk.Button(root, text=translate("update_price"), command=update_price)
    update_button.pack(pady=20)

    add_go_back_button()
    apply_theme(current_theme)

def update_all_prices_by_percentage():
    def apply_percentage_update():
        try:
            percentage = float(percentage_entry.get())
        except ValueError:
            messagebox.showwarning(translate("input_error"), translate("please_enter_valid_percentage"))
            return
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE barcodes SET price = price * (1 + ? / 100)", (percentage,))
        conn.commit()
        conn.close()

        messagebox.showinfo(translate("success"), translate("prices_updated_successfully"))
        clear_window()
        open_renew_prices()

    clear_window()
    tk.Label(root, text=translate("enter_percentage_to_update_prices")).pack(pady=10)

    global percentage_entry

    percentage_entry = tk.Entry(root, width=30)
    percentage_entry.pack(pady=5)

    update_button = tk.Button(root, text=translate("update_prices"), command=apply_percentage_update)
    update_button.pack(pady=20)

    add_go_back_button()
    apply_theme(current_theme)


def open_renew_prices():
    clear_window()
    tk.Label(root, text=translate("renew_prices")).pack(pady=10)

    search_barcode_button = tk.Button(root, text=translate("update_specific_barcode_price"), command=update_price_for_barcode)
    search_barcode_button.pack(pady=10)

    update_all_button = tk.Button(root, text=translate("update_all_prices_by_percentage"), command=update_all_prices_by_percentage)
    update_all_button.pack(pady=10)

    add_go_back_button()
    apply_theme(current_theme)



def open_add_product():
    clear_window()
    tk.Label(root, text=translate("add_product")).pack(pady=10)
    
    global barcode_entry, result_text, add_frame, name_entry, price_entry, details_entry, amount_entry, save_button
    
    barcode_entry = tk.Entry(root, width=30)
    barcode_entry.pack(pady=5)
    
    result_text = tk.StringVar()
    result_label = tk.Label(root, textvariable=result_text, wraplength=300, justify="left")
    result_label.pack(pady=10)
    
    add_frame = tk.Frame(root)
    
    tk.Label(add_frame, text=translate("product_name")).grid(row=0, column=0)
    name_entry = tk.Entry(add_frame)
    name_entry.grid(row=0, column=1)
    
    tk.Label(add_frame, text=translate("price")).grid(row=1, column=0)
    price_entry = tk.Entry(add_frame)
    price_entry.grid(row=1, column=1)
    
    tk.Label(add_frame, text=translate("details")).grid(row=2, column=0)
    details_entry = tk.Entry(add_frame)
    details_entry.grid(row=2, column=1)

    tk.Label(add_frame, text=translate("amount")).grid(row=3, column=0)
    amount_entry = tk.Entry(add_frame)
    amount_entry.grid(row=3, column=1)
    
    save_button = tk.Button(add_frame, text=translate("save"))
    save_button.grid(row=4, column=0, columnspan=2)
    
    save_button.config(command=add_product_info)
    
    add_frame.pack(pady=10)
    
    add_go_back_button()
    apply_theme(current_theme)

def open_general_report():
    clear_window()
    tk.Label(root, text=translate("general_report_functionality")).pack(pady=10)
    add_go_back_button()
    apply_theme(current_theme)

def add_go_back_button():
    go_back_button = tk.Button(root, text=translate("go_back"), command=go_back_to_main_menu)
    go_back_button.pack(pady=10)

def go_back_to_main_menu():
    clear_window()
    create_main_menu()

def clear_window():
    for widget in root.winfo_children():
        widget.pack_forget()

def create_main_menu():
    global button_frame, button_images

    button_frame = tk.Frame(root)
    button_frame.pack(expand=True)
    
    button_images['query_image'] = PhotoImage(file="images/Search.png")
    button_images['sell_image'] = PhotoImage(file="images/Payment.png")
    button_images['settings_image'] = PhotoImage(file="images/Settings.png")
    button_images['renew_prices_image'] = PhotoImage(file="images/Edit.png")
    button_images['add_product_image'] = PhotoImage(file="images/Package.png")
    button_images['general_report_image'] = PhotoImage(file="images/Service.png")

    buttons = [
        (translate("product_query"), open_product_query, button_images['query_image']),
        (translate("sell"), open_sell, button_images['sell_image']),
        (translate("settings"), open_settings, button_images['settings_image']),
        (translate("renew_prices"), open_renew_prices, button_images['renew_prices_image']),
        (translate("add_product"), open_add_product, button_images['add_product_image']),
        (translate("general_report"), open_general_report, button_images['general_report_image'])
    ]
    
    for i, (text, command, image) in enumerate(buttons):
        row = i // 3
        col = i % 3
        button = tk.Button(button_frame, text=text, command=command, image=image, compound='left', font=("Helvetica", 16))
        button.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
    
    for i in range(2):
        button_frame.grid_rowconfigure(i, weight=1)
    for i in range(3):
        button_frame.grid_columnconfigure(i, weight=1)
    
    apply_theme(current_theme)

def create_gui():
    global root, button_frame, current_theme, current_language
    
    root = tk.Tk()
    root.title("Inventory Management System")
    root.attributes('-fullscreen', True)

    load_translations(load_language())
    create_main_menu()
    
    apply_theme(load_theme())
    
    root.mainloop()

if __name__ == "__main__":
    init_db()
    create_gui()
