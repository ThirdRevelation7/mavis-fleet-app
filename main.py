import customtkinter as ctk
from PIL import Image
import json

# load data from json


def load_services_data():
    with open('services.json') as file:
        return json.load(file)


# Populate services based on option selected
def populate_services(option):
    # clear previous content in the services list frame
    for widget in service_list_frame.winfo_children():
        widget.destroy()

    # get the services for the selected category
    services = services_data.get(option.lower(), [])

    # display the services and codes
    for service in services:
        service_label = ctk.CTkLabel(service_list_frame, text=f"{
                                     service.title()}", font=("times new roman", 15, "bold"))
        service_label.pack(padx=10, pady=5)


# Configure Search button
def on_search_click():
    user_search = search_bar.get().lower()
    search_results(user_search)


# Search for any services user inputs by keyword and add to frame if found
def search_results(user_search):
    # clear previous content in the services list frame
    for widget in service_list_frame.winfo_children():
        widget.destroy()

    # get the services with the keywords matching user search
    results_found = []

    for category, codes in services_data.items():
        for code in codes:
            if user_search in code.lower():
                results_found.append(f"{category.capitalize()}: {code}")

    # display the services and codes
    if not results_found:
        error_label = ctk.CTkLabel(service_list_frame, text=f"Sorry no results found for '{user_search}'. ",
                                   font=("times new roman", 15, "bold"), text_color="red")
        error_label.pack(padx=10, pady=100)
    else:
        for result in results_found:
            service_label = ctk.CTkLabel(service_list_frame, text=f"{result}", font=("times new roman", 15, "bold"))
            service_label.pack(padx=10, pady=5)


# create main window
app = ctk.CTk()

# set window size/color
app.geometry("800x800")
app.title("Mavis Fleet Codes")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# configure grid layout
app.grid_columnconfigure(index=0, weight=1)
app.grid_columnconfigure(index=1, weight=3)
app.grid_columnconfigure(index=2, weight=1)
app.rowconfigure(index=0, weight=1)
app.rowconfigure(index=1, weight=1)
app.rowconfigure(index=2, weight=1)
app.rowconfigure(index=3, weight=1)
app.rowconfigure(index=4, weight=1)
app.rowconfigure(index=5, weight=1)


# Load image usint PIL
mavis_image = ctk.CTkImage(Image.open("mavis-logo.png"), size=(500, 200))

# Create label and place image inside
mavis_label = ctk.CTkLabel(master=app, image=mavis_image, text="")
mavis_label.grid(row=0, column=1, pady=20, sticky='nsew')

# load services data from json file
services_data = load_services_data()

# services dropdown menu with categories
categories = ["Brakes", "Engine", "Suspension", "ERAC"]
select_category = ctk.CTkOptionMenu(master=app, values=categories, command=populate_services,
                                    button_hover_color="gold", fg_color="teal", button_color="teal", font=("times new roman", 14),
                                    dropdown_hover_color="gold")
select_category.grid(row=1, column=1)

label_2 = ctk.CTkLabel(master=app, text="Or", text_color="white", font=("times new roman", 30, "bold"))
label_2.grid(row=2, column=1)

# Search feature
search_bar = ctk.CTkEntry(master=app, placeholder_text="Search by keyword")
search_bar.grid(row=3, column=1)

# Search button
search_button = ctk.CTkButton(master=app, command=on_search_click, text="Search", hover_color="gold", fg_color="teal")
search_button.grid(row=4, column=1, sticky="n")
# Allow enter button on keyboard to activate search button
app.bind("<Return>", lambda event: on_search_click())

# Canvas for scrollable frame
canvas = ctk.CTkCanvas(app, width=600, height=300, bg="#2B2B2B")
canvas.grid(row=5, column=1, sticky="nsew", padx=20, pady=40)

# Scrollbar
scrollbar = ctk.CTkScrollbar(master=app, orientation="vertical", command=canvas.yview,
                             button_color="teal", button_hover_color="gold")
scrollbar.grid(row=5, column=1, sticky="nse", pady=40)

# Create inner frame where services will populate
service_list_frame = ctk.CTkFrame(canvas, width=700, height=400, fg_color="#2B2B2B")
canvas.create_window((0, 0), window=service_list_frame, anchor="n")

# Configure the canvas scrolling
service_list_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Set the scrollbar to work with the canvas
canvas.configure(yscrollcommand=scrollbar.set)

# set default option for menu
select_category.set("Select by Category")


# run the application
app.mainloop()
