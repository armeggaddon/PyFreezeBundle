
from fastapi import APIRouter

router = APIRouter(tags=["demo"])

@router.get("/healthCheck", summary='Health Check url', description='Health Check url to check api is up and running')
def health_check():
    """
    Health check endpoint to verify API status.

    Returns "Success" if the API is running, otherwise returns the error string.

    Returns:
        str: "Success" or error message.
    """
    try:
        return "Success"
    except Exception as e:
        return str(e)
    
@router.get("/sumTwoNumbers", summary='Addition of two numbers', description='Adding two given numbers')
def add(number1: int, number2: int):
    """
    Addition of two numbers
    """
    try:
        return number1+ number2
    except Exception as e:
        return str(e)    