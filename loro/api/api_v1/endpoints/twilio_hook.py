#from typing import Optional

from fastapi import APIRouter, Form, HTTPException, Request, Response
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

router = APIRouter()

@router.post("/")
async def chat(request: Request, From: str = Form(...), Body: str = Form(...)):

#    validator = RequestValidator("e55746c4f1e1b2ba94125f9679cb270e")#os.environ["TWILIO_AUTH_TOKEN"])
    access_counter = int(request.cookies.get("session", 0))
    access_counter += 1

    form_ = await request.form()

#    if not validator.validate(
#        str(request.url),
#        form_,
#        request.headers.get("X-Twilio-Signature", "")
#    ):
#        raise HTTPException(status_code=400, detail="Error in Twilio Signature")

    msg_ = (
        """\nAccess_number: {}\n From: {}\n Body: {}\n form_: {}\n """.format(
            access_counter, From, Body, form_
        )
    )

    resp = MessagingResponse()
    msg = resp.message()
    msg.body(msg_)

    response = Response(content=str(resp), media_type="application/xml")
    response.set_cookie(
        key="session", expires=30, httponly=True, value=str(access_counter)
    )
    return response
