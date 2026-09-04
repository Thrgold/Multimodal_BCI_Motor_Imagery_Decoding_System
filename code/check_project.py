"""Check source syntax and the included model using synthetic input only."""
from pathlib import Path
import ast
import torch
from models import CNN_LSTM
root=Path(__file__).resolve().parents[1]
for f in (root/'code').rglob('*.py'):ast.parse(f.read_text(encoding='utf-8-sig'))
torch.manual_seed(0)
model=CNN_LSTM(n_channels=22,n_samples=64).eval()
with torch.no_grad():out=model(torch.zeros(2,22,64))
assert out.shape==(2,4) and torch.isfinite(out).all()
print('PASS: Python syntax and synthetic CNN-LSTM forward shape (2, 4). No accuracy claim.')

from preprocess_eeg import preprocess_eeg_bdf, _read_and_classify_events
for action in [lambda: preprocess_eeg_bdf('not_opened.csv','not_opened.bdf'),
               lambda: _read_and_classify_events('not_opened.bdf', {})]:
    try: action()
    except ValueError: pass
    else: raise AssertionError('Missing protocol configuration was not rejected.')
print('PASS: missing annotation mapping/channel/unit settings rejected before data access.')
