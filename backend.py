from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa la extensión CORS
from decimal import Decimal
import psycopg2

app = Flask(__name__)
CORS(app)  # Habilita CORS en toda la aplicación

def get_db_connection():
    return psycopg2.connect(
        dbname="calculos",
        user="postgres",
        password="postgres",
        host="localhost"
    )

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        # Obtiene los datos JSON del frontend
        data = request.get_json()
        operacion = data['operacion']
        
        # Evalúa la operación
        resultado = eval(operacion)  # Esto devuelve un float
        resultado_decimal = Decimal(str(resultado))  # Convierte a Decimal para mayor precisión

        # Conexión a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO calculos (operacion, resultado) VALUES (%s, %s)", 
            (operacion, resultado_decimal)
        )
        conn.commit()
        cursor.close()
        conn.close()

        # Retorna el resultado al frontend
        return jsonify({"resultado": float(resultado_decimal)})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/historial', methods=['GET'])
def historial():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM calculos ORDER BY fecha DESC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        historial = [
            {
                "id": row[0],
                "operacion": row[1],
                "resultado": float(row[2]),
                "fecha": row[3].strftime('%Y-%m-%d %H:%M:%S')
            }
            for row in rows
        ]

        return jsonify(historial)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
