from tabulate import tabulate

def print_chart(chart):
    table = []
    for id, (nt, prod, dot_loc), (start,end), history in chart:
        production = ''
        if productions[nt][0] == 0:
            production = nt + ' -> ' + ' '.join(productions[nt][prod+1])
        else:
            production = nt + '->' + productions[nt][1][prod]
        
        string = "id: {0}.prod: {1}.dot_loc: {2}.range: ({3},{4}).history: {5}".format(
            id, production, dot_loc, start, end, history)
        entry = string.split('.')
        table.append(entry)

    print(tabulate(table))
        
# 
string = "They can fish in rivers in December".lower()
words = string.split()


def prod_end(entry):
    N, prod, dot_loc = entry
    if productions[N][0] == 0:
        return len(productions[N][prod+1])
    else: # In Pset
        return 1

def dot_end(entry):
    _, _, dot_loc = entry
    e = prod_end(entry)
    return e == dot_loc
    
def extract(chart):
    ret = []
    for entry in chart:
        id, (N, prod, dot_loc), (start,end), history = entry 
        if N == "S" and start == 0 and end == len(words):
            ret.append(entry)
    return ret
    

productions = {
    "S": [ 0, ["NP","VP"] ],
    "NP": [0, ["N"], ["N","PP"]],
    "PP": [0,["P","NP"]],
    "VP": [0, ["V"], ["V","NP"], ["V","VP"],["VP","PP"]],
    "N": [1, ["it","fish","rivers","december","they"]],
    "P": [1, ["in"]],
    "V": [1, ["can", "fish"]],
}

Pset = ["N", "P", "V"]






def predict(chart):
    for _, (nt, prod, dot_loc), (_,end), _ in chart.copy(): # Loop through edges
        if nt not in Pset and not dot_end((nt, prod, dot_loc)): # Skip some edges
            # nt -> dot N, productions of N are extracted
            N = productions[nt][prod+1][dot_loc]
            if N not in Pset:
                new_prods = productions[N][1:]
                for i,_ in enumerate(new_prods):
                    entry = (N, i, 0, end, end,[])
                    if not entry in chart_contains:
                        chart.append([len(chart), (N, i, 0), (end,end), []])
                        chart_contains.append(entry)
    

def scan(chart):
    for _, (N, prod, dot_loc), (start,end), _ in chart.copy(): # Loop through edges
        if N not in Pset and not dot_end((N, prod, dot_loc)):
            nt = productions[N][prod+1][dot_loc]
            if nt in Pset and end < len(words):
                next_word = words[end]
                if next_word in productions[nt][1]:
                    i = productions[nt][1].index(next_word)
                    entry = (nt, i, 1, start, end+1, [])
                    if entry not in chart_contains:
                        chart.append([len(chart), (nt,i,1),(start,end+1),[]])
                        chart_contains.append(entry)



def complete(chart):
    carryOn = True
    while(carryOn):
        carryOn = False
        for id, (N, prod, dot_loc), (start,end), _ in chart.copy():
            if dot_end((N, prod, dot_loc)): # Dot at the end
                for _, e2, (start2,end2), history in chart.copy():
                    (N2, prod2, dot_loc2) = e2
                    if N2 not in Pset and not(dot_end(e2)) and productions[N2][prod2+1][dot_loc2] == N and start == end2:
                        entry = (N2, prod2, dot_loc2+1, start2, end,history+[id])
                        if entry not in chart_contains:
                            chart_contains.append(entry)
                            chart.append(
                                [len(chart), (N2, prod2, dot_loc2+1), 
                                    (start2, end), history+[id]]
                            )
                            carryOn = True


# ID, Production (Non-terminal, index, dot location),  Range, history
chart = [[0, ("S",0, 0), (0,0), []]]

# To avoid duplicates
# non terminal, index, dot location, start_range, end_range
chart_contains = [("S",0,0,0,0,[])]

last_index = 0 # Where to start in complete step

change = 1
while(change > 0):
    n_entries = len(chart)
    print("Predict")
    predict(chart)
    last_index = len(chart)-1
    print("Scan")
    scan(chart)
    print("Complete")
    complete(chart)
    print_chart(chart)
    _ = input("Give input")
    change = len(chart) - n_entries
    


print("Final chart:")
print_chart(chart)

print("Solutions")
print_chart(extract(chart))