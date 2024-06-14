from PIL import Image as PILImage
import customtkinter as ctk
import os
import json

"""
 ___________________________________________________________________________________________________________________
|                                                                                                                   |
|     ______________________________                                                                                |
|    |                              |                                                                               |
|    |      Disclaimer [LEGAL]      |                                                                               |
|    |______________________________|                                                                               |
|                                                                                                                   |
|                                                                                                                   |
|    This software is provided "as is" without any representations or warranties, express or implied.               |
|    The author is not liable for any damages arising from the use or inability to use this software.               |
|    By using this software, you agree to indemnify and hold the author harmless from any claims or liabilities.    |
|    This disclaimer applies to the fullest extent permitted by law.                                                |
|                                                                                                                   |
|___________________________________________________________________________________________________________________|

"""

"""
    FOR DEVS:

    - REQUIRED PACKAGES -

pip install Pillow
pip install customtkinter

    - CODED WITH -

python 3.12.4

    - TESTED ON -

w11 23H2 [64-bit]
    
"""

#           - CONVERT -


def convert(org_filetype, converted_filetype, format_rgb, org_directory, converted_directory):
    # Set up and create window
    ctk.set_appearance_mode(appearance_mode)
    ctk.set_default_color_theme(default_color_theme)

    cnvr = ctk.CTk()
    cnvr.geometry("300x200")
    cnvr.title("Please wait...")

    # Labels
    label = ctk.CTkLabel(master=cnvr, text="Calculating...", justify="left", wraplength=800, font=("Arial", 20))
    label.grid(row=0, column=0)
    cnvr.update()

    # Check/Create directories
    os.makedirs(org_directory, exist_ok=True)
    os.makedirs(converted_directory, exist_ok=True)


    totalimg = 0
    tt = 0

    for filename in os.listdir(org_directory):
        if filename.endswith(org_filetype):
            totalimg += 1

    if totalimg == 1:
        grammar = "image"
    else:
        grammar = "images"

    label = ctk.CTkLabel(master=cnvr, text=f" Converting {totalimg} {grammar} ", justify="left", wraplength=800, font=("Arial", 15, "bold"))
    label.grid(row=1, column=0)


    label = ctk.CTkLabel(master=cnvr, text=f" '{org_filetype}' → '{converted_filetype}' ", justify="left", wraplength=800, font=("Arial", 15, "bold"))
    label.grid(row=0, column=0)

    def convert_stop():
        cnvr.destroy()
        root.destroy()

    button = ctk.CTkButton(master=cnvr, text="Cancel", command=convert_stop, font=("Arial", 15, "bold"), width=80, height=30)
    button.grid(row=6, column=0)

    cnvr.update()

    for filename in os.listdir(org_directory):
        if filename.endswith(org_filetype):
            webp_image = PILImage.open(os.path.join(org_directory, filename))
            png_image = webp_image.convert(format_rgb)
            png_image.save(os.path.join(converted_directory, filename.replace(org_filetype, converted_filetype)))
            tt += 1
            rem = totalimg - tt
            progress_label = ctk.CTkLabel(master=cnvr, text=f" [{tt}] / [{totalimg}] ", justify="left", wraplength=800, font=("Arial", 15, "bold"))
            progress_label.grid(row=2, column=0)

            progress_labela = ctk.CTkLabel(master=cnvr, text=f" [{rem}] remaining... ", justify="left", wraplength=800, font=("Arial", 15, "bold"))
            progress_labela.grid(row=4, column=0)
            cnvr.update()

    if tt == totalimg:
        cnvr.destroy()

    cnvr.mainloop()

#           - SETUP -

with open('config.json', 'r') as file:
    data = json.load(file)

# Assign values to variables
skip_config = data['skip-config']
appearance_mode = data['appearance-mode']
default_color_theme = data['default-color-theme']

if not skip_config:

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    fts = ctk.CTk()
    fts.geometry("800x500")
    fts.title("Set-Up")

    label = ctk.CTkLabel(master=fts, text="Let's make the program yours!", font=("Arial", 26, "bold"), justify="left", wraplength=800)
    label.pack(anchor="n", padx=0, pady=40)

    # - THEME -

    # If the users clicks save before selecting an option, apply this:
    appearance_mode_selected = "dark"
    color_theme_selected = "blue"

    label = ctk.CTkLabel(master=fts, text="Select a prefered theme:", justify="left", wraplength=800, font=("Arial", 16))
    label.pack(anchor="w", padx=100, pady=5)

    def combobox_callback_theme(choice):
        global appearance_mode_selected
        appearance_mode_selected = choice

    combobox = ctk.CTkComboBox(fts, values=["dark", "light"], command=combobox_callback_theme)
    combobox.pack(anchor="w", padx=100, pady=20)

    # - COLOR THEME -

    label = ctk.CTkLabel(master=fts, text="Select a color for the elements (like buttons):", justify="left", wraplength=800, font=("Arial", 16))
    label.pack(anchor="w", padx=100, pady=5)

    def combobox_callback_color_theme(choice):
        global color_theme_selected
        color_theme_selected = choice

    combobox = ctk.CTkComboBox(fts, values=["blue", "dark-blue", "green"], command=combobox_callback_color_theme)
    combobox.pack(anchor="w", padx=100, pady=20)

    # - SAVE -

    def preferances_save():
        with open('config.json', 'r') as file:
            data = json.load(file)

        data['skip-config'] = True
        data['appearance-mode'] = appearance_mode_selected
        data['default-color-theme'] = color_theme_selected

        with open('config.json', 'w') as file:
            json.dump(data, file, indent=4)

        fts.destroy()

    button = ctk.CTkButton(master=fts, text="Save my preferance", command=preferances_save, font=("Arial", 15, "bold"), width=200, height=40)
    button.pack(anchor="w", padx=300, pady=55)

    label = ctk.CTkLabel(master=fts, text="REMINDER:  You will need to restart the program for these changes to take effect.", justify="left", wraplength=800, font=("Arial", 16))
    label.pack(anchor="w", padx=10, pady=0)

    fts.mainloop()

#           - CTK -

ctk.set_appearance_mode(appearance_mode)
ctk.set_default_color_theme(default_color_theme)

root = ctk.CTk()
root.geometry("800x500")
root.title("Convertor")

label = ctk.CTkLabel(master=root, text="What would you like to convert?", justify="left", wraplength=800, font=("Arial", 26, "bold"))
label.pack(anchor="n", padx=0, pady=40)

# If user did not specify:
convert_original = "WEBP"
convert_modified = "WEBP"

def convertwhat():
    convert_original = comboboxin.get()
    convert_modified = comboboxout.get()
    org_directory = entryin.get()
    converted_directory = entryout.get()
    

    if convert_original == "WEBP":
        # ERROR WEBP > WEBP
        if convert_modified == "WEBP":
            ctk.set_appearance_mode(appearance_mode)
            ctk.set_default_color_theme(default_color_theme)

            err = ctk.CTk()
            err.geometry("500x60")
            err.title("Error")

            label = ctk.CTkLabel(master=err, text="Invalid request: WEBP → WEBP", justify="left", wraplength=800, font=("Arial", 20, "bold"))
            label.pack(anchor="n", padx=0, pady=20)

            err.mainloop()
        # WEBP > PNG
        if convert_modified == "PNG":
            org_filetype = ".webp"
            converted_filetype = ".png"
            format_rgb = "RGBA"
            convert(org_filetype, converted_filetype, format_rgb, org_directory, converted_directory)
        # WEBP > JPG
        if convert_modified == "JPG":
            org_filetype = ".webp"
            converted_filetype = ".jpg"
            format_rgb = "RGB"
            convert(org_filetype, converted_filetype, format_rgb, org_directory, converted_directory)
    
    if convert_original == "PNG":
        # PNG > WEBP
        if convert_modified == "WEBP":
            org_filetype = ".png"
            converted_filetype = ".webp"
            format_rgb = "RGBA"
            convert(org_filetype, converted_filetype, format_rgb, org_directory, converted_directory)
        # ERROR: PNG > PNG
        if convert_modified == "PNG":
            ctk.set_appearance_mode(appearance_mode)
            ctk.set_default_color_theme(default_color_theme)

            err = ctk.CTk()
            err.geometry("500x60")
            err.title("Error")

            label = ctk.CTkLabel(master=err, text="Invalid request: PNG → PNG", justify="left", wraplength=800, font=("Arial", 20, "bold"))
            label.pack(anchor="n", padx=0, pady=20)

            err.mainloop()
        # PNG > JPG
        if convert_modified == "JPG":
            org_filetype = ".png"
            converted_filetype = ".jpg"
            format_rgb = "RGB"
            convert(org_filetype, converted_filetype, format_rgb, org_directory, converted_directory)


    if convert_original == "JPG":
        
        if convert_modified == "WEBP":
            org_filetype = ".jpg"
            converted_filetype = ".webp"
            format_rgb = "RGBA"
            convert(org_filetype, converted_filetype, format_rgb, org_directory, converted_directory)

        if convert_modified == "PNG":
            org_filetype = ".jpg"
            converted_filetype = ".png"
            format_rgb = "RGBA"
            convert(org_filetype, converted_filetype, format_rgb, org_directory, converted_directory)

        if convert_modified == "JPG":
            ctk.set_appearance_mode(appearance_mode)
            ctk.set_default_color_theme(default_color_theme)

            err = ctk.CTk()
            err.geometry("500x60")
            err.title("Error")

            label = ctk.CTkLabel(master=err, text="Invalid request: JPG → JPG", justify="left", wraplength=800, font=("Arial", 20, "bold"))
            label.pack(anchor="n", padx=0, pady=20)

            err.mainloop()



# IN

label = ctk.CTkLabel(master=root, text="- INPUT -", justify="left", wraplength=800, font=("Arial", 16, "bold"))
label.pack(anchor="w", padx=100, pady=20)    

# r"str" to ignore \t and \f

entryin = ctk.CTkEntry(root, placeholder_text=r"C:\path\to\input\folder", width=2000)
entryin.pack(anchor="w", padx=100, pady=0)

comboboxin = ctk.CTkComboBox(root, values=["WEBP", "PNG", "JPG"])
comboboxin.pack(anchor="w", padx=100, pady=0)

# OUT

label = ctk.CTkLabel(master=root, text="- OUTPUT -", justify="left", wraplength=800, font=("Arial", 16, "bold"))
label.pack(anchor="w", padx=100, pady=20)

entryout = ctk.CTkEntry(root, placeholder_text=r"C:\path\to\output\folder", width=2000)
entryout.pack(anchor="w", padx=100, pady=0)

comboboxout = ctk.CTkComboBox(root, values=["WEBP", "PNG", "JPG"])
comboboxout.pack(anchor="w", padx=100, pady=0)

# NOTEforDIR:

label = ctk.CTkLabel(master=root, text="NOTE: If specified directory does not exist, it will be created automatically.", justify="left", wraplength=800, font=("Arial", 14, "bold"))
label.pack(anchor="w", padx=100, pady=20)

# BUTTON

button = ctk.CTkButton(master=root, text="Convert", font=("Arial", 15, "bold"), height=50, width=200, command=convertwhat)
button.pack(anchor="n", padx=0, pady=0)

root.mainloop()