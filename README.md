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
python -m spacy package ./output/stonk_pipeline output --name "stonk_pipeline" --version 0.0.1 -m data/ref_meta.json --build wheel
```

To push to huggingspace
```
cd ./output/en_stonk_pipeline-0.0.1/dist
python -m spacy huggingface-hub push en_stonk_pipeline-0.0.1-py3-none-any.whl
```

Make sure 

```python
https://github.com/explosion/spacy-huggingface-hub

```

is installed