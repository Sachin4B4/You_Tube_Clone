import psycopg2
import os
import json
import logging
import azure.functions as func

# Define the Function App with the correct authorization level
app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


# Define the second route for the simple greeting
@app.route(route="Document_translation_azure_1510")
def Document_translation_azure_1510(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Retrieve the 'name' parameter from the query or body
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    # Return a personalized greeting if 'name' is provided
    if name:
        return func.HttpResponse(f"Hiiii, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )
#this is an example
