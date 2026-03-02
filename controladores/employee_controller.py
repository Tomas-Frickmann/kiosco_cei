
# from calendar import Calendar
# from datetime import datetime, timedelta
# from pyexpat import model

# import tkinter as tk
# from tkinter import filedialog

# from fpdf import FPDF
# from modelos.employee_model import EmployeeModel
# from modelos.main_model import MainModel
# """!!!!!!!!!!!"""
# from vistas.employee_view import EmployeeView
# """!!!!!!!!!!!"""
# from Datos import Connect as db
# from Utilitys.util_config import *

# #Faltaban
# import time
# from tkinter import messagebox

# class EmployeeController:
#     def __init__(self,root, main_body, model :MainModel):
        
  
         
#         self.modelo = model
#         self.root = root
#         self.MainBody = main_body
#         self.vista = EmployeeView(main_body,self)
#         self.employee_model= EmployeeModel()
        
#     def manejar_dni(self, entry_Dni,extra=0,motivo=None):
#         dni=entry_Dni().strip()
#         # Verificar si el DNI es válido
#         if not dni.isdigit():
#             self.vista.mostrar_mensaje("error","Error", "El DNI debe ser un número")
#             return

#         query = "SELECT nombre FROM empleados WHERE dni = ?"
#         params = (dni,)
#         result = db.execute_query("Datos/datos.db", query, params, fetch=True)

#         if not result:
#             self.vista.mostrar_mensaje("error","Error", "DNI no encontrado en la base de datos")
#             return

#         nombre=result[0][DNI]
#         if extra!=1:
#             # Verificar si el empleado ya está activo
#             if  self.modelo.esta_activo(dni):
#                 # Registrar salida
#                 self.registrar_salida(dni)

#                 #Verificar si el nombre está en la lista antes de eliminar
#                 if self.modelo.esta_activo(dni):
#                     self.modelo.actualiza_lista_activos(dni,DELETE)
                    
#                 else:
#                     self.vista.mostrar_mensaje("error","Error", f"El empleado {nombre} no está en la lista de activos.")
#             else:
#                 # Registrar entrada
#                 if self.modelo.registro_permitido():
#                     exito = self.registrar_entrada(dni,extra=0, motivo=None)
#                     if exito:
#                         self.modelo.actualiza_lista_activos(dni,ADD)
#                         self.empleados_activos.append(nombre)
#                         self.tiempo_activo.append("00:00")  # Inicializar el tiempo activo
#                         self.hora_entrada.append(datetime.now().strftime("%H:%M:%S"))  # Guardar la hora de entrada
#                         self.actualizar_tiempo_activo()
#                 else:
#                     self.vista.mostrar_mensaje("error","Error", "Máximo 2 empleados activos")
#                     return
#         else:
#             if nombre in self.empleados_activos_extra:
#                 # Registrar salida (No pedir motivo)
#                 self.registrar_salida(dni)

#                 #Verificar si el nombre está en la lista antes de eliminar
#                 if nombre in self.empleados_activos_extra:
#                     index = self.empleados_activos_extra.index(nombre)
#                     self.empleados_activos_extra.pop(index)
#                     self.tiempo_activo_extra.pop(index)  # Eliminar el tiempo correspondiente
#                     self.hora_entrada_extra.pop(index)  # Eliminar la hora de entrada correspondiente
#                     self.motivo_extra.pop(index)  # Eliminar el motivo correspondiente
#                 else:
#                    self.vista.mostrar_mensaje("error","Error", f"El empleado {nombre} no está en la lista de activos.")

#             else:
#                 # Registrar entrada
#                 if not motivo or motivo.strip() == "":
#                     self.vista.mostrar_mensaje("error","Error", "Debe ingresar un motivo para el fichaje extra")
#                     return
#                 if len(motivo) > 50:
#                     self.vista.mostrar_mensaje("error","Error", "El motivo no puede tener más de 50 caracteres.")
#                     return
#                 if len(self.empleados_activos_extra) < 2:
#                     exito = self.registrar_entrada(dni,extra=True,motivo=motivo)
#                     if exito:
#                         self.empleados_activos_extra.append(nombre)
#                         self.tiempo_activo_extra.append("00:00")  # Inicializar el tiempo activo
#                         self.hora_entrada_extra.append(datetime.now().strftime("%H:%M:%S"))  # Guardar la hora de entrada
#                         self.motivo_extra.append(motivo)  # Guardar el motivo
#                         self.actualizar_tiempo_activo()
#                 else:
#                     self.vista.mostrar_mensaje("error","Error", "Máximo 2 empleados activos")
#                     return
        
#         self.actualizar_lista_activos()
        
#         entry_Dni.delete(0, tk.END)  # Limpiar el campo de entrada
   

        
#     def actualizar_tiempo_activo(self):
#             # Verificar si la ventana principal aún existe
#             if not self.root.winfo_exists():
#                 return  # Salir si la ventana principal ya no existe
#             # Actualizar el tiempo activo para cada empleado
#             for i, empleado in enumerate(self.empleados_activos):
#                 # Calcular el tiempo transcurrido desde la hora de entrada
#                 formato_hora = "%H:%M:%S"
#                 hora_actual = datetime.now().strftime(formato_hora)
#                 tiempo_transcurrido = (
#                     datetime.strptime(hora_actual, formato_hora) - datetime.strptime(self.hora_entrada[i], formato_hora)
#                 )
#                 # Convertir el tiempo transcurrido a formato HH:MM
#                 horas, minutos = divmod(tiempo_transcurrido.seconds // 60, 60)
#                 self.tiempo_activo[i] = f"{horas:02}:{minutos:02}"
#                 if tiempo_transcurrido.total_seconds() > 14*3600:
#                     # Registrar la expulsión en la base de datos
#                     query = "SELECT dni FROM empleados WHERE nombre = ?"
#                     dni = db.execute_query("Datos/datos.db", query, (empleado,), fetch=True)  # Función para obtener el DNI del empleado
#                     self.registrar_salida(dni,forced=True)
#                     self.cargar_empleados_activos()

#             # Actualizar el tiempo activo para cada empleado extra
#             for i, empleado in enumerate(self.empleados_activos_extra):
#                 # Calcular el tiempo transcurrido desde la hora de entrada
#                 formato_hora = "%H:%M:%S"
#                 hora_actual = datetime.now().strftime(formato_hora)
#                 tiempo_transcurrido = (
#                     datetime.strptime(hora_actual, formato_hora) - datetime.strptime(self.hora_entrada_extra[i], formato_hora)
#                 )
#                 # Convertir el tiempo transcurrido a formato HH:MM
#                 horas, minutos = divmod(tiempo_transcurrido.seconds // 60, 60)
#                 self.tiempo_activo_extra[i] = f"{horas:02}:{minutos:02}"
#                 if tiempo_transcurrido.total_seconds() > 14*3600:
#                     # Registrar la expulsión en la base de datos
#                     query = "SELECT dni FROM empleados WHERE nombre = ?"
#                     dni = db.execute_query("Datos/datos.db", query, (empleado,), fetch=True)  # Función para obtener el DNI del empleado
#                     self.registrar_salida(dni,forced=True)
#                     self.cargar_empleados_activos()

#             # Actualizar la interfaz
#             self.actualizar_lista_activos()

#             # Llamar a esta función nuevamente después de 60 segundos
#             self.root.after(60000, lambda: self.actualizar_tiempo_activo())
            
#     def cargar_empleados_activos(self):
#         # Consulta para obtener empleados sin hora de salida
#         query = "SELECT dni, nombre,fecha, hora_entrada FROM registros WHERE hora_salida IS NULL AND motivo IS NULL "
#         empleados_sin_salida = db.execute_query("Datos/datos.db", query, fetch=True)

#         query_extra = "SELECT dni, nombre,fecha, hora_entrada, motivo FROM registros WHERE hora_salida IS NULL AND motivo IS NOT NULL "
#         empleados_sin_salida_extra = db.execute_query("Datos/datos.db", query_extra, fetch=True)
#         # Limpiar las listas globales
#         self.empleados_activos.clear()
#         self.empleados_activos_extra.clear()
#         self.tiempo_activo.clear()
#         self.tiempo_activo_extra.clear()
#         self.hora_entrada.clear()
#         self.hora_entrada_extra.clear()
#         self.motivo_extra.clear()

#         # Reconstruir las listas
#         for registro in empleados_sin_salida:
#             dni, nombre,fecha_db, hora_entrada_db = registro
#             self.empleados_activos.append(nombre)
#             self.hora_entrada.append(hora_entrada_db)

#             # Calcular el tiempo activo desde la hora de entrada
#             formato_fecha = "%Y-%m-%d"
#             formato_hora = "%H:%M:%S"
#             entrada_completa = datetime.combine(
#             datetime.strptime(fecha_db, formato_fecha).date(),
#             datetime.strptime(hora_entrada_db, formato_hora).time())
#             hora_actual = datetime.now()
#             tiempo_transcurrido = hora_actual - entrada_completa
#             horas, minutos = divmod(tiempo_transcurrido.seconds // 60, 60)
#             self.tiempo_activo.append(f"{horas:02}:{minutos:02}")

#             # Verificar si el tiempo supera las 14 horas
#             if tiempo_transcurrido.total_seconds() > 14*3600:
#                 # Registrar la expulsión en la base de datos
#                 query = "SELECT dni FROM empleados WHERE nombre = ?"
#                 dni = db.execute_query("Datos/datos.db", query, (nombre,), fetch=True)  # Función para obtener el DNI del empleado
#                 self.registrar_salida(dni,forced=True)
#                 self.cargar_empleados_activos()

#         for registro in empleados_sin_salida_extra:
#             dni, nombre,fecha_db, hora_entrada_db, motivo_db = registro
#             self.empleados_activos_extra.append(nombre)
#             self.hora_entrada_extra.append(hora_entrada_db)
#             self.motivo_extra.append(motivo_db)

#             # Calcular el tiempo activo desde la hora de entrada
#             formato_fecha = "%Y-%m-%d"
#             formato_hora = "%H:%M:%S"
#             entrada_completa = datetime.combine(
#             datetime.strptime(fecha_db, formato_fecha).date(),
#             datetime.strptime(hora_entrada_db, formato_hora).time())
#             hora_actual = datetime.now()
#             tiempo_transcurrido = hora_actual - entrada_completa
#             horas, minutos = divmod(tiempo_transcurrido.seconds // 60, 60)
#             self.tiempo_activo_extra.append(f"{horas:02}:{minutos:02}")

#             # Verificar si el tiempo supera las 14 horas
#             if tiempo_transcurrido.total_seconds() > 14*3600:
#                 # Registrar la expulsión en la base de datos
#                 query = "SELECT dni FROM empleados WHERE nombre = ?"
#                 dni = db.execute_query("Datos/datos.db", query, (nombre,), fetch=True)
#                 self.registrar_salida(dni,forced=True)
#                 self.cargar_empleados_activos()
        

#         # Actualizar las listas en la interfaz
#         self.actualizar_lista_activos()

#         # Iniciar el cronómetro para actualizar los tiempos activos
#         self.actualizar_tiempo_activo()
        
#     def  add_employee(self):
#         if self.modelo.es_admin():
#             self.vista.view_add_employee()
#         else:
#             self.vista.mostrar_mensaje ("error","Error", "No tienes permiso para acceder a esta función.")
    

    
  
        
    
#     def abrir_ventana(self, title):
#         if self.modelo.es_admin():
#             self.vista.abrir_ventana(title)
#         else:
#             self.vista.mostrar_mensaje ("error","Error", "No tienes permiso para acceder a esta función.")
            
#     def guardar_nuevo_empleado(self, nombre, dni, ventana):
#             # Validar que los campos no estén vacíos
#             if not nombre.strip() or not dni.strip():
#                 self.vista.mostrar_mensaje("error","Error", "Todos los campos son obligatorios.")
#                 return

#             # Validar que el DNI sea un número
#             if not dni.isdigit():
#                 self.vista.mostrar_mensaje("error","Error", "El DNI debe ser un número.")
#                 return

#             # Verificar si el DNI ya existe en la base de datos
#             query_verificar = "SELECT * FROM empleados WHERE dni = ?"
#             params_verificar = (dni,)
#             resultado = db.execute_query("Datos/datos.db", query_verificar, params_verificar, fetch=True)

#             if resultado:
#                 self.vista.mostrar_mensaje("error","Error", "El DNI ingresado ya existe en la base de datos.")
#                 return

#             # Insertar el nuevo empleado en la base de datos
#             query_insertar = "INSERT INTO empleados (nombre, dni) VALUES (?, ?)"
#             params_insertar = (nombre.strip(), dni.strip())
#             db.execute_query("Datos/datos.db", query_insertar, params_insertar)

#             # Actualizar la tabla de empleados en la interfaz
#             self.vista.TablaEmpleados(self.frame_nombre, self.frame_dni, "dni")

#             # Cerrar la ventana y mostrar un mensaje de éxito
#             ventana.destroy()
#             self.vista.mostrar_mensaje("info","Éxito", "Empleado agregado correctamente.") 
            
#     def guardar_cambios(self, nuevo_nombre, nuevo_dni, nombre, dni, ventana):
#         # Actualizar la base de datos en la tabla "empleados"
#             query = "UPDATE empleados SET nombre = ?, dni = ? WHERE nombre = ? AND dni = ?"
#             params = (nombre, dni, nombre, dni)
#             db.execute_query("Datos/datos.db", query, params)

#             # Actualizar los registros asociados en la tabla registros
#             query_registros = "UPDATE registros SET nombre = ?, dni = ? WHERE nombre = ? AND dni = ?"
#             params_registros = (nombre, dni, nombre, dni)
#             db.execute_query("Datos/datos.db", query_registros, params_registros)

#             # Actualizar la tabla
#             self.vista.TablaEmpleados(self.frame_nombre, self.frame_dni, "dni")
#             # Cerrar la ventana de edición
#             ventana.destroy()
#             self.vista.mostrar_mensaje("info","Información", "Empleado actualizado correctamente")
    
#     def delete_employee(self, nombre,dni, accion,ventana):
      
#             print(f"Intentando eliminar: {nombre} con DNI {dni}")
#             respuesta = self.vista.mostrar_mensaje("question","Confirmación", f"¿Estás seguro de que deseas eliminar al empleado {nombre} con DNI {dni}?")
#             print(f"Respuesta del usuario: {respuesta}")
#             if not respuesta:
#                 return
            
#             # Eliminar al empleado de la tabla empleados
#             query_empleado = "DELETE FROM empleados WHERE dni = ?"
#             db.execute_query("Datos/datos.db", query_empleado, (dni,))
#             print(f"Ejecutando consulta: {query_empleado} con DNI {dni}")

#             # Eliminar los registros asociados en la tabla registros
#             query_registros = "DELETE FROM registros WHERE dni = ?"
#             db.execute_query("Datos/datos.db", query_registros, (dni,))
#             print(f"se borro: {query_empleado} con DNI {dni}")

#             # Actualizar la tabla de empleados en la interfaz
#             self.vista.TablaEmpleados(self.frame_nombre, self.frame_dni, "dni")
#             print("Tabla actualizada después de la eliminación")
            
#             # Mostrar mensaje de éxito
#             self.vista.mostrar_mensaje("info","Éxito", f"Empleado {nombre} y sus registros han sido eliminados correctamente.")
        
        

# # REGISTRAR# ENTRADA Y SALIDA
#     def registrar_entrada(self, dni,extra=0,motivo=None):
#         # Verificar si el DNI existe en la tabla de empleados
#         query_empleado = "SELECT nombre FROM empleados WHERE dni = ?"
#         params_empleado = (dni,)
#         empleado = db.execute_query("Datos/datos.db", query_empleado, params_empleado, fetch=True)

#         if not empleado:
#             messagebox.showerror("Error", "El DNI ingresado no existe en la base de datos.")
#             return False

#         # Verificar si hay un registro pendiente en la tabla de registros
#         query_registro = "SELECT id FROM registros WHERE dni = ? AND hora_salida IS NULL"
#         params_registro = (dni,)
#         registro_pendiente = db.execute_query("Datos/datos.db", query_registro, params_registro, fetch=True)

#         if registro_pendiente:
#             messagebox.showerror("Error", "Ya existe un registro pendiente. Debe registrar la salida antes de ingresar nuevamente.")
#             return False

#         # Insertar un nuevo registro con la fecha y hora actuales
#         fecha_actual = time.strftime("%Y-%m-%d")
#         hora_actual = time.strftime("%H:%M:%S")
#         query_insert = "INSERT INTO registros (dni, nombre, fecha, hora_entrada, extra, motivo) VALUES (?, ?, ?, ?, ? ,?)"
#         params_insert = (dni, empleado[0][0], fecha_actual, hora_actual,extra,motivo)
#         db.execute_query("Datos/datos.db", query_insert, params_insert)

#         messagebox.showinfo("Éxito", "Registro de entrada realizado correctamente.")
#         return True

#     def registrar_salida(self,dni,forced=False):
#         # Verificar si hay un registro pendiente en la tabla de registros
#         if isinstance(dni, list) and len(dni) > 0 and isinstance(dni[0], tuple):
#             dni = dni[0][0]  # Extraer el valor del primer elemento de la primera tupla
#         query_registro = "SELECT id, hora_entrada FROM registros WHERE dni = ? AND hora_salida IS NULL"
#         params_registro = (dni,)
#         registro_pendiente = db.execute_query("Datos/datos.db", query_registro, params_registro, fetch=True)
#         if not registro_pendiente:
#             messagebox.showerror("Error", "No hay un registro pendiente. Debe registrar su entrada primero.")
#             return
        
#         # Obtener la hora actual
#         hora_actual = time.strftime("%H:%M:%S")
#         # Calcular el tiempo trabajado
#         hora_entrada = registro_pendiente[0][1]
#         formato_hora = "%H:%M:%S"
        
#         if forced:
#             # Calcular la hora de salida como hora de entrada + 1 minuto
#             hora_salida = (datetime.strptime(hora_entrada, formato_hora) + timedelta(minutes=1)).strftime(formato_hora)

#             # Registrar la salida con tiempo total de 1 minuto y marcar como expulsión
#             query_update = """
#                 UPDATE registros
#                 SET hora_salida = ?, tiempo_total = ?, expulsion = ?
#                 WHERE id = ?
#             """
#             params_update = (hora_salida, "00:01:00", 1, registro_pendiente[0][0])
#             db.execute_query("Datos/datos.db", query_update, params_update)
#             messagebox.showinfo("Expulsión", "El empleado ha sido expulsado y su registro ha sido actualizado.")
#         else:
#             tiempo_trabajado = (
#                 datetime.strptime(hora_actual, formato_hora) - datetime.strptime(hora_entrada, formato_hora)
#             )

#             # Actualizar el registro con la hora de salida y el tiempo trabajado
#             query_update = "UPDATE registros SET hora_salida = ?, tiempo_total = ? WHERE id = ?"
#             params_update = (hora_actual, str(tiempo_trabajado), registro_pendiente[0][0])
#             db.execute_query("Datos/datos.db", query_update, params_update)
#             messagebox.showinfo("Éxito", "Registro de salida realizado correctamente.")
            


# #CONSULTAR Y GENERAR INFORME DE EMPLEADOS
#     def consultar_empleados(self):
#         if self.modelo.es_admin():
#             # Crear una ventana para seleccionar el rango de fechas
#             ventana_fechas = tk.Toplevel(self.root, bg=color_menu_lateral)
#             ventana_fechas.title("Consultar Empleados")
#             ventana_fechas.geometry("560x400")
#             #Frame de calendarios
#             Frame_botones=tk.Frame(ventana_fechas,bg=color_menu_lateral,padx=10,pady=10)
#             Frame_botones.pack(side=tk.BOTTOM,fill='both',expand=False)
#             Frame_inicio=tk.Frame(ventana_fechas,bg=color_menu_lateral,padx=10,pady=10)
#             Frame_inicio.pack(side=tk.LEFT,fill='both',expand=False)
#             Frame_fin=tk.Frame(ventana_fechas,bg=color_menu_lateral,padx=10,pady=10)
#             Frame_fin.pack(side=tk.LEFT,fill='both',expand=False)

#             # Fecha actual
#             fecha_actual = datetime.now()
#             primer_dia_mes = fecha_actual.replace(day=1)

#             # Etiqueta para la fecha de inicio
#             label_inicio = tk.Label(Frame_inicio, text="Fecha de inicio:", font=('Calibri', 12), bg=color_menu_lateral, fg="white")
#             label_inicio.pack(pady=10)

#             # Calendario para la fecha de inicio
#             calendario_inicio = Calendar(Frame_inicio, selectmode="day", date_pattern="yyyy-mm-dd")
#             calendario_inicio.pack(pady=10)
#             calendario_inicio.selection_set(primer_dia_mes.strftime("%Y-%m-%d"))  # Seleccionar el primer día del mes actual

#             # Etiqueta para la fecha de fin
#             label_fin = tk.Label(Frame_fin, text="Fecha de fin:", font=('Calibri', 12), bg=color_menu_lateral, fg="white")
#             label_fin.pack(pady=10)

#             # Calendario para la fecha de fin
#             calendario_fin = Calendar(Frame_fin, selectmode="day", date_pattern="yyyy-mm-dd")
#             calendario_fin.pack(pady=10)
#             calendario_fin.selection_set(fecha_actual.strftime("%Y-%m-%d"))  # Seleccionar la fecha actual

#             # Botón para generar el informe
#             boton_generar = tk.Button(
#                 Frame_botones,
#                 text="Generar Informe",
#                 font=('Calibri', 12),
#                 bg='#6D8299',
#                 fg='white',
#                 command=lambda: self.generar_informe(calendario_inicio.get_date(), calendario_fin.get_date(), ventana_fechas)
#             )
#             boton_generar.pack(pady=10)

#             # Botón para cancelar
#             boton_cancelar = tk.Button(
#                 Frame_botones,
#                 text="Cancelar",
#                 font=('Calibri', 12),
#                 bg='#FF6B6B',
#                 fg='white',
#                 command=ventana_fechas.destroy
#             )
#             boton_cancelar.pack(pady=10)
#         else:
#             messagebox.showerror("Error", "No tienes permiso para acceder a esta función.")

#     def generar_informe(self, fecha_inicio, fecha_fin, ventana):
#         # Validar las fechas
#         try:
#             fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
#             fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
#         except ValueError:
#             messagebox.showerror("Error", "Las fechas deben estar en formato YYYY-MM-DD.")
#             return

#         if fecha_inicio > fecha_fin:
#             messagebox.showerror("Error", "La fecha de inicio no puede ser mayor que la fecha de fin.")
#             return

#         # Consultar los registros en el rango de fechas
#         query = """
#             SELECT dni, nombre, fecha, hora_entrada, hora_salida, tiempo_total , COALESCE(expulsion,0) AS expulsion
#             FROM registros
#             WHERE fecha BETWEEN ? AND ?
#         """
#         params = (fecha_inicio.strftime("%Y-%m-%d"), fecha_fin.strftime("%Y-%m-%d"))
#         registros = db.execute_query("Datos/datos.db", query, params, fetch=True)

#         if not registros:
#             messagebox.showinfo("Sin resultados", "No se encontraron registros en el rango de fechas seleccionado.")
#             return

#         # Agrupar registros por empleado y sumar tiempos totales
#         empleados = {}
#         for registro in registros:
#             dni, nombre, fecha, hora_entrada, hora_salida, tiempo_total, expulsion = registro
#             if nombre not in empleados:
#                 empleados[nombre] = {"registros": [], "tiempo_total": datetime.strptime("00:00:00", "%H:%M:%S")}
#             empleados[nombre]["registros"].append((fecha, hora_entrada, hora_salida, tiempo_total,expulsion))
#             if tiempo_total:
#                 tiempo_total_dt = datetime.strptime(tiempo_total, "%H:%M:%S")
#                 empleados[nombre]["tiempo_total"] += timedelta(
#                     hours=tiempo_total_dt.hour, minutes=tiempo_total_dt.minute, seconds=tiempo_total_dt.second
#                 )

#         # Preguntar al usuario dónde guardar el archivo
#         ruta_guardado = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
#         if not ruta_guardado:
#             messagebox.showinfo("Cancelado", "No se guardó el informe.")
#             return

#         # Generar el PDF
#         pdf = FPDF()
#         pdf.set_auto_page_break(auto=True, margin=15)
#         pdf.add_page()
#         pdf.set_font("Arial", size=12)

#         pdf.cell(200, 10, txt="Informe de Registros", ln=True, align="C")
#         pdf.cell(200, 10, txt=f"Rango de fechas: {fecha_inicio.strftime('%Y-%m-%d')} - {fecha_fin.strftime('%Y-%m-%d')}", ln=True, align="C")
#         pdf.ln(10)

#         for nombre, datos in empleados.items():
#             pdf.set_font("Arial", style="B", size=12)
#             pdf.set_fill_color(200, 220, 255)
#             pdf.cell(176, 10, txt=f"Empleado: {nombre}", ln=True, align="L",fill=True)
#             pdf.set_font("Arial", size=10)
#             pdf.cell(176, 10, txt=f"Tiempo total: {datos['tiempo_total'].strftime('%H:%M:%S')}", ln=True, align="L",fill=True)
#             pdf.ln(5)

#             # Encabezados de la tabla
#             pdf.cell(44, 8, txt="Fecha", border=1, align="C")
#             pdf.cell(44, 8, txt="Hora Entrada", border=1, align="C")
#             pdf.cell(44, 8, txt="Hora Salida", border=1, align="C")
#             pdf.cell(44, 8, txt="Tiempo Total", border=1, align="C")
#             pdf.ln()

#             # Registros del empleado
#             for i,registro in enumerate(datos["registros"]):
#                 fecha, hora_entrada, hora_salida, tiempo_total,expulsion = registro

#                 # Asegurarse de que los valores no sean None
#                 fecha = fecha if fecha else "N/A"
#                 hora_entrada = hora_entrada if hora_entrada else "N/A"
#                 hora_salida = hora_salida if hora_salida else "N/A"
#                 tiempo_total = tiempo_total if tiempo_total else "N/A"

#                 # Alternar colores de fondo
#                 if expulsion == 1:
#                     pdf.set_fill_color(255, 0, 0)  # Rojo
#                 elif i % 2 == 0:
#                     pdf.set_fill_color(220, 240, 220)  # Verde clarito
#                 else:
#                     pdf.set_fill_color(255, 255, 255)  # Blanco

#                 pdf.cell(44, 7, txt=str(fecha), border=1, align="C",fill=True)
#                 pdf.cell(44, 7, txt=str(hora_entrada), border=1, align="C",fill=True)
#                 pdf.cell(44, 7, txt=str(hora_salida), border=1, align="C",fill=True)
#                 pdf.cell(44, 7, txt=str(tiempo_total), border=1, align="C",fill=True)
#                 pdf.ln()

#             # Espacio entre empleados
#             pdf.ln(10)

#         # Guardar el PDF
#         pdf.output(ruta_guardado)
#         messagebox.showinfo("Éxito", f"Informe guardado correctamente en {ruta_guardado}")

#     def getEmpleados(self):
#         return db.GetEmpleados()
#     def getEmpleados_activos(self):
#         return self.modelo.dnis_activos

import time
from datetime import datetime, timedelta
from modelos.employee_model import EmployeeModel
from vistas.employee_view import EmployeeView

class EmployeeController:
    def __init__(self, root, main_body, main_modelo):
        # 1. Guardamos al jefe principal (para saber si es admin)
        self.main_modelo = main_modelo
        self.root = root
        
        # 2. Creamos el modelo de empleados (el que habla con la base de datos)
        self.employee_model = EmployeeModel()

        # 3. Creamos la vista y le pasamos este controlador
        self.vista = EmployeeView(root,main_body, self)
        self.actualizar_tiempo_activo()

    # ==========================================
    # LECTURA DE DATOS BÁSICOS
    # ==========================================
    def getEmpleados(self):
        # Le pide la lista al modelo y se la pasa a la vista
        return self.employee_model.obtener_todos_los_empleados()

    def getEmpleados_activos(self):
        return self.employee_model.dnis_activos

    # ==========================================
    # GESTIÓN DE PANELES Y PERMISOS
    # ==========================================
    def add_employee(self):
        if self.main_modelo.es_admin:
            self.vista.view_add_employee() # La vista dibuja la ventanita
        else:
            self.vista.mostrar_mensaje("error", "Error", "No tienes permiso para acceder a esta función.")

    def abrir_ventana(self, title):
        if self.main_modelo.es_admin:
            self.vista.abrir_ventana(title)
        else:
            self.vista.mostrar_mensaje("error", "Error", "No tienes permiso para acceder a esta función.")

    def consultar_empleados(self):
        if self.main_modelo.es_admin:
            self.vista.abrir_ventana_consulta() # La vista dibuja los calendarios
        else:
            self.vista.mostrar_mensaje("error", "Error", "No tienes permiso para acceder a esta función.")

    # ==========================================
    # ABM EMPLEADOS (Agregar, Editar, Borrar)
    # ==========================================
    def guardar_nuevo_empleado(self, nombre, dni, ventana):
        # 1. Validaciones
        if not nombre.strip() or not dni.strip():
            self.vista.mostrar_mensaje("error", "Error", "Todos los campos son obligatorios.")
            return

        if not dni.isdigit():
            self.vista.mostrar_mensaje("error", "Error", "El DNI debe ser un número.")
            return

        # 2. Verificar en el modelo si existe
        if self.employee_model.verificar_dni_existe(dni):
            self.vista.mostrar_mensaje("error", "Error", "El DNI ingresado ya existe en la base de datos.")
            return

        # 3. Guardar usando el modelo
        self.employee_model.guardar_empleado(nombre, dni)

        # 4. Actualizar pantalla
        self.vista.TablaEmpleados(self.vista.frame_nombre, self.vista.frame_dni, "dni")
        ventana.destroy()
        self.vista.mostrar_mensaje("info", "Éxito", "Empleado agregado correctamente.") 

    def guardar_cambios(self, nuevo_nombre, nuevo_dni, nombre_viejo, dni_viejo, ventana):
        self.employee_model.actualizar_empleado(nuevo_nombre, nuevo_dni, nombre_viejo, dni_viejo)
        self.vista.TablaEmpleados(self.vista.frame_nombre, self.vista.frame_dni, "dni")
        ventana.destroy()
        self.vista.mostrar_mensaje("info", "Información", "Empleado actualizado correctamente")

    def delete_employee(self, nombre, dni, accion, ventana=None):
        respuesta = self.vista.mostrar_mensaje("question", "Confirmación", f"¿Estás seguro de que deseas eliminar al empleado {nombre} con DNI {dni}?")
        
        if not respuesta:
            return
        
        # Le da la orden al modelo
        self.employee_model.eliminar_empleado(dni)

        # Actualiza la pantalla
        self.vista.TablaEmpleados(self.vista.frame_nombre, self.vista.frame_dni, "dni")
        self.vista.mostrar_mensaje("info", "Éxito", f"Empleado {nombre} y sus registros han sido eliminados.")

    # ==========================================
    # FICHAJE (Entradas y Salidas)
    # ==========================================
    def manejar_dni(self, dni_ingresado, extra=0, motivo=None):
        dni = dni_ingresado.strip()
        
        if not dni.isdigit():
            self.vista.mostrar_mensaje("error", "Error", "El DNI debe ser un número")
            return

        # Busca el nombre en la BD
        nombre = self.employee_model.obtener_nombre_por_dni(dni)
        if not nombre:
            self.vista.mostrar_mensaje("error", "Error", "DNI no encontrado en la base de datos")
            return

        # Lógica de fichaje (Normal o Extra)
        if extra != 1:
            if self.employee_model.esta_activo(dni):
                self.registrar_salida(dni)
            else:
                if self.employee_model.cantidad_activos_normales() < 2:
                    self.registrar_entrada(dni, extra=0)
                else:
                    self.vista.mostrar_mensaje("error", "Error", "Máximo 2 empleados activos")
                    return
        else:
            if self.employee_model.esta_activo_extra(dni):
                self.registrar_salida(dni)
            else:
                if not motivo or motivo.strip() == "":
                    self.vista.mostrar_mensaje("error", "Error", "Debe ingresar un motivo para el fichaje extra")
                    return
                if len(motivo) > 50:
                    self.vista.mostrar_mensaje("error", "Error", "El motivo no puede tener más de 50 caracteres.")
                    return
                if self.employee_model.cantidad_activos_extra() < 2:
                    self.registrar_entrada(dni, extra=1, motivo=motivo)
                else:
                    self.vista.mostrar_mensaje("error", "Error", "Máximo 2 empleados extra activos")
                    return

        # Le dice a la vista que refresque las cajitas visuales
        self.actualizar_tiempo_activo()

    def registrar_entrada(self, dni, extra=0, motivo=None):
        if self.employee_model.tiene_registro_pendiente(dni):
            self.vista.mostrar_mensaje("error", "Error", "Ya existe un registro pendiente. Registre la salida primero.")
        else:
         self.employee_model.crear_registro_entrada(dni, extra, motivo)
         self.cargar_empleados_activos()
         self.vista.mostrar_mensaje("info", "Éxito", "Registro de entrada realizado correctamente.")
         
        

    def registrar_salida(self, dni, forced=False):
        if isinstance(dni, list) and len(dni) > 0 and isinstance(dni[0], tuple):
            dni = dni[0][0]

        registro_pendiente = self.employee_model.obtener_registro_pendiente(dni)
        
        if not registro_pendiente:
            self.vista.mostrar_mensaje("error", "Error", "No hay un registro pendiente. Debe registrar su entrada primero.")
            return

        id_registro = registro_pendiente["id"]
        hora_entrada = registro_pendiente["hora_entrada"]

        if forced:
            self.employee_model.forzar_salida(id_registro, hora_entrada)
            self.vista.mostrar_mensaje("info", "Expulsión", "El empleado ha sido expulsado por límite de horas.")
        else:
            self.employee_model.marcar_salida_normal(id_registro, hora_entrada)
            self.vista.mostrar_mensaje("info", "Éxito", "Registro de salida realizado correctamente.")

    # ==========================================
    # REPORTES
    # ==========================================
    def generar_informe(self, fecha_inicio, fecha_fin, ventana):
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            self.vista.mostrar_mensaje("error","Error", "Las fechas deben estar en formato YYYY-MM-DD.")
            return
        if fecha_inicio > fecha_fin:
            self.vista.mostrar_mensaje("error", "Error", "La fecha de inicio no puede ser mayor que la fecha de fin.")
            return

        # El modelo busca los registros en la BD
        registros = self.employee_model.obtener_registros_por_fecha(fecha_inicio, fecha_fin)

        if not registros:
            self.vista.mostrar_mensaje("info", "Sin resultados", "No se encontraron registros en esas fechas.")
            return

        # Le pedimos a la vista que abra la ventanita de "Guardar como..."
        ruta_guardado = self.vista.pedir_ruta_guardado()
        
        if not ruta_guardado:
            return # El usuario canceló

        # El modelo fabrica el PDF internamente
        self.employee_model.generar_pdf(registros, fecha_inicio, fecha_fin, ruta_guardado)
        
        self.vista.mostrar_mensaje("info", "Éxito", f"Informe guardado correctamente en {ruta_guardado}")
        ventana.destroy()

    def cargar_empleados_activos(self):
        try:
            # 1. Pedimos a la BD quiénes están trabajando
            activos = self.employee_model.obtener_empleados_trabajando()
            
            # PARCHE SALVAVIDAS: Si la BD no devuelve nada (None), nos aseguramos que sea una lista vacía
            if activos is None:
                activos = []

            # 2. Vaciamos la memoria temporal
            self.employee_model.dnis_activos.clear()
            self.employee_model.dnis_activos_extra.clear()
            
            # 3. Preparamos las listas
            datos_vista = {"normales": [], "extras": []}
            
            for emp in activos:
                # Soporte por si tu base de datos devuelve tuplas en vez de diccionario
                if isinstance(emp, tuple):
                    dni, nombre, fecha, hora_entrada, extra, motivo = emp[1], emp[2], emp[3], emp[4], emp[5], emp[6]
                else:
                    dni, nombre, fecha, hora_entrada, extra, motivo = emp["dni"], emp["nombre"], emp["fecha"], emp["hora_entrada"], emp["extra"], emp["motivo"]
                
                # Asegurarnos de que no haya campos vacíos que rompan la fecha
                if not fecha or not hora_entrada:
                    continue

                # Calculamos el tiempo transcurrido
                entrada_completa = datetime.combine(
                    datetime.strptime(fecha, "%Y-%m-%d").date(),
                    datetime.strptime(hora_entrada, "%H:%M:%S").time()
                )
                tiempo_transcurrido = datetime.now() - entrada_completa
                
                # Si pasaron más de 14 horas, lo expulsamos
                if tiempo_transcurrido.total_seconds() > 14 * 3600:
                    self.registrar_salida(dni, forced=True)
                    continue 

                horas, minutos = divmod(tiempo_transcurrido.seconds // 60, 60)
                tiempo_str = f"{horas:02}:{minutos:02}"
                
                # Guardamos para la pantalla
                if extra == 1:
                    self.employee_model.dnis_activos_extra.append(dni)
                    datos_vista["extras"].append({"nombre": nombre, "tiempo": tiempo_str, "motivo": motivo})
                else:
                    self.employee_model.dnis_activos.append(dni)
                    datos_vista["normales"].append({"nombre": nombre, "tiempo": tiempo_str})

            # 4. Mandamos los datos a la Vista
            self.vista.actualizar_lista_activos(datos_vista)
            
        except Exception as e:
            # SI HAY UN ERROR OCULTO, ESTO IMPRIME EL MOTIVO EXACTO EN LA TERMINAL EN VEZ DE CERRARSE
            print(f"====================================")
            print(f" ERROR FATAL EN EL RELOJ: {e}")
            print(f"====================================")
            
    def actualizar_tiempo_activo(self):
        if not self.root.winfo_exists():
            return
        
        # Calcula todo y actualiza la pantalla
        self.cargar_empleados_activos()
        
        # Se vuelve a llamar a sí misma cada 60 segundos
        self.root.after(60000, self.actualizar_tiempo_activo)