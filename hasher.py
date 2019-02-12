import hashlib

def hashpass(password):
	salt = "bazinga"
	hashed_password = hashlib.sha224((salt + password + salt).encode('utf-8')).hexdigest()
	return hashed_password
