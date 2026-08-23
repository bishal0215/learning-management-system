class PostNotFoundException(Exception):
    def __init__(self, post_id:int):
        self.post_id = post_id
#from exceptions import PostNotFoundException
""" 
@app.exception_handler(PostNotFoundException)
async def post_not_found_handler(request: Request,exc:PostNotFoundException):
    return JSONResponse(
        status_code = 404,
        content ={"error":f"Post with ID {exc.post_id} was not found in database."}
    )
"""