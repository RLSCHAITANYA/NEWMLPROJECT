import sys
from src.logger import logging
# Defining a function to generate an error message with the details of the error.
def error_message_detail(error,error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()   #exc_info gives execution info and gives 3imp info like which file,lineno
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message="Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
     file_name,exc_tb.tb_lineno,str(error))

    return error_message

# Defining a custom exception class that inherits from the built-in Exception class.
 
class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):  # Defining the __init__ method to initialize the error message and error details.
        super().__init__(error_message)   # Calling the __init__ method of the parent class to initialize the exception object.
        self.error_message=error_message_detail(error_message,error_detail=error_detail)  # Generating the error message with the details of the error using the error_message_detail function.
    
    def __str__(self):
        return self.error_message



# 1.here we create a class  custom exception and function called error_messgae_detail
#  that generates an error message with the details of an exception.
# 2.the error_message_detail takes two arguments error (which is the error raised) and 
# error_detail(provides the info about error form sys modeule)
# 3.the function also extracts the filename and line no
# 4.The CustomException class extends the built-in Exception class and overrides its __init__ method.
# 5.The __init__ method calls the __init__ method of the parent class to initialize the exception and then sets its
#  own error_message attribute by calling the error_message_detail function with the error message and 
#  sys module reference as arguments.
#6.When an instance of CustomException is raised, 
# it will contain the error message with details about where the error occurred