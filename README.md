# stonk_spacy_ner
Custom stonk ner tagging via spacy for my various stonk related projects, hosted on huggingspace.

For the initial release, I will just port my regex based entity labelling from spacy as a pipeline as a downloadable file so it can be used everywhere.

## To Publish

If you need to convert spacy to human readable form you can.

```
"python -m spacy package training/model-best packages --name ${vars.name} --version ${vars.version} --force"
```

To publish the pipeline

```
python generate_pipe.py
python -m spacy package ./output/stonk_pipeline output --name "stonk_pipeline" --version 0.0.1 -C
```