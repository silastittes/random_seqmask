import re
import numpy as np
from scipy import stats
import argparse 

parser = argparse.ArgumentParser(description="Get average size and frequency of runs of missing or non-missing bases.")

parser.add_argument("reference", type=str, help="Fasta formatted reference file")

args = parser.parse_args()

#read sequences into dictionary
def fasta_list(file_name):
    seq_dict = dict()
    with open(file_name) as fa:
        for ln in fa:
            line = ln.strip()
            if len(line) > 0:
                if line[0] == ">":
                    seq_name = line[1:]
                    seq_dict[seq_name] = ""
                else:
                    seq_dict[seq_name] += ln.strip()
    return seq_dict


#[i.count('N') for i in re.split("[ATGC]", ss) if len(i) > 0]
def count_N_runs(seq, count_str = "N", split_str = "[ATGC]"):
    return [i.count(count_str) for i in re.split(split_str, seq) if len(i) > 0]

def count_base_runs(seq, count_str =  ["A", "T", "G", "C"], split_str = "N"): 
    return [sum([i.count(b) for b in count_str]) for i in re.split(split_str, seq) if len(i) > 0]

seqs = fasta_list(args.reference)

def stats(runs):
    
    av = np.mean(runs)
    sd = np.std(runs)
    mn = np.min(runs)
    mx = np.max(runs)
    print(f"min\tmean\tmax\tstandard deviation\tlength")
    print(f"{mn:.2f}\t{av:.2f}\t{mx:.2f}\t{sd:.2f}\t{len(runs)}")
    

for name, seq in seqs.items():
    print("missing")
    stats(count_N_runs(seq))
    print("nucleotide")
    stats(count_base_runs(seq))

    #mruns = count_N_runs(seq)
    #nruns = count_base_runs(seq)

    #print(f"mean missing lengths: {np.mean(mruns):.2f}\nstandard deviation of missing lengths: {np.std(mruns):.2f}\nnumber of missing blocks:{len(mruns)}")
    #print(f"mean nucleotide lengths: {np.mean(nruns):.2f}\nstandard devisation of nucleotide lengths: {np.std(nruns):.2f}\nnumer of nucleotide blocks: {len(nruns)}")
