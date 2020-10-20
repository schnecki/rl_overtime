#!/bin/bash
# gnuplot must be installed for this script to work
# Howto: run "sh plot.sh" in the command line once
# ReinforcementLearning/avg_reward_adjusted_agent.py is training
# The files "q_values_learned_results.csv" and "rewards_per_period.csv" must exist
# (they get created automatically by avg_reward_adjusted_agent.py when it trains the ARA_DiRL model)

gnuplot -e "set key autotitle columnhead; plot for [col=2:4] 'aradirl_q_values_learned_results.csv' using 1:col with lines; pause mouse close; " &

gnuplot -e "set key autotitle columnhead bottom right; set title 'Rewards per period'; set ylabel 'Normalized reward'; set xlabel 'Period'; plot for [col=2:3] 'aradirl_rewards_per_period.csv' using 1:col with points; pause mouse close; " &
