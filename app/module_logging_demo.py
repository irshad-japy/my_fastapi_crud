"""
'"C:\\Users\\username\\my_proj\\my_fastapi_crud\\app>uvicorn module_logging_demo:app --reload"'
"""

from fastapi import FastAPI, Depends, HTTPException
from util.fastapi_logger import get_logger

logger = get_logger('main_tmp')

app = FastAPI()

@app.get("/")
def hello_fastapi():
    logger.info('hello_fastapi')
    
    return "hello fastapi"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
