import requests
import tkinter as tk
from tkinter import filedialog, scrolledtext
from concurrent.futures import ThreadPoolExecutor

def verificar_proxy(proxy):
    url = "https://httpbin.org/ip"
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    }

    try:
        response = requests.get(url, proxies=proxies, timeout=5)
        return response.status_code == 200
    except (requests.exceptions.ProxyError,
            requests.exceptions.ConnectTimeout,
            requests.exceptions.SSLError,
            requests.exceptions.RequestException):
        return False

def seleccionar_archivo():
    filename = filedialog.askopenfilename(title="Seleccionar archivo de proxies", filetypes=[("Text files", "*.txt")])
    return filename

def procesar_proxy(proxy):
    proxy = proxy.strip()
    if verificar_proxy(proxy):
        return proxy, True
    else:
        return proxy, False

def procesar_archivo():
    archivo = seleccionar_archivo()
    if archivo:
        with open(archivo, 'r') as file:
            proxies = file.readlines()

        total_proxies = len(proxies)
        proxies_validos = 0
        proxies_invalidos = 0
        proxies_vivos = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            resultados = list(executor.map(procesar_proxy, proxies))

        for proxy, es_valido in resultados:
            if es_valido:
                proxies_validos += 1
                proxies_vivos.append(f"{proxy} - Esta proxy es válida por BSZ")
            else:
                proxies_invalidos += 1

        textarea.config(state=tk.NORMAL)
        textarea.delete(1.0, tk.END)
        for proxy_vivo in proxies_vivos:
            textarea.insert(tk.END, proxy_vivo + '\n')
        textarea.config(state=tk.DISABLED)

        label_resultados.config(text=f"Total de proxies: {total_proxies}\nProxies válidos: {proxies_validos}\nProxies inválidos: {proxies_invalidos}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Verificador de Proxies")
ventana.geometry("400x400")

# Centrar la ventana en la pantalla
ventana.eval('tk::PlaceWindow . center')

# Crear botón para seleccionar archivo
boton_seleccionar = tk.Button(ventana, text="Seleccionar archivo", command=procesar_archivo)
boton_seleccionar.pack(pady=20)

# Crear un label para mostrar los resultados
label_resultados = tk.Label(ventana, text="Total de proxies: 0\nProxies válidos: 0\nProxies inválidos: 0")
label_resultados.pack(pady=10)

# Crear un textarea para mostrar los proxies válidos
textarea = scrolledtext.ScrolledText(ventana, state=tk.DISABLED, width=50, height=10)
textarea.pack(pady=10)

# Ejecutar el bucle principal de la ventana
ventana.mainloop()
