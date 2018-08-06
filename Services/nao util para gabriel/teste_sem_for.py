import os
from functools import reduce


collect = 19
present_parameter = 80
active_parameter = 90

cur_path = os.path.dirname(__file__)
collect_path = os.path.relpath('..\\Coletas\\coleta ' + str(collect) + '.txt', cur_path)
collect_file = open(collect_path)
collect_text = collect_file.read()
collect_file.close()
collect_list = collect_text.split("\n")


first_line_list = collect_list[0].split()
first_timestamp = int(first_line_list[2])
last_line_list = collect_list[-1].split()
last_timestamp = int(last_line_list[2])

TIMESTAMP_RANGE = range(first_timestamp, last_timestamp + 1)

unique_macs = []

def gather_unique_macs(unique_macs_list):
    def check_if_unique(collect_line):
        line_list = collect_line.split()
        mac = line_list[0]
        result_list = list(filter(lambda x: x[0] == mac,unique_macs_list))
        if result_list == []:
            unique_macs_list.append([mac])
    return check_if_unique

list(map(gather_unique_macs(unique_macs), collect_list))

def get_mac_timestamps(collect_list, unique_macs):
    def add_timestamps(index):
        mac = unique_macs[index][0]
        new_list = []
        result_list = list(filter(lambda x: mac in x, collect_list))
        result_list_processed = list(map(lambda x: x.split(), result_list))
        list(map(lambda x: new_list.append(int(x[2])) if int(x[2]) not in new_list else False, result_list_processed))
        unique_macs[index] = unique_macs[index] + new_list
    return add_timestamps

list(map(get_mac_timestamps(collect_list, unique_macs),range(len(unique_macs))))

def get_mac_activity_collection(timestamp_range, present, active, first_timestamp):
    lista = []
    for i in unique_macs:
        timestamps = i[1:]
        list_timestamp_collect = list(map(lambda x:0, timestamp_range))
        status = False
        last_active_stamp = timestamps[0]
        last_present_stamp = timestamps[0]
        for k in timestamps:
            present_time = last_present_stamp + present
            active_time = last_active_stamp + active
            last_active_stamp = k
            if status == True:
                if k > active_time:
                    status = False
                    last_present_stamp = k
                else:
                    #todo verificar isso aqui
                    first_index = k - first_timestamp
                    last_index = active_time - first_timestamp + 1
                    value_list = list(map(lambda x: 1,range(first_index, last_index)))
                    list_timestamp_collect[first_index:last_index] = value_list
            elif k <= present_time:
                continue
            elif k > present_time and k <= active_time:
                status = True
                #todo verificar isso aqui
                first_index = k - first_timestamp
                last_index = active_time - first_timestamp + 1
                value_list = list(map(lambda x: 1, range(first_index, last_index)))
                list_timestamp_collect[first_index:last_index] = value_list
            else:
                last_present_stamp = k
        lista.append(list_timestamp_collect)
    return lista


lista = get_mac_activity_collection(TIMESTAMP_RANGE, present_parameter, active_parameter, first_timestamp)


#---------------------------------------------------------------------------------------------------

def sum_elements(element_a, element_b):
    a = element_a
    b = element_b
    return a + b

for j in range(len(lista) - 1):
    for i in range(len(TIMESTAMP_RANGE)):
        a = lista[j][i]
        b = lista[j+1][i]
        lista[j + 1][i] = sum_elements(a,b)

# lista = list(map(a(timestamp_range, present_parameter, active_parameter, first_timestamp),unique_macs))

def reduce_stamps_collection(list_a, list_b):
    result_list = list(map(lambda x: sum_elements(list_a[x],list_b[x]),range(len(TIMESTAMP_RANGE))))
    return result_list

crowd_density = lista[-1]


# bb = list(reduce(reduce_stamps_collection,lista))



print("a")

# list(map(naosei_onome_,unique_macs))


# for i in range(len(unique_macs)):
#     mac = unique_macs[i][0]
#     new_list = []
#     result_list = list(filter(lambda x: mac in x, collect_list))
#     result_list_processed = list(map(lambda x: x.split(),result_list))
#     list(map(lambda x: new_list.append(x[2]) if x[2] not in new_list else False,result_list_processed))
#     unique_macs[i] = unique_macs[i] + new_list
#     a = unique_macs[i]
#     print(result_list)





real_collect_path = os.path.realpath("..\\Coletas\\coleta {} real.txt".format(str(collect)))


