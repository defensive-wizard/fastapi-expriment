from PIL import Image
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI
import uvicorn
import psycopg2
import os

DB_CONNECTION = os.environ['DB_CONNECTION']

conn = psycopg2.connect(DB_CONNECTION)

app = FastAPI()
model = SentenceTransformer('clip-ViT-B-32')


@app.get("/")
def read_root():
    query_string = "a bike in front of a red brick wall"
    text_emb = model.encode(query_string)
    cur = conn.cursor()
    cur.execute("insert into vectors(vec,type) values (%s,%s);", 
                [text_emb.tolist(),"svg"],)
    conn.commit()
    cur.close()
    
    return {"result": "done"}


# run the app
if __name__ =="__main__":
  uvicorn.run(app,port=8080,host="0.0.0.0")