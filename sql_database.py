import sqlite3
import pandas as pd


# TABLE------------------------------

def crear_tabla():
    try:

        conn = sqlite3.connect(r"chat_member.db")
        cursor = conn.cursor()


        query = f"""
        CREATE TABLE chat_members(
        usuario_id INTEGER,
        username TEXT,
        chat_id INTEGER,
        active BOOLEAN,
        pago_mes BOOLEAN,
        numero_avisos INTEGER,
        UNIQUE(usuario_id,chat_id)
        );
        
        
        """


        cursor.execute(query)


        conn.commit()
        conn.close()


    except Exception as e:
        print(e)
        conn.commit()
        conn.close()


def crear_tabla_datos_personales():
    try:

        conn = sqlite3.connect(r"chat_member.db")
        cursor = conn.cursor()

        query = f"""
        CREATE TABLE chat_members_info(
        usuario_id INTEGER,
        name TEXT,
        email TEXT
        );
        
        
        """


        cursor.execute(query)


        conn.commit()
        conn.close()

    except Exception as e:
        print(e)
        conn.commit()
        conn.close()




def create_user(usuario_id:int,username:str,chat_id:int,active:bool,payment:bool,warnings=None):
    try:
        conn = sqlite3.connect(r"chat_member.db")
        cursor = conn.cursor()
        query = f"""
        
        INSERT INTO chat_members VALUES({usuario_id},'{username}',{chat_id},{active},{payment},{warnings},False);
        
        """
        cursor.execute(query)
        conn.commit()
        conn.close()


    except Exception as e:
        print(e)
        conn.commit()
        conn.close()




def insertar_nombre_datos_personales(user_id: int,nombre: str):
    try:
        conn = sqlite3.connect(r"chat_member.db")
        cursor = conn.cursor()

        query = f"""
        
        INSERT INTO chat_members_info VALUES({user_id},'{nombre}','falta correo');
        
        
        """

        cursor.execute(query)

        conn.commit()
        conn.close()


    except:
        conn.commit()
        conn.close()


def insertar_correo_datos_personales(user_id: int,correo: str):
    try:
        conn = sqlite3.connect(r"chat_member.db")
        cursor = conn.cursor()

        query = f"""
        
        
        UPDATE chat_members_info
        SET email = '{correo}'
        WHERE usuario_id == {user_id};
        
        
        """

        cursor.execute(query)

        conn.commit()
        conn.close()


    except:
        conn.commit()
        conn.close()


def warning_update(user_id:int,chat_id:int,restart_counter=None):

    
        
    try:

        conn = sqlite3.connect(r"chat_member.db")
        cursor = conn.cursor()

        # Reiniciar contador de número de avisos--------------------------------------------------------------
        if restart_counter == True:

            # query = f"""
            
            # SELECT * FROM chat_members WHERE usuario_id == {user_id} AND chat_id == {chat_id};
            
            
            # """

            # cursor.execute(query)

            # valores = cursor.fetchall()


            # valor_nuevo = valores[0][-1] + 1

            new_query = f"""

            UPDATE chat_members
            SET numero_avisos = 0
            WHERE usuario_id == {user_id} AND chat_id == {chat_id};
            
            """
            cursor.execute(new_query)

            conn.commit()
            conn.close()

            # if valor_nuevo == 2:
            #     return 2

            # else:
            #     return 1

        
        else:
            

            query = f"""
            
            SELECT * FROM chat_members WHERE usuario_id == {user_id} AND chat_id == {chat_id};
            
            
            """

            cursor.execute(query)

            valores = cursor.fetchall()
            print(valores)


            valor_nuevo = valores[0][-2] + 1

            print("Ejecutado valor--------------------",valor_nuevo)

            new_query = f"""
            UPDATE chat_members
            SET numero_avisos = {valor_nuevo}
            WHERE usuario_id == {user_id} AND chat_id == {chat_id};
            
            
            """
            cursor.execute(new_query)

            conn.commit()
            conn.close()

            if valor_nuevo == 2:
                return 2

            else:
                return 1


    except Exception as e:
        print(e)
        conn.commit()
        conn.close()
        return 1



        

def payment_update(user_id:int,chat_id:int,paid :bool):


    try:

        conn = sqlite3.connect(r"chat_member.db")
        cursor = conn.cursor()

        if paid == True:

            valor_nuevo = True

            new_query = f"""
            UPDATE chat_members
            SET pago_mes = {valor_nuevo}
            WHERE usuario_id == {user_id} AND chat_id == {chat_id};
            
            
            """
            cursor.execute(new_query)

            conn.commit()
            conn.close()

        else:

            valor_nuevo = False
        

            new_query = f"""
            UPDATE chat_members
            SET pago_mes = {valor_nuevo}
            WHERE usuario_id == {user_id} AND chat_id == {chat_id};
            
            
            """
            cursor.execute(new_query)

            conn.commit()
            conn.close()



    except Exception as e:
        print(e)
        conn.commit()
        conn.close()

def active_update(user_id:int,chat_id:int,active :bool):
    try:

        conn = sqlite3.connect(r"chat_member.db")
        cursor = conn.cursor()

        if active == True:

            valor_nuevo = True

            new_query = f"""
            UPDATE chat_members
            SET active = {valor_nuevo}
            WHERE usuario_id == {user_id} AND chat_id == {chat_id};
            
            
            """
            cursor.execute(new_query)

            conn.commit()
            conn.close()

        elif active  == False:

            valor_nuevo = False

            print("Ejecutado")

            new_query = f"""
            UPDATE chat_members
            SET active = {valor_nuevo}
            WHERE usuario_id == {user_id} AND chat_id == {chat_id};
            
            
            """
            cursor.execute(new_query)

            conn.commit()
            conn.close()



    except Exception as e:
        print(e)
        conn.commit()
        conn.close()

def ban_update(user_id:int,chat_id:int,active :bool):
    try:

        conn = sqlite3.connect(r"chat_member.db")
        cursor = conn.cursor()

        if active == True:

            valor_nuevo = True

            new_query = f"""
            UPDATE chat_members
            SET baneado = {valor_nuevo}
            WHERE usuario_id == {user_id} AND chat_id == {chat_id};
            
            
            """
            cursor.execute(new_query)

            conn.commit()
            conn.close()

        elif active  == False:

            valor_nuevo = False

            print("Ejecutado")

            new_query = f"""
            UPDATE chat_members
            SET baneado = {valor_nuevo}
            WHERE usuario_id == {user_id} AND chat_id == {chat_id};
            
            
            """
            cursor.execute(new_query)

            conn.commit()
            conn.close()



    except Exception as e:
        print(e)
        conn.commit()
        conn.close()



# CONSULTA---------------------------------------------------------------
def consulta_id(user_id: int):
    try:

        conn = sqlite3.connect(r"chat_member.db")
        cursor = conn.cursor()

        query = f"""
        
        SELECT * FROM chat_members_info WHERE usuario_id == {user_id};
        
        """

        cursor.execute(query)

        valores = cursor.fetchall()


        # if valores:
        #     print("Este valor existe")
        #     return True

        # else:
        #     print("Este valor no existe")
        #     return False
        # print(valores)


        conn.commit()
        conn.close()

        return valores

        

    except Exception as e:
        print(e)
        conn.commit()
        conn.close()


def consulta_correo(email: str):
    try:

        conn = sqlite3.connect(r"chat_member.db")
        cursor = conn.cursor()

        query = f"""
        
        SELECT * FROM chat_members_info WHERE email == '{email}';
        
        """

        cursor.execute(query)

        valores = cursor.fetchall()


        conn.commit()
        conn.close()

        return valores

    except Exception as e:
        print(e)
        conn.commit()
        conn.close()

def consulta_id_express(usuario_id: str):
    try:

        conn = sqlite3.connect(r"chat_member.db")
        cursor = conn.cursor()

        query = f"""
        
        SELECT * FROM chat_members WHERE usuario_id == {usuario_id};
        
        """

        cursor.execute(query)

        valores = cursor.fetchall()


        conn.commit()
        conn.close()

        return valores

    except Exception as e:
        print(e)
        conn.commit()
        conn.close()


def extraer_dataframe():
    try:
        conn = sqlite3.connect(r"chat_member.db")
        query = r"SELECT * FROM chat_members;"

        df = pd.read_sql(sql=query,con=conn)
        
        conn.commit()
        conn.close()

        return df
        

    except Exception as e:
        print("Error",e)
        conn.commit()
        conn.close()

# user_id = 1295882191
# chat_id = -1002844428538

# cosas = consulta_id(1295882190)
# if cosas:
#     print("El valor existe")

# else:
#     print("El valor no existe")

# ban_update(8178605322,-4893968469,True)

# valores = consulta_correo("banana@gmail.com")


# valores = consulta_id_express(8178605322)

# print(valores)