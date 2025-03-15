import oracledb
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# Configuración de conexión a Oracle
DB_USER = "SYSTEM"
DB_PASSWORD = "bdp1"
DB_DSN = "localhost:1521/FREE"

def actualizar_contraseñas():
    try:
        print("⏳ Conectando a la base de datos...")
        conn = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
        cursor = conn.cursor()
        print("✅ Conectado correctamente.")

        # Obtener usuarios con contraseñas en texto plano
        print("🔍 Buscando contraseñas sin hashear...")
        cursor.execute("SELECT id, password FROM CLIENTES WHERE password NOT LIKE '$2%'")
        usuarios = cursor.fetchall()

        if not usuarios:
            print("⚠ No hay contraseñas por actualizar.")
            return

        print(f"🔄 Se encontraron {len(usuarios)} contraseñas sin hashear. Actualizando...")

        for user_id, plain_password in usuarios:
            if plain_password:
                # Hashear la contraseña correctamente
                hashed_password = bcrypt.generate_password_hash(plain_password).decode('utf-8')

                # Actualizar en la base de datos
                cursor.execute("UPDATE CLIENTES SET password = :1 WHERE id = :2", (hashed_password, user_id))
                print(f"✅ Contraseña del usuario {user_id} actualizada.")

        # Confirmar cambios en la base de datos
        conn.commit()
        print(f"🎉 Se actualizaron {len(usuarios)} contraseñas correctamente.")

    except Exception as e:
        print(f"❌ Error al actualizar contraseñas: {e}")

    finally:
        # Cerrar cursor y conexión
        if 'cursor' in locals() and cursor:
            cursor.close()
            print("🔒 Cursor cerrado.")
        if 'conn' in locals() and conn:
            conn.close()
            print("🔒 Conexión cerrada.")

# Ejecutar la actualización
actualizar_contraseñas()
