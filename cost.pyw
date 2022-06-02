from os import listdir as listdir
from tkinter import *
from cost_backend import *

REQ_FILES = ["dish.txt","food.txt","ingr.txt"]
TASKS = ["Add", "View", "Remove", "Edit"]
ITEM_TYPES = ["Ingredient", "Food", "Dish"]

def str_two_dec(my_str):
    num = str(my_str)
    if ("." in num):
        if (num.index(".")+3 > len(num)-1):
            return num + "0" * (num.index(".")+3 - len(num)-1)
        else:
            return num[:num.index(".")+3]
    else:
        return num + ".00"

def get_time_str(my_time):
    time = int(my_time)
    return_str = str(time // 3600) + " hours"
    time = time % 3600
    return_str = return_str + ", " + str(time // 60) + " minutes"
    time = time % 60
    return return_str + ", " + str(time) + " seconds"

def get_time_and_unit(my_time):
	time = int(my_time)
	if (time < 120):
		return (my_time, "sec")
	elif (time < 7200):
		return (str_two_dec(time / 60), "min")
	else:
		return (str_two_dec(time / 3600), "hrs")

def donothing (var=''):
	pass

def get_ing_amm(saved_items, ammount_strs):
	list_ing = []
	list_amm = []
	for i in range(len(saved_items)):
		if (float(ammount_strs[i].get()) > 0):
			list_ing.append(saved_items[i].name)
			list_amm.append(ammount_strs[i].get())
	return (list_ing, list_amm)

def add_gui_button(name, itype, ammount, a_unit="", list_ing=[], list_amm=[], time=0, t_unit="", price=0):
	if (t_unit == "min"):
		time = float(time) * 60
	elif (t_unit == "hrs"):
		time = float(time) * 60 * 60
	if (itype == "Ingredient"):
		save_item(Ingr(name, ammount, a_unit, price))
	elif (itype == "Food"):
		save_item(Food(name, ammount, a_unit, list_ing, list_amm, time))
	elif (itype == "Dish"):
		save_item(Dish(name, ammount, list_ing, list_amm, time, price))
	main.gui_main()

def edit_my_item(name, itype, ammount, a_unit="", list_ing=[], list_amm=[], time=0, t_unit="", price=0):
	if (itype == "ingr"):
		edit_item(Ingr(name, ammount, a_unit, price))
	elif (itype == "food"):
		list_amm_str = []
		list_ing_str = []
		for i in range(len(list_amm)):
			if (float(list_amm[i].get()) > 0):
				list_amm_str.append(list_amm[i].get())
				list_ing_str.append(list_ing[i])
		if (t_unit == "min"):
			time = str(float(time) * 60)
		elif (t_unit == "hrs"):
			time = str(float(time) * 3600)
		edit_item(Food(name, ammount, a_unit, list_ing_str, list_amm_str, time))
	else: #itype == "dish"
		list_amm_str = []
		list_ing_str = []
		for i in range(len(list_amm)):
			if (float(list_amm[i].get()) > 0):
				list_amm_str.append(list_amm[i].get())
				list_ing_str.append(list_ing[i])
		if (t_unit == "min"):
			time = str(float(time) * 60)
		elif (t_unit == "hrs"):
			time = str(float(time) * 3600)
		edit_item(Dish(name, ammount, list_ing_str, list_amm_str, time, price))
	main.gui_main()
	
def enter_button_press(task, itype):
	if (task == "Add"):
		main.gui_add(itype)
	if (task == "View"):
		main.gui_view(itype)
	if (task == "Remove"):
		main.gui_remove(itype)
	if (task == "Edit"):
		main.gui_edit(itype)
	return

def delete_item(item):
	delete_saved(item.name, item.itype)
	main.gui_main()

class interface (Tk):
	def __init__(self, name='Interface', size=None):
		super(interface, self).__init__()
		if size:
			self.geometry(size)
		self.title(name)
		self.frame=Frame(self)
		self.frame.pack()
	def gui_print(self, text='', command=donothing):
		self.frame.destroy()
		self.frame=Frame(self)
		self.frame.pack()
		Label(self.frame, text=text).pack()
		Button(self.frame, text='Ok', command=self.quit).pack()
	def gui_main(self, text="Main Window", command=donothing):
		self.title(text)
		self.frame.destroy()
		self.frame=Frame(self)
		self.frame.pack()
		
		menu_1_selection=StringVar(self)
		menu_1_selection.set(TASKS[1])
		menu1 = OptionMenu(self.frame, menu_1_selection, *TASKS).grid(row=1,column=0)
		menu_2_selection=StringVar(self)
		menu_2_selection.set(ITEM_TYPES[0])
		menu2 = OptionMenu(self.frame, menu_2_selection, *ITEM_TYPES).grid(row=1,column=1)
				
		Button(
			self.frame,
			text='Enter',
			command=lambda: command(
				enter_button_press(menu_1_selection.get(), menu_2_selection.get())
			)).grid(row=2,column=0)
	def gui_add(self, itype, text="Add Window", command=donothing):
		self.title(text)
		self.frame.destroy()
		self.frame=Frame(self)
		self.frame.pack()
		
		Label(self.frame, text="Name").grid(row=0,column=0)
		name_str=StringVar(self)
		Entry(self.frame, textvariable=name_str).grid(row=0,column=1)
		
		Label(self.frame, text="Ammount").grid(row=1,column=0)
		ammount_str=StringVar(self)
		ammount_str.set("0")
		Entry(self.frame, textvariable=ammount_str).grid(row=1,column=1)
		if (itype == "Ingredient"):
			a_unit_str=StringVar(self)
			a_unit_str.set(UNIT_LIST[0])
			OptionMenu(self.frame, a_unit_str, *UNIT_LIST).grid(row=1,column=2)
			
			Label(self.frame, text="Price ($)").grid(row=2,column=0)
			price_str=StringVar(self)
			price_str.set("1")
			Entry(self.frame, textvariable=price_str).grid(row=2,column=1)
			
			Button(
				self.frame,
				text='Enter',
				command=lambda: command(
					add_gui_button(name_str.get(), itype, ammount_str.get(), a_unit=a_unit_str.get(), price=price_str.get())
				)).grid(row=3,column=0)
		elif (itype == "Food"):
			a_unit_str=StringVar(self)
			a_unit_str.set(UNIT_LIST[0])
			OptionMenu(self.frame, a_unit_str, *UNIT_LIST).grid(row=1,column=2)
			
			Label(self.frame, text="Time").grid(row=2,column=0)
			time_str=StringVar(self)
			Entry(self.frame, textvariable=time_str).grid(row=2,column=1)
			t_unit_str=StringVar(self)
			t_unit_str.set(T_UNIT_LIST[0])
			OptionMenu(self.frame, t_unit_str, *T_UNIT_LIST).grid(row=2,column=2)
			
			Button(
				self.frame,
				text='Add Food Ingredients',
				command=lambda: command(
					main.gui_add_ingr_select({'itype':itype, 'name':name_str.get(), 'ammount':ammount_str.get(), 'a_unit':a_unit_str.get(), 'time':time_str.get(), 't_unit':t_unit_str.get(), 'price':"0"})
				)).grid(row=3,column=0)
			
		elif (itype == "Dish"):
			Label(self.frame, text="Time").grid(row=2,column=0)
			time_str=StringVar(self)
			Entry(self.frame, textvariable=time_str).grid(row=2,column=1)
			t_unit_str=StringVar(self)
			t_unit_str.set(T_UNIT_LIST[0])
			OptionMenu(self.frame, t_unit_str, *T_UNIT_LIST).grid(row=2,column=2)
			
			Label(self.frame, text="Price").grid(row=3,column=0)
			price_str=StringVar(self)
			Entry(self.frame, textvariable=price_str).grid(row=3,column=1)
			
			Button(
				self.frame,
				text='Add Food Ingredients',
				command=lambda: command(
					main.gui_add_ingr_select({'itype':itype, 'name':name_str.get(), 'ammount':ammount_str.get(), 'a_unit':"item", 'time':time_str.get(), 't_unit':t_unit_str.get(), 'price':price_str.get()})
				)).grid(row=4,column=0)		
	def gui_add_ingr_select (self, param={}, text="Ingredient Selection", command=donothing):
		self.title(text)
		self.frame.destroy()
		self.frame=Frame(self)
		self.frame.pack()
		if (param['itype'] == "Food"):
			saved_items = get_saved_items("ingr")
		elif (param['itype'] == "Dish"):
			saved_items = get_saved_items("food")
		ammount_strs = [None] * len(saved_items)
		for i in range(len(saved_items)):
			Label(self.frame, text=saved_items[i].name).grid(row=i,column=0)
			ammount_strs[i]=StringVar(self)
			ammount_strs[i].set("0")
			Entry(self.frame, textvariable=ammount_strs[i]).grid(row=i,column=1)
			Label(self.frame, text=saved_items[i].a_unit).grid(row=i,column=2)
		
		Button(
			self.frame,
			text='Done',
			command=lambda: command(
				add_gui_button(param['name'], param['itype'], param['ammount'], param['a_unit'], *get_ing_amm(saved_items, ammount_strs), param['time'], param['t_unit'], param['price'])
			)).grid(row=len(saved_items),column=0)
	def gui_view_item(self, itype, item, text="View Item", command=donothing):
		self.title(text)
		self.frame.destroy()
		self.frame=Frame(self)
		self.frame.pack()
		Label(self.frame, text=itype).grid(row=0,column=0)
		Label(self.frame, text=item.name).grid(row=0,column=1)
		Label(self.frame, text=item.ammount).grid(row=1,column=0)
		Label(self.frame, text=item.a_unit).grid(row=1,column=1)
		if (itype == "Ingredient"):
			Label(self.frame, text="Price ($) ").grid(row=2,column=0)
			Label(self.frame, text=item.price).grid(row=2,column=1)
			done_button_row = 3
		elif (itype == "Food"):
			cost, time = get_cost(item.name, item.itype)
			Label(self.frame, text="Cost ($) ").grid(row=2,column=0)
			Label(self.frame, text=str_two_dec(cost)).grid(row=2,column=1)
			Label(self.frame, text="Time to make").grid(row=3,column=0)
			Label(self.frame, text=get_time_str(item.time)).grid(row=3,column=1)
			Label(self.frame, text="Ingredients:").grid(row=4,column=0)
			ingr_type = "ingr"
			for i in range(len(item.list_ing)):
				Button(
					self.frame,
					text=item.list_ing[i],
					command=lambda x=i: command(
						main.gui_view_item("Ingredient", get_saved_item(item.list_ing[x], ingr_type))
					)).grid(row=4+i,column=1)
				Label(self.frame, text=item.list_amm[i]).grid(row=4+i,column=2)
				Label(self.frame, text=get_saved_item(item.list_ing[i], ingr_type).a_unit).grid(row=4+i,column=3)
			done_button_row = 4 + len(item.list_ing)
		elif (itype == "Dish"):
			Label(self.frame, text="Price ($) ").grid(row=2,column=0)
			Label(self.frame, text=str_two_dec(item.price)).grid(row=2,column=1)
			cost, time = get_cost(item.name, item.itype)
			Label(self.frame, text="Cost ($) ").grid(row=3,column=0)
			Label(self.frame, text=str_two_dec(cost)).grid(row=3,column=1)
			Label(self.frame, text="Profit ($) ").grid(row=4,column=0)
			Label(self.frame, text=str_two_dec(float(item.price) - float(cost))).grid(row=4,column=1)
			Label(self.frame, text="Average time to make").grid(row=5,column=0)
			Label(self.frame, text=get_time_str(get_cost(item.name, item.itype)[1])).grid(row=5,column=1)
			Label(self.frame, text="Ingredients:").grid(row=6,column=0)
			ingr_type = "food"
			for i in range(len(item.list_ing)):
				Button(
					self.frame,
					text=item.list_ing[i],
					command=lambda x=i: command(
						main.gui_view_item("Food", get_saved_item(item.list_ing[x], ingr_type))
					)).grid(row=6+i,column=1)
				Label(self.frame, text=item.list_amm[i]).grid(row=6+i,column=2)
				Label(self.frame, text=get_saved_item(item.list_ing[i], ingr_type).a_unit).grid(row=6+i,column=3)
			done_button_row = 6 + len(item.list_ing)
		Button(
			self.frame,
			text="Done",
			command=lambda: command(
				main.gui_main()
			)).grid(row=done_button_row,column=0)		
	def gui_view(self, itype, text="View Window", command=donothing):
		self.title(text)
		self.frame.destroy()
		self.frame=Frame(self)
		self.frame.pack()
		
		if (itype == "Ingredient"):
			saved_items = get_saved_items("ingr")
		elif (itype == "Food"):
			saved_items = get_saved_items("food")
		elif (itype == "Dish"):
			saved_items = get_saved_items("dish")
		for i in range(len(saved_items)):
			Button(
				self.frame,
				text=saved_items[i].name,
				command=lambda x=i: command(
					main.gui_view_item(itype, saved_items[x])
				)).grid(row=i,column=0)	
	def gui_confirm_delete(self, itype, item, text="Confirm Delete", command=donothing):
		self.title(text)
		self.frame.destroy()
		self.frame=Frame(self)
		self.frame.pack()
		Label(self.frame, text="This will delete the items below:").grid(row=0,column=0)
		Label(self.frame, text=itype).grid(row=1,column=0)
		Label(self.frame, text=item.name).grid(row=1,column=1)
		row_num = 2
		if (itype == "Food"):
			for dish in get_dishes_made_with(item.name):
				Label(self.frame, text="Dish").grid(row=row_num,column=0)
				Label(self.frame, text=dish.name).grid(row=row_num,column=1)
				row_num = row_num + 1
		elif (itype == "Ingredient"):
			dish_list = []
			for food in get_foods_made_with(item.name):
				Label(self.frame, text="Food").grid(row=row_num,column=0)
				Label(self.frame, text=food.name).grid(row=row_num,column=1)
				row_num = row_num + 1
				for dish in get_dishes_made_with(food.name):
					if (not dish.name in dish_list):
						dish_list.append(dish.name)
			for dish in dish_list:
				Label(self.frame, text="Dish").grid(row=row_num,column=0)
				Label(self.frame, text=dish).grid(row=row_num,column=1)
				row_num = row_num + 1
		Button(self.frame, text="Confirm", command=lambda: command(delete_item(item))).grid(row=row_num,column=0)
		Button(self.frame, text="Cancel", command=lambda: command(main.gui_main())).grid(row=row_num,column=2)
	def gui_remove(self, itype, text="Remove Window", command=donothing):
		self.title(text)
		self.frame.destroy()
		self.frame=Frame(self)
		self.frame.pack()
		Label(self.frame, text="Remove an item below").grid(row=0,column=0)
		if (itype == "Ingredient"):
			saved_items = get_saved_items("ingr")
		elif (itype == "Food"):
			saved_items = get_saved_items("food")
		else:
			saved_items = get_saved_items("dish")
		for i in range(len(saved_items)):
			Button(
				self.frame,
				text=saved_items[i].name,
				command=lambda x=i: command(
					main.gui_confirm_delete(itype, saved_items[x])
				)).grid(row=i+1,column=0)
		Button(
			self.frame,
			text="Cancel",
			command=lambda: command(
				main.gui_main()
			)).grid(row=len(saved_items)+1,column=1)
	def gui_edit(self, itype, text="Edit Window", command=donothing):
		self.title(text)
		self.frame.destroy()
		self.frame=Frame(self)
		self.frame.pack()
		if (itype == "Ingredient"):
			saved_items = get_saved_items("ingr")
		elif (itype == "Food"):
			saved_items = get_saved_items("food")
		elif (itype == "Dish"):
			saved_items = get_saved_items("dish")
		for i in range(len(saved_items)):
			Button(
				self.frame,
				text=saved_items[i].name,
				command=lambda x=i: command(
					main.gui_edit_item(itype, saved_items[x])
				)).grid(row=i,column=0)	
	def gui_edit_item(self, itype, item, text="Edit Item", command=donothing):
		self.title(text)
		self.frame.destroy()
		self.frame=Frame(self)
		self.frame.pack()
		
		Label(self.frame, text=itype).grid(row=0,column=0)
		Label(self.frame, text=item.name).grid(row=0,column=1)
		ammount_str=StringVar(self)
		ammount_str.set(str(item.ammount))
		Entry(self.frame, textvariable=ammount_str).grid(row=1,column=1)
		a_unit_str=StringVar(self)
		a_unit_str.set(str(item.a_unit))
		
		time_to_make, t_unit = get_time_and_unit(item.time)
		time_str=StringVar(self)
		time_str.set(str(time_to_make))
		t_unit_str=StringVar(self)
		t_unit_str.set(str(t_unit))
		
		price_str=StringVar(self)
		price_str.set(str(item.price))
		
		if (itype == "Ingredient"):
			OptionMenu(self.frame, a_unit_str, *UNIT_LIST).grid(row=1,column=2)
			Label(self.frame, text="Price ($) ").grid(row=2,column=0)
			Entry(self.frame, textvariable=price_str).grid(row=2,column=1)
			Button(
				self.frame,
				text="Done",
				command=lambda: command(
					edit_my_item(item.name, item.itype, ammount_str.get(), a_unit_str.get(), t_unit_str.get(), price=price_str.get()
				))).grid(row=3,column=0)
		elif (itype == "Food"):
			OptionMenu(self.frame, a_unit_str, *UNIT_LIST).grid(row=1,column=2)
			Label(self.frame, text="Time to make").grid(row=2,column=0)
			Entry(self.frame, textvariable=time_str).grid(row=2,column=1)
			OptionMenu(self.frame, t_unit_str, *T_UNIT_LIST).grid(row=2,column=2)
			Button(
				self.frame,
				text="Continue",
				command=lambda: command(
					main.gui_edit_ingr(item, ammount_str.get(), a_unit_str.get(), time_str.get(), t_unit_str.get(), price_str.get())
				)).grid(row=3,column=0)
		elif (itype == "Dish"):
			Label(self.frame, text=item.a_unit).grid(row=1,column=2)
			Label(self.frame, text="Time to make").grid(row=2,column=0)
			Entry(self.frame, textvariable=time_str).grid(row=2,column=1)
			OptionMenu(self.frame, t_unit_str, *T_UNIT_LIST).grid(row=2,column=2)
			Label(self.frame, text="Price ($) ").grid(row=3,column=0)
			Entry(self.frame, textvariable=price_str).grid(row=3,column=1)
			Button(
				self.frame,
				text="Continue",
				command=lambda: command(
					main.gui_edit_ingr(item, ammount_str.get(), a_unit_str.get(), time_str.get(), t_unit_str.get(), price_str.get())
				)).grid(row=4,column=0)
	def gui_edit_ingr(self, item, ammount, a_unit, time, t_unit, price, text="Edit Ingredients", command=donothing):
		self.title(text)
		self.frame.destroy()
		self.frame=Frame(self)
		self.frame.pack()
		if (item.itype == "food"):
			ingr_type = "ingr"
		else: #item.type == "dish"
			ingr_type = "food"
		list_my_ingr = []
		all_ingr = get_saved_items(ingr_type)
		ingr_in_item = get_ingredients (item.name, item.itype)
		list_amm_strs = []
		a_unit_strs = []
		for _ in range(len(all_ingr)):
			list_amm_strs.append(StringVar(self))
			a_unit_strs.append(StringVar(self))
		for i in range(len(item.list_ing)):
			Label(self.frame, text=item.list_ing[i]).grid(row=i,column=0)
			list_amm_strs[i].set(str(item.list_amm[i]))
			Entry(self.frame, textvariable=list_amm_strs[i]).grid(row=i,column=1)
			a_unit_strs[i].set(str(get_saved_item(item.list_ing[i], ingr_type).a_unit))
			OptionMenu(self.frame, a_unit_strs[i], *UNIT_LIST).grid(row=i,column=2)
			list_my_ingr.append(item.list_ing[i])
		row_count = len(item.list_ing)
		for i in range(len(all_ingr)):
			if (not all_ingr[i].name in item.list_ing):
				Label(self.frame, text=all_ingr[i].name).grid(row=row_count,column=0)
				list_amm_strs[row_count].set("0")
				Entry(self.frame, textvariable=list_amm_strs[row_count]).grid(row=row_count,column=1)
				a_unit_strs[row_count].set(str(all_ingr[i].a_unit))
				OptionMenu(self.frame, a_unit_strs[row_count], *UNIT_LIST).grid(row=row_count,column=2)
				list_my_ingr.append(all_ingr[i].name)
				row_count = row_count + 1
		Button(
			self.frame,
			text="Make Edit",
			command=lambda: command(
				edit_my_item(item.name, item.itype, ammount, a_unit, list_my_ingr, list_amm_strs, time, t_unit, price)
			)).grid(row=row_count,column=0)
	def end(self):
		self.destroy()
	def start(self):
		mainloop()


if __name__=='__main__':
	for f in REQ_FILES:
		if (not f in listdir()):
			print("A file was missing. If you have moved files around and not replaced them your data may be missing / corrupted.")
			try:
				f = open(file, "w")		# create missing files if necessary
				f.close()
			except:
				print("File creation error. Quiting...")
				sys.exit(0)
	def start_gui():
		global main
		root_gui = main.gui_main()
	main=interface("Restaurant Cost Calculation Database")
	start_gui()
	main.start()
	

















