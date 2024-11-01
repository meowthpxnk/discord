from sqlalchemy.sql.elements import BinaryExpression


operator_map = {
    "eq": "==",
    "ge": ">=",
    "le": "<=",
    "lt": "<",
    "gt": ">",
    "ne": "!=",
}


class ExpressionHelper:
    def __init__(self, expression: BinaryExpression[any]) -> None:
        self.expression: BinaryExpression = expression

    def __str__(self) -> str:
        column_name = self.expression.left.name
        operator_name = self.expression.operator.__name__
        operator_str = operator_map.get(operator_name, "unknown")

        value = self.expression.right.value

        return f"{column_name} {operator_str} {value}"

    @classmethod
    def stringify_expressions(
        cls, expressions: tuple[BinaryExpression]
    ) -> str:
        return ", ".join(str(cls(expr)) for expr in expressions)
