from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_201_CREATED

from image import config
from image.routers.exceptions import NotFoundHTTPException
from image.schemas.models import PipelineData, ImageData
from image.services.repository import create_document, generate_pipeline_image


global_settings = config.get_settings()
collection = global_settings.collection

router = APIRouter()

@router.post(
    "",
    # Set what the media type will be in the autogenerated OpenAPI specification.
    # fastapi.tiangolo.com/advanced/additional-responses/#additional-media-types-for-the-main-response
    # responses={200: {"content": {"image/png": {}}}},
    # Prevent FastAPI from adding "application/json" as an additional
    # response media type in the autogenerated OpenAPI specification.
    # https://github.com/tiangolo/fastapi/issues/3258
    # 
    status_code=HTTP_201_CREATED,
    response_description="Image generated",
    response_model=ImageData
)
async def generate(pipeline_data: PipelineData):
    """
    Accepts a PipelineData object and generates the corresponding ImageData object.
    Save the image data to the specified collection in MongoDB.
    Returns the corresponding ImageData object
    """

    try:
        generated_image_data = await generate_pipeline_image(pipeline_data)
        #generated_image_data = {"prompt": "Kathmandu", "num_inference_steps": 5, "image_base64": "London"}
        

    except Exception as exception:
        raise NotFoundHTTPException(msg=str(exception))
    try:
        payload = jsonable_encoder(generated_image_data)
        document_data = await create_document(payload, collection)

        return generated_image_data
    except Exception as exception:
         raise NotFoundHTTPException(msg=str(exception))
