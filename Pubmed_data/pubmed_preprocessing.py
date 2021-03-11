import pandas as pd
import re
from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.tokenize import sent_tokenize, word_tokenize
import numpy as np
import random
import warnings
import csv
warnings.filterwarnings('ignore')

print('Start preprocessing Pubmed dataset')


    
def masking(sent):
    mask_word_num = 0
    sent_len = len(sent)
    index = [i for i in range(len(sent))]
    
    while mask_word_num < 0.35*sent_len:
        mask_len = np.random.poisson(lam=3.0)
        anchor = np.random.choice(index, 1)[0]
        for i in range(mask_len):
            if (anchor+i < sent_len) & (anchor+1 in index) & (mask_word_num < 0.35*sent_len):
                index.remove(anchor+i)
                mask_word_num += 1
            else:
                break
            
    new_sent = []
    if index[0] != 0:
        new_sent.append('[MASK]')
    new_sent.append(sent[index[0]])
    for i in range(1, len(index)):
        if index[i]-index[i-1] != 1:
            new_sent.append('[MASK]')
        new_sent.append(sent[index[i]])
    new_sent = TreebankWordDetokenizer().detokenize(new_sent)
    return new_sent


if not os.path.isdir('./pubmed_transformed/'):
    os.mkdir('./pubmed_transformed/')

if not os.path.isdir('./pubmed_preprocessed/'):
    os.mkdir('./pubmed_preprocessed/')
    
transformed_abstract = open("./pubmed_transformed/transformed_abstract.txt","w")
original_abstract = open("./pubmed_transformed/original_abstract.txt","w")

file_list = ['./a_b.csv', './c_h.csv', './i_n.csv', './o_z.csv']
for file_name in file_list:
    print(file_name)
    num = 0
    error = 0
    with open(file_name, 'r') as file:
        my_reader = csv.reader(file, delimiter=',')
        next(my_reader)
        for row in my_reader:
            if len(row) == 2:
                if len(row[1]) < 10:
                    error += 1
                    continue
                para = re.sub(r'[\r\n]+', ' ', row[1])
                sentences = sent_tokenize(para)
                new_sentences = []
                for sent in sentences:
                    sent = TreebankWordTokenizer().tokenize(sent)
                #     sent = word_tokenize(sent)
                    new_sent = masking(sent)
                    new_sentences.append(new_sent)
                random.shuffle(new_sentences)
                new_para = TreebankWordDetokenizer().detokenize(new_sentences)
                original_abstract.write(para+'\n')
                transformed_abstract.write(new_para+'\n')
                num += 1
            else:
                error += 1
            if num % 10000 == 0:
                original_abstract.flush()
                transformed_abstract.flush()
original_abstract.close()
transformed_abstract.close()

print('%d pubmed abstracts are transformed.' % num)

transformed_abstract = open('./pubmed_transformed/transformed_abstract.txt', 'r')
original_abstract = open('./pubmed_transformed/original_abstract.txt', 'r')
train_source = open("./pubmed_preprocessed/train.source","w")
train_target = open("./pubmed_preprocessed/train.target","w")
val_source = open("./pubmed_preprocessed/val.source","w")
val_target = open("./pubmed_preprocessed/val.target","w")
    
val_num = 0
train_num = 0
for trans_abs, ori_abs in zip(transformed_abstract, original_abstract):
    trans_abs = trans_abs.strip()
    ori_abs = ori_abs.strip()
    if val_num < 13000:
        if np.random.choice(['train', 'val'], p = [0.9, 0.1])=='val':
            val_source.write(trans_abs+'\n')
            val_target.write(ori_abs+'\n')
            val_num += 1
        else:
            train_source.write(trans_abs+'\n')
            train_target.write(ori_abs+'\n')
            train_num += 1
    else:
        train_source.write(trans_abs+'\n')
        train_target.write(ori_abs+'\n')
        train_num += 1
    if train_num ==300000:
        break
transformed_abstract.close()
original_abstract.close()
train_source.close()
train_target.close()
val_source.close()
val_target.close()
print('%d training samples are extracted.' % train_num)
print('%d validation samples are extracted.' % val_num)
