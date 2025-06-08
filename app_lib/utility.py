import re
import math, random

# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

class Email():
    @classmethod
    def check_email(cls,email):
        if(re.fullmatch(regex, email)):
            return True
        else:
            return False
        
class Otp():
    def generateOTP() :
        digits = "0123456789"
        OTP = ""
    
        for i in range(4) :
            OTP += digits[math.floor(random.random() * 10)]
        return OTP