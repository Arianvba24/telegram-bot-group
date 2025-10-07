import asyncio
import logging
import sys
import time
from aiogram import Bot, Dispatcher, html,F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram.types import Message, ChatMemberUpdated,InlineKeyboardMarkup,InlineKeyboardButton,CallbackQuery,ChatInviteLink,FSInputFile,ChatJoinRequest
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter,IS_MEMBER,IS_NOT_MEMBER
# Functions-----------------------------------
from sql_database import create_user,insertar_nombre_datos_personales,consulta_id,insertar_correo_datos_personales,active_update,warning_update,ban_update,payment_update,extraer_dataframe
from sql_database import consulta_correo,consulta_id_express
from payment import payment_fetch

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup



with open(r"token.txt","r") as f:
    TOKEN=f.read()


dp = Dispatcher()

class Registro(StatesGroup):
    esperando_nombre = State()
    esperando_correo = State()
    procesar_pago = State()
    nombre_tarjeta = State()
    numero_tarjeta = State()
    usuario_valor = State()
    contraseña_valor = State()
    desbanear_correo = State()





# Comando de inicio al initeractuar con el
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:


    

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Si",callback_data="enviar_afirmacion"),InlineKeyboardButton(text="No",callback_data="enviar_negacion")]

        ]

    )

    valor = await message.answer(f"Hola! Parece ser que deseas entrar al grupo de Telegram de Alex\n¿Deseas comenzar con el registro?",reply_markup=keyboard)



 
@dp.callback_query(F.data.startswith("enviar_"))
async def afirmacion_mensaje(callback: CallbackQuery,state : FSMContext):
    if callback.data == "enviar_afirmacion":
        await callback.message.answer("Estupendo! Ahora necesitaríamos que nos facilite en el siguiente mensaje su nombre y apellido")
        await state.set_state(Registro.esperando_nombre)



    elif callback.data == "enviar_negacion":
        await callback.message.answer("No pasa nada! Vuelve cuando quieras acceder al grupo")


@dp.message(Registro.esperando_nombre)
async def procesar_nombre(message: Message, state: FSMContext):


    try:


        nombre_usuario = message.from_user.full_name
        user_id = message.from_user.id
        chat_id = message.chat.id
        
        nombre = message.text


        if "/" not in nombre:

            valor_x = consulta_id(user_id)

            # if consulta_id(user_id) == True:

            print(valor_x)

            if len(valor_x) == 0:

                await message.answer(f"Perfecto {html.bold(nombre)}, ya tengo tu nombre y apellido\nAhora nos faltaría tu correo electrónico")
                create_user(user_id,nombre_usuario,-4893968469,False,False,0)
                insertar_nombre_datos_personales(user_id,message.text)
                await state.clear()
                await state.set_state(Registro.esperando_correo)

            else:
                await message.answer(f"Tu usuario ya existe en nuestra base de datos. Contacta con un administrador para que te vuelva a dejar entrar")




        else:
            await message.answer("Por favor escriba su nombre y apellidos correctamente sin carácteres")
            await state.clear()
            await state.set_state(Registro.esperando_nombre)

    except Exception as e:
        print(e,"----------------------------------")



@dp.message(Registro.esperando_correo)
async def procesar_correo(message: Message, state: FSMContext,bot:Bot):
    correo = message.text
    user_id = message.from_user.id
    # chat_group_id = -1002844428538
    chat_group_id = -4893968469
    chat_user_id = message.chat.id

    print(f"""
    Chat group id : {chat_group_id}
    Chat user id : {chat_user_id}
    """)


    funcion = [True]
    if "@" in correo:
        # link = r"https://www.google.com/"
        insertar_correo_datos_personales(user_id,correo)
        await message.answer(f"Perfecto! Ya tengo tu correo\nAhora solo haría falta que pagases la cuota mensual de suscripción")
        # await message.answer(f"Aquí tienes el link:\n{link}")
        await message.answer(f"Una vez pagado le proporcionaremos el link para que pueda entrar")
        await asyncio.sleep(3)

        await asyncio.create_task(funcion_pago(message))

        await message.answer("Para poder realizar el pago puede hacerlo a traves del siguiente enlace")
        await asyncio.sleep(1)
        await message.answer(f"Para poder hacer la verificación de si se ha pagado o no use el comando /verificacion_pago para comenzar con el proceso de verificación de pago")

        await state.clear()
        
        # await state.set_state(Registro.procesar_pago)

    else:
        await message.answer("Por favor escriba un correo electrónico válido")
        await state.clear()
        await state.set_state(Registro.procesar_pago)



async def funcion_pago(message: Message):
    await message.answer(f"Para poder realizar el pago puede hacerlo a traves de este enlace:\n{html.link('Enlace de pago','http://127.0.0.1:4242/')}")



@dp.message(Command("verificacion_pago"))
async def verify_payment(message: Message,state: FSMContext):
    await message.answer("Para proceder a la verificación de pago necesitamos primero que nada que nos proporcione el nombre completo de su tarjeta:")
    await state.set_state(Registro.nombre_tarjeta)

# Mover diccionario dentro de las funciones pare que los de las funciones no se pisen unos con otros---
card_values = {

    "Name" : "",
    "Digits" : ""


}

@dp.message(Registro.nombre_tarjeta)
async def state_verify_payment(message: Message,state: FSMContext):
    card_values["Name"] = message.text
    await state.clear()
    await message.answer("Estupendo! Ya tengo el nombre de la tarjeta. Ahora necesito que a continuación me des los últimos cuatro dígitos de la tarjeta")
    await state.set_state(Registro.numero_tarjeta)


@dp.message(Registro.numero_tarjeta)
async def state2_verify_payment(message: Message,state: FSMContext,bot: Bot):
    chat_group_id = -4893968469
    card_values["Digits"] = message.text
    await state.clear()
    await message.answer("Genial! Ya tengo su número de tarjeta. Denos unos segundos para comprobar que el pago se ha hecho correctamente")
    await asyncio.sleep(5)
    payment_status = False
    df = payment_fetch()
    if card_values["Name"] in df["Name"].values and card_values["Digits"] in df["Digits"].values:
        payment_status = True
        payment_update(message.from_user.id,chat_group_id,True)
        await message.answer("Todo esta en orden!\nYa puede acceder al grupo de Telegram :)")


        # Función de crear enlace---------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------

        asyncio.create_task(procesar_pago(chat_group_id,message.from_user.id,bot))

    else:
        payment_update(message.from_user.id,message.chat.id,False)
        await message.answer("El pago no se ha realizado aún. Vuelva a introducir los datos en caso de haberlos introducido de manera incorrecta")

# Función de crear enlace-----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------
async def procesar_pago(chat_group_id:int,chat_user_id:int,bot:Bot):
    un_dia_segundos = 24 * 60 * 60
    fecha_expiracion = int(time.time()) + un_dia_segundos


    await asyncio.sleep(5)
    funcion = [True]
    if funcion:
        enlace = await bot.create_chat_invite_link(chat_group_id,name="Enlace permanente",expire_date=fecha_expiracion,creates_join_request=True)
        await bot.send_message(chat_user_id,f"Puede acceder al grupo en el siguiente enlace:\n{enlace.invite_link}")








# @dp.message(Command("create_link"))
# async def procesar_pago(message : Message,bot:Bot):
#     # enlace = r"https://arianvba24.github.io/portfolio/"
#     un_dia_segundos = 24 * 60 * 60
#     fecha_expiracion = int(time.time()) + un_dia_segundos

#     # mensaje = message.chat.id
#     mensaje = -4893968469
#     # await asyncio.sleep(10)
#     funcion = [True]
#     if funcion:
#         enlace = await bot.create_chat_invite_link(mensaje,name="Enlace permanente",expire_date=fecha_expiracion,member_limit=0)
#         await message.answer(f"Se ha realizado el pago correctamente.\nPuede acceder al grupo en el siguiente enlace:\n{enlace.invite_link}")





# @dp.message(Registro.esperando_nombre)
# async def procesar_correo_electronico(message: Message, state: FSMContext):
#     nombre = message.text
#     await message.answer(f"Perfecto {html.bold(nombre)}, ya tengo tu nombre y apellido\nAhora nos faltaría tu correo electrónico")
#     await state.clear()


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------


@dp.message(F.text.contains("http"))
async def contiene_enlace(message: Message,bot : Bot) -> None:

    valores = message


   
    await bot.delete_message(message_id=valores.message_id,chat_id=message.chat.id)
    valor_final = warning_update(valores.from_user.id,valores.chat.id)
    print(valor_final)
    if valor_final == 2:
        # Eliminar_usuario
        await bot.ban_chat_member(message.chat.id,message.from_user.id)

        # await message.answer("Estas eliminado")

        # Actualizar la columna baneado a True
        ban_update(valores.from_user.id,message.chat.id,True)

        # Actualizar la columna numero avisos a 0
        warning_update(valores.from_user.id,valores.chat.id,restart_counter=True)

        # Ha sido expulsado del grupo. Contacte con un administrador para ver si es posible que pueda entrar
        await bot.send_message(message.from_user.id,"Ha sido expulsado del grupo. Contacte con un administrador para ver si es posible que pueda volver a entrar")


    else:
        await message.answer(f"""

        ¡Hola {html.bold(message.from_user.full_name)}! Esta prohibido enviar enlaces externos dentro del grupo. Hemos borrado su mensaje. Vuelvalo a hacer y será expulsado de manera permanente
        
        """
        )

    


    



@dp.message(F.text=="datos")
async def message_details(message: Message) -> None:
    valores = message

    print(f"""

    Nombre de usuario : {message.from_user.full_name}---{type(message.from_user.full_name)}
    Número de usuario id : {message.from_user.id}---{type(message.from_user.id)}
    Chat ID : {message.chat.id}---{type(message.chat.id)}
    
    """)



# Actualizar la base de datos si los miembros se encuentran en el grupo---------------

@dp.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER>> IS_MEMBER))
async def inicio_usuario(event: ChatMemberUpdated):
    try:

        chat_id = event.chat.id
        user = event.from_user
        print(f"El usuario con nombre {user.full_name}, id {user.id} y proveniente del chat {chat_id} ha entrado en el grupo")
        active_update(user.id,chat_id,True)

    except Exception as e:
        print("Error",e)



@dp.chat_member(ChatMemberUpdatedFilter(IS_MEMBER>> IS_NOT_MEMBER))
async def salida_usuario(event: ChatMemberUpdated):
    chat_id = event.chat.id
    user = event.from_user
    print(f"El usuario con nombre {user.full_name}, id {user.id} y proveniente del chat {chat_id} ha salido del grupo")
    active_update(user.id,chat_id,False)



# Previlegios de usuario admin---------------------------------------------------------------
admin_credentials = {
    "User" : "arian97",
    "Password" : "segarro_amego"


}


@dp.message(Command("admin_role"))
async def comandos_admin(message: Message,state: FSMContext):
    await message.answer("Hola!\nEsta intentando acceder a los comandos de admin. Necesitaríamos que nos facilite el usuario y la contraseña para poder continuar")
    await asyncio.sleep(0.8)
    await message.answer("Comienze facilitando su usuario a continuación:")
    await state.set_state(Registro.usuario_valor)


    
@dp.message(Registro.usuario_valor)
async def comprobar_usuario(message: Message,state: FSMContext):
    if message.text ==  admin_credentials["User"]:
        await message.answer("Estupendo!\nAhora facilítenos su contraseña")
        await state.clear()
        await state.set_state(Registro.contraseña_valor)
    
    else:
        await message.answer("Lo sentimos pero no existe ningún usuario con ese nombre. Vuélvalo a intentar otra vez")


@dp.message(Registro.contraseña_valor)
async def comprobar_contraseña(message: Message, state: FSMContext):
    if message.text == admin_credentials["Password"]:
        await message.answer("Enhorabuena! Ya puedes acceder a las funciones privilegiadas como anfitrión")
        await asyncio.sleep(0.8)
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Desbanear usuarios",callback_data="desbanear"),InlineKeyboardButton(text="Descargar datos de usuario",callback_data="descargar_datos")]

        ]

        )

        await message.answer("Elija cual de las opciones desea llevar a cabo",reply_markup=keyboard)
        await state.clear()

    else:
        await message.answer("Lo siento la contraseña introducida no es la correcta. Compruebela y vuelva a intentarlo")

@dp.callback_query(F.data == "descargar_datos")
async def descargar_datos(callback: CallbackQuery):
    file_path = r"C:\Users\Cash\Desktop\proyectos julio\telegram\datos.xlsx"
    df = extraer_dataframe()
    df.to_excel(file_path,index=False)
    await callback.message.answer("Aquí tiene su archivo")
    documento  = FSInputFile(file_path)
    tamaño = await callback.message.answer_document(document=documento)

@dp.callback_query(F.data == "desbanear")
async def desbanear_usuario(callback: CallbackQuery,state: FSMContext):
    await callback.message.answer("Necesitamos saber el correo electrónico del usuario el cual desea desbanear\nEscríbanos el correo a continuación:")
    await state.set_state(Registro.desbanear_correo)


@dp.message(Registro.desbanear_correo)
async def desbanear_usuario_valor(message: Message, state: FSMContext):
    try:


        valores = consulta_correo(message.text)

        if valores:
            ban_update(message.from_user.id,-4893968469,False)
            await message.answer(f"El usuario {html.bold(message.text)} ha sido desbaneado con éxito!")

        else:
            await message.answer("El correo electrónico que ha facilitado no se encuentra en nuestra base de datos. Intente con otro correo.")

    except Exception as e:
        await message.answer("Ha habido un error. Vuelva a intentarlo más tarde")
            
# PERMISO PARA UNIRSE AL GRUPO---------------------------------------------------
@dp.chat_join_request()
async def handle_join_request(event: ChatJoinRequest,bot: Bot):
    # print(f"El usuario {event.from_user.full_name} ha solicitado unirse a {event.chat.title}")
    valores = consulta_id_express(event.from_user.id)
    print(valores)
    if valores[0][-1] == 1:
        print("Moroso")
        await bot.send_message(event.from_user.id,"Hola!\nSoy admin del grupo.Actualmente usted se encuentra baneado. Pida a algún administrador que le quite el baneo")
        await event.decline()
        

    elif valores[0][-3] == 0:
        print("Baneado")
        await bot.send_message(event.from_user.id,"Hola!\nSoy admin del grupo.No ha pagado su suscripción mensual.Páguela y podrá acceder al chat en caso de que no se encuentre baneado")
        await event.decline()

    else:
        await event.approve()




    



async def main() -> None:

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
