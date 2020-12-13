from passlib.hash import pbkdf2_sha256
import datetime
print(pbkdf2_sha256.hash("test"))
print(datetime.datetime.now())