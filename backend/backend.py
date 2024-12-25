from flask import Flask, request, jsonify
from flask_cors import CORS
from decimal import Decimal
import psycopg2
import os

app = Flask(__name__)

# Permite solo solicitudes desde localhost
CORS(app, resources={r"/api/*": {"origins": "http://localhost"}})

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME', 'calculos'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'postgres'),
        host=os.getenv('DB_HOST', 'db'),
        port=os.getenv('DB_PORT', '5432')
    )

@app.route('/api/calcular', methods=['POST'])
def calcular():
    try:
        data = request.get_json()
        operacion = data['operacion']
        resultado = eval(operacion)
        resultado_decimal = Decimal(str(resultado))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO calculos (operacion, resultado) VALUES (%s, %s)",
            (operacion, resultado_decimal)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"resultado": float(resultado_decimal)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/historial', methods=['GET'])
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
    app.run(debug=True, host='0.0.0.0', port=5000)
