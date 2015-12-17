Functions, definitions and classes to manage propositional logic
Based on pseudo code from Artificial Intelligence a Modern Approach by Russel and Norvig

FolKB
A FolKB is a knowledge base that can contain Horn-clauses.
FolKB implements
 - tell(clause), this stores clause in the knowledge base
 - ask(clause), this asks if clause is entailed by what is already stored (telled) to the knowledge base.
 - retract(clause), removes clause from the knowledge base

If clause is a string, it tries to create an Expr by calling make_expr
FolKB can handle two types of clauses:
- Facts: F(a,b,c...)
- Rules: A & B & C & ... -> D
NOTE: Variables are lower case, constants are upper case (reverse from Prolog)
- Can handle negation as failure with the special keyword Not(...)
See examples by running this with "python unittests.py"
