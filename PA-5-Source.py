import tkinter.ttk
import itertools
from tkinter import *
from functools import partial
import matplotlib.pyplot as plot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

valueText = 'Earnings (Ex: 21.50)'
startTimeText = 'Start Time (Int 0-11)'
endTimeText = 'End Time (Int 1-12)'
labels, values, startTimes, endTimes, clearBtns = [], [], [], [], []
errorLbl = None

def main():
    window = Tk()
    window.geometry("1000x640")
    window.title("Earning Maximization Problem")
    window.grid_rowconfigure(0, weight=1)

    ##  Create frames
    frameLeft = Frame(window)
    frameLeft.grid(row=0, column=0, sticky=NS)
    frameMid = Frame(window)
    frameMid.grid(row=0, column=1, sticky=NS)
    frameMid.rowconfigure(0, weight=1)
    frameRight = Frame(window)
    frameRight.grid(row=0, column=2, sticky=NS)

    ##  Place add task button in its initial position
    addTaskBtn = Button(frameLeft, text='+ Add Task', fg='blue', activeforeground='blue',
                        cursor='hand2', bd=0, relief=FLAT)
    addTaskBtn.config(command=partial(addTask, frameLeft, addTaskBtn))
    addTaskBtn.grid(row=39, column=1, pady=(2,0), sticky=W)

    ##  Button to reset input
    resetBtn = Button(frameLeft, text='Reset', cursor='hand2', width=6)
    resetBtn.config(command=partial(onReset, addTaskBtn))
    resetBtn.grid(row=39, column=2, padx=(20,0), pady=(2,0), sticky=W)

    ##  Create arrays to store Entry objects and add first task entry to UI
    addTask(frameLeft, addTaskBtn)

    ##  Divider
    sep = ttk.Separator(frameMid, orient=VERTICAL)
    sep.grid(row=0, column=0, pady=(20,20), padx=(100,50), sticky=NS)

    ##  Display best path
    bestPathLbl = StringVar()
    bestPathLbl.set('')
    label = Label(frameRight, textvariable=bestPathLbl, fg='blue')
    label.grid(row=0, column=0, pady=(10,0), sticky=N)

    ##  Display total number of path options
    totalPathsLbl = StringVar()
    totalPathsLbl.set('')
    totalLabel = Label(frameRight, textvariable=totalPathsLbl, fg='gray64')
    totalLabel.grid(row=1, column=0, pady=(10,0))

    ##  ListBox to display all possible sequences
    listbox = Listbox(frameRight, width=80, height=12, relief=FLAT)
    scrollbar = Scrollbar(frameRight, orient=VERTICAL)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    listbox.grid(row=2, column=0)
    scrollbar.grid(row=2, column=0, sticky=E+NS)

    ##  Canvas for the chart
    #canvas = FigureCanvas(frameRight, width=466, height=210, bg='white')
    #canvas.grid(row=3, column=0, pady=(30,0), sticky=W)

    ##  Button to submit all input
    submitBtn = Button(frameLeft, text='Submit', cursor='hand2', width=6)
    submitBtn.config(command=partial(submit, frameLeft, frameRight, bestPathLbl, listbox, totalPathsLbl))
    submitBtn.grid(row=39, column=2, pady=(2,0), sticky=E)

    ##  Continue to display UI until user exits
    window.mainloop()

##  Add entry fields for another task to the interface
def addTask(frameLeft, addTaskBtn):
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
    label = Label(frameLeft, textvariable=textVar, width=10)
    label.grid(row=4*i, column=0, pady=(10,0))

    ##  Display the three entry fields for new task
    valueEntry = Entry(frameLeft, fg='light grey', relief=FLAT, width=20)
    valueEntry.grid(row=4*i, column=1, pady=(10,0))
    valueEntry.insert(0, valueText)
    valueEntry.bind('<FocusIn>', partial(onFocusIn, valueEntry))
    valueEntry.bind('<FocusOut>', partial(onFocusOut, valueEntry, 'V'))

    startTimeEntry = Entry(frameLeft, fg='light grey', relief=FLAT, width=20)
    startTimeEntry.grid(row=(4*i)+1, column=1, pady=(5,0))
    startTimeEntry.insert(0, startTimeText)
    startTimeEntry.bind('<FocusIn>', partial(onFocusIn, startTimeEntry))
    startTimeEntry.bind('<FocusOut>', partial(onFocusOut, startTimeEntry, 'S'))

    endTimeEntry = Entry(frameLeft, fg='light grey', relief=FLAT, width=20)
    endTimeEntry.grid(row=(4*i)+1, column=2, pady=(5,0), padx=(5,0))
    endTimeEntry.insert(0, endTimeText)
    endTimeEntry.bind('<FocusIn>', partial(onFocusIn, endTimeEntry))
    endTimeEntry.bind('<FocusOut>', partial(onFocusOut, endTimeEntry, 'E'))

    ##  Create button to clear this task's entry fields
    clear = Button(frameLeft, text='x', fg='light gray', activeforeground='light gray',
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
        if not int(startTime) < int(endTime):
            valid = False
            err = 'ERROR: Start Time must be less than End Time'
            return valid, err, index
        
    return valid, err, index

##  If there is an error, display it under the appropriate task entry
def displayError(frameLeft, valid, err, index):
    global errorLbl
    
    if errorLbl is not None:
        errorLbl.destroy()

    if valid == False:
        errVar = StringVar()
        errVar.set(err)

        errorLbl = Label(frameLeft, textvariable=errVar, fg='red')
        errorLbl.grid(row=(4*index)+2, column=1, columnspan=3)

##  Format the best path for display
def formatBestPath(bestPath, maxProfit):
    bestPathStr = 'MAX PROFIT: '
    
    for task in bestPath:
        bestPathStr += 'Task_%s -> ' % task.number

    bestPathStr = bestPathStr[:-4]
    bestPathStr += ', with a total earning of %s.' % maxProfit

    return bestPathStr

##  Format the list of all paths for display
def formatPaths(paths):
    pathsStrList = []

    count = 1
    for path in paths:
        profit = 0
        pathStr = 'Option %s: ' % count
        count += 1
        
        for task in path:
            pathStr += 'Task_%s -> ' % task.number
            profit += task.value

        pathStr = pathStr[:-4]
        pathStr += ', with a total earning of %s.' % profit

        pathsStrList.append(pathStr)

    return pathsStrList

##  Create string that says the total number of paths
def formatTotalPaths(paths):
    totalPathsStr = 'There are %s options to select different sets of tasks.' % len(paths)
    return totalPathsStr

##  Display the best path and the list of all possible paths
def displayPaths(bestPathLbl, bestPathStr, listbox, pathsStrList, totalPathsLbl, totalPathsStr):
    bestPathLbl.set(bestPathStr)
    totalPathsLbl.set(totalPathsStr)

    listbox.delete(0, END)
    for i in pathsStrList:
        listbox.insert(END, i)

##  Create a chart for the tasks
def createChart(tasks, frameRight):
    figure = plot.figure()
    chart = figure.add_subplot(111)
    chart.set_title("Tasks")

    taskNames = [None] * (len(tasks) + 1)
    for task in tasks:
        taskNames[task.number - 1] = ('Task %s' % task.number)
    
    chart.set_xlim(left=0, right=12)
    chart.set_ylim(bottom=0, top=len(taskNames))
    chart.set_xticks(range(0,13,1))
    chart.set_yticks(range(1,len(taskNames),1))
    chart.set_yticklabels(taskNames)
    chart.grid(color='grey', linestyle=':')

    for task in tasks:
        number = task.number
        width = task.endTime - task.startTime
        left = task.startTime

        chart.barh(number, width, 0.5, left, align='center', edgecolor=(0.2, 0.4, 0.6, 0.6), color=(0.2, 0.4, 0.6, 0.6))

    canvas = FigureCanvasTkAgg(figure, master=frameRight)
    canvas.draw()
    canvas.get_tk_widget().grid(row=3, column=0, pady=(30,0), sticky=W)
    canvas.get_tk_widget().config(width=466, height=220)

##  Represents each task as a single object
class Task:
    def __init__(self, number, startTime, endTime, value):
        self.number = number
        self.startTime = int(startTime)
        self.endTime = int(endTime)
        self.value = float(value)

    def __repr__(self):
        return "Task(number={}, startTime={}, endTime={}, value={})".format(self.number, self.startTime, self.endTime, self.value)

##  Convert data from UI into Task objects
def inputsToObjects():
    rawData = zip(
        ((x + 1) for x in range(0, len(startTimes))),
        (x.get() for x in startTimes),
        (x.get() for x in endTimes),
        (x.get() for x in values),
        )

    objects = [Task(*x) for x in rawData]
    ##  Tasks must be sorted by endTime
    objects.sort(key=lambda x: x.endTime)
    return objects

##  Find latest doable task before tasks[i]
def nextDoableTask(tasks, i):
    startingTask = tasks[i]
    i -= 1
    while i >= 0:
        if tasks[i].endTime <= startingTask.startTime:
            return tasks[i], i
        i -= 1
    return None, None

##  Return optimal schedule and resulting profit.
def maximizeEarnings(tasks):
    length = len(tasks)

    values = [None]*length
    chosenTasks = [None]*length

    for n in range(0, len(tasks)):

        profitIncludingCurrent = tasks[n].value
        tasksIncludingCurrent = [tasks[n]]
        t, i = nextDoableTask(tasks, n)
        if t is not None:
            profitIncludingCurrent += values[i]
            tasksIncludingCurrent = chosenTasks[i] + tasksIncludingCurrent

        if n == 0:
            profitExcludingCurrent = 0
            tasksExcludingCurrent = []
        else:
            profitExcludingCurrent = values[n - 1]
            tasksExcludingCurrent = chosenTasks[n - 1]

        if profitIncludingCurrent >= profitExcludingCurrent:
            values[n] = profitIncludingCurrent
            chosenTasks[n] = tasksIncludingCurrent
        else:
            values[n] = profitExcludingCurrent
            chosenTasks[n] = tasksExcludingCurrent

    return chosenTasks[n], values[-1]

## Calculate the amount of overlap between two tasks.
def overlap(a, b):
    return min(a[1], b[1]) - max(a[0], b[0])

## Calculate all possible paths without collisions.
def calculateValidPaths(tasks, n):
    results = []

    for i in range(1, n + 1):
        for path in list(itertools.combinations(tasks, r=i)):
            ##  Check for collisions before adding a path.
            valid = True
            for a, b in itertools.combinations(path, 2):
                collision = overlap([a.startTime, a.endTime], [b.startTime, b.endTime])
                    
                if collision > 0:
                    valid = False
                    break

            ##  If the path is valid add it to the results.
            if valid:
                results.append(path)

    ##  Remove all unnecessary subsets.
    #results = list(filter(lambda a: not any(set(a) < set(b) for b in results), results))

    return results

##  Calls functions to check entries, run the algorithm, and display output
def submit(frameLeft, frameRight, bestPathLbl, listbox, totalPathsLbl):
    ##  Check entries
    valid, err, index = checkEntries()
    displayError(frameLeft, valid, err, index)

    ##  Execute if entries are valid
    if valid == True:
        tasks = inputsToObjects()
        
        ##  Run the algorithm
        bestPath, maxProfit = maximizeEarnings(tasks)

        ##  Display output
        createChart(tasks, frameRight)
        bestPathStr = formatBestPath(bestPath, maxProfit)
        pathsStrList = calculateValidPaths(tasks, len(tasks))
        pathsStrList = formatPaths(pathsStrList)
        totalPathsStr = formatTotalPaths(pathsStrList)
        
        displayPaths(bestPathLbl, bestPathStr, listbox, pathsStrList, totalPathsLbl, totalPathsStr)

if __name__ == "__main__":
    main()
