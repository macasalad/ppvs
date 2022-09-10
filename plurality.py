import csv
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from math import ceil

def plur_show_figure(plur_figs):
  "shows figure of election"
  st.write(plur_figs[0])

def plurality(csvfilename):
  position = csvfilename.columns[0]
  votes = []
  candidate_names = set()
  log = "Candidate Votes\n"

  for index, row in csvfilename.iterrows():
      for candid in row:
        votes.append(candid)
  
  for name in votes:
    candidate_names.add(name)
      
  #print(votes)
  #print(candidate_names)
  
  D = {}
  
  for items in candidate_names:
          D[items] = votes.count(items)

  winner = ""
  winning_votes = -1
  for candidate, vote_c in D.items():
    if winning_votes < vote_c:
      winning_votes = vote_c
      winner = candidate
    log += candidate + ' : ' + str(vote_c) + '\n'
  
  plur_figs = []
  plur_fig = plt.figure()
 
  plt.bar(range(len(D)), list(D.values()), align='center')
  plt.xticks(range(len(D)), list(D.keys()))

  win = (len(votes)//2) + 1
  plt.axhline(y=win, color='r', linestyle='-')
  #plt.show()
  plt.tight_layout()
  plt.savefig("election_result" + "/" + "plurality_result_" + position + ".png")
  plur_figs.append(plur_fig)

  #print(log)
  winner += " won the election with " + str(winning_votes) + "." 
  return [winner, winning_votes, plur_figs, log]