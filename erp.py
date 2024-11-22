#%%writefile erp_streamlit.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from fpdf import FPDF

logo_path = "data:image/jpeg;base64,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"
# Configuración inicial
st.set_page_config(page_title="Módulos del ERP", layout="wide",page_icon=logo_path)
# Ruta del archivo de imagen (logo)

# Mostrar el logo en la parte superior de la aplicación
st.image(logo_path, width=200)  # Puedes ajustar el tamaño cambiando el valor de 'width'

# Agregar un título o contenido a la aplicación
st.title("Sistema ERP")
st.write("Bienvenido al sistema ERP para la gestión de clientes, inventarios, facturación, reportes y análisis de ventas.")

st.sidebar.title("ERP_ITM")

# Variables de autenticación
USER = "Lira"
PASSWORD = "Lir@1120"

# Inicialización de variables globales
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if "modulo_seleccionado" not in st.session_state:
    st.session_state["modulo_seleccionado"] = None

# Parámetros de ID
if "id_cliente" not in st.session_state:
    st.session_state["id_cliente"] = 1  # El primer ID de cliente

if "id_producto" not in st.session_state:
    st.session_state["id_producto"] = 1  # El primer ID de producto

if "id_factura" not in st.session_state:
    st.session_state["id_factura"] = 1  # El primer ID de factura

# Inicialización de DataFrames
if "clientes" not in st.session_state:
    st.session_state["clientes"] = pd.DataFrame(columns=["ID", "Nombre", "Correo", "Teléfono"])

if "productos" not in st.session_state:
    st.session_state["productos"] = pd.DataFrame(columns=["ID", "Producto", "Cantidad", "Precio Unitario"])

if "facturas" not in st.session_state:
    st.session_state["facturas"] = pd.DataFrame(columns=["Factura ID", "Cliente ID", "Cliente Nombre", "Productos", "Total", "IVA", "Fecha"])
    
# Función de autenticación
with st.sidebar:
    st.title("Módulos ERP")
if not st.session_state["auth"]:
    st.sidebar.subheader("Iniciar Sesión")
    usuario = st.sidebar.text_input("Usuario")
    contraseña = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Ingresar"):
        if usuario == USER and contraseña == PASSWORD:
            st.session_state["auth"] = True
            st.sidebar.success("Inicio de sesión exitoso.")
        else:
            st.sidebar.error("Usuario o contraseña incorrectos.")
else:
    st.sidebar.subheader(f"Bienvenido, {USER}")
    st.session_state["modulo_seleccionado"] = st.sidebar.radio(
        "Selecciona un módulo:",
        ["Gestión de Clientes", "Gestión de Inventario", "Generar Factura", "Generar Reportes", "Análisis de Ventas"],
    )
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state["auth"] = False
        st.session_state["modulo_seleccionado"] = None
        st.sidebar.success("Sesión cerrada correctamente.")


# Funciones auxiliares
def exportar_csv(df, nombre_archivo):
    """Permite exportar un DataFrame como archivo CSV."""
    st.download_button(
        label="Exportar Datos",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=nombre_archivo,
        mime="text/csv",
    )

# Funciones de los módulos
def gestion_clientes():
    st.header("Gestión de Clientes")
    
    # Registro de nuevo cliente
    with st.form("Registro de Cliente"):
        nombre = st.text_input("Nombre")
        correo = st.text_input("Correo Electrónico")
        telefono = st.text_input("Teléfono")
        submitted = st.form_submit_button("Registrar Cliente")
        
        if submitted:
            # Generación de ID para el nuevo cliente
            cliente_id = st.session_state["id_cliente"]
            nuevo_cliente = pd.DataFrame([{
                "ID": cliente_id, "Nombre": nombre, "Correo": correo, "Teléfono": telefono
            }])
            st.session_state["clientes"] = pd.concat([st.session_state["clientes"], nuevo_cliente], ignore_index=True)
            st.session_state["id_cliente"] += 1  # Incrementar el ID para el siguiente cliente
            st.success(f"Cliente {nombre} registrado correctamente con ID: {cliente_id}.")
    
    # Búsqueda de clientes
    st.subheader("Buscar Cliente")
    search_term = st.text_input("Buscar por nombre o ID")
    if search_term:
        clientes_filtrados = st.session_state["clientes"][st.session_state["clientes"]["Nombre"].str.contains(search_term, case=False)]
        st.dataframe(clientes_filtrados)
    else:
        st.dataframe(st.session_state["clientes"])

    # Edición de cliente
    cliente_a_editar = st.selectbox("Seleccionar cliente para editar", st.session_state["clientes"]["ID"])
    cliente_data = st.session_state["clientes"][st.session_state["clientes"]["ID"] == cliente_a_editar]
    if cliente_data.empty:
        st.warning("Cliente no encontrado.")
    else:
        with st.form("Editar Cliente"):
            nombre_edit = st.text_input("Nuevo Nombre", cliente_data["Nombre"].values[0])
            correo_edit = st.text_input("Nuevo Correo", cliente_data["Correo"].values[0])
            telefono_edit = st.text_input("Nuevo Teléfono", cliente_data["Teléfono"].values[0])
            submitted_edit = st.form_submit_button("Actualizar Cliente")
            
            if submitted_edit:
                st.session_state["clientes"].loc[st.session_state["clientes"]["ID"] == cliente_a_editar, "Nombre"] = nombre_edit
                st.session_state["clientes"].loc[st.session_state["clientes"]["ID"] == cliente_a_editar, "Correo"] = correo_edit
                st.session_state["clientes"].loc[st.session_state["clientes"]["ID"] == cliente_a_editar, "Teléfono"] = telefono_edit
                st.success(f"Cliente con ID {cliente_a_editar} actualizado.")

    # Eliminación de cliente
    cliente_a_eliminar = st.selectbox("Seleccionar cliente para eliminar", st.session_state["clientes"]["ID"])
    if st.button("Eliminar Cliente"):
        st.session_state["clientes"] = st.session_state["clientes"][st.session_state["clientes"]["ID"] != cliente_a_eliminar]
        st.success("Cliente eliminado correctamente.")

def gestion_inventario():

    st.header("Gestión de Inventario")
    
    # Registro de producto
    with st.form("Registro de Producto"):
        producto = st.text_input("Producto")
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        precio_unitario = st.number_input("Precio Unitario", min_value=0.0, step=0.1)
        submitted = st.form_submit_button("Registrar Producto")
        
        if submitted:
            # Generación de ID para el nuevo producto
            producto_id = st.session_state["id_producto"]
            nuevo_producto = pd.DataFrame([{
                "ID": producto_id, "Producto": producto, "Cantidad": cantidad, "Precio Unitario": precio_unitario
            }])
            st.session_state["productos"] = pd.concat([st.session_state["productos"], nuevo_producto], ignore_index=True)
            st.session_state["id_producto"] += 1  # Incrementar el ID para el siguiente producto
            st.success(f"Producto {producto} registrado correctamente con ID: {producto_id}.")
    
    # Búsqueda de productos
    st.subheader("Buscar Producto")
    search_term = st.text_input("Buscar producto por nombre")
    if search_term:
        inventario_filtrado = st.session_state["productos"][st.session_state["productos"]["Producto"].str.contains(search_term, case=False)]
        st.dataframe(inventario_filtrado)
    else:
        st.dataframe(st.session_state["productos"])

    # Eliminación de producto
    producto_a_eliminar = st.selectbox("Seleccionar producto para eliminar", st.session_state["productos"]["Producto"])
    if st.button("Eliminar Producto"):
        st.session_state["productos"] = st.session_state["productos"][st.session_state["productos"]["Producto"] != producto_a_eliminar]
        st.success("Producto eliminado correctamente.")

def gestion_facturas():
    st.header("Generar Factura")
    st.write("Selecciona un cliente y productos para crear una factura.")
    
    if st.session_state["clientes"].empty:
        st.warning("No hay clientes registrados. Por favor, registra clientes antes de crear una factura.")
        return
    
    if st.session_state["productos"].empty:
        st.warning("No hay productos en el inventario. Por favor, registra productos antes de crear una factura.")
        return
    
    cliente_id = st.selectbox("Seleccionar Cliente", st.session_state["clientes"]["ID"])
    cliente_nombre = st.session_state["clientes"].loc[
        st.session_state["clientes"]["ID"] == cliente_id, "Nombre"
    ].values[0]
    
    # Selección de productos
    productos_seleccionados = st.multiselect(
        "Selecciona productos", 
        st.session_state["productos"]["Producto"].values
    )
    
    if not productos_seleccionados:
        st.info("Selecciona al menos un producto para generar una factura.")
        return
    
    productos_detalle = []
    total = 0
    
    for producto in productos_seleccionados:
        producto_info = st.session_state["productos"].loc[
            st.session_state["productos"]["Producto"] == producto
        ]
        precio_unitario = producto_info["Precio Unitario"].values[0]
        stock_disponible = producto_info["Cantidad"].values[0]
        
        # Selección de cantidad
        cantidad = st.number_input(
            f"Cantidad de {producto} (Disponible: {stock_disponible})", 
            min_value=1, 
            max_value=stock_disponible, 
            step=1
        )
        
        subtotal = precio_unitario * cantidad
        total += subtotal
        productos_detalle.append({
            "Producto": producto,
            "Cantidad": cantidad,
            "Precio Unitario": precio_unitario,
            "Subtotal": subtotal
        })
    
    # Calcular IVA y total final
    iva = total * 0.16
    total_con_iva = total + iva
    
    # Mostrar resumen
    st.subheader("Resumen de Factura")
    st.table(pd.DataFrame(productos_detalle))
    st.write(f"Subtotal: ${total:,.2f}")
    st.write(f"IVA (16%): ${iva:,.2f}")
    st.write(f"Total: ${total_con_iva:,.2f}")
    
    # Confirmación y registro de factura
    if st.button("Confirmar y Generar Factura"):
        factura_id = st.session_state["id_factura"]
        fecha = pd.to_datetime("today").strftime("%Y-%m-%d")
        
        # Registrar factura
        factura = pd.DataFrame([{
            "Factura ID": factura_id, 
            "Cliente ID": cliente_id, 
            "Cliente Nombre": cliente_nombre,
            "Productos": productos_detalle, 
            "Total": total, 
            "IVA": iva, 
            "Fecha": fecha
        }])
        st.session_state["facturas"] = pd.concat([st.session_state["facturas"], factura], ignore_index=True)
        st.session_state["id_factura"] += 1  # Incrementar el ID para la siguiente factura
        
        # Reducir inventario
        for detalle in productos_detalle:
            producto = detalle["Producto"]
            cantidad = detalle["Cantidad"]
            st.session_state["productos"].loc[
                st.session_state["productos"]["Producto"] == producto, "Cantidad"
            ] -= cantidad
        
        st.success(f"Factura {factura_id} generada correctamente.")
        st.write(f"Total con IVA: ${total_con_iva:,.2f}")
        
        # Exportar factura
        exportar_csv(st.session_state["facturas"], f"factura_{factura_id}.csv")

def gestion_reportes():
 

    st.header("Generar Reportes")

    # Generación de reportes contables
    st.write("Aquí pueden ir los reportes contables.")
    st.write("Funciones específicas para reportes como ingresos, gastos y balances se agregarán aquí.")
    
    # Simulando el reporte básico
    st.text_area("Resumen", "Reporte generado: ingresos, gastos, balance general, etc.")
    
    # Exportar el reporte a CSV
    exportar_csv(st.session_state["facturas"], "reportes_contables.csv")

import plotly.express as px

def analisis_ventas():
    st.header("Análisis de Ventas")
    
    # Verificar si hay datos en las facturas
    if st.session_state["facturas"].empty:
        st.warning("No hay datos de facturas para analizar.")
        return

    # Crear una lista para desglosar productos en facturas
    productos_desglosados = []
    for _, fila in st.session_state["facturas"].iterrows():
        for producto in fila["Productos"]:
            productos_desglosados.append({
                "Producto": producto["Producto"],
                "Cantidad": producto["Cantidad"],
                "Subtotal": producto["Subtotal"],
                "Fecha": fila["Fecha"]
            })

    # Crear un DataFrame con los datos desglosados
    df_productos = pd.DataFrame(productos_desglosados)

    # Verificar si hay datos en el DataFrame desglosado
    if df_productos.empty:
        st.warning("No hay datos suficientes para generar análisis.")
        return

    # Análisis de ventas por producto
    st.subheader("Ventas por Producto")
    ventas_por_producto = df_productos.groupby("Producto").sum().reset_index()
    fig1 = px.bar(
        ventas_por_producto, 
        x="Producto", 
        y="Subtotal", 
        title="Ingresos por Producto", 
        labels={"Subtotal": "Ingresos ($)"},
        text="Subtotal"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Análisis de cantidades vendidas por producto
    st.subheader("Cantidad Vendida por Producto")
    fig2 = px.pie(
        ventas_por_producto, 
        names="Producto", 
        values="Cantidad", 
        title="Distribución de Cantidades Vendidas"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Análisis temporal de ventas
    st.subheader("Ingresos Totales por Fecha")
    df_productos["Fecha"] = pd.to_datetime(df_productos["Fecha"])
    ingresos_por_fecha = df_productos.groupby("Fecha").sum().reset_index()
    fig3 = px.line(
        ingresos_por_fecha, 
        x="Fecha", 
        y="Subtotal", 
        title="Evolución de Ingresos en el Tiempo",
        labels={"Subtotal": "Ingresos ($)", "Fecha": "Fecha"}
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.success("Gráficos interactivos generados correctamente.")

# Navegación entre módulos
if st.session_state["auth"]:
    if st.session_state["modulo_seleccionado"] == "Gestión de Clientes":
        gestion_clientes()
    elif st.session_state["modulo_seleccionado"] == "Gestión de Inventario":
        gestion_inventario()
    elif st.session_state["modulo_seleccionado"] == "Generar Factura":
        gestion_facturas()
    elif st.session_state["modulo_seleccionado"] == "Generar Reportes":
        gestion_reportes()
    elif st.session_state["modulo_seleccionado"] == "Análisis de Ventas":
        analisis_ventas()
else:
    st.warning("Por favor, inicia sesión para continuar.")
