from sqlalchemy.sql._typing import _ColumnExpressionArgument

from .utils.binary_expressions import ExpressionHelper


class AlreadyExistsInDB(Exception):
    def __init__(
        self,
        whereclause: _ColumnExpressionArgument[bool],
        class_name: str,
    ):
        super().__init__(
            f"Already exists {class_name} item in database where"
            f" ({ExpressionHelper.stringify_expressions(whereclause)})"
        )


class NotFoundInDB(Exception):
    def __init__(
        self,
        whereclause: _ColumnExpressionArgument[bool],
        class_name: str,
    ):
        super().__init__(
            f"Not found {class_name} in database where"
            f" ({ExpressionHelper.stringify_expressions(whereclause)})"
        )
