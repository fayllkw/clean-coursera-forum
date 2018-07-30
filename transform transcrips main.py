import srt_to_txt
import os

# settings
ARVR = 'ARVR'
Civil = 'Civil'
Fake = 'Fake'
Privacy = 'Privacy'
COURSE = Fake
DATA_DIR = COURSE + '-Transcripts'
PROCESSED_DIR = "processed data"
CUR_DIR = os.path.split(os.path.realpath(__file__))[0]
OUTPUT_DIR = CUR_DIR + '/' + PROCESSED_DIR + '/' + COURSE + '/Transcripts'

# transform the srt one by one
if __name__ == '__main__':
    for file_name in os.listdir(CUR_DIR + '/' + DATA_DIR):
        if file_name[-4:]!='.srt': continue
        new_file = srt_to_txt.transform(CUR_DIR + '/' + DATA_DIR + '/' + file_name)
        new_file_name = file_name[:-4] + '.txt'
        with open(OUTPUT_DIR + '/' + new_file_name, 'w') as f:
            for line in new_file:
                f.write(line)