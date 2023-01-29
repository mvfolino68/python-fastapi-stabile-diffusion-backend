import base64
import os
from io import BytesIO
from pydantic import BaseModel
import torch
import uvicorn
import pymongo
from diffusers import StableDiffusionPipeline
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# load environment variables
load_dotenv()

# set up limiter for api calls
limiter = Limiter(key_func=get_remote_address, default_limits=["2/minutes"])

# create FastAPI app instance
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up diffusion pipeline
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_API")
model_id = "runwayml/stable-diffusion-v1-5"
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

class PipelineData(BaseModel):
    """ Data class for the pipeline """
    prompt: str
    num_inference_steps: int
    negative_prompt: str = None

def write_data_to_db(data: PipelineData, image_base64: str):
    """
    Write data to MongoDB
    """
    MONGODB_PASS = os.getenv("MONGODB_API_PASS")
    try:
        client = pymongo.MongoClient(f"mongodb+srv://mongodbuser:{MONGODB_PASS}@cluster0.6lnrsjg.mongodb.net/?retryWrites=true&w=majority")
        db = client["stable-diffussion-backend"]
        collection = db["requests-responses"]
        full_data = data.dict()
        full_data["image_base64"] = image_base64
        x = collection.insert_one(full_data)
        return x.inserted_id
    except Exception as e:
        return str(e)
    
@app.get(
    "/image",
    # Set what the media type will be in the autogenerated OpenAPI specification.
    # fastapi.tiangolo.com/advanced/additional-responses/#additional-media-types-for-the-main-response
    responses={200: {"content": {"image/png": {}}}},
    # Prevent FastAPI from adding "application/json" as an additional
    # response media type in the autogenerated OpenAPI specification.
    # https://github.com/tiangolo/fastapi/issues/3258
    response_class=Response,
)
@limiter.limit(limit_value="2/5minutes")
async def get_image(pipeline_data: PipelineData, request: Request):
    """
    Get an image from the diffusion pipeline
    """
    try:
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

        write_data_to_db(data=pipeline_data, image_base64=imgstr.decode("utf"))

        return Response(content=imgstr, media_type="image/png")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")
