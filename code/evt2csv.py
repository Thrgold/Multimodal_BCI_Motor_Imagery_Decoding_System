"""Export BDF annotations with explicit input/output paths."""
import argparse
from pathlib import Path

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input');parser.add_argument('output',type=Path)
    args=parser.parse_args()
    if args.output.exists():parser.error('Output already exists.')
    import mne
    import pandas as pd
    annot=mne.io.read_raw_bdf(args.input,preload=False).annotations
    args.output.parent.mkdir(parents=True,exist_ok=True)
    pd.DataFrame({'onset':annot.onset,'duration':annot.duration,'description':annot.description}).to_csv(args.output,index=False)
if __name__=='__main__':main()
