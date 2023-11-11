import os
from supabase import create_client, Client
import requests

url: str = ("https://pofsyheggdksltqaqyld.supabase.co")
key: str = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBvZnN5aGVnZ2Rrc2x0cWFxeWxkIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTE4ODA0OTcsImV4cCI6MjAwNzQ1NjQ5N30.v8Eiar1gCIuTGYpHc262wYsDzG94gePc3xDpeIoq7MY")  # Reemplaza esto con tu clave API de Supabase
supabase: Client = create_client(url, key)

data = supabase.auth.sign_in_with_password({"email": "amehdmendez@gmail.com", "password": "amehdfer20"})

for i in range(1, 145):
    dip = requests.get(f"https://www.simcompanies.com/api/v4/en/0/encyclopedia/resources/2/{i}/")
    
    if dip.status_code == 200:
        try:
            dip = dip.json()
        except ValueError:
            print(f"La respuesta para el recurso {i} no es un JSON válido.")
            continue

        if isinstance(dip, dict):
            name = dip["name"]
            kind = dip["db_letter"]
            print(name,kind)
            image_url = supabase.storage.from_('simCompanies').create_signed_url(f"iconos/{name}.png", 100)
            image_url=image_url["signedURL"]
            material = {"id": kind, "name": name, "image_url": image_url}

            # Insertar los datos en la tabla 'materiales' en Supabase
            data, count = supabase.table('materiales') \
                .insert({"id": kind, "datos": material}) \
                .execute()
            
            if count == 1:
                print(f"Datos para {name} insertados correctamente.")
            else:
                print(f"Fallo al insertar datos para {name}.")
        else:
            print(f"La respuesta para el recurso {i} no es un diccionario JSON.")
    else:
        print(f"No se pudo obtener datos para el recurso {i}")

print("Procesamiento de recursos completado.")
