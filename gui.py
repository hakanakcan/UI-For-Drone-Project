from pathlib import Path
import json
import mysql.connector


# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Button, PhotoImage, filedialog



def getAddress(longitude, latitude):
    # MySQL connection created
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Hakanakcan123",
        database="project_1",
        charset='utf8'
    )

    # MySQL connection check
    if mydb.is_connected():
        print("Baglanti basarili!")

    # Create cursor
    mycursor = mydb.cursor()

    # Mahalle sorgusu
    mycursor.execute("SELECT Mahalle FROM mahallerler WHERE Longitude_1 <= %s AND Longitude_end >= %s AND Latitude_1 <= %s AND Latitude_end >= %s LIMIT 1", 
                     (longitude, longitude, latitude, latitude))
    
    # Mahalle adını al
    mahalle_row = mycursor.fetchone()
    if mahalle_row:
        mahalle_adi = mahalle_row[0]
        print("Mahalle:", mahalle_adi)

        # Altyapı hasar tahminleri sorgusu
        mycursor.execute("SELECT dogalgaz_boru_hasari, icme_suyu_boru_hasari,atik_su_boru_hasari FROM altyapi_hasar_tahminleri WHERE mahalle_adi = %s", (mahalle_adi,))
        altyapi_hasar_tahminleri = mycursor.fetchall()
        mycursor.execute("SELECT cok_agir_hasarli, agir_hasarli,orta_hasarli,hafif_hasarli FROM hasar_tahminleri WHERE mahalle_adi = %s", (mahalle_adi,))
        hasar_tahminleri = mycursor.fetchall()
        mycursor.execute("SELECT can_kaybi_sayisi, agir_yarali_sayisi,hastanede_tedavi_sayisi,hafif_yarali_sayisi FROM yaralanma_tahminleri WHERE mahalle_adi = %s", (mahalle_adi,))
        yaralanma_tahminleri = mycursor.fetchall()
        
        # Sonuçları al
        return altyapi_hasar_tahminleri, hasar_tahminleri,yaralanma_tahminleri
    else:
        print("Mahalle bulunamadi.")

    mycursor.close()
    mydb.close()

def browse_video_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi"), ("All files", "*.*")])
    print("Selected video file:", file_path)

def browse_location_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    return file_path

def process_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    flight_array = []
    data_list = data['exchange']['message']['flight_logging']['flight_logging_items']
    
    for row in data_list:
        flight_array.append(row)

    general_lon = 0.0
    general_lat = 0.0

    for row in flight_array:
        first_three_elements = row[1:3] 
        general_lon += row[1]
        general_lat += row[2]
        

    general_lon = general_lon/len(flight_array)
    general_lat = general_lat/len(flight_array)
    result = getAddress(general_lon, general_lat)
    print(result)  # Sonuçları yazdır

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:/Users/Hakca/OneDrive/Masaüstü/pythonstuff/UI-For-Drone-Project/assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.geometry("650x400")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=400,
    width=650,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    325.0,
    200.0,
    image=image_image_1
)

def on_button_1_click():
    location = browse_location_file()
    if location:
        process_json_file(location)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=on_button_1_click,
    relief="flat"
)
button_1.place(x=8.0, y=170.0, width=155.0, height=30.0)

canvas.create_text(
    165.0,
    23.0,
    anchor="nw",
    text="Collapse Building Analysis",
    fill="#FFFFFF",
    font=("Inter BlackItalic", 24 * -1)
)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(x=8.0, y=331.0, width=100.0, height=30.0)

# button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
# button_3 = Button(
#     image=button_image_3,
#     borderwidth=0,
#     highlightthickness=0,
#     command=lambda: process_json_file(location),
#     relief="flat"  # Burada 'location' değişkeni tanımlanmadı.
# )
# button_3.place(x=165.0, y=331.0, width=100.0, height=30.0)

canvas.create_text(
    463.0,
    116.0,
    anchor="nw",
    text="Results",
    fill="#FFFFFF",
    font=("Inter BlackItalic", 12 * -1)
)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=browse_video_file,
    relief="flat"
)
button_4.place(x=8.0, y=110.0, width=154.52996826171875, height=30.0)

window.resizable(False, False)
window.mainloop()
