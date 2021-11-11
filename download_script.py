#!/usr/bin/python

import pandas as pd
import os
import pe
## curl -H 'Authorization: Bearer <YOUR_ACCESS_KEY>' \
##    'https://api.tria.ge/v0/samples/<SAMPLE_ID>/sample' \
##    --output sample.bin

access_key = '30e16656282f62bbab331a6e4507d42b0a21794d'


command = "curl -H 'Authorization: Bearer {0}' 'https://api.tria.ge/v0/samples/{1}/sample' --output {1}.zip"
file = pd.ExcelFile('final_export.xlsm')

sheet1 = pd.read_excel(file, 'Sheet1')

samples = sheet1['Sample'].to_list()

print(samples)

file.close()

for sample_id in samples:
    break
    os.system(command.format(access_key, sample_id))
    
    file_cmd_result = os.popen("file '{0}.zip'".format(sample_id)).read()
    print(file_cmd_result)

    if 'archive' in file_cmd_result or 'compressed' in file_cmd_result:
        os.system("unzip {0}.zip -d samples".format(sample_id))
        os.system("rm {0}.zip".format(sample_id))
        continue
    os.system("mv {0}.zip ./samples/{0}".format(sample_id))


for root, dirs, files in os.walk('./samples'):
    for path in files:
        path = os.path.join(root, path)
        if 'blackmatter' in path:
            os.system('mv {0} {1}'.format(path, path[:-len('.darkside')]))
        continue
        
        file_cmd_result = os.popen("file '{0}'".format(path)).read()
        print(file_cmd_result)
        if 'ELF' in file_cmd_result or 'ASCII text' in file_cmd_result:
            os.system('rm {0}'.format(path))
            continue

        if 'UPX' in file_cmd_result:
            print(file_cmd_result)
            os.system('upx -d {0}'.format(path))

        os.system('mv {0} {1}'.format(path, path + '.darkside'))
