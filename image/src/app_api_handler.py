import os
import uvicorn
import boto3
import json

from fastapi import FastAPI, Request
from mangum import Mangum
from pydantic import BaseModel
from query_model import QueryModel
from rag_app.query_rag import query_rag
from line_model import LineModel

LINE_WORKER_LAMBDA_NAME = os.environ.get("LINE_WORKER_LAMBDA_NAME", None)

app = FastAPI()
handler = Mangum(app)  # Entry point for AWS Lambda.



@app.get("/")
def index():
    return {"Hello": "World"}



@app.post("/webhook_line")
async def post_webhook_line(request: Request):
    signature = request.headers.get("X-Line-Signature","")
    if(signature == ""):
        signature = request.headers.get("x-line-signature","")

    print(f"singature in api={signature}")
    # get request body as text
    body = await request.body()
    body = body.decode()
    print(f"body_json={body}")
    line_request = LineModel()
    validate = line_request.signatureValidation(signature,body)
    if(validate):
        if LINE_WORKER_LAMBDA_NAME:
            invoke_line_worker(body)

    return request.method


def invoke_line_worker(body_string):
    # Initialize the Lambda client
    lambda_client = boto3.client("lambda")

    # Get the QueryModel as a dictionary.
    payload = body_string

    # Invoke another Lambda function asynchronously
    response = lambda_client.invoke(
        FunctionName=LINE_WORKER_LAMBDA_NAME,
        InvocationType="Event",
        Payload=payload,
    )

    print(f"✅ Worker Lambda invoked: {response}")


if __name__ == "__main__":
    # Run this as a server directly.
    port = 8000
    print(f"Running the FastAPI server on port {port}.")
    uvicorn.run("app_api_handler:app", host="0.0.0.0", port=port)
