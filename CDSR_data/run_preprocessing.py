import re
import pandas as pd
import os

print('Start preprocessing CDSR data')
save_path = './CDSR/'
if not os.path.isdir(save_path):
    os.mkdir(save_path)
    
train_doi = list(pd.read_csv('train_title_DOI.csv')['DOI'])
val_doi = list(pd.read_csv('validation_title_DOI.csv')['DOI'])
test_doi = list(pd.read_csv('test_title_DOI.csv')['DOI'])

train_source = []
train_target = []
val_source = []
val_target = []
test_source = []
test_target = []

train_num = 0
val_num = 0
test_num = 0

ti = []
flag = 0
f = open('citation-export.txt')
line = f.readline()
while line:
    if 'Record #' in line:
        flag = 0
    elif line[0:4] == 'TI: ':
        title = line.replace('TI: ', '').replace('\n', '')
        if title in ti:
            flag = 1
        else:
            ti.append(title)
    elif line[0:5] == 'DOI: ':
        doi = line.replace('DOI: ', '').replace('\n', '')
        if 'pub' in doi:
            doi = '.'.join(doi.split('.')[:-1])
    elif 'AB: ' in line:
        if ('AB: Abstract - ' in line) and (flag == 0):
            if ('Plain language summary' in line) and (flag == 0):
                source = re.findall('AB: Abstract - (.+?) Plain language summary ', line)[0]
                target = re.findall('Plain language summary (.+?)\n', line)[0]
                if doi in train_doi:
                    train_source.append(source)
                    train_target.append(target)
                    train_num += 1
                elif doi in val_doi:
                    val_source.append(source)
                    val_target.append(target)
                    val_num += 1
                elif doi in test_doi:
                    test_source.append(source)
                    test_target.append(target)
                    test_num += 1
    line = f.readline()
f.close()

f_out = open(save_path+'train.source', 'w')
for i in range(len(train_source)):
    f_out.write(train_source[i]+'\n')
f_out.close()
f_out = open(save_path+'train.target', 'w')
for i in range(len(train_target)):
    f_out.write(train_target[i]+'\n')
f_out.close()
f_out = open(save_path+'val.source', 'w')
for i in range(len(val_source)):
    f_out.write(val_source[i]+'\n')
f_out.close()
f_out = open(save_path+'val.target', 'w')
for i in range(len(val_target)):
    f_out.write(val_target[i]+'\n')
f_out.close()
f_out = open(save_path+'test.source', 'w')
for i in range(len(test_source)):
    f_out.write(test_source[i]+'\n')
f_out.close()
f_out = open(save_path+'test.target', 'w')
for i in range(len(test_target)):
    f_out.write(test_target[i]+'\n')
f_out.close()

print('%d training samples are extracted.' % train_num)
print('%d validation samples are extracted.' % val_num)
print('%d testing samples are extracted.' % test_num)
print('The dataset is saved in "%s".' % save_path)

