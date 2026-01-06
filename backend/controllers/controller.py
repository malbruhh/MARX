from fastapi import HTTPException
from services.marketing_service import run_analysis_service
from services.comprehensive_service import run_comprehensive_analysis
from models.request import MarketingAnalysisRequest

def run_analysis(request: MarketingAnalysisRequest):
    """
    Run comprehensive marketing analysis
    Returns detailed, multi-dimensional recommendations
    """
    try:
        # Use comprehensive analysis instead of simple service
        result = run_comprehensive_analysis(request)

        return{
            'status': 'success',
            'data': result.dict()
        }
    except Exception as e:
        #Handle error
        raise HTTPException(status_code=500, detail=str(e))