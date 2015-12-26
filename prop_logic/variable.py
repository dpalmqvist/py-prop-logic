""" variable.py
    Representation of variables for py-prop-logic
    Standardization and unification
"""

import string
from .expression import Expr


MAX_VARS = 1


def standardize_variables(variables):
    """
    Interface for standardize
    :param variables: old dict of variables
    :return: new dict of variables
    """
    return standardize(variables, {})


def standardize(variables, new_vars):
    """
    Creates unique standardized variable names for internal use
    :param variables: old dict of variables
    :param new_vars: new dict of standardized variable names
    :return:
    """
    global MAX_VARS
    if isinstance(variables, list):
        output = []
        for var in variables:
            output.append(standardize(var, new_vars))
            MAX_VARS += 1
        return output
    elif isinstance(variables, Expr):
        (new_exp, MAX_VARS) = variables.standardize_variables(MAX_VARS, new_vars)
        return new_exp
    elif isinstance(variables, str) and (variables[0] in string.lowercase):
        if variables in new_vars:
            return new_vars[variables]
        else:
            new_var = "x_%d" % MAX_VARS
            MAX_VARS += 1
            new_vars[variables] = new_var
            return new_var
    else:
        return variables


def subst(variables, theta):
    """
    Substitutes in the variable assignments for the variables
    :param variables:
    :param theta:
    :return:
    """
    if isinstance(variables, list):
        output = []
        for var in variables:
            output.append(subst(var, theta))
        return output
    elif isinstance(variables, Expr):
        return Expr(variables.operator, subst(variables.args, theta))
    elif isinstance(variables, str) and (variables[0] in string.uppercase):
        return variables
    elif isinstance(variables, str) and (variables[0] in string.lowercase):
        if variables in theta:
            return subst(theta[variables], theta)
        else:
            return variables
    else:
        return False


def unify(var1, var2, theta):
    """
    Calls unify var based on types
    :param var1: variable
    :param var2: variable
    :param exttheta: dictionary of variables
    :return:
    """
    if theta is None:
        return None
    if var1 == var2:
        return theta
    elif isinstance(var1, str) and (var1[0] in string.lowercase):
        return unify_var(var1, var2, theta)
    elif isinstance(var2, str) and (var2[0] in string.lowercase):
        return unify_var(var2, var1, theta)
    elif isinstance(var1, Expr) and isinstance(var2, Expr):
        return unify(var1.args, var2.args, unify(var1.operator, var2.operator, theta.copy()))
    elif isinstance(var1, list) and isinstance(var2, list):
        return unify(var1[1:], var2[1:], unify(var1[0], var2[0], theta.copy()))
    else:
        return None


def unify_var(var1, var2, theta):
    """
    Unifies var and x to the same entity in theta
    :param var1: variable
    :param var2: variable
    :param theta: dict of variables
    :return:
    """
    if var1 in theta:
        return unify(theta[var1], var2, theta.copy())
    elif var2 in theta:
        return unify(var1, theta[var2], theta.copy())
    elif occurs(var1, var2):
        return None
    else:
        theta[var1] = var2
        return theta


def occurs(var1, exp):
    """
    Checks if the variable occurs in the expression
    :param var1: variable to check
    :param exp: expression, list or string to check
    :return:
    """
    if (isinstance(exp, Expr) and occurs(var1, exp.args)) or \
        (isinstance(exp, list) and var1 in exp) or \
            (var1 == exp):
        return True
    return False
