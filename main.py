# command line instruction:
#
# uvicorn main:app --reload  (local)
# uvicorn main:app --host 0.0.0.0 --port 10000  (render)
#
# main - name of python file (main.py)
# app - name of the varibale that is assigned the FastAPI object

from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import OAuth2PasswordBearer
from typing import List

import backend

server = backend.Backend()

app = FastAPI()

# Define a fake access token for demonstration purposes
fake_access_token = "a3db6c2b68c93a3fcb5bb929390347101906a86db2aa5b39"

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get the current user based on the access token
def get_current_user(token: str = Depends(oauth2_scheme)):
    if token != fake_access_token:
        raise HTTPException(status_code=401, detail="Invalid access token")
    return token

# Your existing code
@app.get("/")#, response_model=List[str])
async def your_endpoint(query: str, current_user: str = Security(get_current_user)):
    # Your existing code here
    return server.get_response(query)
