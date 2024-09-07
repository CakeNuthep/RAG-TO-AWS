from query_model import QueryModel
from rag_app.query_rag import query_rag
from line_model import LineModel
import os


def handler(event, context):
    print(f"event = {event}")
    body_json = event
    print(f"receive body json = {body_json}")
    invoke_rag(body_json)


def invoke_rag(body_json):
    if body_json is not None:
        for event in body_json["events"]:
            if event["type"] == "message":
                if event.get("message",None) is not None:
                    query_text = event["message"]["text"]

                if event.get("source", None) is not None:
                    userId = event["source"]["userId"]
                line_request = LineModel()
                line_request.loadMessage(userId)
                print(query_text)
                new_query = QueryModel(query_text=query_text)
                query_response = query_rag(query_text)
                new_query.answer_text = query_response.response_text
                new_query.sources = query_response.sources
                new_query.is_complete = True
                new_query.put_item()
                answer_text = new_query.answer_text

                line_request.replyMessage(event["replyToken"], [{ "type": "text", "text": answer_text }])


    return "Success"


def main():
    print("Running example RAG call.")
    query_item = QueryModel(
        query_text="How long does an e-commerce system take to build?"
    )
    response = invoke_rag(query_item)
    print(f"Received: {response}")


if __name__ == "__main__":
    # For local testing.
    main()
