import string
from expression import make_expr
from variable import subst, standardize_variables, unify

special_operators = ["Not", "Eq"]


def fol_bc_or(kb, goal, theta, level=0):
    if goal.op == "Not":
        # Negation as failure
        sub_goal = goal.args[0]
        check_goal = subst(sub_goal, theta)
        if any([x is not None for x in fol_bc_or(kb, check_goal, dict())]):
            yield None
        else:
            yield theta.copy()
    elif goal.op == "Eq":
        # Equality between pairs
        val0 = subst(goal.args[0], theta)
        val1 = subst(goal.args[1], theta)
        if val0 != val1:
            yield None
        else:
            yield theta.copy()
    else:
        rules = kb[goal.op]
        for rule in rules:
            srule = standardize_variables(rule)
            if srule.op == "<-":
                (lhs, rhs) = (srule.args[1:], srule.args[0])
            else:
                rhs = srule
                lhs = []
            for thetap in fol_bc_and(kb, lhs, unify(rhs, goal, theta), level + 1):
                if thetap is not None:
                    yield thetap.copy()
                else:
                    yield None
    return


def fol_bc_and(kb, goals, theta, level=0):
    if theta is None:
        yield None
    elif len(goals) == 0:
        yield theta.copy()
    else:
        (first, rest) = (goals[0], goals[1:])
        for thetap in fol_bc_or(kb, subst(first, theta), theta, level + 1):
            for thetapp in fol_bc_and(kb, rest, thetap, level + 1):
                if thetapp:
                    yield thetapp.copy()
                else:
                    yield None
    return


class FolKB:
    def __init__(self):
        self.KB = {}
            
    def tell(self, goal):
        if isinstance(goal, str):
            goal = make_expr(goal)
        if goal.op in special_operators:
            raise Exception("Predicate is reserved word '%s'" % goal.op)
        if goal.op == "<-":
            key = goal.args[0].op
        else:
            key = goal.op
        if key in self.KB:
            self.KB[key].append(goal)
        else:
            self.KB[key] = [goal]

    def retract(self, goal):
        if isinstance(goal, str):
            goal = make_expr(goal)
        if goal.op == "<-":
            key = goal.args[0].op
        else:
            key = goal.op
        if key in self.KB:
            if goal in self.KB[key]:
                self.KB[key].remove(goal)

    def ask(self, query):
        if isinstance(query, str):
            query = make_expr(query)
        query_vars = []
        for i in range(len(query.args)):
            x = query.args[i]
            if x == "_":
                query.args[i] = "silent_var_%d" % i
            elif x[0] in string.lowercase:
                query_vars.append(x)
        if len(query_vars) == 0:
            # Return True or False only. No free variables to assign.
            if any([x is not None for x in self.fol_bc_ask(query)]):
                yield True
            else:
                yield False
        else:
            for r in self.fol_bc_ask(query):
                if r:
                    retval = dict()
                    for c in query_vars:
                        retval[c] = r[c]
                    yield retval
        return

    def fol_bc_ask(self, query):
        return fol_bc_or(self.KB, query, dict())
