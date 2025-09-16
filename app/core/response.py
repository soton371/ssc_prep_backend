from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.encoders import jsonable_encoder


def response_success(status_code: int = status.HTTP_200_OK, data: any = None, message: str = "The request is ok", access_token: str = None, token_type: str = None):
    content = {
        "success": True,
        "message": message,
    }
    if data is not None:
        content["data"] = jsonable_encoder(data)

    if access_token is not None:
        content["access_token"] = access_token

    if token_type is not None:
        content["token_type"] = token_type
        
    return JSONResponse(
        status_code=status_code,
        content=content
    )


def response_failed(status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, message: any = "Something went wrong"):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": str(message)
        }
    )
