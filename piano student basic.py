"""
"piano student basic.py"
by Paul Renaud
9/21/2023

Basic student tracker program.
Only tracks the name and balance of each student, using parallel arrays.
Does not yet save to file.
Options to add student, remove student, change name or balance.
Option to bill student or accept payment (changes balance).
Option to change the order of students in the list, or have it sort
alphabetically.

This does a lot of error checking, for example only accepting a number when
asking for a number, but I haven't fully tested it.
"""
# declare global variables
name = []
balance = []

def loadStudents():
    name.append("Andrew Appleseed")
    balance.append(0.0)

    name.append("Betty Baker")
    balance.append(50.0)

    name.append("Charlie Coom")
    balance.append(60.0)

    name.append("Dennis Devonshire")
    balance.append(-30.0)

def printAndSelect():
    """Main menu of program. Shows list of all students, with line numbers
    by each student, and options to add a student or quit program. Entering
    a line number lets you view and edit that student. Returns False when
    ended. This can be used to exit a larger program loop."""
    inSelect = True
    while inSelect:
        formatString = "{:2d} {:30s} {:>7.2f}"
        print()
        # print list of students with line numbers. Note this does not have
        # limit checks, like checking for screen size. If you have 100
        # students, it will print 100 lines.
        for i in range(len(name)):
            print(formatString.format(i+1, name[i], balance[i]))
        prompt = "A)dd student, R)earrange list, Q)uit program "
        sel = 0  # for getting line number of student
        valid = False
        while not valid:
            mainEntry = input(prompt).lower()  # can enter a letter or number.
            if mainEntry=="-123":exit()
            if mainEntry in ("arq"): valid = True
            try:
                sel = int(mainEntry)   # try to convert to number
                if sel >= 1 and sel <= len(name):
                    valid = True
                else:
                    sel = 0   # number was set, but outside range, so reset
            except:
                if not valid: print("  Invalid entry")
        if mainEntry == "q":
            inSelect = False
            print("Goodbye for now.")
        if sel != 0: showStudent(sel-1)  # entered a line number
        if mainEntry == "a": addStudent()
        if mainEntry == "r": rearrange()
    return False

def rearrange():
    """Shows list of all students, with a * next to current selection.
    You can then move that student up or down in the list, or change the
    selection."""
    inRearrange = True
    selection = 1
    while inRearrange:
        formatString = "{:2d} {:30s} {:>7.2f}"
        print()
        print("Rearranging...")
        for i in range(len(name)):
            if i+1 == selection:
                print("*", end="")  # put a * by current selection
            else:
                print(" ", end="")
            print(formatString.format(i+1, name[i], balance[i]))
        prompt = "A)lphabetical, U)p, D)own, C)hange selection (*), Q)uit to main "
        valid = False
        while not valid:
            entry = input(prompt).lower()
            if entry=="-123":exit()
            if entry in "audcq": valid = True
            sel = 0
            try:
                sel = int(entry)
                if sel >= 1 and sel <= len(name):
                    valid = True
                else:
                    valid = False
                    sel = 0
            except:
                "Not a valid number"  # doesn't actually print
        if sel != 0: selection = sel
        if entry=="a":
            entry = input("Sort alphabetically? Y/N ").lower()
            if entry=="y":
                full = []
                for i in range(len(name)):  # convert to list of tuples, to keep items together
                    full.append((name[i], balance[i]))
                full.sort()              # sort
                for i in range(len(name)):  # convert tuples back to parallel arrays
                    name[i] = full[i][0]      # [0] is name
                    balance[i] = full[i][1]   # [1] is balance
                selection = 1
        if entry=="u":  # move up. Swap with one above it.
            if selection > 1:  # note that [1] is not the first item, [0] is.
                swap(selection - 1, selection - 2)
                selection = selection - 1
        if entry=="d":  # move down. Swap with one below it.
            if selection < len(name):
                swap(selection - 1, selection)
                selection = selection + 1
        if entry=="c": # change selection. Ask for number.
            entry = input("Enter line number to select: ")
            if entry=="-123":exit()
            if entry != "":
                try:
                    selection = int(entry)
                    if selection < 1: selection = 1
                    if selection > len(name): selection = len(name)
                except:
                    print("  Not a valid number.")
            else:
                print("  No entry. Cancelling...")
        if entry=="q": inRearrange = False

def swap(x, y):
    """swapping x and y in Python can use the following syntax:
    x, y = y, x
    """
    name[x], name[y] = name[y], name[x]
    balance[x], balance[y] = balance[y], balance[x]


def showStudent(sel):
    """Show and edit a single student. Continues until q is entered."""
    inStudent = True
    while inStudent:
        n = name[sel]
        b = balance[sel]
        print()
        print("Name: " + n)
        print("Balance: " + "{:.2f}".format(b))
        prompt = "N)ame, B)alance, C)harge, P)ayment, R)emove student, Q)uit to main "
        valid = False
        while not valid:
            entry = input(prompt).lower()
            if entry in "nbcprq": valid = True
        if entry == "n":
            print("Name: " + n)
            entry = input("New name: ")
            if entry != "":
                name[sel] = entry
            else:
                print("  No entry. Cancelling...")
        if entry == "b":
            print("Balance: " + "{:.2f}".format(b))
            entry = input("New balance: ")
            try:
                newB = float(entry)   # if able to convert, update
            except:
                newB = b    # if unable to convert, keep the same as old
            if entry != "":
                balance[sel] = newB
            else:
                print("  No entry. Cancelling...")
        if entry == "c":
            print("Current balance: " + "{:.2f}".format(b))
            entry = input("How much to charge (-): ")
            if entry != "":
                try:
                    charge = float(entry)
                except:
                    charge = 0.0
                b = b - charge
                balance[sel] = b   # update balance
            else:
                print("  No entry. Cancelling...")
        if entry == "p":
            print("Current balance: " + "{:.2f}".format(b))
            entry = input("How much did they pay (+): ")
            if entry != "":
                try:
                    payment = float(entry)
                except:
                    payment = 0.0
                b = b + payment
                balance[sel] = b  # update balance
            else:
                print("  No entry. Cancelling...")
        if entry == "r":
            # confirm wants to remove student
            entry = input("Remove student " + n + "? Y/N ").lower()
            if entry == "y":
                name.pop(sel)  # removes list items with pop() function.
                balance.pop(sel)
                print("  Student " + n + " removed.")
                inStudent = False  # exit student detail loop
            else:
                print("  Keeping student.")
        if entry == "q":
            inStudent = False

def addStudent():
    """Adds a student. Asks for name and starting balance. Balance can be
    positive or negative. If name is blank it cancels."""
    n = input("Enter name of new student: ")
    if n != "":
        name.append(n)
        entry = input("Enter starting balance of " + n + ": ")
        try:
            b = float(entry)
        except:
            print("  Invalid amount. Default to 0.")
            b = 0.0
        balance.append(b)
    else:
        print("  Blank entry. Cancelling...")

def main():
    loadStudents()
    running = True
    while running:
        running = printAndSelect()
    
    input("End of program. Press Enter to quit.")

if __name__ == "__main__":
    main()
