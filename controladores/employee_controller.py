from vistas.employee_view import PanelEmpleados
from Datos import Connect as db

class EmployeeController:
    def __init__(self,root, main_body, model):
        
        self.empleados_activos = []
        self.empleados_activos_extra = []
        self.tiempo_activo = []
        self.tiempo_activo_extra = []
        self.hora_entrada = []
        self.hora_entrada_extra = []
        self.motivo_extra = []
         
        self.modelo = model
        
        self.MainBody = main_body
        self.vista = PanelEmpleados(main_body, self)
        
    def manejar_dni(self, entry_Dni,extra=0,motivo=None):
        dni=entry_Dni.get().strip()
        # Verificar si el DNI es válido
        if not dni.isdigit():
            messagebox.showerror("Error", "El DNI debe ser un número")
            return

        query = "SELECT nombre FROM empleados WHERE dni = ?"
        params = (dni,)
        result = db.execute_query("Datos/datos.db", query, params, fetch=True)

        if not result:
            messagebox.showerror("Error", "DNI no encontrado en la base de datos")
            return

        nombre = result[0][0]
        if extra!=1:
            # Verificar si el empleado ya está activo
            if nombre in self.empleados_activos:
                # Registrar salida
                self.registrar_salida(dni)

                #Verificar si el nombre está en la lista antes de eliminar
                if nombre in self.empleados_activos:
                    index = self.empleados_activos.index(nombre)
                    self.empleados_activos.pop(index)
                    self.tiempo_activo.pop(index)  # Eliminar el tiempo correspondiente
                    self.hora_entrada.pop(index)  # Eliminar la hora de entrada correspondiente
                else:
                    messagebox.showerror("Error", f"El empleado {nombre} no está en la lista de activos.")
            else:
                # Registrar entrada
                if len(self.empleados_activos) < 2:
                    exito = self.registrar_entrada(dni,extra=0, motivo=None)
                    if exito:
                        self.empleados_activos.append(nombre)
                        self.tiempo_activo.append("00:00")  # Inicializar el tiempo activo
                        self.hora_entrada.append(datetime.now().strftime("%H:%M:%S"))  # Guardar la hora de entrada
                        self.actualizar_tiempo_activo()
                else:
                    messagebox.showerror("Error", "Máximo 2 empleados activos")
                    return
        else:
            if nombre in self.empleados_activos_extra:
                # Registrar salida (No pedir motivo)
                self.registrar_salida(dni)

                #Verificar si el nombre está en la lista antes de eliminar
                if nombre in self.empleados_activos_extra:
                    index = self.empleados_activos_extra.index(nombre)
                    self.empleados_activos_extra.pop(index)
                    self.tiempo_activo_extra.pop(index)  # Eliminar el tiempo correspondiente
                    self.hora_entrada_extra.pop(index)  # Eliminar la hora de entrada correspondiente
                    self.motivo_extra.pop(index)  # Eliminar el motivo correspondiente
                else:
                    messagebox.showerror("Error", f"El empleado {nombre} no está en la lista de activos.")

            else:
                # Registrar entrada
                if not motivo or motivo.strip() == "":
                    messagebox.showerror("Error", "Debe ingresar un motivo para el fichaje extra")
                    return
                if len(motivo) > 50:
                    messagebox.showerror("Error", "El motivo no puede tener más de 50 caracteres.")
                    return
                if len(self.empleados_activos_extra) < 2:
                    exito = self.registrar_entrada(dni,extra=True,motivo=motivo)
                    if exito:
                        self.empleados_activos_extra.append(nombre)
                        self.tiempo_activo_extra.append("00:00")  # Inicializar el tiempo activo
                        self.hora_entrada_extra.append(datetime.now().strftime("%H:%M:%S"))  # Guardar la hora de entrada
                        self.motivo_extra.append(motivo)  # Guardar el motivo
                        self.actualizar_tiempo_activo()
                else:
                    messagebox.showerror("Error", "Máximo 2 empleados activos")
                    return
        
        self.actualizar_lista_activos()
        
        entry_Dni.delete(0, tk.END)  # Limpiar el campo de entrada
   

        
    def actualizar_tiempo_activo(self):
            # Verificar si la ventana principal aún existe
            if not self.root.winfo_exists():
                return  # Salir si la ventana principal ya no existe
            # Actualizar el tiempo activo para cada empleado
            for i, empleado in enumerate(self.empleados_activos):
                # Calcular el tiempo transcurrido desde la hora de entrada
                formato_hora = "%H:%M:%S"
                hora_actual = datetime.now().strftime(formato_hora)
                tiempo_transcurrido = (
                    datetime.strptime(hora_actual, formato_hora) - datetime.strptime(self.hora_entrada[i], formato_hora)
                )
                # Convertir el tiempo transcurrido a formato HH:MM
                horas, minutos = divmod(tiempo_transcurrido.seconds // 60, 60)
                self.tiempo_activo[i] = f"{horas:02}:{minutos:02}"
                if tiempo_transcurrido.total_seconds() > 14*3600:
                    # Registrar la expulsión en la base de datos
                    query = "SELECT dni FROM empleados WHERE nombre = ?"
                    dni = db.execute_query("Datos/datos.db", query, (empleado,), fetch=True)  # Función para obtener el DNI del empleado
                    self.registrar_salida(dni,forced=True)
                    self.cargar_empleados_activos()

            # Actualizar el tiempo activo para cada empleado extra
            for i, empleado in enumerate(self.empleados_activos_extra):
                # Calcular el tiempo transcurrido desde la hora de entrada
                formato_hora = "%H:%M:%S"
                hora_actual = datetime.now().strftime(formato_hora)
                tiempo_transcurrido = (
                    datetime.strptime(hora_actual, formato_hora) - datetime.strptime(self.hora_entrada_extra[i], formato_hora)
                )
                # Convertir el tiempo transcurrido a formato HH:MM
                horas, minutos = divmod(tiempo_transcurrido.seconds // 60, 60)
                self.tiempo_activo_extra[i] = f"{horas:02}:{minutos:02}"
                if tiempo_transcurrido.total_seconds() > 14*3600:
                    # Registrar la expulsión en la base de datos
                    query = "SELECT dni FROM empleados WHERE nombre = ?"
                    dni = db.execute_query("Datos/datos.db", query, (empleado,), fetch=True)  # Función para obtener el DNI del empleado
                    self.registrar_salida(dni,forced=True)
                    self.cargar_empleados_activos()

            # Actualizar la interfaz
            self.actualizar_lista_activos()

            # Llamar a esta función nuevamente después de 60 segundos
            self.root.after(60000, lambda: self.actualizar_tiempo_activo())
            
    def cargar_empleados_activos(self):
        # Consulta para obtener empleados sin hora de salida
        query = "SELECT dni, nombre,fecha, hora_entrada FROM registros WHERE hora_salida IS NULL AND motivo IS NULL "
        empleados_sin_salida = db.execute_query("Datos/datos.db", query, fetch=True)

        query_extra = "SELECT dni, nombre,fecha, hora_entrada, motivo FROM registros WHERE hora_salida IS NULL AND motivo IS NOT NULL "
        empleados_sin_salida_extra = db.execute_query("Datos/datos.db", query_extra, fetch=True)
        # Limpiar las listas globales
        self.empleados_activos.clear()
        self.empleados_activos_extra.clear()
        self.tiempo_activo.clear()
        self.tiempo_activo_extra.clear()
        self.hora_entrada.clear()
        self.hora_entrada_extra.clear()
        self.motivo_extra.clear()

        # Reconstruir las listas
        for registro in empleados_sin_salida:
            dni, nombre,fecha_db, hora_entrada_db = registro
            self.empleados_activos.append(nombre)
            self.hora_entrada.append(hora_entrada_db)

            # Calcular el tiempo activo desde la hora de entrada
            formato_fecha = "%Y-%m-%d"
            formato_hora = "%H:%M:%S"
            entrada_completa = datetime.combine(
            datetime.strptime(fecha_db, formato_fecha).date(),
            datetime.strptime(hora_entrada_db, formato_hora).time())
            hora_actual = datetime.now()
            tiempo_transcurrido = hora_actual - entrada_completa
            horas, minutos = divmod(tiempo_transcurrido.seconds // 60, 60)
            self.tiempo_activo.append(f"{horas:02}:{minutos:02}")

            # Verificar si el tiempo supera las 14 horas
            if tiempo_transcurrido.total_seconds() > 14*3600:
                # Registrar la expulsión en la base de datos
                query = "SELECT dni FROM empleados WHERE nombre = ?"
                dni = db.execute_query("Datos/datos.db", query, (nombre,), fetch=True)  # Función para obtener el DNI del empleado
                self.registrar_salida(dni,forced=True)
                self.cargar_empleados_activos()

        for registro in empleados_sin_salida_extra:
            dni, nombre,fecha_db, hora_entrada_db, motivo_db = registro
            self.empleados_activos_extra.append(nombre)
            self.hora_entrada_extra.append(hora_entrada_db)
            self.motivo_extra.append(motivo_db)

            # Calcular el tiempo activo desde la hora de entrada
            formato_fecha = "%Y-%m-%d"
            formato_hora = "%H:%M:%S"
            entrada_completa = datetime.combine(
            datetime.strptime(fecha_db, formato_fecha).date(),
            datetime.strptime(hora_entrada_db, formato_hora).time())
            hora_actual = datetime.now()
            tiempo_transcurrido = hora_actual - entrada_completa
            horas, minutos = divmod(tiempo_transcurrido.seconds // 60, 60)
            self.tiempo_activo_extra.append(f"{horas:02}:{minutos:02}")

            # Verificar si el tiempo supera las 14 horas
            if tiempo_transcurrido.total_seconds() > 14*3600:
                # Registrar la expulsión en la base de datos
                query = "SELECT dni FROM empleados WHERE nombre = ?"
                dni = db.execute_query("Datos/datos.db", query, (nombre,), fetch=True)
                self.registrar_salida(dni,forced=True)
                self.cargar_empleados_activos()
        

        # Actualizar las listas en la interfaz
        self.actualizar_lista_activos()

        # Iniciar el cronómetro para actualizar los tiempos activos
        self.actualizar_tiempo_activo()
        
    def  add_employee():
        pass
    def cargar_empleados_activos():
        pass
    
    def getEmpleados():
        return db.GetEmpleados()
    
    def  editar_empleado(self, nombre, dni):
        pass
    
    def eliminar_empleado(self, nombre, dni):
        pass
    def 