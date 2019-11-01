import sys

disk = {}

OUT_FILE = '20171171_2.txt'

def get_var_str(d):
    temp = ''
    for key, value in sorted(d.items()):
        temp += key + ' ' + str(value) + ' '
    return temp.rstrip()

def recover(logs):
    logs.reverse()
    end_ckpt_seen = False
    start_ckpt_seen = False
    fin_trans = []
    unfin_trans = []

    for log in logs:
        log = log.strip('<>')
        
        if 'END CKPT' in log:
            end_ckpt_seen = True
        elif 'START CKPT' in log:
            if end_ckpt_seen:
                break
            else:
                start_ckpt_seen = True
                active_trans = [x.strip() for x in log.split('START CKPT')[1].strip().strip('()').split(',')]
                for trans_id in active_trans:
                    if trans_id not in fin_trans:
                        unfin_trans.append(trans_id)
        elif 'START' in log:
            if start_ckpt_seen:
                trans_id = log.split()[1]
                if trans_id in unfin_trans:
                    unfin_trans.remove(trans_id)
                    if not unfin_trans:
                        break
        elif 'COMMIT' in log:
            trans_id = log.split()[1]
            fin_trans.append(trans_id)
        else:
            trans_id, attr, value = [x.strip() for x in log.split(',')]
            if trans_id not in fin_trans:
                disk[attr] = value

if __name__ == '__main__':

    input_file = sys.argv[1]
    
    logs = []
    fill_disk = False
    for line in open(input_file).readlines():
        if line.isspace():
            continue
        if not fill_disk:
            line = line.split()
            for i in range(0, len(line), 2):
                disk[line[i]] = int(line[i + 1])
            fill_disk = True
            continue
        logs.append(line.strip())

    recover(logs)
    
    with open(OUT_FILE, 'w') as f:
        f.writelines(get_var_str(disk) + '\n')
