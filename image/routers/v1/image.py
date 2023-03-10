from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_201_CREATED

from image import config
from image.routers.exceptions import NotFoundHTTPException
from image.schemas.models import Document, DocumentResponse, ObjectIdField
from image.services.repository import create_document, retrieve_document


global_settings = config.get_settings()
collection = global_settings.collection

router = APIRouter()

@router.post(
    "",
    status_code=HTTP_201_CREATED,
    response_description="Document created",
    response_model=DocumentResponse,
)
async def add_document(payload: Document):
    """

    :param payload:
    :return:
    """
    try:
        payload = jsonable_encoder(payload)
        return await create_document(payload, collection)
    except ValueError as exception:
        raise NotFoundHTTPException(msg=str(exception))

@router.get(
    "/{object_id}",
    response_description="Document retrieved",
    response_model=DocumentResponse,
)
async def get_document(object_id: ObjectIdField):
    """

    :param object_id:
    :return:
    """
    try:
        return await retrieve_document(object_id, collection)
    except ValueError as exception:
        raise NotFoundHTTPException(msg=str(exception))


# TODO: PUT for replace aka set PATCH for update ?
