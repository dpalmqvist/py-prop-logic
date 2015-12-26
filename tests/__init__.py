import unittest
import prop_logic_test

def prop_logic_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(prop_logic_test)
    return suite