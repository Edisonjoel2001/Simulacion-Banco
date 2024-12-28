#Leccion Emulacion Ingreso a banco
   #Edison Cabezas
     #Tercer Semestre Carrera Desarrollo de Software
        #Emular el ingreso a una aplicacion, bancaria con registro de sus datos

import tkinter as tk            #Empezamos importando las librerias Tkinter para poder representa de forma grafica
from tkinter import messagebox  #Empezamos importando las librerias Tkinter para poder representa de forma grafica
import re                       #Importamos la libreria re
from datetime import datetime   #Importamos la libreria datetime, para obtener la hora y fecha en la transacciones

# Aqui simulamos una base de datos, que guardara nuestros registro, durante la app este abierta 
data = {}

# esta es la clase principal para manejar las importaciones
class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bienvenido a su Banco")
        self.root.geometry("375x375")
        self.root.configure(bg="#A9A9A9")

        self.frames = {}

        for F in (LoginPage, RegisterPage, AccountPage):
            frame = F(self.root, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#A9A9A9")
        self.controller = controller

        tk.Label(self, text="Ingrese sus Datos de Ingreso", font=("Castellar", 15), bg="#A9A9A9").pack(pady=20)

        tk.Label(self, text="Cliente:", bg="#A9A9A9").pack()
        self.entry_username = tk.Entry(self)
        self.entry_username.pack()

        tk.Label(self, text="Contraseña:", bg="#A9A9A9").pack()
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack()

        tk.Button(self, text="Iniciar Sesión", command=self.login).pack(pady=10)
        tk.Button(self, text="Registrarse", command=lambda: controller.show_frame(RegisterPage)).pack()

    def login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if username in data and data[username]["password"] == password:
            self.controller.frames[AccountPage].set_user(username)
            self.controller.show_frame(AccountPage)
        else:
            messagebox.showerror("Acceso Denegado","Usario o contraseña incorrectos.")

class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#A9A9A9")
        self.controller = controller

        tk.Label(self, text="Registro", font=("Castellar", 16), bg="#A9A9A9").pack(pady=20)

        tk.Label(self, text="Cliente", bg="#A9A9A9").pack()
        self.entry_username = tk.Entry(self)
        self.entry_username.pack()

        tk.Label(self, text="Contraseña:", bg="#A9A9A9").pack()
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack()

        tk.Label(self, text="Nombre:", bg="#A9A9A9").pack()
        self.entry_first_name = tk.Entry(self)
        self.entry_first_name.pack()

        tk.Label(self, text="Apellido:", bg="#A9A9A9").pack()
        self.entry_last_name = tk.Entry(self)
        self.entry_last_name.pack()

        tk.Label(self, text="Cédula:", bg="#A9A9A9").pack()
        self.entry_dni = tk.Entry(self)
        self.entry_dni.pack()

        tk.Button(self, text="Registrar", command=self.register).pack(pady=10)
        tk.Button(self, text="Volver", command=lambda: controller.show_frame(LoginPage)).pack()

    def register(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        first_name = self.entry_first_name.get().strip()
        last_name = self.entry_last_name.get().strip()
        dni = self.entry_dni.get().strip()

        if not username or not password or not first_name or not last_name or not dni:
            messagebox.showerror("Por favor, llenar todos los campos*")
            return

        if username in data:
            messagebox.showerror("Error", "Usuario ya registrado")
            return

        if len(password) < 8 or not re.search(r"[A-Z]", password) or not re.search(r"[0-9]", password):
            messagebox.showerror("Error", "La contraseña debe tener al menos 8 caracteres, una mayúscula y un número.")
            return

        if not dni.isdigit() or len(dni) != 10:
            messagebox.showerror("Error", "Su cedula debe constar de 10 numeros")
            return

        for user in data.values():
            if user["dni"] == dni:
                messagebox.showerror("Error", "Cédula ya está registrada.")
                return

        data[username] = {
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "dni": dni,
            "balance": 0.0,
            "transactions": []
        }
        messagebox.showinfo("Cliente Nuevo", "Cliente registrado con éxito.")
        self.controller.show_frame(LoginPage)

class AccountPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#A9A9A9")
        self.controller = controller
        self.username = None

        self.label_welcome = tk.Label(self, text="", font=("Castellar", 16), bg="#A9A9A9")
        self.label_welcome.pack(pady=10)

        self.label_balance = tk.Label(self, text="", font=("Arial", 14), bg="#A9A9A9")
        self.label_balance.pack(pady=10)

        # Aqui realziamos el deposito
        frame_deposit = tk.Frame(self, bg="#A9A9A9")
        frame_deposit.pack(pady=10)

        tk.Label(frame_deposit, text="Depósito:", bg="#A9A9A9").grid(row=0, column=0)
        self.entry_deposit = tk.Entry(frame_deposit)
        self.entry_deposit.grid(row=0, column=1)
        tk.Button(frame_deposit, text="Depositar", command=self.deposit).grid(row=0, column=2)

        # Aqui, es donde realizamos las transfrerencias 
        frame_transfer = tk.Frame(self, bg="#A9A9A9")
        frame_transfer.pack(pady=10)

        tk.Label(frame_transfer, text="Cliente destinado:", bg="#A9A9A9").grid(row=0, column=0)
        self.entry_transfer_user = tk.Entry(frame_transfer)
        self.entry_transfer_user.grid(row=0, column=1)

        tk.Label(frame_transfer, text="Cantidad:", bg="#A9A9A9").grid(row=1, column=0)
        self.entry_transfer_amount = tk.Entry(frame_transfer)
        self.entry_transfer_amount.grid(row=1, column=1)

        tk.Button(frame_transfer, text="Transferir", command=self.transfer).grid(row=2, column=0, columnspan=2)

        # Aqui es donde podemos visualizar las transferencias 
        tk.Button(self, text="Ver transacciones", command=self.view_transactions).pack(pady=10)
        tk.Button(self, text="Cerrar sesión", command=lambda: controller.show_frame(LoginPage)).pack(pady=10)

    def set_user(self, username):
        self.username = username
        self.label_welcome.config(text=f"Bienvenido, {data[username]['first_name']} {data[username]['last_name']}")
        self.label_balance.config(text=f"Saldo: ${data[username]['balance']:.2f}")

    def deposit(self):
        try:
            amount = float(self.entry_deposit.get().strip())
            if amount <= 0:
                raise ValueError
            data[self.username]["balance"] += amount
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data[self.username]["transactions"].append(f"{timestamp} - Depósito: +${amount:.2f}")
            messagebox.showinfo("Éxito", f"Depósito de ${amount:.2f} realizado.")
            self.label_balance.config(text=f"Saldo: ${data[self.username]['balance']:.2f}")
            self.entry_deposit.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad válida.")

    def transfer(self):
        recipient = self.entry_transfer_user.get().strip()
        try:
            amount = float(self.entry_transfer_amount.get().strip())
            if amount <= 0:
                raise ValueError
            if recipient not in data:
                messagebox.showerror("Error", "El cliente solicitado no existe")
                return
            if data[self.username]["balance"] < amount:
                messagebox.showerror("Error", "Saldo insuficiente.")
                return

            data[self.username]["balance"] -= amount
            data[recipient]["balance"] += amount

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data[self.username]["transactions"].append(f"{timestamp} - Transferencia a {recipient}: -${amount:.2f}")
            data[recipient]["transactions"].append(f"{timestamp} - Transferencia de {self.username}: +${amount:.2f}")

            messagebox.showinfo("Éxito", f"Transferencia de ${amount:.2f} a {recipient} realizada.")
            self.label_balance.config(text=f"Saldo: ${data[self.username]['balance']:.2f}")
            self.entry_transfer_user.delete(0, tk.END)
            self.entry_transfer_amount.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad válida.")

    def view_transactions(self):
        transactions = data[self.username]["transactions"]
        if not transactions:
            messagebox.showinfo("Transacciones", "No hay transacciones registradas.")
            return
        transactions_str = "\n".join(transactions)
        messagebox.showinfo("Transacciones", transactions_str)

if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()