import numpy as np
import argparse 


parser = argparse.ArgumentParser(description="Input a fasta of sequence, masks each sequence randomly according to input parameters. Allows identical masking across the input sequences or random masking. See help for more details.")

parser.add_argument("-T", "--mask_type", nargs = "?", 
	  	    choices = ["identical", "random"],
	            default = "random",
		    help = "Apply identical masking across sequences, requires all input sequence to be the same length, OR applies random masking to each sequence, using the same masking parameters.")

parser.add_argument("-f", "--fasta_input", type = str, required = True,
		    help = "Input is alignment file in fasta format.",
    		    )

parser.add_argument("-p", "--penalty", type = float, required = True,
		    help = "Positive real. All else equal, determines how long islands of missing bases will be. Smaller values means shorter islands.")

parser.add_argument("-m", "--missing_factor", type = float, required = True,
		    help = "Positive real. All else equal, determines how frequent missing bases will be. Smaller values result in more missingness.")

parser.add_argument("-o", "--out_file", type = str, required = True,
		    help = "The file to write output to.")

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

#generate a list of 0s and 1s for nucleotide or mask state
def mask_list(seq, penalty, missing_factor):
    Len = len(seq) - 1
    to_missing = 1/(missing_factor*Len*penalty)
    to_base = 1/(Len * penalty)
    state = [0]
    for i in range(Len):
        if(state[-1] == 0):
            state.append(np.random.binomial(1, to_missing, 1)[0])
        else: 
            state.append(np.random.binomial(1, 1-to_base, 1)[0])
    return state


#input fasta, output fasta
def mask_ref(seq_file, out_file, mask_type, penalty, missing_factor):

    fout = open(out_file, "w")
 
    seqs = fasta_list(seq_file)
    seq_names = list(seqs.keys())

    if mask_type == "identical":
        
        seq_len = len(seqs[seq_names[0]])
        state = mask_list(seqs[seq_names[0]], penalty, missing_factor)

        for header, seq in seqs.items():
            if len(seq) == seq_len:
                mask_ref = ""
                for idx, st in enumerate(state):
                    if st == 1:
                        mask_ref += "N"
                    else:
                        mask_ref += seq[idx]
            else:
                raise ValueError("sequence lengths are not all equal.")

            print(f">{header}_mask", file=fout)
            print(mask_ref, file = fout)

    elif mask_type == "random":
        for header, seq in seqs.items():
            state = mask_list(seq, penalty, missing_factor)
            mask_ref = ""
            for idx, st in enumerate(state):
                if st == 1:
                    mask_ref += "N"
                else:
                    mask_ref += seq[idx]
            print(f">{header}_mask", file=fout)
            print(mask_ref, file = fout)

    else:
        raise ValueError("mask_type must be 'identical' or 'random'")


#run program
mask_ref(args.fasta_input, args.out_file, args.mask_type, args.penalty, args.missing_factor)
