""" Provides the First order logic engine FolKB along with
    the resolution methods fol_bc_or and fol_bc_and
"""
import string
from .expression import make_expr
from .variable import subst, standardize_variables, unify

SPECIAL_OPERATORS = ["Not", "Eq"]


def fol_bc_or(knowledge_dict, goal, theta, level=0):
    """ Resolves or-statements
    :param knowledge_dict: dictionary of facts
    :param goal: dictionary of question asked
    :param theta: current resolved variables
    :param level:
    :return:
    """
    if goal.operator == "Not":
        # Negation as failure
        sub_goal = goal.args[0]
        check_goal = subst(sub_goal, theta)
        if any([x is not None for x in fol_bc_or(knowledge_dict, check_goal, dict())]):
            yield None
        else:
            yield theta.copy()
    elif goal.operator == "Eq":
        # Equality between pairs
        val0 = subst(goal.args[0], theta)
        val1 = subst(goal.args[1], theta)
        if val0 != val1:
            yield None
        else:
            yield theta.copy()
    else:
        rules = knowledge_dict[goal.operator]
        for rule in rules:
            standardized_rule = standardize_variables(rule)
            if standardized_rule.operator == "<-":
                (lhs, rhs) = (standardized_rule.args[1:], standardized_rule.args[0])
            else:
                rhs = standardized_rule
                lhs = []
            for thetap in fol_bc_and(knowledge_dict, lhs, unify(rhs, goal, theta), level + 1):
                if thetap is not None:
                    yield thetap.copy()
                else:
                    yield None
    return


def fol_bc_and(knowledge_dict, goals, theta, level=0):
    """ Resolves and-statements
    :param knowledge_dict: dictionary of facts
    :param goal: dictionary of question asked
    :param theta: current resolved variables
    :param level:
    :return:
    """
    if theta is None:
        yield None
    elif len(goals) == 0:
        yield theta.copy()
    else:
        (first, rest) = (goals[0], goals[1:])
        for thetap in fol_bc_or(knowledge_dict, subst(first, theta), theta, level + 1):
            for thetapp in fol_bc_and(knowledge_dict, rest, thetap, level + 1):
                if thetapp:
                    yield thetapp.copy()
                else:
                    yield None
    return


class FolKB(object):
    """
    First order logic knowledge base class
    """
    def __init__(self):
        self.knowledge_base = {}

    def tell(self, goal):
        """
        Adds a new rule to the knowledge base
        :param goal: rule to add
        """
        if isinstance(goal, str):
            goal = make_expr(goal)
        if goal.operator in SPECIAL_OPERATORS:
            raise Exception("Predicate is reserved word '%s'" % goal.operator)
        if goal.operator == "<-":
            key = goal.args[0].operator
        else:
            key = goal.operator
        if key in self.knowledge_base:
            self.knowledge_base[key].append(goal)
        else:
            self.knowledge_base[key] = [goal]

    def retract(self, goal):
        """
        Retracts a rule from the knowledge base
        :param goal: rule to retract
        :return:
        """
        if isinstance(goal, str):
            goal = make_expr(goal)
        if goal.operator == "<-":
            key = goal.args[0].operator
        else:
            key = goal.operator
        if key in self.knowledge_base:
            if goal in self.knowledge_base[key]:
                self.knowledge_base[key].remove(goal)

    def ask(self, query):
        """
        Ask a question of the knowledge base
        :param query: is a goal to fulfill, can be string or Expr
        :return: iterator with dicts containing possible answers
        """
        if isinstance(query, str):
            query = make_expr(query)
        query_vars = []
        for i in range(len(query.args)):
            argument = query.args[i]
            if argument == "_":
                query.args[i] = "silent_var_%d" % i
            elif argument[0] in string.lowercase:
                query_vars.append(argument)
        if len(query_vars) == 0:
            # Return True or False only. No free variables to assign.
            if any([argument is not None for argument in self.fol_bc_ask(query)]):
                yield True
            else:
                yield False
        else:
            for result in self.fol_bc_ask(query):
                if result:
                    retval = dict()
                    for res in query_vars:
                        retval[res] = result[res]
                    yield retval
        return

    def fol_bc_ask(self, query):
        """
        Calls the resolution engine
        :param query:
        :return:
        """
        return fol_bc_or(self.knowledge_base, query, dict())
