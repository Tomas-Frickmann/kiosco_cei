import time
from datetime import datetime, timedelta
from Datos import Connect as db
from fpdf import FPDF

class EmployeeModel:
    def __init__(self):
        # El modelo guarda en su memoria quién está trabajando en este momento
        self.dnis_activos = [] 
        self.dnis_activos_extra = []

    # ==========================================
    # LECTURA DE DATOS (Consultas SELECT)
    # ==========================================
    def obtener_todos_los_empleados(self):
        return db.GetEmpleados()

    def obtener_nombre_por_dni(self, dni):
        query = "SELECT nombre FROM empleados WHERE dni = ?"
        result = db.execute_query("Datos/datos.db", query, (dni,), fetch=True)
        if result:
            # Si activaste el row_factory como charlamos, esto funciona perfecto
            return result[0]["nombre"] 
        return None

    def verificar_dni_existe(self, dni):
        query = "SELECT * FROM empleados WHERE dni = ?"
        resultado = db.execute_query("Datos/datos.db", query, (dni,), fetch=True)
        return len(resultado) > 0

    def obtener_registros_por_fecha(self, fecha_inicio, fecha_fin):
        query = """
            SELECT dni, nombre, fecha, hora_entrada, hora_salida, tiempo_total, COALESCE(expulsion,0) AS expulsion
            FROM registros
            WHERE fecha BETWEEN ? AND ?
        """
        params = (fecha_inicio.strftime("%Y-%m-%d"), fecha_fin.strftime("%Y-%m-%d"))
        return db.execute_query("Datos/datos.db", query, params, fetch=True)

    def obtener_registro_pendiente(self, dni):
        query = "SELECT id, hora_entrada FROM registros WHERE dni = ? AND hora_salida IS NULL"
        resultado = db.execute_query("Datos/datos.db", query, (dni,), fetch=True)
        if resultado:
            return {"id": resultado[0]["id"], "hora_entrada": resultado[0]["hora_entrada"]}
        return None

    def tiene_registro_pendiente(self, dni):
        return self.obtener_registro_pendiente(dni) is not None

    # ==========================================
    # ESTADO DE LOS EMPLEADOS EN TURNO
    # ==========================================
    def esta_activo(self, dni):
        return dni in self.dnis_activos

    def esta_activo_extra(self, dni):
        return dni in self.dnis_activos_extra

    def cantidad_activos_normales(self):
        return len(self.dnis_activos)

    def cantidad_activos_extra(self):
        return len(self.dnis_activos_extra)

    # ==========================================
    # ESCRITURA DE DATOS (ABM EMPLEADOS)
    # ==========================================
    def guardar_empleado(self, nombre, dni):
        query = "INSERT INTO empleados (nombre, dni) VALUES (?, ?)"
        db.execute_query("Datos/datos.db", query, (nombre.strip(), dni.strip()))

    def actualizar_empleado(self, nuevo_nombre, nuevo_dni, nombre_viejo, dni_viejo):
        query1 = "UPDATE empleados SET nombre = ?, dni = ? WHERE nombre = ? AND dni = ?"
        db.execute_query("Datos/datos.db", query1, (nuevo_nombre, nuevo_dni, nombre_viejo, dni_viejo))
        
        query2 = "UPDATE registros SET nombre = ?, dni = ? WHERE nombre = ? AND dni = ?"
        db.execute_query("Datos/datos.db", query2, (nuevo_nombre, nuevo_dni, nombre_viejo, dni_viejo))

    def eliminar_empleado(self, dni):
        db.execute_query("Datos/datos.db", "DELETE FROM empleados WHERE dni = ?", (dni,))
        db.execute_query("Datos/datos.db", "DELETE FROM registros WHERE dni = ?", (dni,))

    # ==========================================
    # FICHAJE Y HORARIOS (INSERT Y UPDATE)
    # ==========================================
    def crear_registro_entrada(self, dni, extra=0, motivo=None):
        nombre = self.obtener_nombre_por_dni(dni)
        fecha_actual = time.strftime("%Y-%m-%d")
        hora_actual = time.strftime("%H:%M:%S")
        
        query = "INSERT INTO registros (dni, nombre, fecha, hora_entrada, extra, motivo) VALUES (?, ?, ?, ?, ?, ?)"
        db.execute_query("Datos/datos.db", query, (dni, nombre, fecha_actual, hora_actual, extra, motivo))
        
        # Agregamos el DNI a la memoria del programa
        if extra == 1:
            self.dnis_activos_extra.append(dni)
        else:
            self.dnis_activos.append(dni)

    def marcar_salida_normal(self, id_registro, hora_entrada):
        hora_salida = time.strftime("%H:%M:%S")
        formato_hora = "%H:%M:%S"
        tiempo_trabajado = datetime.strptime(hora_salida, formato_hora) - datetime.strptime(hora_entrada, formato_hora)

        query = "UPDATE registros SET hora_salida = ?, tiempo_total = ? WHERE id = ?"
        db.execute_query("Datos/datos.db", query, (hora_salida, str(tiempo_trabajado), id_registro))
        self._limpiar_memoria_activos(id_registro)

    def forzar_salida(self, id_registro, hora_entrada):
        formato_hora = "%H:%M:%S"
        hora_salida = (datetime.strptime(hora_entrada, formato_hora) + timedelta(minutes=1)).strftime(formato_hora)

        query = "UPDATE registros SET hora_salida = ?, tiempo_total = ?, expulsion = ? WHERE id = ?"
        db.execute_query("Datos/datos.db", query, (hora_salida, "00:01:00", 1, id_registro))
        self._limpiar_memoria_activos(id_registro)

    def _limpiar_memoria_activos(self, id_registro):
        # Una pequeña función interna para sacar al empleado de las listas cuando se va
        query = "SELECT dni, extra FROM registros WHERE id = ?"
        result = db.execute_query("Datos/datos.db", query, (id_registro,), fetch=True)
        if result:
            dni = result[0]["dni"]
            extra = result[0]["extra"]
            if extra == 1 and dni in self.dnis_activos_extra:
                self.dnis_activos_extra.remove(dni)
            elif extra == 0 and dni in self.dnis_activos:
                self.dnis_activos.remove(dni)

    # ==========================================
    # GENERACIÓN DE PDF
    # ==========================================
    def generar_pdf(self, registros, fecha_inicio, fecha_fin, ruta_guardado):
        # Esta es tu misma lógica de PDF, pero guardada de forma segura en el Modelo
        empleados = {}
        for registro in registros:
            dni, nombre, fecha, hora_entrada, hora_salida, tiempo_total, expulsion = registro
            if nombre not in empleados:
                empleados[nombre] = {"registros": [], "tiempo_total": datetime.strptime("00:00:00", "%H:%M:%S")}
            empleados[nombre]["registros"].append((fecha, hora_entrada, hora_salida, tiempo_total, expulsion))
            
            if tiempo_total:
                tiempo_total_dt = datetime.strptime(tiempo_total, "%H:%M:%S")
                empleados[nombre]["tiempo_total"] += timedelta(
                    hours=tiempo_total_dt.hour, minutes=tiempo_total_dt.minute, seconds=tiempo_total_dt.second
                )

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Informe de Registros", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Fechas: {fecha_inicio.strftime('%Y-%m-%d')} a {fecha_fin.strftime('%Y-%m-%d')}", ln=True, align="C")
        pdf.ln(10)

        for nombre, datos in empleados.items():
            pdf.set_font("Arial", style="B", size=12)
            pdf.set_fill_color(200, 220, 255)
            pdf.cell(176, 10, txt=f"Empleado: {nombre}", ln=True, align="L", fill=True)
            pdf.set_font("Arial", size=10)
            pdf.cell(176, 10, txt=f"Tiempo total: {datos['tiempo_total'].strftime('%H:%M:%S')}", ln=True, align="L", fill=True)
            pdf.ln(5)

            pdf.cell(44, 8, txt="Fecha", border=1, align="C")
            pdf.cell(44, 8, txt="Entrada", border=1, align="C")
            pdf.cell(44, 8, txt="Salida", border=1, align="C")
            pdf.cell(44, 8, txt="Total", border=1, align="C")
            pdf.ln()

            for i, registro in enumerate(datos["registros"]):
                fecha, hora_entrada, hora_salida, tiempo_total, expulsion = registro
                fecha = fecha if fecha else "N/A"
                hora_entrada = hora_entrada if hora_entrada else "N/A"
                hora_salida = hora_salida if hora_salida else "N/A"
                tiempo_total = tiempo_total if tiempo_total else "N/A"

                if expulsion == 1:
                    pdf.set_fill_color(255, 0, 0)
                elif i % 2 == 0:
                    pdf.set_fill_color(220, 240, 220)
                else:
                    pdf.set_fill_color(255, 255, 255)

                pdf.cell(44, 7, txt=str(fecha), border=1, align="C", fill=True)
                pdf.cell(44, 7, txt=str(hora_entrada), border=1, align="C", fill=True)
                pdf.cell(44, 7, txt=str(hora_salida), border=1, align="C", fill=True)
                pdf.cell(44, 7, txt=str(tiempo_total), border=1, align="C", fill=True)
                pdf.ln()
            pdf.ln(10)

        pdf.output(ruta_guardado)
        
    def obtener_empleados_trabajando(self):
        query = "SELECT id, dni, nombre, fecha, hora_entrada, extra, motivo FROM registros WHERE hora_salida IS NULL"
        return db.execute_query("Datos/datos.db", query, fetch=True)