import re
import os
import time
from os.path import isdir, splitext, isfile, exists
import sys

print(sys.argv)

start = time.time()


if len(sys.argv) > 1:
    path = os.path.abspath(sys.argv[1])
    if exists(path):
        os.chdir(path)
        
print('执行文件夹:', os.getcwd())


def add_ret(file_path,dialog):
    pattern1 = '(?<!SVret\s=\s)(?<!ret\s=\s)FW_SetValue_w.+?;'
    repl_s = 'SVret = '

    pattern2 = '(?<=VAR)\s+?\{'
    repl2 = '\n{\n\tint SVret;'

    repl_e = 'if(SVret!=0){FW_Dialog1(' + \
                    dialog + ');return(0);}'

    encode_list = ['utf-16', 'utf-8']
    txt_string = ''
    for encode in encode_list:
            try:
                with open(file_path, 'r', encoding=encode) as fp:
                    txt_string = fp.read()
            except Exception as e:
                continue
            else:
                if re.findall('FW_SetValue_w', txt_string):
                    for ts in re.findall(pattern1, txt_string):
                        txt_string = re.sub(
                            re.escape(ts) + '(?!if)', repl_s + ts + repl_e, txt_string)
                    if not re.findall('int\sSVret', txt_string):
                        txt_string = re.sub(
                            pattern2, repl2, txt_string)
                    with open(file_path, 'w', encoding=encode) as fp:
                        fp.write(txt_string)
                break


for name in os.listdir():
    if isdir(name):
        for f in os.listdir(name):
            if isfile:
                if splitext(f)[1] == '.txt':
                    form_id = name
                    file_path = '{0}/{1}'.format(form_id, f)
                    add_ret(file_path,form_id)
                    

    else:
        if splitext(name)[1] == '.txt':
            if re.findall('^\d{4}', name):
                form_id = re.findall('^\d{4}', name)[0]
                add_ret(name,form_id)
            else:
                print('未执行文件',name)

end = time.time()
print('执行时间:', end-start)
