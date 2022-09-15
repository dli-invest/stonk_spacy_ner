#/bin/sh

python generate_pipe.py

python -m spacy package ./output/stonk_pipeline output --name "stonk_pipeline" --version 0.0.1 -f -m data/ref_meta.json --build wheel

cd ./output/en_stonk_pipeline-0.0.1/dist
python -m spacy huggingface-hub push en_stonk_pipeline-0.0.1-py3-none-any.whl