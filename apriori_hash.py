import time
import sys
import pandas as pd

def load_dataset():
    dataset = []
    dataDc={}
    trans_id=0
    f=open('dataset.txt','r')
    content=f.readlines()
    f.close()

    for c in content:
        ls=c.split()
        newLs=[]
        for k in ls:
            if k!='-1' and k!='-2':
                newLs.append(int(k))
        dataDc[str(trans_id)]=newLs
        trans_id+=1
    
    for key,val in dataDc.items():
        dataset.append(val)
    return dataset

    


def freq_c1(cur_data, cur_sup):
    # print(cur_data)
    dict_one = {}
    total_len = len(cur_data)
    for row in cur_data:
        for val in row:
            if val in dict_one:
                dict_one[val] += 1
            else:
                dict_one[val] = 1

    freq_1_dataset = []
    for key, cnt in dict_one.items():
        if cnt >= cur_sup:
            freq_1_dataset.append(([key], cnt))
    return freq_1_dataset


def create_index(diff_items,new_dataset):
    index_map={}
    for key,val in diff_items.items():
        for trans_no in range(len(new_dataset)):
            if key in new_dataset[trans_no]:
                if key not in index_map:
                    index_map[key] = [trans_no]
                else:
                    index_map[key].append(trans_no)
    
    return index_map

def intersect_lst(d):
    result = set(d[0]).intersection(*d[1:])
    return result

def insert_hash(new_data_tuple,diff_items,new_dataset):
#     print(diff_items)
#     print(new_data_tuple)
    index_map = create_index(diff_items,new_dataset)
#     print(index_map)
    hash_tree = {}
    for cur_lst in new_data_tuple:
        
        fs_lst = []
        for val in cur_lst:
            fs_lst.append(index_map[val])
#         print(cur_lst)
#         print(fs_lst)
        inter_val = intersect_lst(fs_lst)
#         print(inter_val)
        temp_len = len(cur_lst)
        hsh_val = 0
        for val in cur_lst:
            hsh_val += pow(10,temp_len)*(diff_items[val])
            temp_len -= 1
        mod = 1311
        hsh_val = hsh_val%mod
#         print(hsh_val)
        if hsh_val not in hash_tree:
            hash_tree[hsh_val] = [0,{}]
            hash_tree[hsh_val][0]=len(inter_val)
            if cur_lst not in hash_tree[hsh_val][1]:
                hash_tree[hsh_val][1][cur_lst] = len(inter_val)
            else:
                hash_tree[hsh_val][1][cur_lst] += len(inter_val)
        else:
            hash_tree[hsh_val][0] += len(inter_val)
            if cur_lst not in hash_tree[hsh_val][1]:
                hash_tree[hsh_val][1][cur_lst] = len(inter_val)
            else:
                hash_tree[hsh_val][1][cur_lst] += len(inter_val)
    
    return hash_tree

                
def is_prefix(list_1, list_2):
    for i in range(len(list_1) - 1):
        if list_1[i] != list_2[i]:
            return False
    return True

def cal_diff_items(prev_items):
    diff_items={}
    cur=1
    for val in prev_items:
        if val not in diff_items:
            diff_items[val] = cur
            cur += 1
    return diff_items


def prune(hash_tree, support, dataset):
    new_dataset_tuples=[]
    for key,val in hash_tree.items():
        if val[0] >= support:
            for tpl,cnt in val[1].items():
                if cnt >= support:
                    new_dataset_tuples.append(tpl)
    
    temp_lst = []
    for tup in new_dataset_tuples:
        for val in tup:
            temp_lst.append(val)
    new_items = set(temp_lst)
    diff_items = cal_diff_items(new_items)
    new_dataset = []
    for row in dataset:
        temp_lst = []
        for val in row:
            if val in new_items:
                temp_lst.append(val)
        if len(temp_lst) > 0 :
            new_dataset.append(temp_lst)
    
    return new_dataset, new_dataset_tuples,diff_items,new_items



def apriori_generate_frequent_itemsets(dataset, support):
    
    all_frequent_itemsets=[]
    fnl_freq_itemset = freq_c1(dataset, support)
    prev_freq = [x[0] for x in fnl_freq_itemset]
    length = 2
    fnl_length = 0
    new_dataset = dataset 
    fnl_hash_tree = []
    temp_lst = []
    for val in prev_freq:
        temp_lst.append(val[0])
    diff_items = cal_diff_items(temp_lst)
#     print(len(diff_items))
#     print(len(new_dataset))
    while len(prev_freq) > 1:
        print("Finding frequent dataset for length : ",length)
        new_data_tuple=[]
        for i in range(len(prev_freq)):
            j = i + 1
            while j < len(prev_freq) and is_prefix(prev_freq[i], prev_freq[j]):
                cur_lst = prev_freq[i][:-1]+[prev_freq[i][-1]]+[prev_freq[j][-1]]
                (cur_lst).sort()
#                 print(cur_lst)
                new_data_tuple.append(tuple(cur_lst))
                j += 1

        hash_tree = insert_hash(new_data_tuple,diff_items,new_dataset)
        fnl_hash_tree.append(hash_tree)
#         print(hash_tree)
        new_dataset, new_dataset_tuples,diff_items, new_items = prune(hash_tree, support, new_dataset)
#         print(new_dataset)
#         print(new_dataset_tuples)
#         print(diff_items)
#         print(new_items)

        all_frequent_itemsets.append(new_dataset_tuples)
#         print(new_dataset_tuples)
#         print(len(new_dataset_tuples))
        prev_freq = [list(tup) for tup in new_dataset_tuples]
        prev_freq.sort()
        for val in prev_freq:
            val.sort()
#         print(prev_freq)
        fnl_length += len(new_dataset_tuples)
        length += 1
#         break
#     print(fnl_length)
    return all_frequent_itemsets,fnl_hash_tree

def fnl_hash_tree(hash_tree_ap, support,length):
    hash_tree_list = []
    for h_tree in hash_tree_ap:
        for key,val in h_tree.items():
            if val[0] >= support:
                for tpl,cnt in val[1].items():
                    if cnt >= support:
                        hash_tree = {}
                        hash_tree["itemset"] = tpl
                        hash_tree["support"] = cnt/length
                        hash_tree_list.append(hash_tree)
    return hash_tree_list

##########............CLOSED ITEMSET..........############


def get_closed_items(hash_tree_closed_ap):
    temp_patterns = hash_tree_closed_ap
    
    for v in temp_patterns:
        v['support']=round(v['support'],3)

    frequent = pd.DataFrame(temp_patterns)
    su = frequent.support.unique()#all unique support count
    #Dictionay storing itemset with same support count key
    fredic = {}
    for i in range(len(su)):
        inset = list(frequent.loc[frequent.support == su[i]]['itemset'])
        fredic[su[i]] = inset

    #Find Closed frequent itemset
    # start_time = time.time()
    cl = []
    for index, row in frequent.iterrows():
        isclose = True
        cli = frozenset(tuple(row['itemset']))
        cls = row['support']
        checkset = fredic[cls]
        for i in checkset:
            i=frozenset(tuple(i))
            if (cli!=i):
                if(frozenset.issubset(cli,i)):
                    isclose = False
                    break

        if(isclose):
            cl.append(row['itemset'])
    
    return cl


start = time.time()
dataset = load_dataset()
support = float(sys.argv[1])
support = support*(len(dataset))
freq_output , hash_tree_ap = apriori_generate_frequent_itemsets(dataset,support)
file = open("output_apriori_hash.txt","w")
file.write(str(freq_output))
file.close()
end = time.time()
print("Total time taken -- : ",end - start)


print("Calculating closed itemset from frequent itemsets obtained for the given support!!")
hash_tree_closed_ap = fnl_hash_tree(hash_tree_ap, support, len(dataset))
print("Number of closed itemset are -- ", len(hash_tree_closed_ap))

