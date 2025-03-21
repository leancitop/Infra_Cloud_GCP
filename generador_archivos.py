# Generación de archivos de datos
import csv
import numpy as np
import pandas as pd
import random as rd
import string as st
from datetime import datetime
from datetime import timedelta
import os

def generar_codigos_sku(productos):
    codigos_sku = {}

    for producto in productos:
        caracteres = st.ascii_uppercase + st.digits
        sku_codigo = ''.join(rd.choice(caracteres) for _ in range(10))
        codigos_sku[producto] = sku_codigo

    return codigos_sku

def main():
    # Definir rutas
    path = 'excel_especificacion/TP_Final_Especificacion.xlsx'
    path_destino = 'datos_generados'

    # Crear directorio de destino si no existe
    os.makedirs(path_destino, exist_ok=True)
    os.makedirs(os.path.join(path_destino, 'Archivos_VentaClientes'), exist_ok=True)
    os.makedirs(os.path.join(path_destino, 'Archivos_Stock'), exist_ok=True)
    os.makedirs(os.path.join(path_destino, 'Archivos_Maestro'), exist_ok=True)

    # Leer las hojas de cálculo del archivo
    print("Leyendo archivo de especificación...")
    df_sheets_desc = pd.read_excel(path, sheet_name=None)
    df_cond_vta = df_sheets_desc['Condicion_Venta']
    df_unidades = df_sheets_desc['Unidades']
    df_tipo_negocio = df_sheets_desc['Tipo_Negocio']
    df_cadena = df_sheets_desc['Cadena']
    df_dias_visita = df_sheets_desc['Dias_Visita']
    df_productos = df_sheets_desc['Productos']
    df_cond_venta = df_sheets_desc['Condicion_Venta']
    df_localidades = df_sheets_desc['Localidades']
    df_estado = df_sheets_desc['Estado_cliente']
    df_dias_visita = df_sheets_desc['Dias_Visita']

    # Generar códigos SKU
    print("Generando códigos SKU...")
    codigos_sku = generar_codigos_sku(df_productos['nombre'])

    # Configuración de parámetros
    columns_v = df_sheets_desc['Desc_VentaClientes']['Campo']
    columns_s = df_sheets_desc['Desc_StockClientes']['Campo']
    columns_m = df_sheets_desc['Desc_Maestro']['Campo']
    cant_dias = 5
    fecha_actual = datetime.now()
    cant_dist = 3
    cant_clientes = 10
    cant_sucursales = 25

    # Generar datos para cada distribuidor y día
    print("Generando archivos de datos...")
    for distribuidor in range(1, cant_dist):
        print(f"Procesando distribuidor {distribuidor}...")
        for d in range(0, cant_dias):
            # Fecha de cierre
            fech_cierre = fecha_actual - timedelta(days=d)
            fech_cierre_string = f'{fech_cierre.year}-{fech_cierre.month:02d}-{fech_cierre.day:02d}'
            fech_cie_com_data = [fech_cierre_string for _ in range(cant_clientes)]

            # Generar datos
            vta_unidades_data = [(rd.randint(0,100)) for _ in range(cant_clientes)]
            vta_importe_data = [round((rd.uniform(100,1000)),2) for _ in range(cant_clientes)]
            cond_vta_data = [rd.choice(df_cond_vta['codigo_condicion']) for _ in range(cant_clientes)]
            sucursales_dist = [(rd.randint((cant_sucursales*distribuidor)+1,cant_sucursales*(distribuidor+1))) for _ in range(cant_clientes)]
            clientes = [(rd.randint(1000,9999)) for _ in range(cant_clientes)]
            provincia = [(rd.choice(df_localidades.columns.values)) for _ in range(cant_clientes)]

            ciudades_aleatorias = []
            for provincias in provincia:
                ciudades_provincia = df_localidades[provincias].dropna().tolist()
                ciudad_aleatoria = rd.choice(ciudades_provincia)
                ciudades_aleatorias.append(ciudad_aleatoria)

            estado = [(rd.choices(df_estado['nombre'], weights=df_estado['probabilidades'], k=1)[0]) for _ in range(cant_clientes)]
            nombre_cliente = [(f'Cliente_{_}') for _ in range(cant_clientes)]
            cuit = [(rd.randint(10000000, 99999999)) for _ in range(cant_clientes)]
            razon_social = [(f"Empresa_{_}") for _ in range(cant_clientes)]
            direccion = [(f"Dirección_{_}") for _ in range(cant_clientes)]
            dias_visita = [(rd.choice(df_dias_visita['codigo_dia'])) for _ in range(cant_clientes)]
            telefono = [(f"{rd.randint(100, 999)}-{rd.randint(100, 999)}-{rd.randint(1000, 9999)}") for _ in range(cant_clientes)]
            fecha_alta = [('2023-01-01') for _ in range(cant_clientes)]
            fecha_baja = [('ver') for _ in range(cant_clientes)]
            coordenada_latitud = [(round(rd.uniform(-90, 90), 6)) for _ in range(cant_clientes)]
            coordenada_longitud = [(round(rd.uniform(-180, 180), 6)) for _ in range(cant_clientes)]
            tipo_negocio = [(rd.choice(df_tipo_negocio['nombre'])) for _ in range(cant_clientes)]
            deuda_vencida = [(round(rd.uniform(0, 10000), 2)) for _ in range(cant_clientes)]
            unidad = [(rd.choice(df_unidades['codigo_unidad'])) for _ in range(cant_clientes)]
            stock = [(rd.randint(100, 500) if unidad == "UNI" else rd.randint(1, 100)) for _ in range(cant_clientes)]

            # Producto y SKU
            producto = list(codigos_sku.keys())
            producto.extend(producto)
            sku_codigo = list(codigos_sku.values())
            sku_codigo.extend(sku_codigo)

            # Crear DataFrames
            venta_clientes_data = list(zip(sucursales_dist,clientes,fech_cie_com_data,sku_codigo,vta_unidades_data,vta_importe_data,cond_vta_data))
            stock_data = list(zip(sucursales_dist, fech_cie_com_data, sku_codigo, producto, stock, unidad))
            maestro_data = list(zip(sucursales_dist, clientes, ciudades_aleatorias, provincia, estado, nombre_cliente, cuit, razon_social, direccion, dias_visita, telefono, fecha_alta, fecha_baja, coordenada_latitud, coordenada_longitud, cond_vta_data, deuda_vencida, tipo_negocio))

            df_vta_cli = pd.DataFrame(venta_clientes_data, columns=columns_v)
            df_stock = pd.DataFrame(stock_data, columns=columns_s)
            df_maestro = pd.DataFrame(maestro_data, columns=columns_m)

            # Guardar archivos
            carpeta_destino_v = os.path.join(path_destino, 'Archivos_VentaClientes', f'Distribuidor_{distribuidor}')
            carpeta_destino_s = os.path.join(path_destino, 'Archivos_Stock', f'Distribuidor_{distribuidor}')
            carpeta_destino_m = os.path.join(path_destino, 'Archivos_Maestro', f'Distribuidor_{distribuidor}')

            os.makedirs(carpeta_destino_v, exist_ok=True)
            os.makedirs(carpeta_destino_s, exist_ok=True)
            os.makedirs(carpeta_destino_m, exist_ok=True)

            archivo_destino_v = os.path.join(carpeta_destino_v, f'Venta_Clientes_{fech_cierre_string}.csv')
            archivo_destino_s = os.path.join(carpeta_destino_s, f'StockPeriodo_{fech_cierre_string}.csv')
            archivo_destino_m = os.path.join(carpeta_destino_m, f'Maestro_{fech_cierre_string}.csv')

            df_vta_cli.to_csv(archivo_destino_v, encoding='utf-8', index=False)
            df_stock.to_csv(archivo_destino_s, encoding='utf-8', index=False)
            df_maestro.to_csv(archivo_destino_m, encoding='utf-8', index=False)

    print("¡Proceso completado exitosamente!")

if __name__ == "__main__":
    main() 