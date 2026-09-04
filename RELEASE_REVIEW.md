# In-place release review

- Renamed non-English files to descriptive English names; document contents were not translated or certified.
- Corrected README claims: missing real-time frontend/backend and multimodal fusion are not presented as implemented.
- Disabled the legacy port-killing launcher; fixed model imports to export only CNN_LSTM, which is actually included.
- Removed hard-coded personal recording paths from conversion/inspection tools; added argument parsing and overwrite protection.
- BDF conversion uses SI units and higher precision, and no longer invents an all-zero stimulus channel. This changes the legacy conversion behavior deliberately; validate units before preprocessing.
- Preserved local office documents, photo archive and output.csv while excluding them from publication. These were not opened or certified as anonymized.
- Existing user deletions were not restored. The remote URL is retained. With owner authorization, main was rebuilt as a single audited initial commit; local excluded materials were preserved.
- Source syntax and a synthetic model forward pass are checked; GUI/hardware integration, raw-data processing, training and scientific efficacy remain unverified.
- Model and electrode-file provenance are not established by file presence. No blanket license was added.
