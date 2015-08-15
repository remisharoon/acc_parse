from acc_parse import Account_parser
import unittest

class Account_parser_acc_parse(unittest.TestCase):
    def setUp(self):
        fpath = 'C:/lab/test/test.txt'
        self.acc_parser = Account_parser(fpath)    
    
    def tearDown(self):
        pass
    
    def test_get_decimal_from_bits(self):
        num_bits = [0,0,0,0,0,1,0,0,1]
        res = self.acc_parser.get_decimal_from_bits(num_bits)
        
        self.assertEquals(res, 1, "Should convert number bits to decimal equivalent")        
        
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(Account_parser_acc_parse))        