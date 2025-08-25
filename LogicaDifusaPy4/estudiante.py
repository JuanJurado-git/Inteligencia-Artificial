
import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import tkinter as tk
from tkinter import messagebox


# SISTEMA DIFUSO SKFUZZY


# 1. Definición de variables 
asistencia = ctrl.Antecedent(np.arange(0, 101, 1), 'asistencia')
nota = ctrl.Antecedent(np.arange(0, 11, 0.1), 'nota')
desempeno = ctrl.Consequent(np.arange(0, 101, 1), 'desempeño')

# 2. Conjutnos
asistencia['baja'] = fuzz.trimf(asistencia.universe, [0, 0, 60])
asistencia['media'] = fuzz.trimf(asistencia.universe, [40, 70, 90])
asistencia['alta'] = fuzz.trimf(asistencia.universe, [60, 100, 100])

nota['bajo'] = fuzz.trimf(nota.universe, [0, 0, 6])
nota['medio'] = fuzz.trimf(nota.universe, [4, 6, 8])
nota['alto'] = fuzz.trimf(nota.universe, [6, 10, 10])

desempeno['deficiente'] = fuzz.trimf(desempeno.universe, [0, 30, 50])
desempeno['aceptable'] = fuzz.trimf(desempeno.universe, [40, 60, 75])
desempeno['excelente'] = fuzz.trimf(desempeno.universe, [70, 90, 100])

# 3. Reglas difusas
reglas = [
    ctrl.Rule(asistencia['baja'] & nota['bajo'], desempeno['deficiente']),
    ctrl.Rule(asistencia['media'] & nota['medio'], desempeno['aceptable']),
    ctrl.Rule(asistencia['alta'] & nota['alto'], desempeno['excelente']),
    ctrl.Rule(asistencia['media'] & nota['alto'], desempeno['aceptable']),
    ctrl.Rule(asistencia['alta'] & nota['medio'], desempeno['aceptable']),
    ctrl.Rule(asistencia['baja'] & nota['alto'], desempeno['aceptable']),
    ctrl.Rule(asistencia['alta'] & nota['bajo'], desempeno['deficiente'])
]

sistema_ctrl = ctrl.ControlSystem(reglas)
evaluador = ctrl.ControlSystemSimulation(sistema_ctrl)


# INTERFAZ GRÁFICA


class StudentFuzzyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Evaluador Difuso de Estudiantes")
        self.root.geometry("850x600")
        self.root.configure(bg="#e0f7fa")
        self.username = ""
        self.create_login_screen()

    def create_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Sistema difuso de evaluación académica", font=("Helvetica", 18), bg="#e0f7fa").pack(pady=40)
        tk.Label(self.root, text="Ingrese su nombre:", font=("Helvetica", 14), bg="#e0f7fa").pack()
        self.username_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.username_entry.pack(pady=10)
        tk.Button(self.root, text="Ingresar", font=("Helvetica", 14), command=self.start_system, bg="#00796b", fg="white").pack(pady=20)

    def start_system(self):
        name = self.username_entry.get().strip()
        if not name:
            messagebox.showwarning("Advertencia", "Debe ingresar un nombre.")
            return
        self.username = name
        self.create_main_screen()

    def create_main_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text=f"Hola, {self.username}", font=("Helvetica", 16, "bold"), bg="#e0f7fa").pack(pady=10)
        tk.Label(self.root, text="Ingrese el porcentaje de asistencia (%):", font=("Helvetica", 14), bg="#e0f7fa").pack()
        self.att_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.att_entry.pack(pady=5)
        tk.Label(self.root, text="Ingrese el promedio de notas (0-10):", font=("Helvetica", 14), bg="#e0f7fa").pack()
        self.grade_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.grade_entry.pack(pady=5)
        tk.Button(self.root, text="Evaluar", font=("Helvetica", 14), command=self.process_input, bg="#0288d1", fg="white").pack(pady=20)
        self.result_text = tk.Text(self.root, height=20, font=("Courier", 11), width=95, bg="#ffffff", wrap="word")
        self.result_text.pack(pady=10)

    def process_input(self):
        try:
            att = float(self.att_entry.get())
            grade = float(self.grade_entry.get())
            if not (0 <= att <= 100) or not (0 <= grade <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores válidos (Asistencia 0-100, Nota 0-10).")
            return

        # Evaluación con lógica difusa
        evaluador.input['asistencia'] = att
        evaluador.input['nota'] = grade
        evaluador.compute()
        resultado = evaluador.output['desempeño']

        # Mostrar resultados
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "------ FUSIFICACIÓN ------\n")
        for name, mf in asistencia.terms.items():
            val = fuzz.interp_membership(asistencia.universe, mf.mf, att)
            self.result_text.insert(tk.END, f"Asistencia '{name}': {val:.2f}\n")
        for name, mf in nota.terms.items():
            val = fuzz.interp_membership(nota.universe, mf.mf, grade)
            self.result_text.insert(tk.END, f"Nota '{name}': {val:.2f}\n")

        self.result_text.insert(tk.END, "\n------ REGLAS APLICADAS ------\n")
        for idx, rule in enumerate(sistema_ctrl.rules):
            a = rule.antecedent
            self.result_text.insert(tk.END, f"Regla {idx+1}: SI {a} → {rule.consequent}\n")

        self.result_text.insert(tk.END, "\n------ DESFUSIFICACIÓN ------\n")
        self.result_text.insert(tk.END, f"Resultado final (desempeño): {resultado:.2f} / 100\n")

        self.result_text.insert(tk.END, "\n------ EVALUACIÓN FINAL ------\n")
        if resultado < 50:
            estado = "RENDIMIENTO DEFICIENTE - Se recomienda reforzar el estudio y mejorar la asistencia."
        elif resultado < 75:
            estado = "RENDIMIENTO ACEPTABLE - Buen trabajo, sigue así."
        else:
            estado = "RENDIMIENTO EXCELENTE - ¡Felicidades!"

        self.result_text.insert(tk.END, f"Estado del estudiante: {estado}\n")


# EJECUCIÓN DEL SISTEMA
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentFuzzyGUI(root)
    root.mainloop()


