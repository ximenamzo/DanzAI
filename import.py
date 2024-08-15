import csv
import sqlite3


def import_data_from_csv(db_file, csv_file):
    # Conexión a la base de datos SQLite
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Leer datos desde el archivo CSV
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # Usamos DictReader para manejar fácilmente las columnas por nombre

        # Preparar la declaración de inserción SQL
        columns = ', '.join(reader.fieldnames)
        placeholders = ', '.join('?' * len(reader.fieldnames))
        sql = f'INSERT INTO posturas ({columns}) VALUES ({placeholders})'

        # Insertar cada fila de datos en la base de datos
        for row in reader:
            values = [row[column] for column in reader.fieldnames]
            cursor.execute(sql, values)

    # Guardar (commit) los cambios y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()


# Llamar a la función para cargar los datos
import_data_from_csv('danzai.db', 'data.csv')
