from app_web.config.generador_token import generar
from app_web.config.pagopar import CrearPedido
from datetime import datetime, time, timedelta
import dolarpy
import json

#tarjetas de debito o pagos al contado
private_key_deb = "520281c5bbc1e8910ab1a9c5c840512c"
public_key_deb = "1b85c4c48b70160f3b0ec66e46f4ade2"

#tarjetas de credito o financiados
private_key_cred = "1d98c69bb9c71a9529ca1e13e228040a"
public_key_cred = "c8928436431b6c6de669edb2ad199b3f"

id_pago = {'bancard':9, 'procard': 1, 'aqui_pago': 2, 'pago_exp': 3, 'pract_pag':4, 'cuent_ban':7, 'tigo':10 }

def procesar(data, id_pedido):

    if data['payment'] == 'bancard' or data['payment'] == 'procard':
        if data['ocupation'] == 'Estudiante Nacional' or data['ocupation'] == 'Estudiante Extranjero':
            descripcion = "Inscripción Estudiante Nacional/Internacional, el monto que figura corresponde a la moneda local (Guaraníes) lo cual equivale al monto total de 100 USD (Tipo de cambio del día)"
            descripcion_resumen = "Inscripción Estudiante Nacional/Internacional"
            precio = 100
        elif data['ocupation'] == 'Profesional Nacional':
            descripcion = "Inscripción Profesional Nacional, el monto que figura corresponde a la moneda local (Guaraníes) lo cual equivale al monto total de 150 USD (Tipo de cambio del día)"
            descripcion_resumen = "Inscripción Profesional Nacional"
            precio = 150
        else:
            descripcion = "Inscripción Profesional Internacional, el monto que figura corresponde a la moneda local (Guaraníes) lo cual equivale al monto total de 200 USD (Tipo de cambio del día)"
            descripcion_resumen = "Inscripción Profesional Internacional"
            precio = 150

        #-----------------Se utiliza token api INFONA credito----------------------
        cotizacion = dolarpy.get_venta(provider='cambioschaco')#obtiene la cotizacion del dia
        monto = int(cotizacion)*precio#el monto entero de la inscripcion en guaranies
        monto_total = int((monto*100)/(100-6.82))

        #TODO: Colocar datos de la transaccion en la BD

        #Generamos el token a partir del pedido
        token = generar(private_key_cred, id_pedido, monto_total)

        dates = datetime.today()#obtengo la fecha de hoy
        max = dates+timedelta(days=1)#le sumo 1 dia=24hrs
        fecha_maxima_pago = max.strftime("%Y-%m-%d %H:%M:%S")#la fecha maxima de pago

        #enviamos el token y creamos el pedido
        response = CrearPedido(token,data['ruc'],data['mail'], data['name'],data['phone'],data['n_document'],data['nombre_razon_social'], public_key_cred, monto_total, descripcion, descripcion, monto_total, fecha_maxima_pago, id_pedido, descripcion_resumen)
        num = id_pago.get(data['payment'])
        all = json.loads(response)

        if all['response'] == False:
            print(all['resultado'])
        else:
            token_recive = all['resultado'][0]['data']
            #TODO: Colocar datos de la transaccion en la BD

    else:

        if data['ocupation'] == 'Estudiante Nacional' or data['ocupation'] == 'Estudiante Extranjero':
            descripcion = "Inscripción Estudiante Nacional/Internacional, el monto que figura corresponde a la moneda local (Guaraníes) lo cual equivale al monto total de 100 USD (Tipo de cambio del día)"
            descripcion_resumen = "Inscripción Estudiante Nacional/Internacional"
            precio = 100
        elif data['ocupation'] == 'Profesional Nacional':
            descripcion = "Inscripción Profesional Nacional, el monto que figura corresponde a la moneda local (Guaraníes) lo cual equivale al monto total de 150 USD (Tipo de cambio del día)"
            descripcion_resumen = "Inscripción Profesional Nacional"
            precio = 150
        else:
            descripcion = "Inscripción Profesional Internacional, el monto que figura corresponde a la moneda local (Guaraníes) lo cual equivale al monto total de 200 USD (Tipo de cambio del día)"
            descripcion_resumen = "Inscripción Profesional Internacional"
            precio = 150

        #-----------------Se utiliza token api INFONA credito----------------------
        cotizacion = dolarpy.get_venta(provider='cambioschaco')#obtiene la cotizacion del dia
        monto = int(cotizacion)*precio#el monto entero de la inscripcion en guaranies
        monto_total = int((monto*100)/(100-5.39))

        #TODO: Colocar datos de la transaccion en la BD

        #Generamos el token a partir del pedido
        token = generar(private_key_deb, id_pedido, monto_total)

        dates = datetime.today()#obtengo la fecha de hoy
        max = dates+timedelta(days=1)#le sumo 1 dia=24hrs
        fecha_maxima_pago = max.strftime("%Y-%m-%d %H:%M:%S")#la fecha maxima de pago

        #enviamos el token y creamos el pedido
        response = CrearPedido(token,data['ruc'],data['mail'], data['name'],data['phone'],data['n_document'],data['nombre_razon_social'], public_key_cred, monto_total, descripcion, descripcion, monto_total, fecha_maxima_pago, id_pedido, descripcion_resumen)
        f_pago = id_pago.get(data['payment'])
        all = json.loads(response)

        if all['response'] == False:
            print(all['resultado'])
        else:
            token_received = all['resultado'][0]['data']
            #TODO: Colocar datos de la transaccion en la BD

    return response, f_pago
