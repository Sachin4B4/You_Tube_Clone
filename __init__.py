import psycopg2
import os
import json
import logging
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Extract Admin_id from the request parameters
        admin_id = req.params.get('admin_id')
        
        if not admin_id:
            return func.HttpResponse(
                "Please provide an 'admin_id'.",
                status_code=400
            )
        
        # Get connection details from environment variables
        host = os.getenv('DB_HOST')
        database = os.getenv('DB_NAME')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        port_str = os.getenv('DB_PORT')

        # Ensure all variables are set
        if not all([host, database, user, password, port_str]):
            return func.HttpResponse(
                "Database connection details are not set properly.",
                status_code=500
            )
        
        # Convert port to integer
        try:
            port = int(port_str)
        except (ValueError, TypeError) as e:
            logging.error(f"Port conversion error: {e}")
            return func.HttpResponse(
                "Invalid port number.",
                status_code=500
            )

        # Connect to PostgreSQL
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        cursor = connection.cursor()
        
        # Query the database for the settings associated with the given Admin_id
        query = """
        SELECT key, text_translation_endpoint, document_translation_endpoint, region, storage_connection_string
        FROM settings
        WHERE admin_id = %s;
        """
        
        cursor.execute(query, (admin_id,))
        result = cursor.fetchone()
        
        if not result:
            return func.HttpResponse(
                f"No settings found for Admin_id {admin_id}.",
                status_code=404
            )
        
        # Prepare the response
        settings = {
            'key': result[0],
            'text_translation_endpoint': result[1],
            'document_translation_endpoint': result[2],
            'region': result[3],
            'storage_connection_string': result[4]
        }
        
        # Close the connection
        cursor.close()
        connection.close()
        
        return func.HttpResponse(
            json.dumps(settings),
            mimetype="application/json",
            status_code=200
        )
    
    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(
            "An error occurred while retrieving the settings.",
            status_code=500
        )
