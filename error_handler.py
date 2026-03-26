from flask import jsonify
import traceback

class ErrorHandlingMiddleware:
    def __init__(self, app):
        self.app = app
        app.register_error_handler(Exception, self.processexecution)
    
    def processexecution(self, e):
        errormessage = self.geterrormessage(e.__str__())
        tb = traceback.format_exc()
        print("TRACEBACK : ", tb)
        return jsonify({"errorCode" :1, "errorMessage": str(errormessage)})

    def geterrormessage(self,errorcode):
        error_codes = {
                    "101": "Please provide valid input, one or more fields are empty",
                    "102" : "Oops ! Something went wrong",
                    "103" : "Failed to connect to database",
                    "104" : "Please provide email address in valid format",
                    "105" : "Username is taken, please choose a new username to register",
                    "106" : "User with this email id already exist",
                    "107" : "Invalid credentials",
                    "108" : "No such user exist",
                    "109" : "Please choose as password that must have at least 1 lower case, 1 upper case, and one special character and no space",
                    "110" : "Invalid secret key",
                    "111" : "No such item exist in the databse",
                    "112" : "Invalid datatype for one or more columns",
                    "114" : "A product with the same name already exist, try updating instead rather than creating new",
                    "115" : "You are trying to reduce the quantity of the item more than it exist already",
                    "116" : "Either the url has some error or no image exist for this item",
                    "117" : "The url is incorrect, maybe its missing some parameters after the host" ,              
                    "118" : "Product not found",
                    "119" : "Oldpassword is not correct",   
                    "120" : "Your token has expired",
                    "121" : "Authentication token missing",
                    "122" : "Invalid Authentication token!",  
                    "123" : "Some discrepancy in the auth token, or the token have been used somewhere and thus expired kindly check"  ,    
                    "124" : "You don't have sufficient balance, consider recharging",
                    "125" : "Kindly do the payment",
                    "126" : "You need admin access for modifying these details",
                    "127" : "You have no balance",   
                    "128" : "Coupon already present with that code",
                    "129" : "Invalid coupon",
                    "130" : "You are not authorized to access this API",
                    "131" : "You are not owner of this product",      
                    "132" : "Invalid image format or missing image",  
                    "133" : "No task exist with given id"
                }
        return error_codes.get(errorcode, errorcode)
    
