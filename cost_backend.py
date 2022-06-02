ILLEGAL_NAME_CHARS = ",:_$\n"
UNIT_LIST = ["kg","g","lbs","oz","mL","L","item"]
T_UNIT_LIST = ["sec", "min", "hrs"]
TYPES = ["ingr","food","dish"]

class Res_Item:
	def __init__ (self, name, itype, ammount, a_unit, list_ing, list_amm, time, price):
		self.name = name
		self.itype = itype
		self.ammount = float(ammount)
		if (itype == "dish"):
			self.a_unit = "item"
		else:
			self.a_unit = a_unit
		self.price = float(price)
		if (itype == "ingr"):
			self.list_ing = []
			self.list_amm = []
			self.time = 0
		else:							# non ingredient item
			self.list_ing = list_ing
			self.list_amm = []
			self.time = float(time)
			for amm in list_amm:
				#print(amm)
				self.list_amm.append(float(amm))
	def get_attr (self):
		return {"name":self.name, "itype":self.itype, "ammount":self.ammount, "a_unit":self.a_unit, "list_ing":self.list_ing, "list_amm":self.list_amm, "time":self.time, "price":self.price}
	def savable (self):
		if (self.name == "" or self.ammount < 0):
			return False
		for char in ILLEGAL_NAME_CHARS:
			if (char in self.name):			# if illegal char in name
				return False
		if (not (self.itype in TYPES and self.a_unit in UNIT_LIST and not self.price < 0)):
			return False
		saved_items = get_saved_items(self.itype)
		names_saved = []
		for item in saved_items:
			names_saved.append(item.name)
		if self.name in names_saved:
			return False
		if (len(self.list_ing) != len(self.list_amm)):
			return False
		saved_ingr = get_saved_items("ingr")
		names = []
		for ingredient in saved_ingr:
			names.append(ingredient.name)
		for ingredient in self.list_ing:
			if (not ingredient in names):
				return False
		return True

class Ingr(Res_Item):
	def __init__ (self, name, ammount, a_unit, price):
		Res_Item.__init__(self, name, "ingr", ammount, a_unit, [], [], 0, price)
	def get_attr(self):						# name, ammount, amm_unit, cost
		attr = Res_Item.get_attr(self)
		ing_attr = {"name":attr["name"], "itype":attr["itype"], "ammount":attr["ammount"], "a_unit":attr["a_unit"], "price":attr["price"]}
		return ing_attr

class Food(Res_Item):
	def __init__ (self, name, ammount, a_unit, list_ing, list_amm, time):
		Res_Item.__init__(self, name, "food", ammount, a_unit, list_ing, list_amm, time, 0)
	def get_attr(self):						# name, itype, ammount, amm_unit, list_ing, list_amm, time
		attr = Res_Item.get_attr(self)
		attr.pop("price")
		return attr

class Dish(Food):
	def __init__ (self, name, ammount, list_ing, list_amm, time, price):
		Res_Item.__init__(self, name, "dish", ammount, "item", list_ing, list_amm, time, price)
	def get_attr(self):						# name, itype, ammount, a_unit, list_ing, list_amm, time
		attr = Res_Item.get_attr(self)
		attr.pop("a_unit")
		return attr


def save_items(items):
	for i in items:
		save_item(i)
	return
	
def save_item(item):
	name = item.name.lower().title()
	if (not item.savable()):
		print("Invalid item")
		return False
	with open(item.itype + ".txt", "r") as file:
		lines = file.readlines()
		for line in lines:
			if (line.split(",")[0] == name):
				print("Item already exists")
				return False
	with open(item.itype + ".txt", "a") as file:
		file.write(str(name) + ",")				# 0
		file.write(str(item.ammount) + ",")				# 1
		file.write(str(item.a_unit) + ",")				# 2
		if (len(item.list_ing) > 0):
			for i in range(len(item.list_ing) - 1):		# 3
				file.write(item.list_ing[i] + "_")					####
			file.write(item.list_ing[-1] + ",")
			for i in range(len(item.list_amm) - 1):		# 4
				file.write(str(item.list_amm[i]) + "_")
			file.write(str(item.list_amm[-1]) + ",")
		else:
			file.write(",,")							# (alternate 3, 4)
		file.write(str(item.time) + ",")				# 5
		file.write(str(item.price) + "\n")				# 6
	return True

def get_saved_items(itype):
	items = []
	with open(itype + ".txt", "r") as file:
		lines = file.readlines()
		for line in lines:
			attr = line.split(",")
			if (itype == "ingr"):
				items.append(Ingr(attr[0], attr[1], attr[2], attr[6]))													#name, ammount, a_unit, price
			elif (itype == "food"):
				items.append(Food(attr[0], attr[1], attr[2], attr[3].split("_"), attr[4].split("_"), attr[5]))	#name, ammount, a_unit, list_ing, list_amm, time
			elif (itype == "dish"):
				items.append(Dish(attr[0], attr[1], attr[3].split("_"), attr[4].split("_"), attr[5], attr[6]))	#name, ammount, list_ing, list_amm, time, price
			else:
				print("Invalid itype")
				return
	return items

def get_saved_item(name, itype):
	with open(itype + ".txt", "r") as file:
		lines = file.readlines()
		for line in lines:
			attr = line.split(",")
			if (attr[0] == name):
				if (itype == "ingr"):
					return Ingr(attr[0], attr[1], attr[2], attr[6])														#name, ammount, a_unit, price
				elif (itype == "food"):
					return Food(attr[0], attr[1], attr[2], attr[3].split("_"), attr[4].split("_"), attr[5])	#name, ammount, a_unit, list_ing, list_amm, time
				elif (itype == "dish"):
					return Dish(attr[0], attr[1], attr[3].split("_"), attr[4].split("_"), attr[5], attr[6])	#name, ammount, list_ing, list_amm, time, price
	
def delete_saved (name, itype):
	list_items = get_saved_items(itype)
	for i in list_items:
		if (i.name == name):
			if (itype == "ingr"):
				for j in get_foods_made_with(i.name):
					delete_saved (j.name, j.itype)
			elif (itype == "food"):
				for j in get_dishes_made_with(i.name):
					delete_saved (j.name, j.itype)
			list_items.remove(i)
			break
	with open(itype + ".txt", "w") as _:
		pass
	save_items(list_items)
	return

def get_ingredients (name, itype):
	if (itype == "ingr"):
		return []
	elif (itype == "food"):
		ingr_type = "ingr"
	else:					# itype == "dish"
		ingr_type = "food"
	item = get_saved_item(name, itype)
	list_ing = []
	for ingr in item.list_ing:
		list_ing.append(get_saved_item(ingr, ingr_type))
	return list_ing

def get_foods_made_with (ingr_name):
	foods_list = []
	for food in get_saved_items ("food"):
		if (ingr_name in food.list_ing):
			foods_list.append(food)
	return foods_list

def get_dishes_made_with (food_name):
	dish_list = []
	for dish in get_saved_items ("dish"):
		if (food_name in dish.list_ing):
			dish_list.append(dish)
	return dish_list

def get_cost(name, itype):
	cost = -1				# if these values are found then the item with that name doesn't exist
	time = -1
	if (itype == "ingr"):
		for ingr in get_saved_items (itype):
			if (ingr.name == name):
				return (ingr.price, 0)
	elif (itype == "food"):
		for item in get_saved_items (itype):
			if (item.name == name):
				cost = 0
				time = item.time
				for i in range(len(item.list_ing)):
					current_ingr = get_saved_item (item.list_ing[i], "ingr")
					cost = cost + current_ingr.price * item.list_amm[i] / current_ingr.ammount
	elif (itype == "dish"):
		for item in get_saved_items (itype):
			if (item.name == name):
				cost = 0
				time = item.time
				for i in range(len(item.list_ing)):
					current_ingr = get_saved_item (item.list_ing[i], "food")
					current_ingr_cost, sub_time = get_cost(current_ingr.name, "food")
					cost = cost + current_ingr_cost * item.list_amm[i] / current_ingr.ammount
					time = time + current_ingr.time * item.list_amm[i] / current_ingr.ammount
	return (cost, time)

def show_all():
	for itype in TYPES:
		list_saved = get_saved_items(itype)
		print("\n" + itype)
		for i in list_saved:
			print(i.get_attr())

def edit_item(new_item):
	list_items = get_saved_items(new_item.itype)
	for i in list_items:
		if (i.name == new_item.name):
			list_items.remove(i)
			list_items.append(new_item)
			break
	with open(new_item.itype + ".txt", "w") as _:
		pass
	save_items(list_items)
	return


def test_get_cost():
	items = [Ingr("Tomato","1","kg","1"), Ingr("Potato","1","kg","1"), Ingr("Pork","1","kg","10.50"), Ingr("Porkchop","2","lbs","10.60"), Ingr("Carrot","10","kg","1"), Ingr("Onion","1","kg","1"), Food("Pork Broth","1","L", ["Pork","Carrot","Onion","Tomato"], ["1","2","3","4"], "10800"), Food("Pork Chops","1","item", ["Porkchop","Onion"], ["1","2"], "1200"), Dish("Pork in Broth","1",["Pork Chops","Pork Broth"], ["1","1"], "120", "20")]
	save_items(items)
	print("Pork", get_cost("Pork", "ingr"))
	print("Carrot", get_cost("Carrot", "ingr"))
	print("Onion", get_cost("Onion", "ingr"))
	print("Tomato", get_cost("Tomato", "ingr"))
	print("Pork Broth", get_cost("Pork Broth", "food"))
	print("Pork Chops", get_cost("Pork Chops", "food"))
	print("Pork Chops in Broth", get_cost("Pork in Broth", "dish"))
	for i in items:
		delete_saved(i.name, i.itype)
	return

def test_get_saved():
	ingredients = []
	ingredients.append(Ingr("Tomato","1","kg","1"))
	ingredients.append(Ingr("Potato","1","kg","1"))
	ingredients.append(Ingr("Pork","1","kg","10.50"))
	ingredients.append(Ingr("Porkchop","2","lbs","10.60"))
	ingredients.append(Ingr("Carrot","10","kg","1"))
	ingredients.append(Ingr("Onion","1","kg","1"))
	save_items(ingredients)
	foods = []
	foods.append(Food("Pork Broth","1","L", ["Pork","Carrot","Onion","Tomato"], ["1","2","3","4"], "10800"))
	foods.append(Food("Pork Chops","1","item", ["Porkchop","Onion"], ["1","2"], "1200"))
	save_items(foods)
	save_item(Dish("Pork in Broth","1",["Pork Chops","Pork Broth"], ["1","1"], "120", "20"))
	tom = get_saved_item("Tomato", "ingr")
	por = get_saved_item("Pork Chops", "food")
	prk = get_saved_item("Pork in Broth", "dish")
	for item in [tom, por, prk]:
		print(item.get_attr())
	return

def test_create_delete():
	ingredients = []
	ingredients.append(Ingr("Pork","1","kg","10.50"))
	ingredients.append(Ingr("Porkchop","2","lbs","10.60"))
	ingredients.append(Ingr("Carrot","10","kg","1"))
	ingredients.append(Ingr("Onion","1","kg","1"))
	ingredients.append(Ingr("Tomato","1","kg","1"))
	ingredients.append(Ingr("Potato","1","kg","1"))
	save_items(ingredients)
	foods = []
	foods.append(Food("Pork Broth","1","L", ["Pork","Carrot","Onion","Tomato"], ["1","2","3","4"], "10800"))
	foods.append(Food("Pork Chops","1","item", ["Porkchop","Onion"], ["1","2"], "1200"))
	save_items(foods)
	save_item(Dish("Pork in Broth","1",["Pork Chops","Pork Broth"], ["1","1"], "120", "20"))
	show_all()
	delete_saved("Pork Chops", "food")
	show_all()
	delete_saved("Onion", "ingr")
	show_all()
	for i in ingredients:
		delete_saved(i.name, i.itype)
	return

def test_create_delete_ingr():
	ingredients = []
	ingredients.append(Ingr("Tomato","1","kg","1"))
	ingredients.append(Ingr("Potato","1","kg","1"))
	ingredients.append(Ingr("Pork","1","kg","10.50"))
	ingredients.append(Ingr("Porkchop","2","lbs","10.60"))
	ingredients.append(Ingr("Carrot","10","kg","1"))
	ingredients.append(Ingr("Onion","1","kg","1"))
	save_items(ingredients)
	print("BEFORE")
	new_ingr = get_saved_items("ingr")
	for i in new_ingr:
		print(i.get_attr())
	for i in ingredients:
		delete_saved(i.name, i.itype)
	print("AFTER")
	new_ingr = get_saved_items("ingr")
	for i in new_ingr:
		print(i.get_attr())
	return

def test_get_ingredients():
	for ingr in get_ingredients ("Tuesday Special", "dish"):
		print(ingr.name)

def test_edit_item():
	edit_item(Ingr("Tomato","1","kg","1"))

def main():
	test_edit_item()
	return


#main()





















