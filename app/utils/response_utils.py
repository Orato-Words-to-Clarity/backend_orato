from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, List

T = TypeVar("T")

class ResponseModel(BaseModel, Generic[T]):
    status: str
    message: str
    data: Optional[T]
    status_code: int

class PaginatedResponseModel(BaseModel, Generic[T]):
    status: str
    message: str
    data: Optional[List[T]]
    pagination: Optional[dict]
    status_code: int

class ResponseHandler:
    @staticmethod
    def success(data=None, message="Operation successful", status_code=200):
        """
        Generates a standardized success response.
        """
        response = ResponseModel[
            type(data) if data is not None else None
        ](
            status="success",
            message=message,
            data=data,
            status_code=status_code
        )
        return JSONResponse(status_code=status_code, content=response.model_dump())

    @staticmethod
    def error(message="An error occurred", details=None, status_code=400):
        """
        Generates a standardized error response.
        """
        response = ResponseModel[
            type(details) if details is not None else None
        ](
            status="error",
            message=message,
            data=details,
            status_code=status_code
        )
        return JSONResponse(status_code=status_code, content=response.model_dump())

    @staticmethod
    def paginated(data: List[T], total_count: int, page: int, page_size: int, message="Data fetched successfully", status_code=200):
        """
        Generates a paginated response.
        """
        response = PaginatedResponseModel[
            type(data[0]) if data else None
        ](
            status="success",
            message=message,
            data=data,
            pagination={
                "total_count": total_count,
                "current_page": page,
                "page_size": page_size,
                "total_pages": (total_count + page_size - 1) // page_size,
            },
            status_code=status_code
        )
        return JSONResponse(status_code=status_code, content=response.model_dump())
