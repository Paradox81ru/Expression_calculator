from . import NUMBER, SIGN, PARENTHESIS, PARENTHESIS_CLOSE


class ParserExpression:
    def __init__(self, expression: str):
        self._parenthesis_num = 0
        self._list_result = []
        self._processing(expression)

    def _processing(self, expression: str):
        # str_nun: str = ""
        expression_length = len(expression)
        i = 0
        while i < expression_length:
            if expression[i] == " ":
                i += 1
                continue
            if expression[i].isdigit():
                str_num = ""
                while i < expression_length and expression[i].isdigit():
                    str_num += expression[i]
                    i += 1
                self._list_result.append((NUMBER, int(str_num)))
            elif expression[i] in ["+", "-", "*", "/"]:
                self._list_result.append((SIGN, expression[i]))
                i += 1
            elif expression[i] == "(":
                self._parenthesis_num += 1
                self._list_result.append((PARENTHESIS, self._parenthesis_num))
                i += 1
            elif expression[i] == ")":
                self._list_result.append((PARENTHESIS_CLOSE, self._parenthesis_num))
                self._parenthesis_num -= 1
                i += 1
            else:
                raise ValueError(f"Invalid character {expression[i]}")

    @property
    def list_result(self):
        return self._list_result
