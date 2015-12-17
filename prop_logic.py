#prop_logic.py

#Copyright (C) 2011 Ulf Daniel Palmqvist
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import string
from expression import Expr, make_expr
from variable import subst, standardize_variables, unify
special_operators = ["Not", "Eq"]


def fol_bc_or(KB,goal,theta,level=0):
    if goal.op=="Not":
        #Negation as failure
        sub_goal = goal.args[0]
        check_goal = subst(sub_goal,theta)
        if any([x!=None for x in fol_bc_or(KB,check_goal,{})]):
            yield None
        else:
            yield dict(theta)
    elif goal.op=="Eq":
        #Equality between pairs
        val0 = subst(goal.args[0],theta)
        val1 = subst(goal.args[1],theta)
        if val0!=val1:
            yield None
        else:
            yield dict(theta)
    else:
        rules = KB[goal.op]
        for rule in rules:
            srule = standardize_variables(rule)
            if srule.op=="<-":
                (lhs,rhs) = (srule.args[1:],srule.args[0])
            else:
                rhs = srule
                lhs = []
            for thetap in fol_bc_and(KB,lhs,unify(rhs,goal,theta),level+1):
                if not thetap is None:
                    yield dict(thetap)
                else:
                    yield None
    
    raise StopIteration()
                    
def fol_bc_and(KB,goals,theta,level=0):
    if theta == None:
        yield None
    elif len(goals)==0:
        yield dict(theta)
    else:
        (first,rest) = (goals[0],goals[1:])
        for thetap in fol_bc_or(KB,subst(first,theta),theta,level+1):
            for thetapp in fol_bc_and(KB,rest,thetap,level+1):
                if thetapp:
                    yield dict(thetapp)
                else:
                    yield None
    raise StopIteration()

class FolKB:
    def __init__(self):
        self.KB =  {}
            
    def tell(self,goal):
        if isinstance(goal,str):
            goal=make_expr(goal)
        if goal.op in special_operators:
            raise Exception("Predicate is reserved word '%s'" % goal.op)
        if goal.op=="<-":
            key = goal.args[0].op
        else:
            key = goal.op
        try:
            self.KB[key].append(goal)
        except:
            self.KB[key] = [goal]

    def retract(self,goal):
        if isinstance(goal,str):
            goal = make_expr(goal)
        if goal.op=="<-":
            key = goal.args[0].op
        else:
            key = goal.op
        if key in self.KB:
            if goal in self.KB[key]:
                self.KB[key].remove(goal)

    def ask(self,query):
        if isinstance(query,str):
            query = make_expr(query)
        query_vars = []
        for i in range(len(query.args)):
            x = query.args[i]
            if x=="_":
                query.args[i]="silent_var_%d"%i
            elif x[0] in string.lowercase:
                query_vars.append(x)
        if len(query_vars)==0:
            #Return True or False only. No free variables to assign.
            if any([x!=None for x in self.fol_bc_ask(query)]):
                yield True
            else:
                yield False
            raise StopIteration()
        else:
            for r in self.fol_bc_ask(query):
                if r:
                    retval = dict()
                    for c in query_vars:
                        retval[c] = r[c]
                    yield retval
            raise StopIteration()                    

    def fol_bc_ask(self, query):
        #return prove_any(self.KB, query,{})
        return fol_bc_or(self.KB,query,{})

if __name__ == "__main__":
    pass
