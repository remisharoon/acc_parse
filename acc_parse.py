import os

class Account_parser():
    def __init__(self, fpath):
        self.fpath = fpath
        self.file_dir = os.path.dirname(fpath)
        self.num_dict = {1:[0,0,0,0,0,1,0,0,1], 2:[0,1,0,0,1,1,1,1,0], 3:[0,1,0,0,1,1,0,1,1], 4:[0,0,0,1,1,1,0,0,1], 5:[0,1,0,1,1,0,0,1,1], 6:[0,1,0,1,1,0,1,1,1], 7:[0,1,0,0,0,1,0,0,1], 8:[0,1,0,1,1,1,1,1,1], 9:[0,1,0,1,1,1,0,1,1], 0:[0,1,0,1,0,1,1,1,1]}
    def read_file(self):
        with open(self.fpath) as f:
            lines = f.readlines()
        return lines
    
    def write_output(self):
        acc_nums = self.parse_file()
        res = self.validate_num(acc_nums)        
        out_file = self.file_dir+"/report.txt"
        f = open(out_file, 'w')
        f.write("\n".join(res))
        f.close()
        
    def accno_stringify(self, acc_num):
        return "".join("{0}".format(n if n > -1 else '?') for n in acc_num)
    
    def check_alternative(self, acc_num):
        alt_acc_nums = list()
        for idx, each_digit_code in enumerate(acc_num):
            new_dig_codes = [[ (1 if (code == 0 and idx == itr) else code) for idx, code in enumerate(each_digit_code.values()[0])]  for itr in range(0,9) if ([(1 if (code == 0 and idx == itr) else code) for idx, code in enumerate(each_digit_code.values()[0])] in self.num_dict.values() and [(1 if (code == 0 and idx == itr) else code) for idx, code in enumerate(each_digit_code.values()[0])] != each_digit_code.values()[0])]
            if len(new_dig_codes) > 0:
                alt_acc_no = acc_num[:]
                for dig_code in new_dig_codes:
                    alt_acc_no[idx] = dig_code
                    alt_acc = {self.get_decimal_from_bits(alt_acc_no) : alt_acc_no}
                if self.checksum(alt_acc) == 0:
                    alt_acc_nums.append(self.accno_stringify(alt_acc))
        return alt_acc_nums
    def get_decimal_from_bits(self, num_bits):
        num = [key for key,value in self.num_dict.items() if value==num_bits]
        if len(num) != 1:
            return -1
        else:
            return num[0]
    
    def parse_file(self):
        lines = self.read_file()
        line_cnt = 0
        acc_num = list()
        num_lst = list()
        parsed_num_lst = list()
        tmp_lst = list()
        for line in lines:
            line_cnt = line_cnt +1
            if line_cnt == 4:
                line_cnt = 0
                continue
            char_cnt = 0
            chr_lst = list()
            for char in line:
                char_cnt = char_cnt +1
                chr_lst.append (1 if char in ['_','|'] else 0)
                if char_cnt == 3:
                    num_lst.append(chr_lst[:])
                    chr_lst[:] = []
                    char_cnt = 0
            acc_num.append(num_lst[:])
            num_lst[:]=[]

            if line_cnt == 3:
                for idx, acc in enumerate(acc_num[0]):
                    num_bits = acc_num[0][idx] + acc_num[1][idx] + acc_num[2][idx]
                    num = self.get_decimal_from_bits(num_bits)
                    tmp_lst.append({ num : num_bits})
                parsed_num_lst.append(tmp_lst[:])
                tmp_lst[:]=[]
                acc_num[:]=[]                
        return parsed_num_lst
    
    def checksum(self, num):
        return (sum([digit*(9-idx) for idx, digit in enumerate(num)])%11)
                
    def validate_num(self, num_lst):
        res = list()
        for acc_num in num_lst:
            status = "GOOD"
            for each_digit in acc_num:
                if -1 in each_digit.keys():
                    status = "ERR"
            num = [d.keys()[0] for d in acc_num]
            if self.checksum(num) != 0:
                alt = self.check_alternative(acc_num)
                if len(alt) > 0:
                    status = "AMB("+alt+")"
                else:
                    status = "ILL"
            acc_decimal = [self.get_decimal_from_bits(n.values()[0]) for n in acc_num] 
            res.append(self.accno_stringify(acc_decimal) + " " + status)
        return res
if __name__ == "__main__":
    fpath = 'C:/lab/test/test.txt'
    acc = Account_parser(fpath)       
    acc_nums = acc.parse_file()
    print acc_nums
    res = acc.validate_num(acc_nums)
#     acc.write_output()
