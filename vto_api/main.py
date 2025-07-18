from fastapi import FastAPI

app = FastAPI(title="VTO_API")

@app.get('/')
def hello_world():
    return {'Hello':'World'}

@app.get('/tryOn')
def try_on():
    # calls some function
    return 

app.get('/tryOff')
def try_off():
    # calls some function
    return 


# what am i expecting the inputs to be
# structured input and output
# write everything out in a pydantic class
# try_on and try_off
# input, mask, kpts, inference, segmentation