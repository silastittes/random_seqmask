Input a fasta of sequence, masks each sequence randomly according to input
parameters. Allows identical masking across the input sequences or random
masking. See help for more details.

Example:

`python random_seqmask.py -T identical -f fake.fa -p 0.01 -m 5 -o fake_mask.fa`

```
usage: random_seqmask.py [-h] [-T [{identical,random}]] -f FASTA_INPUT
                         [-p PENALTY] [-m MISSING_FACTOR] -o OUT_FILE

optional arguments:
  -h, --help            show this help message and exit
  -T [{identical,random}], --mask_type [{identical,random}]
                        Apply identical masking across sequences, requires all
                        input sequence to be the same length, OR applies
                        random masking to each sequence, using the same
                        masking parameters.
  -f FASTA_INPUT, --fasta_input FASTA_INPUT
                        Input is alignment file in fasta format.
  -p PENALTY, --penalty PENALTY
                        Positive real. All else equal, determines how long
                        islands of missing bases will be. Smaller values means
                        shorter islands.
  -m MISSING_FACTOR, --missing_factor MISSING_FACTOR
                        Positive real. All else equal, determines how frequent
                        missing bases will be. Smaller values result in more
                        missingness.
  -o OUT_FILE, --out_file OUT_FILE
                        The file to write output to.
```

The repo includes two other helpful scripts: `fake_seq.py` and `count_missing.py`, which create a really simple fasta sequence to test the masking out on, and  summarize the resulting run lengths of missing and non-missing bases, respectively.

Usage: 

```
python fake_seq.py #modify size and number of sequence in script


#fake_seq.py write fake_mask.fa
python count_missing.py fake_mask.fa
```
