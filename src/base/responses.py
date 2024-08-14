from starlette import status

from src.base.base import ExceptionSchema, ExceptionValidationSchema


class ResponseSchema:
    """Response Schema."""

    @classmethod
    def get_base_statuses(cls) -> dict:
        """Get base statuses."""
        return {
            status.HTTP_401_UNAUTHORIZED: {'model': ExceptionSchema},
            status.HTTP_403_FORBIDDEN: {'model': ExceptionSchema},
            status.HTTP_405_METHOD_NOT_ALLOWED: {'model': ExceptionSchema},
            status.HTTP_422_UNPROCESSABLE_ENTITY: {'model': ExceptionValidationSchema},
        }

    def statuses(self, schema, response_status: int = status.HTTP_200_OK, statuses: list = None) -> dict:
        """Get create statuses."""
        exception_schema = {'model': ExceptionSchema}
        if statuses is None:
            statuses = []
        get_status = {response_status: {'model': schema}}
        for status_ in statuses:
            get_status[status_] = exception_schema if status_ != status.HTTP_204_NO_CONTENT else {'model': None}
        return {**get_status, **self.get_base_statuses()}

    def __call__(self, schema=None, response_status: int = status.HTTP_200_OK, statuses: list = None):
        return self.statuses(schema=schema, response_status=response_status, statuses=statuses)
