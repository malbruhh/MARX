#app -> controller -> service -> engine model
import sys
import collections
# Fixed 'collections' has no attribute 'Mapping' error in Python 3.10+
if sys.version_info >= (3, 10):
    import collections.abc
    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping
    collections.Iterable = collections.abc.Iterable
    collections.MutableSet = collections.abc.MutableSet
    collections.Callable = collections.abc.Callable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.controller import run_analysis
from models.request import MarketingAnalysisRequest


app = FastAPI(title="MARX Marketing Expert System")

#CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.post('/api/analyze')
async def analyze(request: MarketingAnalysisRequest):
    return run_analysis(request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)