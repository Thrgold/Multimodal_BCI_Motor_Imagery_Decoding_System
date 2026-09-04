"""Inspect the first SNIRF stimulus group; not a full SNIRF validator."""
import argparse

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    args=parser.parse_args()
    import h5py
    with h5py.File(args.input,'r') as f:
        if 'nirs/stim1/data' not in f:parser.error('Missing nirs/stim1/data.')
        data=f['nirs/stim1/data'][:]
        print('Stimulus array shape:',data.shape)
        if data.ndim==2 and len(data):print('First onset (seconds):',float(data[0,0]))
if __name__=='__main__':main()
