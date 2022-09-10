import matplotlib.pyplot as plt
import streamlit as st

def make_db(lines):
    "Make a list of dictionaries out of the txt file"
    dblist = []
    round = 0
    for Xx in lines:
        x = Xx[:-1]
        temp_db = {}
        data_list = [i for i in x.split(';')]
        #print(data_list)

        for data in data_list:
            candid, vote = data.split('|')
            temp_db[candid] = int(vote)

        dblist.append(temp_db)
        round += 1

    return [dblist, round]

def alph_candids(db):
    "Returns an alphabetical list of candidates"
    lst = []
    for candid in db.keys():
        if candid == "Abstain":
            continue
        lst.append(candid)

    lst.sort()
    if "Abstain" in db.keys():
        lst.append("Abstain")

    return lst

def make_graph(x, y, gtitle, maj_c, voter_c, figs):
    clr = {0 : 'blue',
             1 : 'orange',
             2 : 'limegreen',
             3 : 'magenta',
             4 : 'gold',
             5 : 'palevioletred',
             6 : 'cyan'
    }

    lgnd = []
    r = len(y)-1
    fig = plt.figure()
    while(r >= 0):
        #print(r)
        if r != 0 and y[r] == y[r-1]: # remove legends that don't appear on the graph
            r -= 1
            continue
        plt.barh(x, y[r], color=clr[r])
        
        if r == 0:
            lgnd.append("Preliminary Votes")
        else:
            lgnd.append("Round " + str(r) + " Elim")
        r -= 1
    
    plt.ylabel("Candidates")
    plt.xlabel("No. of First Preference Votes")
    plt.legend(lgnd)
    plt.xlim([0, voter_c])
    plt.axvline(x=maj_c, color='r', linestyle='-')
    plt.title(gtitle)
    #plt.show()
    plt.tight_layout()
    plt.savefig("election_result" + "/" + gtitle + ".png")
    figs.append(fig)

def make_figures(lines, maj_c, voter_c):
    db, round = make_db(lines)
    #print(db)
    #print(round)
    figs = []
    titles = []
    for rnd in range(round):
        x_candids = alph_candids(db[rnd])
        y_vals = []
        for rnd_i in range(rnd+1):
            temp_lst = []
            for candid in x_candids:
                temp_lst.append(db[rnd_i][candid])
            y_vals.append(temp_lst)
            #print(temp_lst)
        
        gtitle = "Round " + str(rnd) + " Elimination"
        if rnd == 0:
            gtitle = "Preliminary Votes"
        #print(y_vals)
        titles.append(gtitle)
        make_graph(x_candids, y_vals, gtitle, maj_c, voter_c, figs)
    return [figs, titles]

def show_figures(figs, titles):
    for i in range(len(figs)):
        st.subheader(titles[i])
        st.write(figs[i])
