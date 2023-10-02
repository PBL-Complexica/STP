import pyotp

# OTP Generation
class OTPGeneration:
    def __init__(self, otp_code=None):
        self.otp_code = otp_code

    def generateOTP(self):
        self.totp = pyotp.TOTP('base32secret3232', interval=120)
        self.otp_code = self.totp.now()

    def verifyOTP(self, user_otp_code):
        return self.totp.verify(user_otp_code)
