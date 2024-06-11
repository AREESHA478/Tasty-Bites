import tkinter as tk
from tkinter import messagebox
import random

# Create or check for the salesdata.txt file
try:
    with open("salesdata.txt", "x") as file:
        print("salesdata.txt created")
except FileExistsError:
    print("salesdata.txt already exists")

def save_to_file(txt):
    with open("salesdata.txt", "a") as file:
        file.write(txt + "\n\n")

# Data and UI Elements
elements = {
    'labels': [],
    'entries': {},
}

foodItems = [
    {
        "name": "Pasta",
        "price": 600
    },
    {
        "name": "Fries",
        "price": 200
    },
    {
        "name": "macroni",
        "price": 500
    },
    {
        "name": "pizza",
        "price": 999
    },
    {
        "name": "Shrimps",
        "price": 700
    },
    {
        "name": "Soup",
        "price": 650
    },
    {
        "name": "Burger",
        "price": 400
    },
    {
        "name": "Spagitti",
        "price": 800
    },
]

totalSales = {}

root = tk.Tk()

def only_numbers(char):
    return char.isdigit() or char == ""

def edit_item(main_frame):
    main_frame.destroy()

    new_window = tk.Toplevel(root)
    new_window.title("Add or Delete Item")
    new_window.geometry("300x400")
    new_window.configure(bg="light slate gray")
    new_window.attributes('-topmost', True)
    vcmd = (root.register(only_numbers), '%P')

    label1 = tk.Label(new_window, text="Name", bg="light slate gray", fg="white")
    label1.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

    n_entry = tk.Entry(new_window, bg="dark slate gray", fg="white", insertbackground="white")
    n_entry.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)

    label2 = tk.Label(new_window, text="Price", bg="light slate gray", fg="white")
    label2.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

    n_entry_price = tk.Entry(new_window, validate='key', validatecommand=vcmd, bg="dark slate gray", fg="white", insertbackground="white")
    n_entry_price.grid(row=3, column=2, padx=10, pady=5, sticky=tk.W)

    def add_to_list():
        try:
            item_name = n_entry.get()
            item_price = int(n_entry_price.get())
            n_entry.delete(0, 'end')
            n_entry_price.delete(0, 'end')
            
            foodItems.append({'name': item_name, 'price': item_price})
            messagebox.showinfo("Item Added", f"The item '{item_name}' has been added to the menu.")
            new_window.destroy()
            edit_item(main_frame)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid price.")

    add_item_button = tk.Button(new_window, text="Add", command=add_to_list, bg="dark slate gray", fg="white")
    add_item_button.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)

    def delete_item(item):
        for i in range(len(foodItems)):
            if foodItems[i]['name'] == item:
                del foodItems[i]
                break
        new_window.destroy()
        edit_item(main_frame)

    for x in range(len(foodItems)):
        label = tk.Label(new_window, text=(foodItems[x]['name'] + ":\t Rs: " + str(foodItems[x]['price'])), bg="light slate gray", fg="white")
        label.grid(row=(x + 5), column=1, sticky=tk.E)
        delete_button = tk.Button(new_window, text="Delete", command=lambda item=foodItems[x]['name']: delete_item(item), bg="dark slate gray", fg="white")
        delete_button.grid(row=(x + 5), column=2, padx=10, pady=5, sticky=tk.W)

    def reload_main_win():
        new_window.destroy()
        main_window()

    new_window.protocol("WM_DELETE_WINDOW", reload_main_win)
    
    close_button = tk.Button(new_window, text="Close", command=reload_main_win, bg="dark slate gray", fg="white")
    close_button.grid(row=4, column=2, padx=10, pady=5, sticky=tk.W)

def submit():
    total_amount = 0
    receipt = "Order Receipt: " + str(random.randint(1000, 9999)) + "\n"
    for x in foodItems:
        try:
            temp = 0 if elements['entries'][x['name']].get() == "" else int(elements['entries'][x['name']].get())
            elements['entries'][x['name']].delete(0, 'end')      
            total_amount += x['price'] * temp
            if temp != 0:
                receipt += f"{x['name']}\t{temp}\t{x['price'] * temp}\n"
        except ValueError:
            messagebox.showerror("Error", "Please enter valid quantity for all items.")
            
    receipt += "Total: " + str(total_amount)
    save_to_file(receipt)    
    messagebox.askokcancel("Confirm Order", receipt)

def main_window():
    try:
        root.title("Tasty Bites")
        root.configure(bg="light slate gray")

        frame = tk.Frame(root, bg="light slate gray")
        frame.pack(padx=10, pady=10)

        tasty_bites_frame = tk.LabelFrame(frame, text="Tasty Bites", bg="light slate gray", fg="white")
        tasty_bites_frame.grid(row=0, column=0)

        title_label = tk.Label(tasty_bites_frame, text="Menu", font=("Helvetica", 16), bg="light slate gray", fg="white")
        title_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        item_label = tk.Label(tasty_bites_frame, text="Items", font=("Helvetica", 12), bg="light slate gray", fg="white")
        item_label.grid(row=2, column=0, padx=10, columnspan=2, pady=5, sticky=tk.W)

        quantity_label = tk.Label(tasty_bites_frame, text="Quantity", font=("Helvetica", 12), bg="light slate gray", fg="white")
        quantity_label.grid(row=2, column=1, padx=10, columnspan=2, pady=5, sticky=tk.W)
        
        vcmd = (root.register(only_numbers), '%P')

        for x in range(len(foodItems)):
            label = tk.Label(tasty_bites_frame, text=(foodItems[x]['name'] + ":\t Rs: " + str(foodItems[x]['price'])), bg="light slate gray", fg="white")
            label.grid(row=(x + 3), column=0, sticky=tk.E)

            entry = tk.Entry(tasty_bites_frame, validate='key', validatecommand=vcmd, bg="dark slate gray", fg="white", insertbackground="white")
            entry.grid(row=(x + 3), column=1, padx=10, pady=5, sticky=tk.W)

            elements['labels'].append(label)
            elements['entries'][foodItems[x]['name']] = entry

        submit_button = tk.Button(tasty_bites_frame, text="Submit", command=submit, bg="dark slate gray", fg="white")
        submit_button.grid(row=len(foodItems) + 4, column=0, columnspan=2, pady=(10, 0))

        add_button = tk.Button(tasty_bites_frame, text="Edit Items", command=lambda: edit_item(frame), bg="dark slate gray", fg="white")
        add_button.grid(row=len(foodItems) + 5, column=0, columnspan=2, pady=(10, 5))

        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", str(e))

main_window()
