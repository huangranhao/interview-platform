"""统一错误处理中间件"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """统一错误处理中间件"""
    
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as exc:
            # 处理HTTP异常
            logger.error(f"HTTP Error: {exc.status_code} - {exc.detail}")
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": "HTTP_ERROR",
                    "message": exc.detail,
                    "status_code": exc.status_code
                }
            )
        except ValidationError as exc:
            # 处理数据验证异常
            logger.error(f"Validation Error: {exc}")
            errors = []
            for error in exc.errors():
                field = ".".join(str(x) for x in error["loc"])
                errors.append(f"{field}: {error['msg']}")
            
            return JSONResponse(
                status_code=400,
                content={
                    "error": "VALIDATION_ERROR",
                    "message": "数据验证失败",
                    "details": errors,
                    "status_code": 400
                }
            )
        except SQLAlchemyError as exc:
            # 处理数据库异常
            logger.error(f"Database Error: {exc}")
            return JSONResponse(
                status_code=500,
                content={
                    "error": "DATABASE_ERROR",
                    "message": "数据库操作失败，请稍后重试",
                    "status_code": 500
                }
            )
        except Exception as exc:
            # 处理未知异常
            logger.error(f"Unexpected Error: {exc}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={
                    "error": "INTERNAL_ERROR",
                    "message": "服务器内部错误，请稍后重试",
                    "status_code": 500
                }
            )

def register_error_handlers(app):
    """注册错误处理器"""
    # 添加中间件
    app.add_middleware(ErrorHandlerMiddleware)
    
    # 自定义异常处理器示例
    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=404,
            content={
                "error": "NOT_FOUND",
                "message": "请求的资源未找到",
                "status_code": 404
            }
        )
    
    @app.exception_handler(403)
    async def forbidden_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=403,
            content={
                "error": "FORBIDDEN",
                "message": "无权限访问此资源",
                "status_code": 403
            }
        )
    
    @app.exception_handler(401)
    async def unauthorized_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=401,
            content={
                "error": "UNAUTHORIZED",
                "message": "未授权访问，请先登录",
                "status_code": 401
            }
        )
