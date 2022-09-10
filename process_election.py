from collections import deque
import pandas as pd

class Candid_data:
    def __init__(self, ballots, vote_c, elim):
        self.ballots = ballots
        self.vote_c = vote_c
        self.elim = elim

    def ret_vote_c(self):
        return self.vote_c

    def ret_ballots(self):
        return self.ballots
    
    def is_elim(self):
        return self.elim

    def add_ballot(self, ballot):
        self.ballots.append(ballot)
        self.vote_c += 1
    
    def make_elim(self):
        self.elim = True

class Winner:
    def __init__(self, name, votes):
        self.name = name
        self.votes = votes
    
    def set_winner(self, name, votes):
        self.name = name
        self.votes = votes
    
    def is_Winner(self):
        if (self.votes > 0):
            return True
        else:
            return False
    
    def ret_name(self):
        return self.name
    
    def ret_votes(self):
        return self.votes

def process_ballot(csvf):
    ballots = []
    voter_c = len(csvf)
    cand_c = len(csvf.columns)

    for index, row in csvf.iterrows():
        ballot = deque()
        for i in range(cand_c):
            ballot.append(row[i])
        ballots.append(ballot)
    
    return [ballots, voter_c, cand_c] 

def process_iv(ballot_list, cand_c):
    initial_db = {}
    for name in ballot_list[0]:
        initial_db[name] = [0 for i in range(cand_c)]

    for ballot in ballot_list:
        for i in range(cand_c):
            initial_db[ballot[i]][i] += 1
    
    return initial_db

def eliminate(initial_db, rem_candids, db):
    l_votes = []
    least_fpv = 100000000
    for candid in rem_candids:
        least_fpv = min(db[candid].ret_vote_c(), least_fpv)

    for candid in rem_candids:
        if db[candid].ret_vote_c() == least_fpv:
            l_votes.append(candid)
    
    if len(l_votes) == 1:
        return l_votes
    else:
        elim = []
        valid_votes = []
        for candid in l_votes:
            valid_votes.append(initial_db[candid]) # CONSIDER FIRST PREF VOTES FOR TIEBREAKER
        least_vote = min(valid_votes)

        for candid in l_votes:
            if initial_db[candid] == least_vote:
                elim.append(candid)
        
        return elim

def print_fvotes(db, announce):
    L = []
    L.append(announce+"\n")
    for candid, data in db.items():
        if data.is_elim():
            continue
        L.append("  " + candid + ": " + str(data.ret_vote_c()) + "\n")
    L.append("\n")
    return L

def save_vote(db, file):
    sv_db = {}
    for candid, data in db.items():
        if data.is_elim():
            continue
        sv_db[candid] = data.ret_vote_c()
    
    rnd_votes = ''
    for candid, vote in sv_db.items():
        rnd_votes += candid + "|" + str(vote) + ";"
    file.append(rnd_votes)
    return file

def calc_winner(csvf):
    log = ""
    save_votes = []
    ballot_list, voter_c, cand_c = process_ballot(csvf)
    majority_c = voter_c//2 + 1
    
    initial_db = process_iv(ballot_list, cand_c)
    
    db = {}
    rem_candids = set()
    for name in ballot_list[0]:
        db[name] = Candid_data([], 0, False)
        rem_candids.add(name)

    for ballot in ballot_list:
        db[ballot[0]].add_ballot(ballot)
	
    winner = Winner(" ", 0)
    round = 1
    for line in print_fvotes(db, "Preliminary Votes:"):
        log += line

    save_votes = save_vote(db, save_votes)

    while(True):
        for candid, data in db.items():
            if data.is_elim():
                continue

            if (data.ret_vote_c() >= majority_c):
                winner.set_winner(candid, data.ret_vote_c())
                break
       
        if (winner.is_Winner()) or round == cand_c:
            break

        elim_candids = eliminate(initial_db, rem_candids, db)

        if len(elim_candids) == len(rem_candids):
            break
        
        log += "[ELIMINATION ROUND " + str(round) + "]\n"

        log += "Eliminated Candidate/s: | "
        for candid in elim_candids:
            log += candid + " | "
        log += '\n'

        added_votes = {}
        for name in rem_candids:
            added_votes[name] = 0

        for candid in elim_candids:
            db[candid].make_elim()
            rem_candids.remove(candid)
            added_votes.pop(candid, None)

            for ballot in db[candid].ret_ballots():
                while(True):
                    ballot.popleft()

                    if (db[ballot[0]].is_elim() == False):
                        db[ballot[0]].add_ballot(ballot)
                        added_votes[ballot[0]] += 1
                        break

                    elif len(ballot) == 1:
                        log += "ERROR: EXHAUSTED BALLOT \n"
                        break
        
        log += "\nTransferred Votes:\n"
        for candid, votes in added_votes.items():
            log += "  " + str(votes) + " --> " + candid + "\n"

        for line in print_fvotes(db, "\nUpdated Votes:"):
            log += line

        save_votes = save_vote(db, save_votes)
        round += 1

    log += "[ELECTION RESULT]\n"
    res = ''
    if (winner.ret_votes == 0):
        res = "No candidate won the election."
    else:
        res = winner.ret_name() + " won the election with " + str(winner.ret_votes()) + " final votes."
    log += res + "\n"

    return [majority_c, voter_c, log, save_votes, res]
    # log - election results per round
    # save_votes - for graph processing