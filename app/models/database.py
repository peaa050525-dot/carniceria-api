import sqlite3
import os

DB_NAME = "carniceria.db"

def get_connection():
    return sqlite3.connect(DB_NAME)


def crear_tablas():
    conn = get_connection()
    cursor = conn.cursor()

  
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        corte TEXT NOT NULL,
        kilos REAL NOT NULL,
        precio REAL NOT NULL
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS proveedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT NOT NULL,
        tipo_carne TEXT NOT NULL
    )
    """)

   
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT NOT NULL,
        tipo TEXT NOT NULL,
        corte TEXT NOT NULL,
        kilos REAL NOT NULL,
        precio REAL NOT NULL,
        subtotal REAL NOT NULL,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
        estado TEXT DEFAULT 'PENDIENTE'
    )
    """)

   
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS abastecimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
        tipo TEXT NOT NULL,
        corte TEXT NOT NULL,
        kilos REAL NOT NULL,
        proveedor TEXT NOT NULL
    )
    """)

  
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos_online (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT NOT NULL,
        correo TEXT NOT NULL,
        tipo TEXT NOT NULL,
        corte TEXT NOT NULL,
        kilos REAL NOT NULL,
        estado TEXT DEFAULT 'Pendiente',
        codigo_verificacion TEXT,
        intentos INTEGER DEFAULT 0,
        reenvios INTEGER DEFAULT 0,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cortes_caja (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
        total_kilos REAL NOT NULL,
        total_dinero REAL NOT NULL,
        detalles_txt TEXT NOT NULL
)
""")
    
    # --- TRUCO PARA ACTUALIZAR TABLA EXISTENTE ---
    # Si la tabla ya existía sin la columna 'estado', la añadimos manualmente:
    try:
        cursor.execute("ALTER TABLE ventas ADD COLUMN estado TEXT DEFAULT 'PENDIENTE'")
    except sqlite3.OperationalError:
        # Si ya existe la columna, SQLite dará error, lo ignoramos
        pass

    conn.commit()
    conn.close()


def insertar_inventario_inicial():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM inventario")
    cantidad = cursor.fetchone()[0]

    if cantidad == 0:
        datos = [
            ('Res','Molida',20.0,73.69),
            ('Res','Bistec',15.0,95.07),
            ('Res','Mondongo',10.0,70.0),
            ('Res','Lengua',5.0,240.0),
            ('Res','Arrachera',15.0,165.0),
            ('Res','Tuetano',8.0,40.07),
            ('Res','T-Bone',15.0,145.60),
            ('Res','Costilla',23.0,94.0),

            ('Pollo','Pechuga',25.0,90.69),
            ('Pollo','Muslo',15.0,109.0),
            ('Pollo','Pierna',7.0,106.07),
            ('Pollo','milanesa de pollo',15.0,95.07),

            ('Cerdo','Chuleta',18.0,85.50),
            ('Cerdo','Costilla',10.0,149.08),
            ('Cerdo','Medallon',5.0,35.79),
            ('Cerdo','Milanesa de cerdo',15.0,150.50),
            ('Cerdo','Longaniza',11.0,120.00)
        ]

        cursor.executemany("""
        INSERT INTO inventario (tipo, corte, kilos, precio)
        VALUES (?, ?, ?, ?)
        """, datos)

    conn.commit()
    conn.close()


def inicializar_base():
    crear_tablas()
    insertar_inventario_inicial()