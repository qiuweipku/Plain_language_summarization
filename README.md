# Plain Language Summarization
This repository provides the dataset and model training details of the novel task of automated generation of lay language summaries of biomedical scientific reviews. Please refer to our AAAI-2021 paper [Automated Lay Language Summarization of Biomedical Scientific Reviews](https://arxiv.org/abs/2012.12573) for more details.

## Installation
Run
```
git clone https://github.com/qiuweipku/Plain_language_summarization.git
cd Plain_language_summarization
```

## Datasets
### CDSR (Cochrane Database of Systematic Review) dataset
Please follow the following steps to generate the CDSR dataset:
1. Click on the following link https://www.cochranelibrary.com/cdsr/reviews
2. Click the "Select all" button and then click "Export selected citation(s)"
3. Select "Include abstract", then save the file as "citation-export.txt".
4. Move "citation-export.txt" to './CDSR_data/'
5. Run
```
cd ./CDSR_data/
python run_preprocessing.py
```

The preprocessed CDSR dataset will be saved in "./CDSR_data/CDSR/". The "xxx.source" files include the abstracts. The "xxx.target" files include the plain language summarizations.

Note that some articals may be removed from the Cochrane Library when the database is updated, so the preprocessed dataset may include less samples than the data we used in our work. 

### CNN / Daily Mail summarization dataset
Follow the instructions [here](https://github.com/abisee/cnn-dailymail) to download the original CNN and Daily Mail datasets.

### PubMed abstracts
Download the the PMC articles dataset from [here](https://www.kaggle.com/cvltmao/pmc-articles)

## Model
### BART
For BART model, we use the [Fairseq BART](https://github.com/pytorch/fairseq/tree/master/examples/bart) implementation. Below list the hyperparameters for training BART on the CDSR data.
```
TOTAL_NUM_UPDATES=50000
WARMUP_UPDATES=500
LR=3e-05
MAX_TOKENS=2048
UPDATE_FREQ=32
max-tokens=2048
required-batch-size-multiple=1
arch=bart_large
criterion=label_smoothed_cross_entropy
label-smoothing=0.1
dropout=0.1
attention-dropout=0.1
weight-decay=0.01
optimizer=adam
adam-betas=(0.9, 0.999)
adam-eps=1e-08
clip-norm=0.1
lr-scheduler=polynomial_decay
lr=3e-05
total-num-update=50000
warmup-updates=500
update-freq=32
```
Below list the hyperparameters for testing BART on the CDSR data.
```
beam=4
lenpen=2.0
max_len_b=1000
min_len=300
no_repeat_ngram_size=3
```

### BERT extractive
For BERT extractive model, we use the [presumm](https://github.com/nlpyang/presumm) implementation. Below list the hyperparameters for training BERT extractive on the CDSR data.
```
ext_dropout=0.1
lr=2e-3
batch_size=140
train_steps=50000
accum_count=2
use_interval=true
warmup_steps=10000
max_pos=512
```
Below list the hyperparameters for testing BERT extractive on the CDSR data.
```
use_interval=true
max_pos=512
max_length=700
alpha=0.95
min_length=100
```
Other hyperparameters are set to default values.

### Pointer-generator 
For pointer-generator  model, we use the [neural-summ-cnndm-pytorch](https://github.com/lipiji/neural-summ-cnndm-pytorch/) implementation. Below list the hyperparameters for training Pointer-generator on the CDSR data.
```
MIN_LEN_X=300
MIN_LEN_Y=100
MAX_LEN_X=1000
MAX_LEN_Y=700
BATCH_SIZE =4
```
Below list the hyperparameters for testing Pointer-generator on the CDSR data.
```
IS_UNICODE=False
BATCH_SIZE=16
MIN_LEN_PREDICT=100
MAX_LEN_PREDICT=700
MAX_BYTE_PREDICT=None
REMOVES_PUNCTION=False
```
Other hyperparameters are set to default values.

## Citation
For now, cite [the Arxiv paper](https://arxiv.org/abs/2012.12573):

```
@article{guo2020automated,
  title={Automated Lay Language Summarization of Biomedical Scientific Reviews},
  author={Guo, Yue and Qiu, Wei and Wang, Yizhong and Cohen, Trevor},
  journal={arXiv preprint arXiv:2012.12573},
  year={2020}
}
```


## Contact information

For help or issues, please submit a GitHub issue. Please contact Wei Qiu
(`wqiu0528@cs.washington.edu`) for communication related to this repository.