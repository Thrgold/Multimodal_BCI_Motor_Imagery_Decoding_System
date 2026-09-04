"""Export BDF channels in MNE SI units without rounding small EEG voltages to zero."""
import argparse
from pathlib import Path

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    if args.output.exists():parser.error('Output already exists; choose another filename.')
    import mne
    import pandas as pd
    raw=mne.io.read_raw_bdf(args.input,preload=True)
    df=pd.DataFrame(raw.get_data().T,columns=raw.ch_names)
    df.insert(0,'time_seconds',raw.times)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(args.output,index=False,float_format='%.12g')
    print('Exported SI-unit signals; EEG channels are in volts.')
if __name__=='__main__':main()
