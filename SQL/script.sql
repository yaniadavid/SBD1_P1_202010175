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
