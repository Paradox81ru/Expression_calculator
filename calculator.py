
from . import NUMBER, SIGN, PARENTHESIS, PARENTHESIS_CLOSE
from .parser_expression import ParserExpression


class Calculator:
    def run(self):
        print("Enter a mathematical expression or q to exit")

        while True:
            # sys.stdout.write("> ")
            s = input()
            if s.lower() == "q" or s.lower() == "quit":
                print("Quit")
                break
            else:
                print(self._processing_all(s))

    def _processing_all(self, string: str):
        parsed_list = ParserExpression(string).list_result
        return self._processing_parenthesis(parsed_list)[1]

    def _processing_parenthesis(self, tokens_list: list, parenthesis_num=1):
        i = 0
        while True:
            try:
                parenthesis_index = tokens_list.index((PARENTHESIS, parenthesis_num), i)
                parenthesis_close_index = tokens_list.index((PARENTHESIS_CLOSE, parenthesis_num), parenthesis_index)
                tokens_list[parenthesis_close_index] = \
                    self._processing_parenthesis(
                        tokens_list[parenthesis_index + 1:parenthesis_close_index], parenthesis_num + 1)
                for j in range(parenthesis_index, parenthesis_close_index):
                    tokens_list[j] = None
                i = parenthesis_close_index
            except ValueError:
                break
        parse_token_list = [item for item in tokens_list if item is not None]
        calc_token_list = self._processing_multiplication_signs(parse_token_list)
        result_token = self._processing_addition_signs(calc_token_list)
        # После расчтётов должен остаться список с одним кортежем
        # и надо вернуть этот кортеж.
        return result_token[0]

    def _processing_sign(self, tokens_list: list, is_addition: bool):
        """ Обработка знаков """
        i = 1
        while i < len(tokens_list):
            if tokens_list[i][0] == SIGN and (is_addition or tokens_list[i][1] in ["*", "/"]):
                result = self._calc(tokens_list[i-1][1], tokens_list[i][1], tokens_list[i+1][1])
                tokens_list[i+1] = (NUMBER, result)
                tokens_list[i] = None
                tokens_list[i-1] = None
                i += 2
            else:
                i += 2
        return [item for item in tokens_list if item is not None]

    def _processing_multiplication_signs(self, tokens_list):
        """ Обработка умножения и деления """
        return self._processing_sign(tokens_list, False)

    def _processing_addition_signs(self, tokens_list):
        """ Обработка сложения и вычитания """
        return self._processing_sign(tokens_list, True)

    def _calc(self, num1, sign, num2):
        if sign == "+":
            return num1 + num2
        elif sign == "-":
            return num1 - num2
        elif sign == "*":
            return num1 * num2
        elif sign == "/":
            return num1 / num2
        else:
            raise ValueError(f"Invalid sign {sign}")