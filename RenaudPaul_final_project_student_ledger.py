"""
RenaudPaul_final_project_student_ledger.py
by Paul Renaud
10/5/2023

for SDEV140
Instructor: Patrick Scherrer

This program is to help someone like a private music teacher
to keep track of which students have paid ahead and which
are behind. The left side shows a list of students which can
be selected, and the right side shows the selected student's
details, like name, address, phone number, etc. The right
side also has buttons to edit the student's info, charge the
student for a lesson, or receive payment.

I wanted to keep track of individual transactions, but this
early version just keeps track of the total. So when entering
a transaction, some information, like the date, check
number, and description are basically lost and not saved
anywhere yet.

This autoloads and autosaves to a file.

I have also not done a full check for errors.

"""

from breezypythongui import EasyFrame  # for main window
from breezypythongui import EasyDialog # for text-entry dialogs
from tkinter import font            # for making font bigger
import copy                         # for copying class items
from tkinter import PhotoImage      # for using images
import datetime                     # for prefilling today's date
from tkinter.messagebox import askokcancel  # for ok/cancel box
from tkinter.filedialog import askopenfilename

DEFAULT_LESSON_COST = 30.0   # used when creating a new student
NEW_STUDENT_STRING = "(new student)"   # to change the text that displays for the new student line
DEFAULT_PIC = "blank_face.png"    # default picture. Didn't feel right hard-coding these in multiple places.

class Student(object):
    """Student class. Holds all information for one student.
        string name
        string lessonDayTime
        string address
        string phone
        float lessonCost
        string profilePic (path to PNG image)
        list transactions (not implemented)
        float balance
    """

    def __init__(self, name=NEW_STUDENT_STRING, lessonDayTime="", address="",\
                 phone="", lessonCost=DEFAULT_LESSON_COST, profilePic=DEFAULT_PIC,\
                 transactions="", balance=0):
        """New student can be created with name and/or balance.
        Probably best to use name=value when using constructor.
        Most values not specified default to empty string or 0; except name, lessonCost, and profilePic.
        """
        self.name = name
        self.lessonDayTime = ""
        self.address = ""
        self.phone = phone
        self.lessonCost = lessonCost
        self.profilePic = profilePic
        self.transactions = transactions
        self.balance = balance

    def __str__(self):
        final = ""
        final += "Name:" + self.name
        final += " | Day:" + self.lessonDayTime
        final += " | Add:" + self.address
        final += " | Ph:" + self.phone
        final += " | Cost:" + str(self.lessonCost)
        final += " | Pic:" + self.profilePic
        final += " | Bal:" + str(self.balance)
        return final

    # I did not write any accessor or mutator methods. I find it easier to access the fields directly.


class Transaction(object):

    def __init__(self, date=None, charged=None, paid=None, checkNo=None, desc=None):
        """Create new transaction. Constructor should probably be called with
        name=value pairs.
        date is a string. charged and paid are floats. checkNo is string.
        desc is string.
        NOTE: This is not yet implemented.
        """
        self.date = date
        self.charged = charged
        self.paid = paid
        self.checkNo = checkNo
        self.desc = desc


class TransactionEditor(EasyDialog):
    """Pops up a simple dialog to enter transaction fields."""
    
    def __init__(self, student, name="", date="", charge=0.0, paid=0.0,
                 checkNo="", desc="", master=None, focus="paid"):
        """Opens dialog box with certain items prefilled.
        Must be passed a student record.
        focus is a string field saying which item should have the focus
        after building the window. It is a string that matches any of the
        field names with boxes (date, charge, paid, checkNo, desc).
        """

        # puts today's date in the transaction
        # This doesn't actually save yet. Only the total updates.
        if date == "":
            dt_now = datetime.date.today()
            self.date = "{:d}/{:d}/{:d}".format(dt_now.month, dt_now.day, dt_now.year)
        else:
            self.date = date

        self.student = student
        self.master = master
        self.name = name
        self.charge = charge
        self.paid = paid
        self.checkNo = checkNo
        self.desc = desc
        self.focus = focus

        # Note: __init__ automatically calls the body function.
        EasyDialog.__init__(self, parent=master, title="A Transaction for " + name)

    def body(self, master):
        """Puts the labels and fields in the dialog box. body() is called
        automatically from __init__()"""

        # Add labels and boxes.
        self.addLabel(master, text="A transaction for " + self.name, row=0, column=0, columnspan=2)

        #self.addLabel(master, text="( ) = not actually saved yet.", row=1, column=0, columnspan=2)

        ORDER = 1

        self.addLabel(master, text="(Date)", row=ORDER, column=0)
        self.dateField = self.addTextField(master, text=self.date, row=ORDER, column=1, columnspan=2, state="disabled")

        self.addLabel(master, text="Bill for lesson", row=ORDER+1, column=0)
        chargeFormat = "{:.2f}".format(self.charge)
        self.chargeField = self.addTextField(master, text=chargeFormat, row=ORDER+1, column=1)

        self.addLabel(master, text="Receive payment", row=ORDER+2, column=0)
        paidFormat = "{:.2f}".format(self.paid)
        self.paidField = self.addTextField(master, text=paidFormat, row=ORDER+2, column=1)

        self.addLabel(master, text="(Check #)", row=ORDER+3, column=0)
        self.checkNoField = self.addTextField(master, text=self.checkNo, row=ORDER+3, column=1, state="disabled")

        self.addLabel(master, text="(Description)", row=ORDER+4, column=0)
        self.descField = self.addTextField(master, text=self.desc, row=ORDER+4, column=1, state="disabled")


        #self.addButton(master, text="Save", row=6, column=0, command=self.saveTrans)
        #self.addButton(master, text="Cancel", row=6, column=1, command=self.cancelTrans)

        if   self.focus == "date":
            focus = self.dateField
            self.dateField.selection_range(0, "end")
        elif self.focus == "charge":
            focus = self.chargeField
            self.chargeField.selection_range(0, "end")
        elif self.focus == "paid":
            focus = self.paidField
            self.paidField.selection_range(0, "end")
        elif self.focus == "checkNo":
            focus = self.checkNoField
            self.checkNoField.selection_range(0, "end")
        else:
            focus = self.descField
            self.descField.selection_range(0, "end")
        return focus

    def apply(self):
        """Clicks the OK button."""
        
        self.saveTrans()

    def saveTrans(self):
        """Command to update transaction and balance."""
        try:
            charge = float(self.chargeField.get())  # error checking for valid number
        except:
            charge = 0.0   # if not valid number, default to 0.0
        try:
            paid = float(self.paidField.get())  # error checking for valid number
        except:
            paid = 0.0   # if not valid, default to 0.0
        if charge < 0 or paid < 0:
            if askokcancel(title="Negative numbers",
                           message="Entered:\nCharge: " + str(charge) + "\nPaid: " + str(paid) + \
                           "\n\nThere should not be negative numbers here. " + \
                           "Changing them to positive numbers.\n\nChanged:\nCharge: " + \
                            str(abs(charge)) + "\nPaid: " + str(abs(paid))):
                charge, paid = abs(charge), abs(paid)
                self.student.balance -= charge
                self.student.balance += paid
                self.destroy()
        else:
            self.student.balance -= charge
            self.student.balance += paid
            # self.destroy()  # dialog is closed when OK is clicked.
            
    
    def cancelTrans(self):
        """Button to close transaction dialog, without saving."""
        pass

class StudentView(EasyFrame):
    """This is the main window of the program. It displays a listBox of student names and balances on the left.
    On the right are the selected student's details and buttons to make changes."""

    def __init__(self):
        EasyFrame.__init__(self, title="Students")

        bigText = font.Font(weight="normal", size=16)   # used to make all fonts bigger.
        bigMonoText = font.Font(family="Consolas", weight="normal", size=16)  # use a monospaced font for lined up numbers.

        self.currentSel = 1

        # set up move up and move down buttons
        b1 = self.addButton(text = "Move Up", row=1, column=0, command=self.up)
        b1.grid(sticky = "SEW")
        b2 = self.addButton(text = "Move Down", row=2, column=0, command=self.down)
        b2.grid(sticky="NEW")
        self.upImage = PhotoImage(file="up_arrow.png") # must use self.variable for the image, or the image disappears
        self.downImage = PhotoImage(file="down_arrow.png")
        b1["image"] = self.upImage  # must use self.variable for the image, or the image disappears
        b2["image"] = self.downImage
        self.addLabel(text="rearrange", row=3, column=0).grid(sticky="NEW")

        # Set up the list box
        # Note the event handler parameter for selecting a list item
        self.listBox = self.addListbox(row = 0, column = 1, rowspan = 9, columnspan=3, width=40,
                                       listItemSelected = self.listItemSelected)
        self.listBox.config(font=bigMonoText)  # use mono-spaced text for listBox

        self.newButton = self.addButton(text = "New Student", row = 9, column = 1, command=self.new)
        self.newButton.config(font=bigText)
        # self.bind("<Alt_L><n>", lambda x: self.new())  # could not figure out keybindings. Doesn't seem to have focus.

        self.editButton = self.addButton(text = "Edit Student",
                       row=9, column=2,
                       command=self.edit)
        self.editButton.config(font=bigText)

        self.deleteButton = self.addButton(text = "Delete Student",
                       row=9, column=3,
                       command=self.delete)
        self.deleteButton.config(font=bigText)

        #original code for sample listBox
        """
        self.listBox.insert("end", "Apple")
        self.listBox.insert("end", "Banana")
        self.listBox.insert("end", "Cherry")
        self.listBox.insert("end", "Orange")
        """

        # Set up labels and variable labels.
        # Any value with an assignment (=) can be modified by the
        # code later. This will be used to dynamically change the view.

        LABELCOL = 4  # used to shift everything if I want to add another column somewhere

        self.addLabel(text="(X closes without saving)", row=0, column=LABELCOL+2, sticky="NE")

        self.nameLabel  = self.addLabel(text="", row=0, column=LABELCOL,
                                        columnspan=2)
        self.nameLabel.config(font=bigText)
        self.profilePic = self.addLabel(text="(pic)", row=1, column=LABELCOL,
                                        columnspan=2)
        
        self.addLabel(text="Lesson day/time:", row=2, column=LABELCOL).config(font=bigText)  # putting config at the end returns None, but still applies the formatting.
        self.dayTimeLabel = self.addLabel(text="", row=2, column=LABELCOL+1,
                                          columnspan=2)
        self.dayTimeLabel.config(font=bigText)
        
        self.addLabel(text="Address:", row=3, column=LABELCOL).config(font=bigText)
        self.addressLabel = self.addLabel(text="", row=3, column=LABELCOL+1,
                                          columnspan=2)
        self.addressLabel.config(font=bigText)
        
        self.addLabel(text="Phone:", row=4, column=LABELCOL).config(font=bigText)
        self.phoneLabel = self.addLabel(text="", row=4, column=LABELCOL+1,
                                        columnspan=2)
        self.phoneLabel.config(font=bigText)

        self.addLabel(text="Lesson cost:", row=5, column=LABELCOL).config(font=bigText)
        self.lessonCostLabel = self.addLabel(text="", row=5, column=LABELCOL+1,
                                             columnspan=2)
        self.lessonCostLabel.config(font=bigText)

        self.addLabel(text="Balance:", row=6, column=LABELCOL).config(font=bigText)
        self.balanceLabel = self.addLabel(text="", row=6, column=LABELCOL+1,
                                          columnspan=2)
        self.balanceLabel.config(font=bigText)

        # Set up buttons
        self.chargeButton = self.addButton(text = "Charge for lesson", row=7, column=LABELCOL, command=self.charge)
        self.chargeButton.config(font=bigText)
        
        self.paymentButton = self.addButton(text = "Receive Payment", row=7, column=LABELCOL+1, command=self.payment)
        self.paymentButton.config(font=bigText)

        """
        self.addButton(text = "Transactions",
                       row=8, column=LABELCOL,
                       state="disabled",
                       command=self.showTransactions).config(font=bigText)
        """
        


        self.addButton(text = "Save and Quit",
                       row=9, column=LABELCOL+2,
                       command=self.saveAndQuit).config(font=bigText)

        self.student = []  # create blank students list
        self.loadStudents("studentsn.txt")  # load students from file into list
        self.populate()  # refresh view and run

        """
        # This was from the original sample code I was basing this off of.
        # Set up the labels, fields, and buttons
        self.addLabel(text = "Input", row = 0, column = 1).config(font=bigText)
        self.addLabel(text = "Index", row = 1, column = 1).config(font=bigText)
        self.addLabel(text = "Current item", row = 2, column = 1).config(font=bigText)
        self.inputField = self.addTextField(text = "", row = 0,
                                            column = 2, width = 30)
        self.inputField.config(font=bigText)
        self.indexField = self.addIntegerField(value = "", row = 1,
                                               column = 2, width = 10)
        self.indexField.config(font=bigText)
        self.itemField = self.addTextField(text = "", row = 2,
                                           column = 2, width = 30)
        self.itemField.config(font=bigText)
        self.addButton(text = "Add", row = 3,
                       column = 1, command = self.add).config(font=bigText)
        self.removeButton = self.addButton(text = "Remove", row = 3,
                                           column = 2, command = self.remove)
        self.removeButton.config(font=bigText)
        """

        # Display current index and currently selected item
        # self.listItemSelected(0) # commented out. This is now done in populate.

    def new(self):
        """Creates a new student."""
        savedIndex = self.currentSel
        tempStudent = Student(name=NEW_STUDENT_STRING, lessonDayTime="", address="",
                  phone="", lessonCost=DEFAULT_LESSON_COST,
                  profilePic=DEFAULT_PIC,
                  balance=0.0)
        self.student.append(copy.deepcopy(tempStudent))  # last student is now blank
        me = self.student[len(self.student)-1]
        editor = StudentEditorDialog(me, master=self)   # creates dialog, sets modified flag
        # if edited the (new student) field, create a new one
        if editor.modified():
            self.populate()
            self.listBox.selection_clear(0, "end")
            self.listBox.setSelectedIndex(len(self.student)-1)  # select last student
            self.listItemSelected(len(self.student)-1)  # refresh view after editing. Maybe not necessary.
        else:
            self.student.pop(len(self.student)-1)   # did not save changes, so delete new student record
            self.listBox.setSelectedIndex(savedIndex)  # reselect previous student
            self.listItemSelected(savedIndex)  # refresh view after editing. Maybe not necessary.
        
    def up(self):
        """Moves selected student up. If not already at top, swaps places with student above it."""
        if self.currentSel > 0: # and self.currentSel < len(self.student)-1:
            # to swap variables in python, we can use x, y = y, x
            self.student[self.currentSel], self.student[self.currentSel - 1] = self.student[self.currentSel - 1], self.student[self.currentSel]
            newIndex = self.currentSel - 1  # move selection up (to stay on this one)
            self.listBox.setSelectedIndex(newIndex)
            self.populate()

    def down(self):
        """Moves selected student down. If not already at bottom, swaps places with student below it."""
        if self.currentSel < len(self.student)-1: #-2:
            self.student[self.currentSel], self.student[self.currentSel + 1] = self.student[self.currentSel + 1], self.student[self.currentSel]
            newIndex = self.currentSel + 1  # move selection down (to stay on this one)
            self.listBox.selection_clear(0, "end")  # clear was necessary because it is selecting multiple and using the first tuple.
            self.listBox.setSelectedIndex(newIndex)
            self.populate()

    def charge(self):
        """Brings up transaction dialog with some fields filled out
        for charging student for lesson."""
        oldIndex = self.currentSel
        me = self.student[self.currentSel]  # get selected student
        t = TransactionEditor(me, name=me.name, master=self,
                              charge=me.lessonCost, focus="charge")
        
        self.listBox.selection_clear(0, "end")  # clear was necessary because it is selecting multiple and using the first tuple.
        self.listBox.setSelectedIndex(oldIndex)
        self.populate()

    def payment(self):
        """Brings up transaction dialog with payment fields filled out
        for receiving payment."""
        oldIndex = self.currentSel
        me = self.student[self.currentSel]  # get selected student
        if me.balance < 0:
            p = -(me.balance)  # if they owe, prefill with total due.
        else:
            p = me.lessonCost  # if they don't owe, prefill with lesson cost.
        
        t = TransactionEditor(me, name=me.name, master=self,
                              paid=p, focus="paid")
        self.listBox.selection_clear(0, "end")  # clear was necessary because it is selecting multiple and using the first tuple.
        self.listBox.setSelectedIndex(oldIndex)
        self.populate()

    def showTransactions(self):
        """Shows a list of all transactions. Each transaction can
        be modified."""
        # This is not yet implemented. Would eventually be using Treeview in a grid formation, I think.
        pass

    def edit(self):
        """Opens dialog to update student info. Fields are pre-filled with
        existing data from selected student."""
        savePosition = self.currentSel
        
        me = self.student[self.currentSel]
        editor = StudentEditorDialog(me, master=self)   # creates dialog, sets modified flag

        if editor.modified():
            self.populate()
            self.listBox.selection_clear(0, "end")
            self.listBox.setSelectedIndex(savePosition)  # reselect where you were
            self.listItemSelected(savePosition) # update view

    def delete(self):
        """Deletes current student, after confirmation dialog."""
        savePosition = self.currentSel
        if len(self.student) == 0:  # don't try to delete an empty list
            pass
        else:
            if askokcancel(title="Delete student?",
                           message="Are you sure you want to remove " + self.student[self.currentSel].name + "?"):

                index = self.listBox.getSelectedIndex()
                self.student.pop(index)  # remove student from data
                self.listBox.delete(index)  # remove student from listBox
                self.listItemSelected(self.currentSel) # update view
                """
                if self.listBox.size() > 0:
                    if index > 0:
                        index -= 1
                    self.listBox.setSelectedIndex(index)
                    self.listItemSelected(index)
                else:
                    self.listItemSelected(-1)
                """
        self.populate()
        self.listBox.selection_clear(0, "end")
        if savePosition > len(self.student)-1: savePosition = len(self.student)-1  # if deleted last item, move selection to new last item
        self.listBox.setSelectedIndex(savePosition)  # reselect where you were
        self.listItemSelected(savePosition) # update view


    def saveAndQuit(self):
        """Saves, then quits."""
        
        self.saveStudents("studentsn.txt")
        self.master.destroy()  # just self.destroy() clears the frame, but
                               # the window stays open. So, self.master.destroy()
    
    def populate(self):
        """Saves selected spot, clears list, then, using a monospaced font,
        add names and balances to list and reselects where you were. This is
        often called after a change in the data."""
        saveSpot = self.listBox.getSelectedIndex()  # remember position
        if saveSpot < 0: saveSpot = 0  #  if position is -1, nothing selected. So make it the first item.
        self.listBox.delete(0, "end")  # clear listBox
        maxNameLength = 30  # display will truncate long names at this point
        # the following loop to find the longest name can probably be put in one "pythonic" line.
        longest = 0
        for i in range(len(self.student)):
            size = len(self.student[i].name)
            if size > longest:
                longest = size
        if longest > maxNameLength: longest = maxNameLength  # don't exceed maxNameLength
        # alignment is dynamic based on longest name
        formatString = "{:"+str(longest+2)+"s} {:6.2f}"  # pad with spaces to longest name + 2. End with balance with 2 decimals.
        # add each name and balance to box
        for i in range(len(self.student)):
            n = self.student[i].name[:maxNameLength]  # slice to truncate
            viewString = formatString.format(n, self.student[i].balance)
            self.listBox.insert("end", viewString)  # add name and balance line item to listBox
        self.listBox.setSelectedIndex(saveSpot)  # reselect where you were
        self.listItemSelected(saveSpot)     # update view from selection
        # disables some buttons (Delete, Charge, and Payment) if nothin in list.
        if len(self.student) <= 0:
            self.deleteButton["state"] = "disabled"
            self.chargeButton["state"] = "disabled"
            self.paymentButton["state"] = "disabled"
            self.editButton["state"] = "disabled"
        else:
            self.deleteButton["state"] = "active"
            self.chargeButton["state"] = "active"
            self.paymentButton["state"] = "active"
            self.editButton["state"] = "active"



    def loadStudents(self, filepath="studentsn.txt"):
        """Fills student list from file studentsn.txt. filepath
        can be optionally specified."""
        fileExists = True
        try:
            with open(filepath, "r") as f:
                pass
        except:
            fileExists = False
        if fileExists:
            with open(filepath, "r") as f:
                totalStudents = int(f.readline())  # first line is number of records
                tempStudent = Student()
                # this assumes strict adherance to order of data.
                for i in range(totalStudents):
                    tempStudent.name =          f.readline().strip()
                    tempStudent.lessonDayTime = f.readline().strip()
                    tempStudent.address =       f.readline().strip()
                    tempStudent.phone =         f.readline().strip()
                    tempStudent.lessonCost =    float(f.readline().strip())
                    tempStudent.profilePic =    f.readline().strip()
                    tempStudent.balance =       float(f.readline().strip())
                    
                    # insert all other fields here in order
                    # read another number for number of transactions
                    # start another loop to fill transactions list
                    self.student.append(copy.deepcopy(tempStudent))
                    """deepcopy was needed beacause objects assign by reference, not by
                    # value. So the student[] list would just be pointing to the same
                    # copy of tempStudent over and over, unless I copy it.
                    # Alternately, I could create a new Student during the append method.
                    """

        #debugging print. Commented out.
        #formatString = "{:30s} {:6.2f}"
        #for i in range(len(self.student)):
        #    print(formatString.format(self.student[i].name, self.student[i].balance))

    def saveStudents(self, filepath="studentsn.txt"):
        """Fills student list from file studentsn.txt. filepath
        can be optionally specified."""
        with open(filepath, "w") as f:
            totalStudents = len(self.student)
            f.write(str(totalStudents) + "\n")   # write the number of records. All records are the same size.
            # this assumes strict adherance to order of data.
            for i in range(totalStudents):
                me = self.student[i]
                f.write(me.name + "\n")
                f.write(me.lessonDayTime + "\n")
                f.write(me.address + "\n")
                f.write(me.phone + "\n")
                f.write(str(me.lessonCost) + "\n")
                f.write(me.profilePic + "\n")
                f.write(str(me.balance) + "\n")

    def listItemSelected(self, index):
        """Responds to the selection of an item in the list box.
        Updates all the fields."""
        self.currentSel = index
        if index >= len(self.student): index = len(self.student) - 1
        if index != -1:            
            me = self.student[index]  #save a bunch of typing later
            
            #self.indexField.setNumber(index)
            #self.itemField.setText(self.listBox.getSelectedItem())

            # Note: setText() method only works on textFields, not on Labels.
            # So I had to change the Label text directly.

            self.nameLabel["text"] = me.name[:50]   # trim to 50 chars max
            try:
                self.image = PhotoImage(file = me.profilePic)
            except:  # catches all exceptions, like file not found or file format not recognized.
                self.image = PhotoImage(file = DEFAULT_PIC)  # if loading image failed, default to this blank image
            
            #if image is too big, halve it until it is small enough.
            while self.image.width() > 400 or self.image.height() > 400: self.image = self.image.subsample(2)
            self.profilePic["image"] = self.image
            self.dayTimeLabel["text"] = me.lessonDayTime[:50]
            self.addressLabel["text"] = me.address[:50]
            self.phoneLabel["text"] = me.phone[:50]
            costString = "${:.2f}".format(me.lessonCost)
            self.lessonCostLabel["text"] = costString
            self.chargeButton["text"] = "Charge for lesson " + costString
            balanceString = "{:.2f}".format(me.balance)
            if me.balance < 0: balanceString += " (owes)"
            elif me.balance > 0: balanceString += " (paid ahead)"
            self.balanceLabel["text"] = balanceString

        

    def add(self):
        """If an input is present, insert it before the selected
        item in the list box.  The selected item remains current.
        If the first item is added, select it and enable the
        remove button.
        (Paul's note: This method was here with the initial listBox
        program I was using as a base. I was keeping it for reference, but
        I don't use it myself.)
        """
        item = self.inputField.getText()
        if item != "":
            index = self.listBox.getSelectedIndex()
            if index == -1:
                self.listBox.insert(0, item)
                self.listBox.setSelectedIndex(0)
                self.listItemSelected(0)
                self.removeButton["state"] = NORMAL
            else:
                self.listBox.insert(index, item)
                self.listItemSelected(index + 1)
            self.inputField.setText("")

    def remove(self):
        """If there are items in the list, remove
        the selected item, select previous one,
        and update the fields.  If there was no previous
        item, select the next one.  If the last item is
        removed, disable the remove button.
        (Paul's note: Like the add() method, I don't use this
        for anything except reference from the base program I
        started with.)
        """
        index = self.listBox.getSelectedIndex()
        self.listBox.delete(index)
        if self.listBox.size() > 0:
            if index > 0:
                index -= 1
            self.listBox.setSelectedIndex(index)
            self.listItemSelected(index)
        else:
            self.listItemSelected(-1)
            self.removeButton["state"] = DISABLED

class StudentEditorDialog(EasyDialog):
    """Pops up a simple dialog to change student info."""
    
    def __init__(self, student, master):
        """Opens dialog box with certain items prefilled."""

        self.student = student  # this is not a copy, but a reference.

        # Note: __init__ automatically calls the body function.
        EasyDialog.__init__(self, parent=master, title="Editing " + self.student.name[:50])
        # body() is called automatically to fill the rest.

    def body(self, master):

        ORDER = 0

        # Add labels and boxes.
        self.addLabel(master, text="Name", row=ORDER+0, column=0)
        self.nameField = self.addTextField(master, text=self.student.name, row=ORDER+0, column=1, columnspan=2, sticky="W", width=25)

        self.addLabel(master, text="Lesson Day/Time", row=ORDER+1, column=0)
        self.lessonDayTimeField = self.addTextField(master, text=self.student.lessonDayTime, row=ORDER+1, column=1, columnspan=2, sticky="W", width=25)

        self.addLabel(master, text="Address", row=ORDER+2, column=0)
        self.addressField = self.addTextField(master, text=self.student.address, row=ORDER+2, column=1, columnspan=2, sticky="W", width=25)
    
        self.addLabel(master, text="Phone", row=ORDER+3, column=0)
        self.phoneField = self.addTextField(master, text=self.student.phone, row=ORDER+3, column=1, columnspan=2, sticky="W", width=25)

        self.addLabel(master, text="Lesson Cost", row=ORDER+4, column=0)
        costFormat = "{:.2f}".format(self.student.lessonCost)
        self.lessonCostField = self.addTextField(master, text=costFormat, row=ORDER+4, column=1, columnspan=2, sticky="W", width=25)

        self.addLabel(master, text="Profile Picture", row=ORDER+5, column=0)
        self.profilePicField = self.addTextField(master, text=self.student.profilePic, row=ORDER+5, column=1, sticky="W", width=20)
        self.addButton(master, text="...", row=ORDER+5, column=2, command=self.pickPic)  # button to choose picture file

        self.addLabel(master, text="Balance", row=ORDER+6, column=0)
        balanceFormat = "{:.2f}".format(self.student.balance)
        self.balanceField = self.addTextField(master, text=balanceFormat, row=ORDER+6, column=1, columnspan=2, sticky="W", width=25)


        #self.addButton(master, text="Save", row=6, column=0, command=self.saveTrans)
        #self.addButton(master, text="Cancel", row=6, column=1, command=self.cancelTrans)

        # If new student, focus on name field. It starts selected, so you can just type over it.
        if self.student.name == NEW_STUDENT_STRING:
            self.nameField.selection_range(0, "end")  # pre-select text so you can just type over it.
            return self.nameField

        # optional: return field to focus on
        # return self.nameField

    def pickPic(self):
        """Opens a file dialog to select the profile picture. Updates the dialog box field."""
        #tkinter PhotoImage can only read PNG, GIF, PGM, and PPM files.
        fileTypes = [("PNG", "*.png"), ("GIF", "*.gif"), ("Portable Gray Map", "*.pgm"), ("Portable Pixel Map", "*.ppm"), ("All Files", "*.*")]
        fileName = askopenfilename(filetypes=fileTypes)
        self.profilePicField.setText(fileName)
        
    def apply(self):
        """Clicks the OK button. Change all the fields. There is no undo.
        You can Quit without Saving with the X, so that's always an option.
        If you mess this up, you'll have to quit like that so it doesn't save.
        """
        self.student.name =          self.nameField.get()
        self.student.lessonDayTime = self.lessonDayTimeField.get()
        self.student.address =       self.addressField.get()
        self.student.phone =         self.phoneField.get()

        try:  # check if a valid number
            entry = float(self.lessonCostField.get())
            if entry < 0:
                text = str(entry) + "\n\nLesson cost should not be negative. Making positive.\n\nNew value:" + str(abs(entry))
                entry = abs(entry)
                askokcancel("Negatives not allowed", text)
        except:   # error, default to previous value
            entry = self.student.lessonCost
        self.student.lessonCost =    entry
        
        self.student.profilePic =    self.profilePicField.get()

        try:   # check if valid number
            entry = float(self.balanceField.get())
        except:
            entry = self.student.balance   # if not a valid number, silently default to previous entry
        self.student.balance =       entry

        self.setModified()  # raise modified flag to True

def main():
    StudentView().mainloop()

if __name__ == "__main__":
    main()
