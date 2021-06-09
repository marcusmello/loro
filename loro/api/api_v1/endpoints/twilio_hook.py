# from typing import Optional

from fastapi import APIRouter, Form, HTTPException, Request, Response
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse
from loro.lib.chatbot import ChatFlowHandler
from loro.core.config import settings

TWILIO_AUTH_TOKEN = settings.twilio.auth_token
router = APIRouter()


@router.post("/")
async def chat(request: Request, From: str = Form(...), Body: str = Form(...)):
    twilio_response = MessagingResponse()
    response_message = twilio_response.message()

    validator = RequestValidator(TWILIO_AUTH_TOKEN)
    twilio_incoming_form = await request.form()

    if not validator.validate(
        str(request.url),
        twilio_incoming_form,
        request.headers.get("X-Twilio-Signature", ""),
    ):
        raise HTTPException(
            status_code=400, detail="Error in Twilio Signature"
        )

    answer_sequence_cookie = request.cookies.get("answerSequence", str())

    chat_flow = ChatFlowHandler(
        from_user=From,
        form=twilio_incoming_form,
    )
    chat_flow.run(
        incoming_msg=Body, answer_sequence_string=answer_sequence_cookie
    )
    response_message.body(chat_flow.response)

    response = Response(
        content=str(twilio_response), media_type="application/xml"
    )
    response.set_cookie(
        key="answerSequence",
        httponly=True,
        value=chat_flow.answer_sequence.string_,
    )
    return response
