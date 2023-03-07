import json
import requests

url = "https://api.pagopar.com/api/comercios/1.1/iniciar-transaccion"

def CrearPedido(token, ruc, email, nombre, telefono, documento, razon_social, public_key ,monto_total, nombre_item, descripcion, precio_total, fecha_maxima_pago, id_pedido, descripcion_resumen):

    payload = {
    "token": token,
    "comprador": {
    "ruc": ruc,
    "email": email,
    "ciudad": None,
    "nombre": nombre,
    "telefono": telefono,
    "direccion": "",
    "documento": documento,
    "coordenadas": "",
    "razon_social": razon_social,
    "tipo_documento": "CI",
    "direccion_referencia": None
    },
    "public_key": public_key,
    "monto_total": monto_total,
    "tipo_pedido": "VENTA-COMERCIO",
    "compras_items": [
    {
    "ciudad": "1",
    "nombre": nombre_item,
    "cantidad": 1,
    "categoria": "909",
    "public_key": public_key,
    "url_imagen": "",
    "descripcion": descripcion,
    "id_producto": 1,
    "precio_total": precio_total,
    "vendedor_telefono": "",
    "vendedor_direccion": "",
    "vendedor_direccion_referencia": "",
    "vendedor_direccion_coordenadas": ""
    }
    ],
    "fecha_maxima_pago": fecha_maxima_pago,
    "id_pedido_comercio": id_pedido,
    "descripcion_resumen": descripcion_resumen
    }

    #print(payload)

    #print(json.dumps(payload))

    response = requests.request("POST", url, data=json.dumps(payload))

    #print(response.text)

    return response.text