import os
import csv

USER_INFO_PATH = "user_info.csv"


class User():

	def __init__(self):
		self._load_users()
		pass

	def _load_users(self):
		file = open(USER_INFO_PATH, 'r')
		file = csv.reader(file)
		self.ids = {}
		self.user_names = {}
		for line in file:
			self.ids[line[0]] = line[1]
			self.user_names[line[1]] = line[0]

	def add_user_info(self, id, user_name):
		with open(USER_INFO_PATH, 'a') as f:
			f.write("%s,%s\n" %(id, user_name))

	def sign_up(self, id, user_name):
		message = ""
		if id in self.ids:
			message = f"{id} is already registered with User Name:{self.ids[id]}"
		elif user_name in self.user_names:
			message = f"{user_name} username is already taken, pick another :)"
		else:
			self.add_user_info(id, user_name)
			self.ids[str(id)] = str(user_name)
			self.user_names[str(user_name)] = str(id)
			message = f"username: {user_name} with id: {id} added successfully"
		return message


user = User()


def signup(query):
	query = query.split()
	id = query[1]
	user_name = query[2]
	r = user.sign_up(id, user_name)
	return r


if __name__ == "__main__":
	r = signup('12345 ben')
	print(r)