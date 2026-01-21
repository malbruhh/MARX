from fastapi import HTTPException
from services.comprehensive_service import run_comprehensive_analysis
from models.request import MarketingAnalysisRequest
from models.model import (
    ProductType,
    TargetCustomer,
    PrimaryGoal,
    TimeHorizon,
    ContentCapability,
    SalesStructure,
    PriorityKPI
)

async def run_analysis(request: MarketingAnalysisRequest):
    try:
        # Use comprehensive analysis instead of simple service
        result = await run_comprehensive_analysis(request)

        return{
            'status': 'success',
            'data': result.dict()
        }
    except Exception as e:
        #Handle error
        raise HTTPException(status_code=500, detail=str(e))


# def get_product_types():
#     """Get all available product types"""
#     return {
#         'status': 'success',
#         'data': [
#             {'value': item.value, 'label': _format_label(item.name)}
#             for item in ProductType
#         ]
#     }


# def get_target_customers():
#     """Get all available target customer types"""
#     return {
#         'status': 'success',
#         'data': [
#             {'value': item.value, 'label': _format_label(item.name)}
#             for item in TargetCustomer
#         ]
#     }


# def get_primary_goals():
#     """Get all available primary goals"""
#     return {
#         'status': 'success',
#         'data': [
#             {'value': item.value, 'label': _format_label(item.name)}
#             for item in PrimaryGoal
#         ]
#     }


# def get_time_horizons():
#     """Get all available time horizons"""
#     return {
#         'status': 'success',
#         'data': [
#             {'value': item.value, 'label': _format_label(item.name)}
#             for item in TimeHorizon
#         ]
#     }


# def get_content_capabilities():
#     """Get all available content capability levels"""
#     return {
#         'status': 'success',
#         'data': [
#             {'value': item.value, 'label': _format_label(item.name)}
#             for item in ContentCapability
#         ]
#     }


# def get_sales_structures():
#     """Get all available sales structures"""
#     return {
#         'status': 'success',
#         'data': [
#             {'value': item.value, 'label': _format_label(item.name)}
#             for item in SalesStructure
#         ]
#     }


# def get_priority_kpis():
#     """Get all available priority KPIs"""
#     return {
#         'status': 'success',
#         'data': [
#             {'value': item.value, 'label': _format_label(item.name)}
#             for item in PriorityKPI
#         ]
#     }


# def get_all_input_options():
#     """Get all input options in a single request"""
#     return {
#         'status': 'success',
#         'data': {
#             'product_types': [
#                 {'value': item.value, 'label': _format_label(item.name)}
#                 for item in ProductType
#             ],
#             'target_customers': [
#                 {'value': item.value, 'label': _format_label(item.name)}
#                 for item in TargetCustomer
#             ],
#             'primary_goals': [
#                 {'value': item.value, 'label': _format_label(item.name)}
#                 for item in PrimaryGoal
#             ],
#             'time_horizons': [
#                 {'value': item.value, 'label': _format_label(item.name)}
#                 for item in TimeHorizon
#             ],
#             'content_capabilities': [
#                 {'value': item.value, 'label': _format_label(item.name)}
#                 for item in ContentCapability
#             ],
#             'sales_structures': [
#                 {'value': item.value, 'label': _format_label(item.name)}
#                 for item in SalesStructure
#             ],
#             'priority_kpis': [
#                 {'value': item.value, 'label': _format_label(item.name)}
#                 for item in PriorityKPI
#             ]
#         }
#     }


# def _format_label(name: str) -> str:
#     """Format enum name to readable label"""
#     # Replace underscores with spaces and title case
#     return name.replace('_', ' ').title()