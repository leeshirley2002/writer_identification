import os
import random
from feature_exaction import FeatureExaction

def main():
    ##get all file names
    file_name_list = os.listdir('smooth_5_char_old\\smooth_5_char_old')
    #remove numbers and daxie
    file_name_list = [i for i in file_name_list if i.split('.')[0][-1].islower()] 
    file_dict = {}
    for i in file_name_list:
        writer_id = i.split('_')[1][0:3]
        char = i.split('.')[0][-1]
        #convert A to A1
        if char.isupper():
            char = char+'1'
        file_dict[i] = [writer_id,char]
    ##char / wirterlist
    char_list = list(set([file_dict[key][1] for key in file_dict]))
    char_list.sort()
    writer_list = list(set([file_dict[key][0] for key in file_dict]))
    writer_list.sort()
    
    #outPut files
    out_Files = {}
    for char in char_list:
        out_Files[char] = open("models\\"+char+'.desc','wb')
    test_log = open("models\\"+"test_file_name",'wb')
    train_log = open("models\\train_file_name",'wb')
    for writer in writer_list:
        for char in char_list:
            temp_name = [name for name in file_dict if file_dict[name][0] == writer and file_dict[name][1] == char]
            #get test set
            test_set = random.sample(temp_name,int(len(temp_name)*0.1))
            #if char == 'z':
            #    print 1
            for i in test_set:
                test_log.write(i+'\n')
            train_1 = [temp for temp in temp_name if temp not in test_set]
            if len(train_1) < 80:
                train_set = train_1
            else:
                train_set = random.sample(train_1,80)
            for i in train_set:
                train_log.write(i+'\n')
            #write svm file
            for name in train_set:
                desc_line = str(writer_list.index(writer)+1)+' '
                feat = FeatureExaction('smooth_5_char_old\\smooth_5_char_old\\'+name)
                desc_line += feat.getLibsvmDescLine(write_name=False)
                out_Files[char].write(desc_line+'\n')

if __name__ == '__main__':
    main()
