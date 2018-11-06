from tkinter import *
from functools import partial

valueText = 'Earnings (Ex: 21.50)'
startTimeText = 'Start Time (Int 0-11)'
endTimeText = 'End Time (Int 1-12)'
labels, values, startTimes, endTimes, clearBtns = [], [], [], [], []
errorLbl = None

def main():
    window = Tk()
    window.geometry("1000x700")
    window.title("Earning Maximization Problem")

    ##  Place add task button in its initial position
    addTaskBtn = Button(window, text='+ Add Task', fg='blue', activeforeground='blue',
                        cursor='hand2', bd=0, relief=FLAT)
    addTaskBtn.config(command=partial(addTask, window, addTaskBtn))
    addTaskBtn.grid(row=39, column=1, pady=(2,0), sticky=W)

    ##  Button to reset input
    resetBtn = Button(window, text='Reset', cursor='hand2', width=6)
    resetBtn.config(command=partial(onReset, addTaskBtn))
    resetBtn.grid(row=39, column=2, padx=(20,0), pady=(2,0), sticky=W)

    ##  Button to submit all input
    submitBtn = Button(window, text='Submit', cursor='hand2', width=6)
    submitBtn.config(command=partial(submit, window))
    submitBtn.grid(row=39, column=2, pady=(2,0), sticky=E)

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
    labels.append(label)
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

##  Reset all user input
def onReset(addTaskBtn):
    ##  Remove all task entry fields except for the first task
    if len(values) > 1:
        for i in range(len(values) - 1, 0, -1):
            onClear(i)

            labels[i].destroy()
            values[i].destroy()
            startTimes[i].destroy()
            endTimes[i].destroy()
            clearBtns[i].destroy()

            labels.pop()
            values.pop()
            startTimes.pop()
            endTimes.pop()
            clearBtns.pop()

    ##  Clear the first task's entry fields
    onClear(0)

    ##  Remove error message if there is one
    if errorLbl is not None:
        errorLbl.destroy()

    ##  Replace the add task button
    addTaskBtn.grid(row=39, column=1, pady=(2,0), sticky=W)

##  For each task, check that:
##  All fields are filled out (or all are blank)
##  The earnings entry is a float value >= 0
##  Start time is an integer between 0 and 11
##  End time is an integer between 1 and 12
##  Start time is less than end time
def checkEntries():
    disallowedStrings = [valueText, startTimeText, endTimeText, '']
    numTasks = len(values)
    valid = True
    err = ''
    index = None

    for i in range(0, numTasks):
        index = i
        value = values[i].get()
        startTime = startTimes[i].get()
        endTime = endTimes[i].get()

        ##  Make sure all fields are filled out
        for j in [value, startTime, endTime]:
            if j in disallowedStrings:
                valid = False
                err = 'ERROR: Field(s) left blank.'
                return valid, err, index

        ##  Check the earnings entry
        try:
            if float(value) < 0:
                valid = False
                err = 'ERROR: Earnings must be a positive value.'
                return valid, err, index
        except:
            valid = False
            err = 'ERROR: Earnings must be a float value.'
            return valid, err, index

        ##  Check the startTime entry
        try:
            if int(startTime) not in range(0, 12):
                valid = False
                err = 'ERROR: Start Time must be between 0 - 11'
                return valid, err, index
        except:
            valid = False
            err = 'ERROR: Start Time must be an int between 0 - 11'
            return valid, err, index
        
        ##  Check the endTime entry
        try:
            if int(endTime) not in range(1, 13):
                valid = False
                err = 'ERROR: End Time must be between 1 - 12'
                return valid, err, index
        except:
            valid = False
            err = 'ERROR: End Time must be an int between 1 - 12'
            return valid, err, index

        ##  Check that startTime < endTime
        if not startTime < endTime:
            valid = False
            err = 'ERROR: Start Time must be less than End Time'
            return valid, err, index
        
    return valid, err, index

##  If there is an error, display it under the appropriate task entry
def displayError(window, valid, err, index):
    global errorLbl
    
    if errorLbl is not None:
        errorLbl.destroy()

    if valid == False:
        errVar = StringVar()
        errVar.set(err)

        errorLbl = Label(window, textvariable=errVar, fg='red')
        errorLbl.grid(row=(4*index)+2, column=1, columnspan=3)

##  Calls functions to check entries, run the algorithm, and display output
def submit(window):
    ##  Check entries
    valid, err, index = checkEntries()
    displayError(window, valid, err, index)

if __name__ == "__main__":
    main()
