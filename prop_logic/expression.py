""" expression
    Representation of logical expressions for py-prop-logic
"""

import string


def make_expr(exp):
    """
    Creates Expr objects from strings with minimal syntax checking
    :param exp: String
    :return: Expr that represents the expression
    """
    exp = exp.strip()
    if "->" in exp:
        exp = exp.split("->")
        implication = exp[1]
        args = [make_expr(implication.strip())]
        clauses = exp[0].split('&')
        for clause in clauses:
            args.append(make_expr(clause.strip()))
        return Expr("<-", args)
    elif exp[0:3] == "Not":
        sub_exp = exp[4:(exp.rfind(")", 4))]
        sub_expr = make_expr(sub_exp)
        operator = "Not"
        args = [sub_expr]
        return Expr(operator, args)
    else:
        exp = exp.split("(")
        operator = exp[0]
        exp[1] = exp[1].rstrip(")")
        args = exp[1].split(',')
        return Expr(operator, args)


class Expr(object):
    """ represents logical expressions """
    def __init__(self, operator, args):
        self.operator = operator
        self.args = args

    def __repr__(self):
        if self.operator == "<-":
            args = [str(a) for a in self.args[1:]]
            operator = str(self.args[0])
            return " & ".join(args) + " -> " + operator
        else:
            args = [str(a) for a in self.args]
            operator = self.operator
            return "#:"+operator+"("+",".join(args)+")"

    def standardize_variables(self, i, new_vars):
        """
        :param i:
        :param new_vars:
        :return:
        """
        output = []
        for variable in self.args:
            if isinstance(variable, Expr):
                (new_variable, i) = variable.standardize_variables(i, new_vars)
                output.append(new_variable)
            elif variable not in new_vars and variable[0] in string.lowercase:
                new_vars[variable] = "x_%d" % i
                output.append(new_vars[variable])
                i += 1
            elif variable[0] in string.lowercase:
                output.append(new_vars[variable])
            else:
                output.append(variable)
        return Expr(self.operator, output), i

    def __eq__(self, other):
        equal = (other.operator == self.operator)
        equal &= len(self.args) == len(other.args)
        if not equal:  # Safequarding the zip operation below
            return False
        # Compare each argument, will recursively call __eq__ if there are Expr's among them
        return all([x == y for (x, y) in zip(self.args, other.args)])
