from bson import ObjectId
from pymongo.errors import WriteError

import image.main as image
from image.routers.exceptions import AlreadyExistsHTTPException
from image import config
from image.schemas.models import PipelineData, ImageData


import base64
import os
from io import BytesIO

from diffusers import StableDiffusionPipeline
import torch

global_settings = config.get_settings()
collection = global_settings.collection


async def document_id_helper(document: dict) -> dict:
    document["id"] = document.pop("_id")
    return document


async def retrieve_document(document_id: str, collection: str) -> dict:
    """

    :param document_id:
    :param collection:
    :return:
    """
    document_filter = {"_id": ObjectId(document_id)}
    if document := image.app.state.mongo_collection[collection].find_one(document_filter):
        return document_id_helper(document)
    else:
        raise ValueError(f"No document found for {document_id=} in {collection=}")


async def create_document(document: dict, collection: str) -> dict:
    """

    :param document:
    :param collection:
    :return:
    """
    try:
        document = image.app.state.mongo_collection[collection].insert_one(document)
        return await retrieve_document(document.inserted_id, collection)
    except WriteError:
        raise AlreadyExistsHTTPException(f"Document with {document.inserted_id=} already exists")


async def get_mongo_meta() -> dict:
    list_databases = await image.app.state.mongo_client.list_database_names()
    list_of_collections = {}
    for db in list_databases:
        list_of_collections[db] = await image.app.state.mongo_client[db].list_collection_names()
    mongo_meta = await image.app.state.mongo_client.server_info()
    return {"version": mongo_meta["version"], "databases": list_databases, "collections": list_of_collections}




# Set up diffusion pipeline global settings
HUGGINGFACE_TOKEN = global_settings.huggingface_api_key
model_id = "runwayml/stable-diffusion-v1-5"


async def generate_pipeline_image(pipeline_data: PipelineData)->ImageData:
    '''

    Generates a pipeline and returns a ImageData object
    '''
    device = "cpu"
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        # revision="fp16",
        # torch_dtype=torch.float16,
        use_auth_token=HUGGINGFACE_TOKEN,
        custom_pipeline="lpw_stable_diffusion",
    )

    if torch.cuda.is_available():
        device = "cuda"
        pipe = pipe.to("device")
        pipe.enable_xformers_memory_efficient_attention()

    prompt = pipeline_data.prompt
    num_inference_steps = pipeline_data.num_inference_steps
    negative_prompt = pipeline_data.negative_prompt
    image = pipe(
        prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=int(num_inference_steps),
        guidance_scale=8.5,
    ).images[0]
    image.save("testimage.png")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    imgstr = base64.b64encode(buffer.getvalue())
    image_data = ImageData(prompt=prompt,num_inference_steps=num_inference_steps, negative_prompt=negative_prompt, image_base64=imgstr)


    return image_data

