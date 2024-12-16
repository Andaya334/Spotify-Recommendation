from flask import Flask, jsonify, request
import snowflake.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Default route to handle the root URL
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Snowflake API! Use /get_data/<table_name> to query data."})

# Snowflake connection configuration
def get_snowflake_connection():
    return snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse='MUSIC_WAREHOUSE',
        database='SPOTIFY_SNOWFLAKE',
        schema='MUSIC_SCHEMA'
    )

@app.route('/get_data/<table_name>', methods=['GET'])
def get_data(table_name):
    allowed_tables = {'spotify_songs'}  # Define allowed tables here
    if table_name not in allowed_tables:
        return jsonify({"error": "Unauthorized access to table"}), 403
    
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        # Specify the database, schema, and table name in the query
        query = f"SELECT * FROM SPOTIFY_SNOWFLAKE.MUSIC_SCHEMA.{table_name}"
        cursor.execute(query)
        
        data = cursor.fetchall()
        
        # If data is empty, let the user know
        if not data:
            return jsonify({"message": "No data found in the table."})
        
        # Get column names and format data as JSON
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in data]
        
        return jsonify(result)
    except snowflake.connector.errors.ProgrammingError as e:
        return jsonify({"error": f"Database query error: {e}"})
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"})
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
