import random
import tkinter as tk
from tkinter import messagebox

peliculas_por_genero = {
    "Acción": ["Mad Max: Furia en el camino", "John Wick", "Duro de matar"],
    "Comedia": ["¿Qué pasó ayer?", "Supercool", "Tonto y retonto"],
    "Drama": ["Sueño de fuga", "Forrest Gump", "El Padrino"],
    "Ciencia Ficción": ["Interestelar", "Matrix", "Blade Runner"],
    "Terror": ["El conjuro", "¡Huye!", "Un lugar en silencio"],
    "Romántica": ["Diario de una pasión", "Titanic", "La La Land"]
}


usuario_actual = None  # Guarda el nombre del usuario

def mostrar_login():
    ventana_principal.withdraw()  # Oculta la ventna principal si ya estaba abierta
    ventana_login.deiconify()     # Muestra la ventana de loguin

def iniciar_sesion():
    global usuario_actual
    nombre = entrada_nombre.get().strip()
    if nombre:
        usuario_actual = nombre
        etiqueta_bienvenida.config(text=f"Bienvenido, {usuario_actual}")
        entrada_nombre.delete(0, tk.END)
        ventana_login.withdraw()       # Oculta login
        ventana_principal.deiconify()  # Muestra principal
    else:
        messagebox.showwarning("Campo vacío", "Por favor, ingresa tu nombre.")

def cerrar_sesion():
    global usuario_actual
    usuario_actual = None
    var_genero.set("")  # Limpiar selección de género
    mostrar_login()


def recomendar_pelicula():
    genero = var_genero.get()
    texto_explicacion.delete("1.0", tk.END)  # Limpia el área de texto

    if genero:
        if genero == "Terror" and usuario_actual.lower() == "juan":
            mensaje = "Recomendación especial para Juan: ¡Evita el terror! Mejor mira 'Forrest Gump'."
            explicacion = (
                f"Regla activada: Regla especial para Juan\n"
                f"Condición: Usuario = 'Juan' y Género = 'Terror'\n"
                f"Acción: Se recomienda 'Forrest Gump' en lugar de una película de terror.\n"
            )
        else:
            recomendacion = random.choice(peliculas_por_genero[genero])
            mensaje = f"{usuario_actual}, te recomendamos ver: {recomendacion}"
            explicacion = (
                f"Regla activada: Regla general\n"
                f"Condición: Usuario ≠ 'Juan' o Género ≠ 'Terror'\n"
                f"Acción: Se recomienda una película aleatoria del género '{genero}'.\n"
                f"Película elegida: {recomendacion}\n"
            )

        messagebox.showinfo("Recomendación", mensaje)
        texto_explicacion.insert(tk.END, explicacion)
    else:
        messagebox.showwarning("Sin selección", "Por favor selecciona un género.")
        texto_explicacion.insert(tk.END, " No se activó ninguna regla: no se seleccionó ningún género.\n")


# Interfaz de usuario: Login

ventana_login = tk.Tk()
ventana_login.title("Inicio de sesión")
ventana_login.geometry("300x200")
ventana_login.config(bg="#e6f2ff")

tk.Label(ventana_login, text="Ingresa tu nombre:", font=("Arial", 12), bg="#e6f2ff").pack(pady=20)
entrada_nombre = tk.Entry(ventana_login, font=("Arial", 12))
entrada_nombre.pack(pady=5)
tk.Button(ventana_login, text="Iniciar sesión", font=("Arial", 12), bg="#4CAF50", fg="white", command=iniciar_sesion).pack(pady=10)


# Interfaz de usuario: Principal

ventana_principal = tk.Toplevel()
ventana_principal.title("Sistema Experto de Películas")
ventana_principal.geometry("400x400")
ventana_principal.config(bg="#f0f8ff")
ventana_principal.withdraw()  # Ocultar hasta que inicie sesión

etiqueta_bienvenida = tk.Label(ventana_principal, text="", font=("Arial", 14), bg="#f0f8ff", fg="#333")
etiqueta_bienvenida.pack(pady=10)

tk.Label(ventana_principal, text="Selecciona un género de película:", font=("Arial", 12), bg="#f0f8ff").pack(pady=10)

var_genero = tk.StringVar()

generos = ["Acción", "Comedia", "Drama", "Ciencia Ficción", "Terror", "Romántica"]
for genero in generos:
    tk.Radiobutton(
        ventana_principal,
        text=genero,
        variable=var_genero,
        value=genero,
        font=("Arial", 11),
        bg="#007bff",
        fg="white",
        selectcolor="#4CAF50",
        relief="ridge",
        width=20
    ).pack(pady=4)

tk.Button(ventana_principal, text="Obtener recomendación", font=("Arial", 12), bg="#28a745", fg="white", command=recomendar_pelicula).pack(pady=20)
tk.Button(ventana_principal, text="Cerrar sesión", font=("Arial", 11), bg="#dc3545", fg="white", command=cerrar_sesion).pack(pady=5)

# Información del sistema experto
tk.Label(ventana_principal, text="📘 Explicación del sistema experto:", font=("Arial", 12, "bold"), bg="#f0f8ff").pack(pady=10)

texto_explicacion = tk.Text(ventana_principal, height=7, width=50, font=("Arial", 10), wrap="word", bg="#e8f0fe")
texto_explicacion.pack(pady=5)


# Iniciar aplicación

ventana_login.mainloop()

