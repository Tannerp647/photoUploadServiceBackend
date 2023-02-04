import boto3
import psycopg2

from typing import List
from pydantic import BaseModel

import uvicorn
from fastapi import FastAPI, UploadFile

class PhotoModel(BaseModel):
        id: int
        photo_name: str
        photo_url: str
        is_deleted: bool

app = FastAPI(debug=True)

@app.get("/status")
async def check_status():
        return "Hello World"

@app.get("/photos", response_model=List[PhotoModel])
async def get_all_photos():
        #connect to database
        conn = psycopg2.connect(
                database="exampledb", user="docker", password="docker", host="0.0.0.0"
        )
        cur = conn.cursor()
        cur.execute("select * from photo order by id desc")
        rows = cur.fetchall()

        formatted_photos = []
        for row in rows:
                formatted_photos.append(
                        PhotoModel(
                                id=row[0],
                                photo_name=row[1],
                                photo_url=row[2],
                                is_deleted=row[3]
                        )
                )
        cur.close()
        conn.close()
        return formatted_photos


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)


