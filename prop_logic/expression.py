__author__ = 'danielpalmqvist'
import string

def make_expr(exp):
    #Makes the necessary Expr's from an input string. Minimal syntax check.
    exp=exp.strip()
    if "->" in exp:
        exp = exp.split("->")
        implication = exp[1]
        args = [make_expr(implication.strip())]
        clauses = exp[0].split('&')
        for c in clauses:
            args.append(make_expr(c.strip()))
        return Expr("<-",args)
    elif exp[0:3]=="Not":
        sub_exp = exp[4:(exp.rfind(")",4))]
        sub_expr = make_expr(sub_exp)
        op = "Not"
        args = [sub_expr]
        return Expr(op,args)
    else:
        exp = exp.split("(")
        op = exp[0]
        exp[1]=exp[1].rstrip(")")
        args = exp[1].split(',')
        return Expr(op,args)




class Expr:
    def __init__(self, op, args):
        self.op = op
        self.args = args

    def __repr__(self):
        if self.op=="<-":
            args = [str(a) for a in self.args[1:]]
            op = str(self.args[0])
            return " & ".join(args)+" -> "+op
        else:
            args = [str(a) for a in self.args]
            op = self.op
            return "#:"+op+"("+",".join(args)+")"

    def standardize_variables(self,i,new_vars):
        output = []
        for v in self.args:
            if isinstance(v,Expr):
                (new_v,i) = v.standardize_variables(i,new_vars)
                output.append(new_v)
            elif v not in new_vars and v[0] in string.lowercase:
                new_vars[v]="x_%d"%i
                output.append(new_vars[v])
                i += 1
            elif v[0] in string.lowercase:
                output.append(new_vars[v])
            else:
                output.append(v)
        return (Expr(self.op, output),i)

    def __eq__(self, other):
        equal =  (other.op == self.op)
        equal &= len(self.args)==len(other.args)
        if not equal:   #Safequarding the zip operation below
            return False
        return all([x==y for (x,y) in zip(self.args,other.args)]) #This compares each argument, will
                                                                 # recursively call __eq__ if there are
                                                                 # Expr's among them.
