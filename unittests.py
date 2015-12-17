import unittest
from prop_logic import FolKB
from expression import make_expr, Expr

class TestWumpus(unittest.TestCase):
    def test_cats(self):
        print "==================================================================================="
        print "Cats"
        print "==================================================================================="
        myKB = FolKB()
        to_tell = []
        to_tell.append("Likes(Adam,Cats)")  #Adam likes Cats
        to_tell.append("Likes(x,x)")        #Everyone likes themselves
        to_tell.append("Likes(Jonas,x)")    #Jonas likes everyone

        to_ask = []
        to_ask.append("Likes(x,Cats)")      #Who likes cats?
        answers = []
        answers.append([{'x': 'Adam'}, {'x': 'Cats'}, {'x': 'Jonas'}])
        for fact in to_tell:
            print "telling: %s" % fact
            myKB.tell(fact)

        for (question, answer) in zip(to_ask, answers):
            print "Asking: %s" % question
            results = [r for r in myKB.ask(question)]
            self.assertEquals(results, answer)

    def test_weapon_sales(self):
        print "==================================================================================="
        print "Weapon sales"
        print "==================================================================================="
        myKB = FolKB()

        to_tell = []
        to_tell.append("American(x) & Weapon(y) & Hostile(z) & Sells(x,y,z) -> Criminal(x)")
        to_tell.append("NewYorker(x) -> American(x)")
        to_tell.append("American(West)")
        to_tell.append("Weapon(Missile)")
        to_tell.append("Hostile(Nono)")
        to_tell.append("Sells(West,Missile,Nono)")
        to_tell.append("Sells(East,Missile,Nono)")
        to_tell.append("NewYorker(East)")
        to_tell.append("American(North)")

        for fact in to_tell:
            print "telling: %s" % fact
            myKB.tell(make_expr(fact))

        to_ask = []
        to_ask.append("Criminal(West)") #Is West a criminal?
        to_ask.append("Criminal(East)") #Is East a criminal?
        to_ask.append("Criminal(North)")#Is North a criminal? (He is not, Iranically)
        to_ask.append("Criminal(x)") #Get the whole list of criminals

        answers = []
        answers.append([True])
        answers.append([True])
        answers.append([False])
        answers.append([{'x': 'East'}, {'x': 'West'}])

        for (question, answer) in zip(to_ask, answers):
            print "Asking %s" % question
            result = [r for r in myKB.ask(make_expr(question))]
            self.assertEquals(answer, result)

        print "Retracting NewYorker(East)"
        myKB.retract("NewYorker(East)")
        print "Asking Criminal(x)"
        result = [r for r in myKB.ask("Criminal(x)")]
        self.assertEquals([{'x': 'West'}], result)

    def test_family_matters(self):
        #This contains some more complicated relations
        print "==================================================================================="
        print "Family matters"
        print "==================================================================================="
        to_tell = []
        to_tell.append("Parent(Pam,Bob)")
        to_tell.append("Parent(Tom,Bob)")
        to_tell.append("Parent(Tom,Liz)")
        to_tell.append("Parent(Bob,Ann)")
        to_tell.append("Parent(Bob,Pat)")
        to_tell.append("Parent(Pat,Jim)")
        to_tell.append("Not(Male(x)) -> Female(x)") #Anything that is not Male is Female through negation as failure
        to_tell.append("Male(Tom)")
        to_tell.append("Male(Bob)")
        to_tell.append("Male(Jim)")
        to_tell.append("Parent(x,y) -> Offspring(y,x)")
        to_tell.append("Parent(x,y) & Female(x) -> Mother(x,y)")
        to_tell.append("Parent(y,x) & Parent(z,y) -> Grandparent(z,x)")
        to_tell.append("Parent(x,y) & Male(x) -> Father(x,y)")
        to_tell.append("Offspring(x,y) -> Descendant(x,y)")
        to_tell.append("Offspring(z,y) & Descendant(x,z)-> Descendant(x,y)")
        to_tell.append("Parent(z,x) & Parent(z,y) & Female(x) & Not(Eq(x,y)) -> Sister(x,y)")
        to_tell.append("Father(x,y) & Father(y,z) -> PaternalGrandfather(x,z)")
        to_ask = []
        to_ask.append("Parent(x,Bob)")
        to_ask.append("Parent(Pam,Bob)")
        to_ask.append("Parent(x,y)")
        to_ask.append("Mother(x,y)")
        to_ask.append("Offspring(y,x)")
        to_ask.append("Grandparent(x,y)")
        to_ask.append("Father(x,Bob)")
        to_ask.append("Father(Bob,x)")
        to_ask.append("Descendant(x,Pam)")
        to_ask.append("Sister(x,y)")
        to_ask.append("PaternalGrandfather(x,_)")
        to_ask.append("Female(Jim)")
        to_ask.append("Female(Pam)")
        answers = []
        answers.append([{'x': 'Pam'}, {'x': 'Tom'}])
        answers.append([True])
        answers.append([{'y': 'Bob', 'x': 'Pam'},
            {'y': 'Bob', 'x': 'Tom'},
            {'y': 'Liz', 'x': 'Tom'},
            {'y': 'Ann', 'x': 'Bob'},
            {'y': 'Pat', 'x': 'Bob'},
            {'y': 'Jim', 'x': 'Pat'}])
        answers.append([{'y': 'Bob', 'x': 'Pam'},
            {'y': 'Jim', 'x': 'Pat'}])
        answers.append([{'y': 'Bob', 'x': 'Pam'},
            {'y': 'Bob', 'x': 'Tom'},
            {'y': 'Liz', 'x': 'Tom'},
            {'y': 'Ann', 'x': 'Bob'},
            {'y': 'Pat', 'x': 'Bob'},
            {'y': 'Jim', 'x': 'Pat'}])
        answers.append([{'y': 'Ann', 'x': 'Pam'},
            {'y': 'Ann', 'x': 'Tom'},
            {'y': 'Pat', 'x': 'Pam'},
            {'y': 'Pat', 'x': 'Tom'},
            {'y': 'Jim', 'x': 'Bob'}])
        answers.append([{'x': 'Tom'}])
        answers.append([{'x': 'Ann'},
            {'x': 'Pat'}])
        answers.append([{'x': 'Bob'},
            {'x': 'Ann'},
            {'x': 'Pat'},
            {'x': 'Jim'}])
        answers.append([{'y': 'Bob', 'x': 'Liz'},
            {'y': 'Pat', 'x': 'Ann'},
            {'y': 'Ann', 'x': 'Pat'}])
        answers.append([{'x': 'Tom'},
            {'x': 'Tom'}])

        answers.append([False])
        answers.append([True])

        myKB = FolKB()
        for fact in to_tell:
            print "telling: %s" % fact
            myKB.tell(make_expr(fact))
        for (question, answer) in zip(to_ask, answers):
            print "asking: %s" % question
            result = [r for r in myKB.ask(make_expr(question))]
            self.assertEqual(answer, result)

    def test_wumpus(self):
        print "==================================================================================="
        print "Wumpus!"
        print "==================================================================================="

        myKB = FolKB()
        physical_rules = []
        physical_rules.append("Neighbor(x,y) & Wumpus(y) -> Stench(x)")
        physical_rules.append("Visited(x) -> Safe(x)")
        physical_rules.append("Neighbor(x,y) & Stench(y) & Not(Visited(x)) -> Unsafe(x)")
        print "Telling some physics rules"
        for r in physical_rules:
            print "telling: %s" % r
            myKB.tell(r)
        wumpus  = "Wumpus(B13)"
        n1      = "Neighbor(B12,B11)"
        n2      = "Neighbor(B12,B13)"
        v1      = "Visited(B11)"
        v2      = "Visited(B12)"
        q1      = "Unsafe(B11)"
        q2      = "Stench(B12)"
        q3      = "Unsafe(x)"
        q4      = "Safe(x)"
        a1      = [False]
        a2      = [True]
        a3      = [{'x': 'B22'},
                    {'x': 'B13'},
                    {'x': 'B13'},
                    {'x': 'B24'},
                    {'x': 'B15'},
                    {'x': 'B13'},
                    {'x': 'B22'},
                    {'x': 'B33'},
                    {'x': 'B24'}]
        a4      = [{'x': 'B11'},
                    {'x': 'B12'}]

        neighbor_comm = Expr("<-",[Expr("Neighbor",["x","y"]),Expr("Neighbor",["y","x"])])
        to_tell = [v1, v2, wumpus]
        to_ask  = [q1, q2, q3, q4]
        answers = [a1, a2, a3, a4]
        ymax=5
        xmax=5
        for fact in to_tell:
            print "Telling: %s" % fact
            myKB.tell(fact)
        for x in range(1,xmax+1):
            for y in range(1,ymax+1):
                if x>1:
                    neighbor="Neighbor(B%d%d,B%d%d)"%((x-1),y,x,y)
                    print "Telling: %s" %neighbor
                    myKB.tell(neighbor)
                if y>1:
                    neighbor="Neighbor(B%d%d,B%d%d)"%(x,(y-1),x,y)
                    print "Telling: %s"% neighbor
                    myKB.tell(neighbor)
                if x<xmax:
                    neighbor="Neighbor(B%d%d,B%d%d)"%((x+1),y,x,y)
                    print "Telling: %s" %neighbor
                    myKB.tell(neighbor)
                if y<ymax:
                    neighbor="Neighbor(B%d%d,B%d%d)"%(x,(y+1),x,y)
                    print "Telling: %s"% neighbor
                    myKB.tell(neighbor)
        for (question, answer) in zip(to_ask, answers):
            print "Asking  %s?"%question
            result = [r for r in myKB.ask(question)]
            self.assertEqual(result, answer)

if __name__ == '__main__':
    unittest.main()
