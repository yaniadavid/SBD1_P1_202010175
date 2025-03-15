from typing import Optional
import oracledb
from pydantic import BaseModel
from fastapi import FastAPI

# MODELOS ---------------------------------------------------
class Customer(BaseModel):
    nationalId: int
    name: str
    lastname: str
    email: str
    phone: str
    active: str
    confirmed_email: int

class CustomerPatch(BaseModel):
    nationalId: Optional[int] = None
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    active: Optional[str] = None
    confirmed_email: Optional[int] = None

# CONFIGURACIÓN DE LA APP -----------------------------------
app = FastAPI()

# DSN - base de datos Oracle
DSN = "C##SYSTEM/bdp1@localhost:1522/FREE"

# ENDPOINTS -------------------------------------------------

# 1. Crear Cliente (POST /clients)
# @app.post("/clients")
# def create_client(customer: Customer):
#     with oracledb.connect(DSN) as connection:
#         cursor = connection.cursor()
        
#         # 1. Calcular nuevo ID (usando conteo de registros)
#         cursor.execute("SELECT COUNT(*) FROM CUSTOMER")
#         totalClients = cursor.fetchone()[0]
#         new_id = totalClients + 1

#         # 2. Insertar el nuevo cliente
#         insert_query = """
#             INSERT INTO CUSTOMER 
#             (ID, NATIONAL_ID, NAME, LASTNAME, EMAIL, PHONE, ACTIVE, CONFIRMED_EMAIL) 
#             VALUES (:id, :nationalId, :name, :lastname, :email, :phone, :active, :confirmed_email)
#         """
#         cursor.execute(insert_query, {
#             "id": new_id,
#             "nationalId": customer.nationalId,
#             "name": customer.name,
#             "lastname": customer.lastname,
#             "email": customer.email,
#             "phone": customer.phone,
#             "active": customer.active,
#             "confirmed_email": customer.confirmed_email
#         })
        
#         connection.commit()
#         return {"message": "Client created successfully", "id": new_id}

# 2. Listar todos los clientes (GET /clients)
@app.get("/clients")
def list_clients():
    with oracledb.connect(DSN) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM CLIENTEs")

        # Convertir filas a diccionarios
        columns = [col[0] for col in cursor.description]  
        data = []
        for row in cursor:
            data.append(dict(zip(columns, row)))

        return data
    

@app.get("/clients/count")
def get_clients_count():
    with oracledb.connect(DSN) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM CLIENTES")  
        count = cursor.fetchone()[0]

    return {"count": count}

# 3. Obtener un cliente por ID (GET /clients/{client_id})
@app.get("/clients/{client_id}")
def get_client(client_id: int):
    with oracledb.connect(DSN) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM CUSTOMER WHERE ID = :id", {"id": client_id})

        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        if row:
            return dict(zip(columns, row))
        else:
            return {"message": "Client not found"}

# 4. Actualizar parcialmente un cliente (PATCH /clients/{client_id})
@app.patch("/clients/{client_id}")
def update_client(client_id: int, customer: CustomerPatch):
    with oracledb.connect(DSN) as connection:
        cursor = connection.cursor()

        # Construir la consulta dinámicamente
        fields = []
        params = {}

        if customer.nationalId is not None:
            fields.append("NATIONAL_ID = :nationalId")
            params["nationalId"] = customer.nationalId

        if customer.name is not None:
            fields.append("NAME = :name")
            params["name"] = customer.name

        if customer.lastname is not None:
            fields.append("LASTNAME = :lastname")
            params["lastname"] = customer.lastname

        if customer.email is not None:
            fields.append("EMAIL = :email")
            params["email"] = customer.email

        if customer.phone is not None:
            fields.append("PHONE = :phone")
            params["phone"] = customer.phone

        if customer.active is not None:
            fields.append("ACTIVE = :active")
            params["active"] = customer.active

        if customer.confirmed_email is not None:
            fields.append("CONFIRMED_EMAIL = :confirmed_email")
            params["confirmed_email"] = customer.confirmed_email

        if not fields:
            return {"message": "No fields to update"}

        query = f"UPDATE CUSTOMER SET {', '.join(fields)} WHERE ID = :id"
        params["id"] = client_id

        cursor.execute(query, params)
        connection.commit()

        return {"message": "Client updated successfully"}

# 5. Eliminar (marcar como inactivo) un cliente (DELETE /clients/{client_id})
@app.delete("/clients/{client_id}")
def delete_client(client_id: int):
    with oracledb.connect(DSN) as connection:
        cursor = connection.cursor()
        # Marcar como inactivo en lugar de borrar físicamente
        cursor.execute("UPDATE CUSTOMER SET ACTIVE = 'N' WHERE ID = :id", {"id": client_id})
        connection.commit()

    return {"message": "Client deleted successfully"}



if __name__ == "__main__":
    import uvicorn
    # Aquí definimos la ejecución directa del servidor
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)