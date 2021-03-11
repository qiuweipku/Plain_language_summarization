from nltk.tokenize import sent_tokenize
from rouge import Rouge
import numpy as np
rouge = Rouge()

source_all = []
target_all = []
with open('./CDSR/test.source','r+') as f:
    for line in f.readlines():
        source_all.append(line.strip())
with open('./CDSR/'+'test.target','r+') as f:
    for line in f.readlines():
        target_all.append(line.strip())
print(len(source_all))
print(len(target_all))

f_out = open('./test_oracle_extractive.txt', 'w')
for i in range(len(source_all)):
    if i%100 == 0:
        print(i)
    source = source_all[i]
    target = target_all[i]
    extracted_abstract = ''
    source_sent = sent_tokenize(source)
    target_sent = sent_tokenize(target)
    for trg_s in target_sent:
        score_temp = []
        for src_s in source_sent:
            try:
                score_temp.append(rouge.get_scores(src_s, trg_s)[0]['rouge-2']['f'])
            except:
                score_temp.append(0)
        extracted_abstract += source_sent[np.argmax(np.array(score_temp))]+' '
    f_out.write(extracted_abstract+'\n')
f_out.close()