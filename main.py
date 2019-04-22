#!/usr/bin/env python3
# coding: utf-8

import uuid
import random
import tkinter as tk


class Results(tk.Toplevel):
    """
    Description: This class creates a new window containing only a listbox
    The listbox occupies the entire window and sticks to all boundaries.
    There is only the __init__ function on this class.
    There is a logic to display a minimum of 34 digits + 25% in order to show the full window header.

    Parameters:
        data = the data that will be displayed in the listbox
        digits = the width of the listbox, althought it can be expanded manually
        master = the parent window that owns this one

    Properties:
        data = receives the value of the data parameter
        ListValues = the variable that controls the what is displayed on the listbox
        digits = receives the value of the digits parameter
    """

    def __init__(self, data, digits, master=None):
        tk.Toplevel.__init__(self)

        # Properties:
        self.master = master
        self.ListValues = tk.StringVar()
        self.data = data
        self.ListValues.set(self.data)
        # This will make the window header to be full displayed
        if digits < 34:
            self.digits = 34
        else:
            self.digits = digits+int(digits/4)

        # row and column configuration
        self.rowconfigure(0, weight=1)           
        self.columnconfigure(0, weight=1)

        # widget creation
        self.listbox = tk.Listbox(self, listvariable=self.ListValues, exportselection=1, width=self.digits, height=11,
                                  activestyle='dotbox')

        # widget deployment
        self.listbox.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)


class Application(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        self.master.title('Password Generator')
        self.master.resizable(True, False)
        
        self.grid(pady=10, padx=10, sticky=tk.W+tk.E+tk.N+tk.S)
        self.radios_value = tk.StringVar()
        self.radios_value.set('n')
        self.spin_value = tk.StringVar()
        self.spin_value.set('16')
        self.special_value = tk.StringVar()
        self.special_value.set('!@#$%-_*')

        self.generateButton = tk.Button(self, text='Generate!', command=self.showresults)
        self.label_radios = tk.Label(self, text='Choose one of the options below:')
        self.radio_n_only = tk.Radiobutton(self, text='Numbers Only', variable=self.radios_value, value='n')
        self.radio_c_only = tk.Radiobutton(self, text='Characters Only', variable=self.radios_value, value='c')
        self.radio_ch_n = tk.Radiobutton(self, text='Character and Numbers', variable=self.radios_value, value='cn')
        self.radio_ch_n_sc = tk.Radiobutton(self, text='Characters, Numbers and Special Characters',
                                            variable=self.radios_value, value='cns')
        self.label_digits = tk.Label(self, text='How many digits?')
        self.spin_digits = tk.Spinbox(self, from_=1, to=256, increment=1, textvariable=self.spin_value)
        self.label_special = tk.Label(self, text='Special characters included (if needed):')
        self.entry_special = tk.Entry(self, width=30, textvariable=self.special_value)

        self.create_widgets()
        
        self.update_idletasks()
        x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth()) / 2
        y = (self.master.winfo_screenheight() - self.master.winfo_reqheight()) / 2
        self.master.geometry("+%d+%d" % (x, y))

    def create_widgets(self):
        top = self.winfo_toplevel()

        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=0)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.label_radios.grid(row=0, column=0, sticky=tk.W+tk.E, columnspan=2)
        self.radio_n_only.grid(row=1, column=0, sticky=tk.W)
        self.radio_c_only.grid(row=2, column=0, sticky=tk.W)
        self.radio_ch_n.grid(row=3, column=0, sticky=tk.W)
        self.radio_ch_n_sc.grid(row=4, column=0, sticky=tk.W)
        self.label_special.grid(row=5, column=0, sticky=tk.W)
        self.entry_special.grid(row=5, column=1, sticky=tk.E+tk.W)
        self.label_digits.grid(row=6, column=0, sticky=tk.W)
        self.spin_digits.grid(row=6, column=1, stick=tk.E)
        
        self.generateButton.grid(row=7, column=0, columnspan=2, stick=tk.S)

    def showresults(self):
        data = self.generateresults()
        digits = int(self.spin_value.get())
        results = Results(data=data, digits=digits, master=self)
        results.title('Results')
        results.transient(self)
        results.resizable(True, False)
        results.update_idletasks()
        x = (results.winfo_screenwidth() - results.winfo_reqwidth()) / 2
        y = (results.winfo_screenheight() - results.winfo_reqheight()) / 2
        results.geometry("+%d+%d" % (x, y))
        results.mainloop()

    def generateresults(self):
        size = int(self.spin_value.get())
        data = list()
        if self.radios_value.get() == 'n':
            minimum = str('0')*size
            maximum = str('9')*size
            for i in range(0, 11):
                value = str(random.randint(int(minimum), int(maximum)))
                while len(value) < size:
                    value = '0'+value
                data.append(value)
        elif self.radios_value.get() == 'c':
            import string
            chars_list = string.ascii_lowercase + string.ascii_uppercase
            for i in range(0, 11):
                chars_only = ''
                for j in range(0, size+1):
                    chars_only += random.choice(chars_list)
                data.append(chars_only)
        elif self.radios_value.get() == 'cn':
            for i in range(0, 11):
                my_uuid = str(uuid.uuid4())*(int(size / 32)+1)
                my_uuid = my_uuid.replace('-', '')
                my_uuid = my_uuid[:size]
                my_list = list(my_uuid)
                for j in range(len(my_list)):
                    randomness = random.random()
                    if randomness > 0.5 and not str(my_list[j]).isnumeric():
                        my_list[j] = my_list[j].upper()
                data.append(''.join(my_list))
        elif self.radios_value.get() == 'cns':
            special_chars = self.special_value.get()
            for i in range(0, 11):
                my_uuid = str(uuid.uuid4())*(int(size / 32)+1)
                my_uuid = my_uuid.replace('-', '')
                my_uuid = my_uuid[:size]
                my_list = list(my_uuid)
                for j in range(len(my_list)):
                    randomness = random.random()
                    # 10% of chance to include a special char
                    if randomness > 0.9: 
                        random_special = random.choice(special_chars)
                        my_list[j] = random_special
                    
                    # 50% of chance to upper case a non-numeric character
                    if randomness > 0.5 and not str(my_list[j]).isnumeric():
                        my_list[j] = my_list[j].upper()
                data.append(''.join(my_list))

        return tuple(data)


# startup
if __name__ == '__main__':
    window_name = tk.Tk(None, None, 'Password Generator')
    app = Application()
    app.mainloop()
