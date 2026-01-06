from fastapi import HTTPException
from services.marketing_service import run_analysis_service
from models.request import MarketingAnalysisRequest

def run_analysis(request: MarketingAnalysisRequest):
    try:
        result = run_analysis_service(request)
    
        return{
            'status': 'success',
            'data':{
                'result': result
            }
        }
    except Exception as e:
        #Handle error
        raise HTTPException(status_code=500, detail=str(e))