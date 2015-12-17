__author__ = 'danielpalmqvist'
from expression import Expr
import string

_i = 1
def standardize_variables(variables):
    return standardize(variables, {})

def standardize(variables,new_vars):
    global _i
    if isinstance(variables,list):
        output = []
        for v in variables:
            output.append(standardize(v,new_vars))
            _i += 1
        return output
    elif isinstance(variables,Expr):
        (new_exp,_i) = variables.standardize_variables(_i,new_vars)
        return new_exp
    elif isinstance(variables,str) and (variables[0] in string.lowercase):
        if variables in new_vars:
            return new_vars[variables]
        else:
            new_var = "x_%d" % _i
            _i += 1
            new_vars[variables] = new_var
            return new_var
    else:
        return variables

def subst(x, theta):
    if isinstance(x, list):
        output = []
        for xx in x:
            output.append(subst(xx, theta))
        return output
    elif isinstance(x,Expr):
        return Expr(x.op, subst(x.args, theta))
    elif isinstance(x,str) and (x[0] in string.uppercase):
        return x
    elif isinstance(x,str) and (x[0] in string.lowercase):
        if x in theta:
            return subst(theta[x], theta)
        else:
            return x
    else:
        return False


def unify(x,y, exttheta = {}):
    if exttheta == None:
        return None
    theta = dict(exttheta)
    if (x==y):
        return theta
    elif isinstance(x,str) and (x[0] in string.lowercase):
        return unify_var(x,y,theta)
    elif isinstance(y,str) and (y[0] in string.lowercase):
        return unify_var(y,x,theta)
    elif isinstance(x,Expr) and isinstance(y,Expr):
        return unify(x.args,y.args,unify(x.op,y.op,theta))
    elif isinstance(x,list) and isinstance(y,list):
        return unify(x[1:],y[1:],unify(x[0],y[0],theta))
    else:
        return None


def unify_var(var,x,theta):
    if var in theta:
        return unify(theta[var],x,theta)
    elif x in theta:
        return unify(var,theta[x],theta)
    elif occurs(var,x):
        return None
    else:
        theta[var]=x
        return theta

def occurs(var,x):
    if isinstance(x,Expr):
        if occurs(var,x.args):
            return True
    if isinstance(x,list):
        if var in x:
            return True
    else:
        if var==x:
            return True
    return False
