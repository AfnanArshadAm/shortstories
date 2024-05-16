from typing import Optional
from supabase import create_client, Client
from fastapi import FastAPI, HTTPException
from openai import OpenAI
from openai._exceptions import OpenAIError, APIStatusError
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(
    api_key = "sk-proj-lj5uJ9v92PQxK56nz9RhT3BlbkFJGzvQiX5IiCVfAw7l7CVx",
)

# Initialize Supabase client
SUPABASE_URL = "https://iztjpcdzqqnqbupuqgdo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml6dGpwY2R6cXFucWJ1cHVxZ2RvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTU2ODcyMDEsImV4cCI6MjAzMTI2MzIwMX0.Gr2G_5vWsnW3JUFJsxIDFli9w9xg4jUVnfwChXio6d4"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)



@app.post("/api/create_character", status_code=201)
async def create_character(name:str, detail: str):
    try:
        data = supabase.table("character").insert({"name":name, "detail":detail}).execute()
        logger.info(f"Character created: {data}")
        return {"data": data}
    except Exception as e:
        logger.error(f"Error creating character: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# @app.get("/api/get_character", status_code=200)
# async def get_character(character_name:str, character_id:int):
#     data = supabase.table("character").select("*").ilike("name", character_name).eq("id", character_id).execute()
#     return {"data": data}


@app.post("/api/generate_story", status_code=201)
async def create_character(character_name: Optional[str] = None, character_id: Optional[int] = None):
    try: 
        query = supabase.table("character").select("*")

        if character_name:
            query = query.ilike("name", character_name)
        if character_id:
            query = query.eq("id", character_id)

        result = query.execute()
        result = result.dict()

        if not result["data"]:
                raise HTTPException(status_code=404, detail="Character not found")
        
        char_name = result["data"][0]["name"]
        char_detail = result["data"][0]["detail"]

        chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Write a short story about {char_name} who is {char_detail}, 4 to 5 sentences is enough.",
            }
        ],
        model="gpt-3.5-turbo",
        )
        logger.info(f"Generated story for character {char_name}")

        print("response : ",chat_completion.choices[0].message)

        return {"story": chat_completion.choices[0].message}
        # return {"character": result}
        
    except HTTPException as e:
        logger.warning(f"HTTP exception occurred: {e.detail}")
        raise
    except OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise HTTPException(status_code=500, detail="OpenAI API error")
# OpenAI.