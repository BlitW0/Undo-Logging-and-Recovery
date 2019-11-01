import sys

disk = {}
main_mem = {}
local_var = {}
write_que = {}
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

    if ':=' in action:
        var, expr = [x.strip() for x in action.split(':=')]
        local_var[var] = eval(expr, local_var)
    else:
        arg_list = [x.strip() for x in action.split('(')[1].strip(')').split(',')]
        attr = arg_list[0]
        var = None if len(arg_list) == 1 else arg_list[1]

        if 'READ' in action:
            if attr not in main_mem:
                main_mem[attr] = disk[attr]
            local_var[var] = main_mem[attr]
        elif 'WRITE' in action:
            if attr not in main_mem:
                main_mem[attr] = disk[attr]
            old_attr_val = main_mem[attr]
            main_mem[attr] = local_var[var]
            write_que[transaction].append(attr)
            write_to_output('<' + transaction + ', ' + attr + ', ' + str(old_attr_val) + '>')
        elif 'OUTPUT' in action:
            disk[attr] = main_mem[attr]
            write_que[transaction].remove(attr)
            if not write_que[transaction]:
                write_to_output('<COMMIT ' + transaction + '>')
        else:
            print('Invalid action', action, 'in transaction', transaction)
            exit(1)

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
            for i in range(0, len(line), 2):
                disk[line[i]] = int(line[i + 1])
            fill_disk = True
            continue
        transactions[trans_cnt - 1].append(line.strip())

    round_robin(transactions, time_quantum)

    with open(OUT_FILE, 'w') as f:
        f.writelines(out_lines)
    