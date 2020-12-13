from passlib.hash import pbkdf2_sha256
import datetime
print(pbkdf2_sha256.hash("super secret matonet password"))
print(datetime.datetime.now())
