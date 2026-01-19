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
from controllers.controller import (
    run_analysis,
    get_product_types,
    get_target_customers,
    get_primary_goals,
    get_time_horizons,
    get_content_capabilities,
    get_sales_structures,
    get_priority_kpis,
    get_all_input_options
)
from models.request import MarketingAnalysisRequest


app = FastAPI(title="MARX Marketing Expert System")

#CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"], # For development; specify ["http://127.0.0.1:5500"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# POST endpoint for analysis
@app.post('/api/analyze')
async def analyze(request: MarketingAnalysisRequest):
    return run_analysis(request)

# # GET endpoints for input options
# @app.get('/api/inputs/product-types')
# async def product_types():
#     return get_product_types()

# @app.get('/api/inputs/target-customers')
# async def target_customers():
#     return get_target_customers()

# @app.get('/api/inputs/primary-goals')
# async def primary_goals():
#     return get_primary_goals()

# @app.get('/api/inputs/time-horizons')
# async def time_horizons():
#     return get_time_horizons()

# @app.get('/api/inputs/content-capabilities')
# async def content_capabilities():
#     return get_content_capabilities()

# @app.get('/api/inputs/sales-structures')
# async def sales_structures():
#     return get_sales_structures()

# @app.get('/api/inputs/priority-kpis')
# async def priority_kpis():
#     return get_priority_kpis()

# # GET endpoint for all input options in one request
# @app.get('/api/inputs/all')
# async def all_input_options():
#     return get_all_input_options()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)