from tkinter import *
from functools import partial

valueText = 'Earnings (Ex: 21.50)'
startTimeText = 'Start Time (Int 0-11)'
endTimeText = 'End Time (Int 1-12)'
values, startTimes, endTimes, clearBtns = [], [], [], []

def main():
    window = Tk()
    window.geometry("1000x600")
    window.title("Earning Maximization Problem")

    ##  Place add task button in its initial position
    addTaskBtn = Button(window, text='+ Add Task', fg='blue', activeforeground='blue',
                        cursor='hand2', bd=0, relief=FLAT)
    addTaskBtn.config(command=partial(addTask, window, addTaskBtn))
    addTaskBtn.grid(row=35, column=1, pady=(0,10), sticky=W)

    ##  Create arrays to store Entry objects and add first task entry to UI
    addTask(window, addTaskBtn)

    ##  Continue to display UI until user exits
    window.mainloop()

##  Add entry fields for another task to the interface
def addTask(window, addTaskBtn):
    ##  The current number of task entries
    i = len(values)

    ##  Stop displaying the add task button when task limit is reached
    if i >= 9:
        addTaskBtn.grid_forget()

    ##  Find new task number
    text = 'Task %s:' % (i + 1)
    textVar = StringVar()
    textVar.set(text)

    ##  Display new task number
    label = Label(window, textvariable=textVar, width=10)
    label.grid(row=4*i, column=0, pady=(10,0), padx=(10,0))

    ##  Display the three entry fields for new task
    valueEntry = Entry(window, fg='light grey', relief=FLAT, width=20)
    valueEntry.grid(row=4*i, column=1, pady=(10,0))
    valueEntry.insert(0, valueText)
    valueEntry.bind('<FocusIn>', partial(onFocusIn, valueEntry))
    valueEntry.bind('<FocusOut>', partial(onFocusOut, valueEntry, 'V'))

    startTimeEntry = Entry(window, fg='light grey', relief=FLAT, width=20)
    startTimeEntry.grid(row=(4*i)+1, column=1, pady=(5,0))
    startTimeEntry.insert(0, startTimeText)
    startTimeEntry.bind('<FocusIn>', partial(onFocusIn, startTimeEntry))
    startTimeEntry.bind('<FocusOut>', partial(onFocusOut, startTimeEntry, 'S'))

    endTimeEntry = Entry(window, fg='light grey', relief=FLAT, width=20)
    endTimeEntry.grid(row=(4*i)+1, column=2, pady=(5,0), padx=(5,0))
    endTimeEntry.insert(0, endTimeText)
    endTimeEntry.bind('<FocusIn>', partial(onFocusIn, endTimeEntry))
    endTimeEntry.bind('<FocusOut>', partial(onFocusOut, endTimeEntry, 'E'))

    ##  Create button to clear this task's entry fields
    clear = Button(window, text='x', fg='light gray', activeforeground='light gray',
                   cursor='hand2', bd=0, relief=FLAT)
    clear.config(command=partial(onClear, i))
    clear.grid(row=(4*i)+1, column=3, pady=(5,0), padx=(5,0))

    ##  Force FocusIn on valueEntry when user adds a task
    if i >= 1:
        valueEntry.focus_force()

    ##  Add the newly created objects to lists for later access
    values.append(valueEntry)
    startTimes.append(startTimeEntry)
    endTimes.append(endTimeEntry)
    clearBtns.append(clear)

##  Removes placeholder text in Entry when user focuses in
def onFocusIn(entry, e):
    allowedStrings = [valueText, startTimeText, endTimeText]
    if entry.get() in allowedStrings:
        entry.delete(0, END)
    entry.config(fg='black')

##  Replaces placeholder text if the user focuses out and no input was given
def onFocusOut(entry, entryType, e):
    if entry.get() == '':
        if entryType == 'V':
            entry.insert(0, valueText)
        elif entryType == 'S':
            entry.insert(0, startTimeText)
        elif entryType == 'E':
            entry.insert(0, endTimeText)
        entry.config(fg='light grey')

##  Clear all entry fields for a task
def onClear(i):
    values[i].delete(0, END)
    values[i].focus_force()
    
    startTimes[i].delete(0, END)
    onFocusOut(startTimes[i], 'S', None)
    
    endTimes[i].delete(0, END)
    onFocusOut(endTimes[i], 'E', None)
            
if __name__ == "__main__":
    main()
