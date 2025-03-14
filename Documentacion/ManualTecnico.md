# <h1 align="center">Proyecto 01</h1>

<div align="center">
📕 Sistemas de Bases de Datos 1
</div>
<div align="center"> 🏛 Universidad de San Carlos de Guatemala</div>
<div align="center"> 📆 Primer Semestre 2025</div>
<div align="center">📎 Yania Eszter Dávid </div>
<div align="center"> 🖋️ 202010175 </div>

---


## Descripción del proyecto

 Este proyecto tiene como objetivo el diseño y desarrollo de una base de datos relacional optimizada y normalizada para un centro de ventas en línea de gran escala.

La base de datos estará diseñada bajo los principios de integridad referencial y normalización, garantizando el almacenamiento y procesamiento eficiente de grandes volúmenes de información. Para ello, se definirán entidades clave como:

- **Usuarios** (clientes y administradores del sistema).
- **Trabajadores** (empleados encargados de la gestión operativa).
- **Productos** (inventario disponible para la venta).
- **Órdenes de compra** (transacciones realizadas por los clientes).
- **Pagos** (procesamiento y validación de transacciones financieras).
- **Envíos** (gestión de la logística y distribución).
- **Devoluciones** (mecanismos para el procesamiento de reembolsos y cambios).
- **Traslados de productos** (movimientos internos de inventario entre almacenes o centros de distribución).

Además, el sistema deberá permitir la incorporación automatizada de datos mediante dos mecanismos principales:

1. **Carga masiva** a través de archivos en formato CSV, facilitando la migración y actualización de grandes volúmenes de información.
2. **API de integración**, que posibilite la comunicación con plataformas externas y la actualización en tiempo real de los datos del sistema.

Este enfoque garantizará un sistema escalable, flexible y capaz de adaptarse a las necesidades operativas de un comercio electrónico de gran alcance.

---

## Diseño Sin Normalizar

### Modelo Conceptual

![Modelo Conceptual](img/Conceptual_1.png)

Modelo Conceptual sin Normalizar

### Modelo Lógico

![Modelo Logico](img/Logical_1.png)

Modelo Lógico sin Normalizar

### Modelo Físico

![Modelo Fisico](img/Relational_1.png)

Modelo Físico sin Normalizar

---

## Normalización

### Primera Forma Normal (1FN)

---

##### Tabla: `clientes`

| Clientes             |
|------------------|
| id              |
| national_document |
| name            |
| lastname        |
| email          |
| phone          |
| active         |
| confirmed_email |
| address        |
| payment_method |
| created_at     |
| updated_at     |

 `clientes (1FN)`
| Clientes             |
|------------------|
| id              |
| national_document |
| name            |
| lastname        |
| email          |
| phone          |
| active         |
| confirmed_email |
| created_at     |
| updated_at     |

 `Direccciones (1FN)`
| Direcciones             |
|------------------|
| id              |
| client_id |
| address            |
| created_at     |
| updated_at     |

 `Métodos de Pago (1FN)`
| Métodos de Pago            |
|------------------|
| id              |
| client_id |
| payment_method            |
| created_at     |
| updated_at     |

---

#### Tabla: `orden_de_compra`

| Orden_de_compra       |
|------------|
| id         |
| client_id  |
| created_at |
| updated_at |
 

 `orden_de_compra (1FN)`

| Orden_de_compra       |
|------------|
| id         |
| client_id  |
| created_at |
| updated_at |

Esta tabla no presenta atributos con varios valores

---

#### Tabla: `detalle_orden_de_compra`

| detalle_orden_de_compra      |
|-----------|
| id        |
| order_id  |
| product_id |
| quantity  |
| price     |
| created_at |
| updated_at |


`detalle_orden_de_compra (1FN)`

| detalle_orden_de_compra      |
|-----------|
| id        |
| order_id  |
| product_id |
| quantity  |
| price     |
| created_at |
| updated_at |

Esta tabla no presenta atributos con varios valores

---

#### Tabla: `pago`

| pago         |
|--------------|
| id          |
| order_id    |
| mount       |
| payment_method |
| status      |
| created_at  |
| updated_at  |

`pago (1FN)`

| pago         |
|--------------|
| id          |
| order_id    |
| mount       |
| payment_method |
| status      |
| created_at  |
| updated_at  |

Esta tabla no presenta atributos con varios valores

---

#### Tabla: `envios`

| envios             |
|------------------|
| id              |
| order_id        |
| address        |
| transport_company |
| tracking_id    |
| status         |
| created_at     |
| updated_at     |

`envios (1FN)`

| envios             |
|------------------|
| id              |
| order_id        |
| address        |
| transport_company |
| tracking_id    |
| status         |
| created_at     |
| updated_at     |

Esta tabla no presenta atributos con varios valores


---

#### Tabla: `producto`

| producto       |
|------------|
| id         |
| sku        |
| name       |
| description |
| price      |
| slug       |
| active     |
| imagen_id     |
| imagen_url     |
| categoria |
| created_at |
| updated_at |

`producto (1FN)`

| producto       |
|------------|
| id         |
| sku        |
| name       |
| description |
| price      |
| slug       |
| active     |
| imagen_id     |
| imagen_url     |
| categoria_id |
| created_at |
| updated_at |

`categoria (1FN)`

| categoria       |
|------------|
| id         |
| name       |
| created_at |
| updated_at |

---

#### Tabla: `trabajadores`

| trabajadores           |
|---------------|
| id            |
| national_document |
| name          |
| lastname      |
| job          |
| department   |
| phone        |
| email        |
| sede_id      |
| sede_name    |
| active       |
| created_at   |
| updated_at   |

`trabajadores (1FN)`

| trabajadores           |
|---------------|
| id            |
| national_document |
| name          |
| lastname      |
| job          |
| department   |
| phone        |
| email        |
| sede_id      |
| sede_name    |
| active       |
| created_at   |
| updated_at   |


Esta tabla no presenta atributos con varios valores



---

#### Tabla: `inventario`

| inventario       |
|------------|
| id         |
| product_id |
| location_id |
| quantity   |
| created_at |
| updated_at |
| sede_id    |

`inventario (1FN)`

| inventario       |
|------------|
| id         |
| product_id |
| location_id |
| quantity   |
| created_at |
| updated_at |
| sede_id    |


Esta tabla no presenta atributos con varios valores


---

#### Tabla: `traslados`

| traslados        |
|------------|
| id         |
| order_id   |
| origin_id  |
| destination_id |
| products_id |
| status     |
| requested_date |
| arrive_date |
| created_at |
| updated_at |

`traslados (1FN)`

| traslados        |
|------------|
| id         |
| order_id   |
| origin_id  |
| destination_id |
| products_id |
| status     |
| requested_date |
| arrive_date |
| created_at |
| updated_at |

Esta tabla no presenta atributos con varios valores


---

#### Tabla: `devolucion`

| devolucion        |
|------------|
| id         |
| order_id   |
| request_date |
| reason     |
| status     |
| product_id |
| created_at |
| updated_at |

`devolucion (1FN)`

| devolucion        |
|------------|
| id         |
| order_id   |
| request_date |
| reason     |
| status     |
| product_id |
| created_at |
| updated_at |


---

##### Modelo Lógico 1FN

![Modelo Logico](img/Logical_1FN.png)

Modelo Lógico 1FN

##### Modelo Físico 1FN

![Modelo Fisico](img/Relational_1FN.png)

Modelo Físico 1FN

---

### Segunda Forma Normal (2FN)

* Se omite copiar las tablas nuevamente si no se ven afectadas 

---

#### Tabla: `Cliente`
No presenta valores que dependan de otro id diferente a la Primary Key

---

#### Tabla: `Direcciones`
No presenta valores que dependan de otro id diferente a la Primary Key

---

#### Tabla: `Método de Pago`
No presenta valores que dependan de otro id diferente a la Primary Key

---

#### Tabla: `Orden de Compra`
No presenta valores que dependan de otro id diferente a la Primary Key

---

#### Tabla: `Pago`
No presenta valores que dependan de otro id diferente a la Primary Key

---

#### Tabla: `Detalle Orden de Compra`
No presenta valores que dependan de otro id diferente a la Primary Key

---

#### Tabla: `Envios`
No presenta valores que dependan de otro id diferente a la Primary Key

---

#### Tabla: `Inventario`
No presenta valores que dependan de otro id diferente a la Primary Key

---

#### Tabla: `Devolución`
No presenta valores que dependan de otro id diferente a la Primary Key

---

#### Tabla:  `producto`

| producto       |
|------------|
| id         |
| sku        |
| name       |
| description |
| price      |
| slug       |
| active     |
| imagen_id     |
| imagen_url     |
| categoria_id |
| created_at |
| updated_at |

`categoria`

| categoria       |
|------------|
| id         |
| name       |
| created_at |
| updated_at |


 `producto (2FN)`

| producto       |
|------------|
| id         |
| sku        |
| name       |
| description |
| price      |
| slug       |
| active     |
| imagen_id     |
| categoria_id |
| created_at |
| updated_at |

`Imagen (2FN)`

| Imagen       |
|------------|
| id         |
| product_id       |
| imagen_url |
| created_at |
| updated_at |

---

#### Tabla: `traslados`

| traslados        |
|------------|
| id         |
| order_id   |
| origin_id  |
| destination_id |
| products_id |
| status     |
| requested_date |
| arrive_date |
| created_at |
| updated_at |

`traslados (2FN)`

| traslados        |
|------------|
| id         |
| order_id   |
| origin_id  |
| destination_id |
| status     |
| requested_date |
| arrive_date |
| created_at |
| updated_at |

`Detalle Traslados (2FN)`

| Detalle Traslados        |
|------------|
| id         |
| traslado_id   |
| products_id |
| quantity |
| created_at |
| updated_at |

---

#### Tabla: `trabajadores`

| trabajadores           |
|---------------|
| id            |
| national_document |
| name          |
| lastname      |
| job          |
| department   |
| phone        |
| email        |
| sede_id      |
| sede_name    |
| active       |
| created_at   |
| updated_at   |


`trabajadores (2FN)`

| trabajadores           |
|---------------|
| id            |
| national_document |
| name          |
| lastname      |
| job          |
| department   |
| phone        |
| email        |
| sede_id      |
| active       |
| created_at   |
| updated_at   |


`sede (2FN)`

| sede           |
|---------------|
| id            |
| name          |
| created_at   |
| updated_at   |


---

## Tercera Forma Normal (3FN)

Después de analizar el diseño de la base de datos, se confirmó que todas las tablas ya cumplen con la **Tercera Forma Normal (3FN)**.

- Todos los atributos dependen únicamente de la clave primaria.  
- No hay dependencias transitivas entre columnas.  
- La estructura está bien organizada, evitando redundancia y manteniendo la integridad de los datos.

Por estas razones, no fue necesario hacer cambios adicionales en esta etapa.


---

## Diseño Final

### Modelo Conceptual

![Modelo Conceptual](img/Conceptual_3FN.png)

Modelo Conceptual 3FN

### Modelo Lógico

![Modelo Logico](img/Logical_3FN.png)

Modelo Lógico 3FN

### Modelo Físico

![Modelo Fisico](img/Relational_3FN.png)

Modelo Físico 3FN

---


## Descripción de las Relaciones

Aplica para todas las relaciones:
![Relaciones](imgs/relations.png)

---

## Tablas
Aplica para todas las tablas:
![Tabla](imgs/table.png)

---

## Script de Creación de la Base de Datos

```sql
-- Tabla 1: categoria
CREATE TABLE categoria (
    id         INTEGER  NOT NULL,
    name       VARCHAR2(250) NOT NULL,
    created_at DATE NOT NULL,
    updated_at DATE NOT NULL,
    CONSTRAINT categoria_PK PRIMARY KEY (id)
);

-- Tabla 2: clientes
CREATE TABLE clientes (
    id                INTEGER  NOT NULL,
    national_document INTEGER  NOT NULL,
    name              VARCHAR2(250) NOT NULL,
    lastname          VARCHAR2(250) NOT NULL,
    email             VARCHAR2(300) NOT NULL,
    phone             VARCHAR2(15) NOT NULL,
    active            CHAR(1) NOT NULL,
    confirrmed_email  CHAR(1),
    address_id        VARCHAR2(300),
    payment_method    VARCHAR2(200),
    created_at        DATE NOT NULL,
    updated_at        DATE NOT NULL,
    CONSTRAINT clientes_PK PRIMARY KEY (id, national_document)
);

-- Tabla 3: detalle_orden_de_compra
CREATE TABLE detalle_orden_de_compra (
    id                        INTEGER  NOT NULL,
    order_id                  INTEGER  NOT NULL,
    product_id                INTEGER  NOT NULL,
    quantity                  INTEGER  NOT NULL,
    price                     NUMBER  NOT NULL,
    created_at                DATE NOT NULL,
    updated_at                DATE NOT NULL,
    orden_de_compra_id        INTEGER  NOT NULL,
    orden_de_compra_client_id INTEGER  NOT NULL,
    CONSTRAINT detalle_orden_de_compra_PK PRIMARY KEY (id, order_id)
);

-- Tabla 4: Detalle_Traslado
CREATE TABLE Detalle_Traslado (
    id                 INTEGER  NOT NULL,
    traslado_id        INTEGER  NOT NULL,
    product_id         INTEGER,
    quantity           INTEGER  NOT NULL,
    created_at         DATE NOT NULL,
    updated_at         DATE NOT NULL,
    traslados_id       INTEGER  NOT NULL,
    traslados_order_id INTEGER  NOT NULL,
    CONSTRAINT Detalle_Traslado_PK PRIMARY KEY (id)
);

-- Tabla 5: devolucion
CREATE TABLE devolucion (
    id             INTEGER  NOT NULL,
    order_id       INTEGER  NOT NULL,
    requested_date DATE NOT NULL,
    reason         VARCHAR2(350) NOT NULL,
    status         VARCHAR2(50) NOT NULL,
    product_id     INTEGER  NOT NULL,
    created_at     DATE NOT NULL,
    updated_at     DATE NOT NULL,
    inventario_id  INTEGER  NOT NULL,
    CONSTRAINT devolucion_PK PRIMARY KEY (id, order_id)
);

-- Tabla 6: direcciones
CREATE TABLE direcciones (
    id                         INTEGER  NOT NULL,
    client_id                  INTEGER  NOT NULL,
    address                    VARCHAR2(300) NOT NULL,
    created_at                 DATE,
    updated_at                 DATE NOT NULL,
    clientes_id                INTEGER  NOT NULL,
    clientes_national_document INTEGER  NOT NULL,
    CONSTRAINT direcciones_PK PRIMARY KEY (id)
);

-- Tabla 7: envios
CREATE TABLE envios (
    id                        INTEGER  NOT NULL,
    order_id                  INTEGER  NOT NULL,
    address                   VARCHAR2(300) NOT NULL,
    transport_company         VARCHAR2(100) NOT NULL,
    tracking_id               INTEGER  NOT NULL,
    status                    VARCHAR2(30) NOT NULL,
    created_at                DATE NOT NULL,
    updated_at                DATE NOT NULL,
    orden_de_compra_id        INTEGER  NOT NULL,
    orden_de_compra_client_id INTEGER  NOT NULL,
    CONSTRAINT envios_PK PRIMARY KEY (id, order_id)
);

-- Tabla 8: imagen
CREATE TABLE imagen (
    id           INTEGER  NOT NULL,
    product_id   INTEGER  NOT NULL,
    imagen_url   VARCHAR2(300) NOT NULL,
    created_at   DATE NOT NULL,
    updated_at   DATE NOT NULL,
    producto_id  INTEGER  NOT NULL,
    producto_sku VARCHAR2(25) NOT NULL,
    id3          INTEGER  NOT NULL,
    order_id     INTEGER  NOT NULL,
    CONSTRAINT imagen_PK PRIMARY KEY (id)
);

-- Tabla 9: inventario
CREATE TABLE inventario (
    id          INTEGER  NOT NULL,
    product_id  INTEGER  NOT NULL,
    location_id INTEGER  NOT NULL,
    quantity    INTEGER  NOT NULL,
    created_at  DATE NOT NULL,
    updated_at  DATE NOT NULL,
    sede_id     INTEGER  NOT NULL,
    sede_id2    INTEGER  NOT NULL,
    CONSTRAINT inventario_PK PRIMARY KEY (id)
);

-- Tabla 10: metodos_de_pago
CREATE TABLE metodos_de_pago (
    id                         INTEGER  NOT NULL,
    client_id                  INTEGER,
    payment_method             VARCHAR2(100) NOT NULL,
    created_at                 DATE,
    updated_at                 DATE NOT NULL,
    clientes_id                INTEGER  NOT NULL,
    clientes_national_document INTEGER  NOT NULL,
    CONSTRAINT metodos_de_pago_PK PRIMARY KEY (id)
);

-- Tabla 11: orden_de_compra
CREATE TABLE orden_de_compra (
    id                         INTEGER  NOT NULL,
    client_id                  INTEGER  NOT NULL,
    created_at                 DATE NOT NULL,
    updated_at                 DATE NOT NULL,
    clientes_id                INTEGER  NOT NULL,
    clientes_national_document INTEGER  NOT NULL,
    CONSTRAINT orden_de_compra_PK PRIMARY KEY (id, client_id)
);

-- Tabla 12: pago
CREATE TABLE pago (
    id                        INTEGER  NOT NULL,
    order_id                  INTEGER  NOT NULL,
    mount                     NUMBER  NOT NULL,
    payment_method            VARCHAR2(50) NOT NULL,
    status                    VARCHAR2(50) NOT NULL,
    updated_at                DATE NOT NULL,
    created_at                DATE NOT NULL,
    orden_de_compra_id        INTEGER  NOT NULL,
    orden_de_compra_client_id INTEGER  NOT NULL,
    CONSTRAINT pago_PK PRIMARY KEY (id, order_id)
);

-- Tabla 13: producto
CREATE TABLE producto (
    id                               INTEGER  NOT NULL,
    sku                              VARCHAR2(25) NOT NULL,
    name                             VARCHAR2(250) NOT NULL,
    description                      VARCHAR2(500) NOT NULL,
    price                            NUMBER NOT NULL,
    slug                             VARCHAR2(100) NOT NULL,
    sede                             INTEGER NOT NULL,
    active                           CHAR(1) NOT NULL,
    imagen_id                        VARCHAR2(300) NOT NULL,
    created_at                       DATE NOT NULL,
    updated_at                       DATE NOT NULL,
    inventario_id                    INTEGER NOT NULL,
    imagen_url                       VARCHAR2(350) NOT NULL,
    categoria_id                     INTEGER NOT NULL,
    detalle_orden_de_compra_id       INTEGER NOT NULL,
    det_orden_order_id               INTEGER NOT NULL,  -- se optimizó el nombre (anteriormente excedía 30 caracteres)
    CONSTRAINT producto_PK PRIMARY KEY (id, sku)
);

-- Tabla 14: sede
CREATE TABLE sede (
    id         INTEGER NOT NULL,
    name       VARCHAR2(250) NOT NULL,
    created_at DATE NOT NULL,
    updated_at DATE NOT NULL,
    CONSTRAINT sede_PK PRIMARY KEY (id)
);

-- Tabla 15: trabajadores
CREATE TABLE trabajadores (
    id                INTEGER NOT NULL,
    national_document INTEGER NOT NULL,
    name              VARCHAR2(250) NOT NULL,
    lastname          VARCHAR2(250) NOT NULL,
    job               VARCHAR2(250) NOT NULL,
    departament       INTEGER NOT NULL,
    phone             VARCHAR2(15) NOT NULL,
    email             VARCHAR2(300),
    sede_id           INTEGER NOT NULL,
    active            CHAR(1) NOT NULL,
    created_at        DATE NOT NULL,
    updated_at        DATE NOT NULL,
    inventario_id     INTEGER NOT NULL,
    sede_name         VARCHAR2(100) NOT NULL,
    sede_id2          INTEGER NOT NULL,
    CONSTRAINT trabajadores_PK PRIMARY KEY (id, national_document)
);

-- Tabla 16: traslados
CREATE TABLE traslados (
    id             INTEGER NOT NULL,
    order_id       INTEGER NOT NULL,
    origin_id      INTEGER NOT NULL,
    destination_id INTEGER,
    products_id    INTEGER NOT NULL,
    quantities     INTEGER NOT NULL,
    requested_date DATE NOT NULL,
    arrive_date    DATE NOT NULL,
    created_at     DATE NOT NULL,
    updated_at     DATE NOT NULL,
    inventario_id  INTEGER NOT NULL,
    status         VARCHAR2(50) NOT NULL,
    CONSTRAINT traslados_PK PRIMARY KEY (id, order_id)
);

```

---

# <h1 align="center">Integración a la Base de Datos</h1>

### Endpoints

Descripción de los endpoints