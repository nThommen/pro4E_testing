# src/evaluate.py
import datetime
import pandas as pd
import matplotlib.pyplot as plt
CSV="results.csv"
def init(): 
    if not pd.io.common.file_exists(CSV):
        open(CSV,"w").write("timestamp,test,roll,pitch,yaw\n")
def log_result(name, diffs):
    init()
    ts=datetime.datetime.now().isoformat()
    with open(CSV,"a") as f:
        f.write(f"{ts},{name},{diffs[0]},{diffs[1]},{diffs[2]}\n")
def plot_results():
    df=pd.read_csv(CSV,parse_dates=["timestamp"]).set_index("timestamp")
    df[["roll","pitch","yaw"]].plot()
    plt.show()