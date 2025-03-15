import oracledb
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
import bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

def get_db_connection():
    return oracledb.connect(user="SYSTEM", password="bdp1", dsn="localhost:1521/FREE")

@app.route('/api/test', methods=['GET'])
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Ejecutar consulta
        cursor.execute("SELECT id, name FROM CLIENTES")
        users = [{'id': row[0], 'nombre': row[1]} for row in cursor.fetchall()]

        # Cerrar conexión
        cursor.close()
        conn.close()
        return jsonify(users), 200

    except Exception as e:
        return jsonify({'status': 500, 'message': str(e)}), 500


# -------------- GESTION DE USUARIOS -------------------------
 
 # 1. Crear Usuario (POST /api/users)
@app.route('/api/users', methods=['POST'])
def crear_usuario():
    try:
        data = request.json
        name = data.get('name')
        lastname = data.get('lastname')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone')
        national_document = data.get('national_document')

        if not all([name, lastname, email, password, phone, national_document]):
            return jsonify({'status': 400, 'message': 'Faltan datos obligatorios'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM CLIENTES WHERE email = :1", (email,))
        if cursor.fetchone():
            return jsonify({'status': 409, 'message': 'El email ya está registrado'}), 409


        cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM CLIENTES")
        new_id = cursor.fetchone()[0]

        # Encriptar la contraseña con bcrypt
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        active = 1  
        confirmed_email = 0

        # Insertar nuevo usuario
        cursor.execute("""
            INSERT INTO CLIENTES
            VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """, (new_id, national_document, name, lastname, email, hashed_password, phone, active, confirmed_email))

        conn.commit()

        # Cerrar conexión
        cursor.close()
        conn.close()

        return jsonify({'status': 200, 'message': 'Usuario creado con éxito', 'id': new_id}), 200
    except Exception as e:
        return jsonify({'status': 500, 'message': str(e)}), 500

 # 2. Iniciar Sesión (Login) (POST /api/users/login)
@app.route('/api/users/login', methods=['POST'])
def iniciar_sesion():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not all([email, password]):
            return jsonify({'status': 400, 'message': 'Faltan datos obligatorios'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, password FROM CLIENTES WHERE email = :1", (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'status': 404, 'message': 'Usuario no encontrado'}), 404

        user_id, hashed_password = user

        if not bcrypt.check_password_hash(hashed_password, password):
            return jsonify({'status': 401, 'message': 'Contraseña incorrecta'}), 401

        return jsonify({'status': 200, 'message': 'Inicio de sesión exitoso', 'id': user_id}), 200
    except Exception as e:
        return jsonify({'status': 500, 'message': str(e)}), 500

 # 3. Obtener Perfil de Usuario (GET /api/users/:id)
@app.route('/api/users/<int:user_id>', methods=['GET'])
def obtener_perfil_usuario(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, national_document, name, lastname, email, phone, active, confirmed_email, created_at
            FROM CLIENTES WHERE id = :1
        """, (user_id,))
        
        user = cursor.fetchone()
        
        if not user:
            return jsonify({'status': 404, 'message': 'Usuario no encontrado'}), 404

        user_data = {
            'id': user[0],
            'national_document': user[1],
            'name': user[2],
            'lastname': user[3],
            'email': user[4],
            'phone': user[5],
            'active': bool(user[6]),
            'confirmed_email': bool(user[7]),
            'created_at': user[8].strftime('%Y-%m-%d %H:%M:%S')  # Formatear fecha
        }

        return jsonify({'user': user_data}), 200

    except Exception as e:
        return jsonify({'status': 500, 'message': str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

 # 4. Actualizar Usuario (PUT /api/users/:id)
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def actualizar_usuario(user_id):
    try:
        data = request.json
        campos_permitidos = ['national_document', 'name', 'lastname', 'email', 'phone', 'active', 'confirmed_email']
        
        # Filtrar solo los campos permitidos para actualizar
        campos_a_actualizar = {campo: data[campo] for campo in campos_permitidos if campo in data}

        if not campos_a_actualizar:
            return jsonify({'status': 400, 'message': 'No se proporcionaron datos válidos para actualizar'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si el usuario existe
        cursor.execute("SELECT id FROM CLIENTES WHERE id = :1", (user_id,))
        if not cursor.fetchone():
            return jsonify({'status': 404, 'message': 'Usuario no encontrado'}), 404

        # Construir la consulta dinámicamente
        set_clause = ", ".join(f"{campo} = :{i+1}" for i, campo in enumerate(campos_a_actualizar.keys()))
        valores = list(campos_a_actualizar.values()) + [user_id]

        sql = f"UPDATE CLIENTES SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = :{len(valores)}"
        cursor.execute(sql, valores)

        conn.commit()
        
        return jsonify({'status': 200, 'message': 'Usuario actualizado correctamente'}), 200

    except Exception as e:
        return jsonify({'status': 500, 'message': str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

 # 5. Eliminar Usuario (DELETE /api/users/:id)
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def eliminar_usuario(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si el usuario existe
        cursor.execute("SELECT id FROM CLIENTES WHERE id = :1", (user_id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'status': 404, 'message': 'Usuario no encontrado'}), 404

        # Marcar como inactivo
        cursor.execute("UPDATE CLIENTES SET active = 0 WHERE id = :1", (user_id,))
        conn.commit()

        return jsonify({'status': 200, 'message': 'Usuario desactivado correctamente'}), 200

    except Exception as e:
        return jsonify({'status': 500, 'message': str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# -------------- GESTION DE PRODUCTOS -------------------------

# 1. Listar Productos (GET /api/products)
@app.route('/api/products', methods=['GET'])
def listar_productos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Obtener todos los productos activos
        cursor.execute("""
            SELECT id, sku, name, description, price, slug, active, category_id, created_at, updated_at
            FROM PRODUCTOS
        """)
        productos = [
            {
                'id': row[0],
                'sku': row[1],
                'name': row[2],
                'description': row[3],
                'price': float(row[4]),  # Convertir a número flotante
                'slug': row[5],
                'active': row[6],
                'category_id': row[7],
                'created_at': row[8].isoformat(),
                'updated_at': row[9].isoformat()
            }
            for row in cursor.fetchall()
        ]

        return jsonify({'products': productos}), 200

    except Exception as e:
        return jsonify({'status': 500, 'message': str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# 2. Detalle de Producto (GET /api/products/:id)
@app.route('/api/products/<int:product_id>', methods=['GET'])
def obtener_detalle_producto(product_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Buscar el producto por ID
        cursor.execute("""
            SELECT id, sku, name, description, price, slug, active, category_id, created_at, updated_at
            FROM PRODUCTOS
            WHERE id = :1
        """, (product_id,))
        
        producto = cursor.fetchone()

        # Si no existe, devolver error 404
        if not producto:
            return jsonify({'status': 404, 'message': 'Producto no encontrado'}), 404

        # Construir la respuesta con el detalle del producto
        producto_data = {
            'id': producto[0],
            'sku': producto[1],
            'name': producto[2],
            'description': producto[3],
            'price': float(producto[4]),
            'slug': producto[5],
            'active': producto[6],
            'category_id': producto[7],
            'created_at': producto[8].isoformat(),
            'updated_at': producto[9].isoformat()
        }

        return jsonify({'product': producto_data}), 200

    except Exception as e:
        return jsonify({'status': 500, 'message': str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# 3. Crear Producto (POST /api/products)
@app.route('/api/products', methods=['POST'])
def crear_producto():
    try:
        data = request.json
        sku = data.get('sku')
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        slug = data.get('slug')
        active = data.get('active')
        category_id = data.get('category_id')

        if not all([sku, name, description, price, slug, active, category_id]):
            return jsonify({'status': 400, 'message': 'Faltan datos obligatorios'}), 400

        if not isinstance(price, (int, float)) or price <= 0:
            return jsonify({'status': 400, 'message': 'El precio debe ser un número positivo'}), 400

        if active not in ['T', 'F']:
            return jsonify({'status': 400, 'message': "El campo 'active' debe ser 'T' o 'F'"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM PRODUCTOS")
        new_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO PRODUCTOS (id, sku, name, description, price, slug, active, category_id, created_at, updated_at)
            VALUES (:1, :2, :3, :4, :5, :6, :7, :8, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """, (new_id, sku, name, description, price, slug, active, category_id))

        conn.commit()

        return jsonify({'status': 200, 'message': 'Producto creado exitosamente', 'id': new_id}), 200

    except Exception as e:
        return jsonify({'status': 500, 'message': str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# 4. Actualizar Producto (PUT /api/products/:id)
@app.route('/api/products/<int:product_id>', methods=['PUT'])
def actualizar_producto(product_id):
    try:
        data = request.json

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM PRODUCTOS WHERE id = :1", (product_id,))
        producto = cursor.fetchone()

        if not producto:
            return jsonify({'status': 404, 'message': 'Producto no encontrado'}), 404

        campos_actualizar = []
        valores = []

        for campo in ["sku", "name", "description", "price", "slug", "active", "category_id"]:
            if campo in data:
                campos_actualizar.append(f"{campo} = :{len(valores) + 1}")
                valores.append(data[campo])

        if not campos_actualizar:
            return jsonify({'status': 400, 'message': 'No se proporcionaron datos para actualizar'}), 400

        valores.append(product_id) 

        sql = f"UPDATE PRODUCTOS SET {', '.join(campos_actualizar)}, updated_at = CURRENT_TIMESTAMP WHERE id = :{len(valores)}"
        cursor.execute(sql, valores)
        conn.commit()

        return jsonify({'status': 200, 'message': 'Producto actualizado correctamente'}), 200

    except Exception as e:
        return jsonify({'status': 500, 'message': str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


# 5. Elimiar Producto (DELETE /api/products/:id)
@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def eliminar_producto(product_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM PRODUCTOS WHERE id = :1", (product_id,))
        producto = cursor.fetchone()

        if not producto:
            return jsonify({'status': 404, 'message': 'Producto no encontrado'}), 404

        cursor.execute("UPDATE PRODUCTOS SET active = 'F', updated_at = CURRENT_TIMESTAMP WHERE id = :1", (product_id,))
        conn.commit()

        return jsonify({'status': 200, 'message': 'Producto inactivado correctamente'}), 200

    except Exception as e:
        return jsonify({'status': 500, 'message': str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# ------------------ GESTIÓN DE ORDENES ----------------------

# 1. Crear Orden de Compra (POST /api/orders)   
@app.route('/api/orders', methods=['POST'])
def crear_orden():
    try:
        data = request.json
        user_id = data.get('userId')
        items = data.get('items')
        shipping_address = data.get('shippingAddress')
        payment_method = data.get('paymentMethod')

        if not all([user_id, items, shipping_address, payment_method]):
            return jsonify({'status': 400, 'message': 'Faltan datos obligatorios'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM CLIENTES WHERE id = :1", (user_id,))
        if not cursor.fetchone():
            return jsonify({'status': 404, 'message': 'Usuario no encontrado'}), 404

        cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM ORDENES_DE_COMPRA")
        order_id = cursor.fetchone()[0]

        location_id = 1

        cursor.execute("""
            INSERT INTO ORDENES_DE_COMPRA (id, client_id, location_id, created_at, updated_at)
            VALUES (:1, :2, :3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """, (order_id, user_id, location_id))

        total_amount = 0

        for item in items:
            product_id = item.get('productId')
            quantity = item.get('quantity')

            cursor.execute("SELECT price FROM PRODUCTOS WHERE id = :1", (product_id,))
            product = cursor.fetchone()

            if not product:
                return jsonify({'status': 404, 'message': f'Producto con ID {product_id} no encontrado'}), 404

            price = product[0]
            total_price = price * quantity
            total_amount += total_price

            cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM DETALLE_ORDEN_COMPRA")
            detail_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO DETALLE_ORDEN_COMPRA (id, order_id, product_id, quantity, price, created_at, updated_at)
                VALUES (:1, :2, :3, :4, :5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """, (detail_id, order_id, product_id, quantity, price))

        conn.commit()

        return jsonify({
            'status': 'success',
            'message': 'Orden creada exitosamente',
            'orderId': order_id,
            'totalAmount': total_amount,
            'orderStatus': 'processing'
        }), 201

    except Exception as e:
        return jsonify({'status': 500, 'message': str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# 2. Listar Ordenes de Compra (GET /api/orders)
@app.route('/api/orders', methods=['GET'])
def listar_ordenes():
    try:
        fecha_inicio = request.args.get('startDate')  # Filtro opcional por fecha inicio (YYYY-MM-DD)
        fecha_fin = request.args.get('endDate')  # Filtro opcional por fecha fin (YYYY-MM-DD)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Query principal para obtener las órdenes
        query = """
            SELECT oc.id, oc.client_id, TO_CHAR(oc.created_at, 'YYYY-MM-DD') AS created_at
            FROM ORDENES_DE_COMPRA oc
            WHERE 1=1
        """
        params = []

        if fecha_inicio:
            query += " AND oc.created_at >= TO_DATE(:start_date, 'YYYY-MM-DD')"
            params.append(fecha_inicio)

        if fecha_fin:
            query += " AND oc.created_at <= TO_DATE(:end_date, 'YYYY-MM-DD')"
            params.append(fecha_fin)

        query += " ORDER BY oc.created_at DESC"

        cursor.execute(query, params)
        orders = cursor.fetchall()

        # Construir la respuesta con productos
        order_list = []

        for order in orders:
            order_id, user_id, created_at = order

            # Obtener los productos de cada orden
            cursor.execute("""
                SELECT product_id, quantity, price 
                FROM DETALLE_ORDEN_COMPRA 
                WHERE order_id = :1
            """, (order_id,))
            
            items = [
                {"productId": row[0], "quantity": row[1], "price": float(row[2])}
                for row in cursor.fetchall()
            ]

            # Calcular el totalAmount sumando precio * cantidad
            total_amount = sum(item["price"] * item["quantity"] for item in items)

            order_list.append({
                "orderId": order_id,
                "userId": user_id,
                "totalAmount": total_amount,
                "createdAt": created_at,
                "items": items
            })

        return jsonify({"orders": order_list}), 200

    except Exception as e:
        return jsonify({'status': 500, 'message': str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


# 3. Detalle de Orden de Compra (GET /api/orders/:id)
@app.route('/api/orders/<int:order_id>', methods=['GET'])
def detalle_orden(order_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT oc.id, oc.client_id, TO_CHAR(oc.created_at, 'YYYY-MM-DD') AS created_at
            FROM ORDENES_DE_COMPRA oc
            WHERE oc.id = :1
        """, (order_id,))
        
        order = cursor.fetchone()
        if not order:
            return jsonify({'status': 404, 'message': 'Orden no encontrada'}), 404

        order_id, user_id, created_at = order

        cursor.execute("""
            SELECT product_id, quantity, price 
            FROM DETALLE_ORDEN_COMPRA 
            WHERE order_id = :1
        """, (order_id,))
        
        items = [
            {"productId": row[0], "quantity": row[1], "price": float(row[2])}
            for row in cursor.fetchall()
        ]

        total_amount = sum(item["price"] * item["quantity"] for item in items)

        response = {
            "orderId": order_id,
            "userId": user_id,
            "totalAmount": total_amount,
            "createdAt": created_at,
            "items": items
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'status': 500, 'message': str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# ------------------- GESTION DE PAGOS -----------------------
# 1. Registrar Pago (POST /api/payments)
@app.route('/api/payments', methods=['POST'])
def registrar_pago():
    try:
        data = request.json
        order_id = data.get('orderId')
        amount = data.get('amount')
        payment_method = data.get('method')

        if not all([order_id, amount, payment_method]):
            return jsonify({'status': 400, 'message': 'Faltan datos obligatorios'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM ORDENES_DE_COMPRA WHERE id = :1", (order_id,))
        if not cursor.fetchone():
            return jsonify({'status': 404, 'message': 'Orden no encontrada'}), 404

        cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM PAGOS")
        payment_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO PAGOS (id, order_id, payment_method, status, updated_at, created_at)
            VALUES (:1, :2, :3, :4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """, (payment_id, order_id, payment_method, "PAID"))

        conn.commit()

        return jsonify({'status': 200, 'message': 'Pago registrado correctamente', 'paymentId': payment_id}), 200

    except Exception as e:
        return jsonify({'status': 500, 'message': str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


# 2. Consultar Pagos (GET /api/payments)
@app.route('/api/payments', methods=['GET'])
def consultar_pagos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, order_id, payment_method, status, TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI:SS') AS created_at
            FROM PAGOS
        """)
        payments = [
            {
                'paymentId': row[0],
                'orderId': row[1],
                'paymentMethod': row[2],
                'status': row[3],
                'createdAt': row[4]
            }
            for row in cursor.fetchall()
        ]

        return jsonify({'payments': payments}), 200

    except Exception as e:
        return jsonify({'status': 500, 'message': str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# ------------------- MAIN -----------------------

if __name__ == '__main__':
    app.run(debug=True)