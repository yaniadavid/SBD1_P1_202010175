-- Tabla 1: CATEGORIAS
CREATE TABLE CATEGORIAS (
    id         INTEGER       PRIMARY KEY,
    name       VARCHAR2(250) NOT NULL,
    created_at TIMESTAMP     DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP     DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Tabla 2: SEDES
CREATE TABLE SEDES (
    id         INTEGER       PRIMARY KEY,
    name       VARCHAR2(250) NOT NULL,
    created_at TIMESTAMP     DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP     DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Tabla 3: CLIENTES
CREATE TABLE CLIENTES (
    id                INTEGER       PRIMARY KEY,
    national_document INTEGER       NOT NULL,
    name              VARCHAR2(250) NOT NULL,
    lastname          VARCHAR2(250) NOT NULL,
    email             VARCHAR2(300) NOT NULL,
    password          VARCHAR2(255) NOT NULL,
    phone             VARCHAR2(15)  NOT NULL,
    active            BOOLEAN       NOT NULL CHECK (active IN (0, 1)),
    confirmed_email   BOOLEAN       NOT NULL CHECK (confirmed_email IN (0, 1)),
    created_at        TIMESTAMP     DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at        TIMESTAMP     DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Tabla 4: PRODUCTOS
CREATE TABLE PRODUCTOS (
    id                               INTEGER       PRIMARY KEY,
    sku                              VARCHAR2(25)  NOT NULL,
    name                             VARCHAR2(250) NOT NULL,
    description                      VARCHAR2(500) NOT NULL,
    price                            NUMBER        NOT NULL,
    slug                             VARCHAR2(100) NOT NULL,
    active                           CHAR(1)       NOT NULL,
    category_id                      INTEGER       NOT NULL,
    created_at                       TIMESTAMP     DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at                       TIMESTAMP     DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_category_id FOREIGN KEY (category_id) REFERENCES CATEGORIAS (id)
);

-- Tabla 5: ORDENES_DE_COMPRA
CREATE TABLE ORDENES_DE_COMPRA (
    id                         INTEGER   PRIMARY KEY,
    client_id                  INTEGER   NOT NULL,
    location_id                INTEGER   NOT NULL,
    created_at                 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at                 TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_client_id FOREIGN KEY (client_id) REFERENCES CLIENTES (id),
    CONSTRAINT fk_location_id FOREIGN KEY (location_id) REFERENCES SEDES (id)
);

-- Tabla 6: DIRECCIONES
CREATE TABLE DIRECCIONES (
    id                         INTEGER       PRIMARY KEY,
    client_id                  INTEGER       NOT NULL,
    address                    VARCHAR2(300) NOT NULL,
    created_at                 TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    updated_at                 TIMESTAMP     DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_client_address FOREIGN KEY (client_id) REFERENCES CLIENTES (id)
);

-- Tabla 7: INVENTARIOS
CREATE TABLE INVENTARIOS (
    id          INTEGER   PRIMARY KEY,
    product_id  INTEGER   NOT NULL,
    location_id INTEGER   NOT NULL,
    quantity    INTEGER   NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_product_inventory FOREIGN KEY (product_id) REFERENCES PRODUCTOS (id),
    CONSTRAINT fk_location_inventory FOREIGN KEY (location_id) REFERENCES SEDES (id)
);

-- Tabla 8: DETALLE_ORDEN_COMPRA
CREATE TABLE DETALLE_ORDEN_COMPRA (
    id                        INTEGER   PRIMARY KEY,
    order_id                  INTEGER   NOT NULL,
    product_id                INTEGER   NOT NULL,
    quantity                  INTEGER   NOT NULL,
    price                     NUMBER    NOT NULL,
    created_at                TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at                TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_order_detail FOREIGN KEY (order_id) REFERENCES ORDENES_DE_COMPRA (id),
    CONSTRAINT fk_product_detail FOREIGN KEY (product_id) REFERENCES PRODUCTOS (id)
);

-- Tabla 9: METODOS_DE_PAGO
CREATE TABLE METODOS_DE_PAGO (
    id                         INTEGER       PRIMARY KEY,
    client_id                  INTEGER,
    payment_method             VARCHAR2(100) NOT NULL,
    created_at                 TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    updated_at                 TIMESTAMP     DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_client_method FOREIGN KEY (client_id) REFERENCES CLIENTES (id)
);

-- Tabla 10: PAGOS
CREATE TABLE PAGOS (
    id                        INTEGER   PRIMARY KEY,
    order_id                  INTEGER   NOT NULL,
    payment_method            VARCHAR2(50) NOT NULL,
    status                    VARCHAR2(50) NOT NULL,
    updated_at                TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    created_at                TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_order_payment FOREIGN KEY (order_id) REFERENCES ORDENES_DE_COMPRA (id)
);

-- Tabla 11: ENVIOS
CREATE TABLE ENVIOS (
    id                        INTEGER       PRIMARY KEY,
    order_id                  INTEGER       NOT NULL,
    address                   VARCHAR2(300) NOT NULL,
    transport_company         VARCHAR2(100) NOT NULL,
    tracking_id               INTEGER       NOT NULL,
    status                    VARCHAR2(30)  NOT NULL,
    delivered_at                TIMESTAMP     DEFAULT CURRENT_TIMESTAMP NOT NULL,
    created_at                TIMESTAMP     DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at                TIMESTAMP     DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_order_ship FOREIGN KEY (order_id) REFERENCES ORDENES_DE_COMPRA (id)
);

-- Tabla 12: DEVOLUCIONES
CREATE TABLE DEVOLUCIONES (
    id             INTEGER   PRIMARY KEY,
    requested_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    reason         VARCHAR2(350) NOT NULL,
    status         VARCHAR2(50)  NOT NULL,
    product_id     INTEGER   NOT NULL,
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_product_devolucion FOREIGN KEY (product_id) REFERENCES PRODUCTOS (id)
);

-- Tabla 13: TRABAJADORES
CREATE TABLE TRABAJADORES (
    id                INTEGER       PRIMARY KEY,
    national_document INTEGER       NOT NULL,
    name              VARCHAR2(250) NOT NULL,
    lastname          VARCHAR2(250) NOT NULL,
    job               VARCHAR2(250) NOT NULL,
    deparment          INTEGER       NOT NULL,
    phone             VARCHAR2(15)  NOT NULL,
    email             VARCHAR2(300),
    sede_id           INTEGER       NOT NULL,
    active            BOOLEAN       NOT NULL CHECK (active IN (0, 1)),
    created_at        TIMESTAMP     DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at        TIMESTAMP     DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_sede_employee FOREIGN KEY (sede_id) REFERENCES SEDES (id)

);

-- Tabla 14: IMAGENES
CREATE TABLE IMAGENES (
    id           INTEGER       PRIMARY KEY,
    product_id   INTEGER       NOT NULL,
    imagen_url   VARCHAR2(300) NOT NULL,
    created_at   TIMESTAMP     DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at   TIMESTAMP     DEFAULT CURRENT_TIMESTAMP NOT NULL,
   CONSTRAINT fk_product_image FOREIGN KEY (product_id) REFERENCES PRODUCTOS (id)
);

-- Tabla 15: TRASLADOS
CREATE TABLE TRASLADOS (
    id             INTEGER       PRIMARY KEY,
    origin_id      INTEGER       NOT NULL,
    destination_id INTEGER      NOT NULL,
    requested_date TIMESTAMP     NOT NULL,
    arrive_date    TIMESTAMP     NOT NULL,
    created_at     TIMESTAMP     DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at     TIMESTAMP     DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_origin_movement FOREIGN KEY (origin_id) REFERENCES SEDES (id),
    CONSTRAINT fk_destination_movement FOREIGN KEY (destination_id) REFERENCES SEDES (id)
);

-- Tabla 16: DETALLE_TRASLADO
CREATE TABLE DETALLE_TRASLADO (
    id                 INTEGER   PRIMARY KEY,
    movement_id        INTEGER   NOT NULL,
    product_id         INTEGER   NOT NULL,
    quantity           INTEGER   NOT NULL,
    created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_movement_movement FOREIGN KEY (movement_id) REFERENCES TRASLADOS (id),
    CONSTRAINT fk_product_movement FOREIGN KEY (product_id) REFERENCES PRODUCTOS (id)
);