import sys

disk = dict()
main_mem = dict()
local_var = dict()
write_que = dict()
out_lines = []
transactions = []

OUT_FILE = '20171171_1.txt'

def get_var_str(d):
    temp = ''
    for key, value in sorted(d.items()):
        temp += key + ' ' + str(value) + ' '
    return temp.rstrip()

def write_to_output(log_record):
    global disk, main_mem, out_lines
    out_lines.append(log_record + '\n')
    out_lines.append(get_var_str(main_mem) + '\n')
    out_lines.append(get_var_str(disk) + '\n')

def execute_action(action, transaction):
    global disk, main_mem, local_var, write_que
    
    if 'READ' in action:
        arg_list = action.split('(')[1].split(')')[0].split(',')
        arg_list = list(map(lambda x: x.split()[0], arg_list))
        if arg_list[0] not in main_mem:
            main_mem[arg_list[0]] = disk[arg_list[0]]
        local_var[arg_list[1]] = main_mem[arg_list[0]]
        
    elif 'WRITE' in action:
        arg_list = action.split('(')[1].split(')')[0].split(',')
        arg_list = list(map(lambda x: x.split()[0], arg_list))
        old_val = disk[arg_list[0]] if arg_list[0] not in main_mem else main_mem[arg_list[0]]
        main_mem[arg_list[0]] = local_var[arg_list[1]]
        write_que[transaction].append(arg_list[0])
        write_to_output('<' + transaction + ', ' + arg_list[0] + ', ' + str(old_val) + '>')
    
    elif 'OUTPUT' in action:
        attr = action.split('(')[1].split(')')[0]
        disk[attr] = main_mem[attr]
        write_que[transaction].remove(attr)
        if len(write_que[transaction]) == 0:
            write_to_output('<COMMIT ' + transaction + '>')
    
    elif ':=' in action:
        action = action.split(':=')
        action = list(map(lambda x: x.split()[0], action))
        local_var[action[0]] = eval(action[1], local_var)

def round_robin(transactions, quantum):
    global write_que
    
    instr_cnt = [1]*len(transactions)
    trans_name = []
    for transaction in transactions:
        trans_name.append(transaction[0].split()[0])
        write_que[trans_name[-1]] = []
    
    trans_fin = 0
    while trans_fin < len(transactions):
        for i in range(len(transactions)):
            lim = instr_cnt[i] + quantum
            while instr_cnt[i] < min(lim, len(transactions[i])):
                if instr_cnt[i] == 1:
                    write_to_output('<START ' + trans_name[i] + '>')
                execute_action(transactions[i][instr_cnt[i]], trans_name[i])
                instr_cnt[i] += 1
                if instr_cnt[i] == len(transactions[i]):
                    trans_fin += 1

if __name__ == '__main__':

    input_file = sys.argv[1]
    time_quantum = int(sys.argv[2])

    fill_disk = False
    trans_cnt = 0
    for line in open(input_file).readlines():
        if line.isspace():
            if fill_disk:
                transactions.append([])
                trans_cnt += 1
            continue
        if not fill_disk:
            line = line.split()
            i = 0
            while i < len(line):
                disk[line[i]] = int(line[i + 1])
                i += 2
            fill_disk = True
            continue
        transactions[trans_cnt - 1].append(line)
    
    round_robin(transactions, time_quantum)

    with open(OUT_FILE, 'w') as f:
        f.writelines(out_lines)
    