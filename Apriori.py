import pandas as pd
import itertools
import time


def load_csv(filename):
    df = pd.read_csv("DATA\\" + filename)
    names = list(df.columns.values)[1:]
    dl = list(df.values.tolist())
    for idx, t in enumerate(dl):
        dl[idx] = t[1:]
    for t in dl:
        for i, v in enumerate(t):
            t[i] = names[i] + "_" + str(v)
    return dl


def apriori(data, min_sup, min_conf):
    set_supports = find_freq(data, min_sup)
    print_itemsets(set_supports)
    assoc_rules = apriori_gen(set_supports, min_conf)
    print_rules(assoc_rules)
    return assoc_rules


def apriori_gen(set_supports, min_conf):
    max_len = 0
    assoc_itemsets = {}
    for key in set_supports:
        max_len = len(key)
    for key in set_supports:
        if len(key) != max_len:
            assoc_itemsets[key] = set_supports[key]

    assoc_rules = []
    for lhs in assoc_itemsets:
        for rhs in assoc_itemsets:
            if not lhs.issubset(rhs) and not rhs.issubset(lhs) and not any(x in lhs for x in rhs):
                superset = lhs.union(rhs)
                if len(superset) <= max_len and superset in set_supports and lhs in set_supports:
                    confidence = set_supports[superset]/set_supports[lhs]
                    if confidence > min_conf:
                        assoc_rules.append((lhs, rhs, set_supports[superset], confidence))
    return assoc_rules


def find_freq(data, min_sup):
    initial_items = initial_freq(data, min_sup)
    supersets = []
    for i in range(1, len(initial_items)):
        combinations = itertools.combinations(list(initial_items), i)
        for c in combinations:
            supersets.append(frozenset(c))
    set_supports = get_support(data, supersets, min_sup)
    return set_supports


def get_support(data, sets, min_sup):
    set_support = {}
    for s in sets:
        count = 0
        for tran in data:
            if s.issubset(set(tran)):
                count += 1
        support = float(count)/float(len(data))
        if support >= min_sup:
            set_support[s] = support
    return set_support


def initial_freq(data, min_sup):
    v_c = {}
    for tran in data:
        for item in tran:
            if item in v_c:
                v_c[item] = v_c[item] + 1
            else:
                v_c[item] = 1
    to_del = []
    for key in v_c:
        sup = float(v_c[key]) / float(len(data))
        if sup < min_sup:
            to_del.append(key)
    for key in to_del:
        del v_c[key]
    return set(v_c.keys())


def print_itemsets(set_supports):
    print("The following " + str(len(set_supports)) + " frequent itemsets were found:")
    for itemset in set_supports:
        print(str(itemset) + ": support = " + str(set_supports[itemset]))
    print("")


def print_rules(assoc_rules):
    print("The following " + str(len(assoc_rules)) + " rules that satisfy min_sup and min_conf are generated: ")
    for rule in assoc_rules:
        print(str(rule[0]) + " -> " + str(rule[1]) + " | support: " +
              str(rule[2]) + " | confidence: " + str(rule[3]))
    print("")


def main():
    start = time.time()

    # dl = load_csv("pokemon.csv")
    # dl = load_csv("stock_prices_2018.csv")
    dl = load_csv("fifa_player_data.csv")
    # dl = [['a', 'b', 'c', 'e', 'f'], ['a', 'b', 'c', 'd', 'f']]
    min_sup = 0.3
    min_conf = 0.6
    print("min_sup = " + str(min_sup))
    print("min_conf = " + str(min_conf))
    print("")

    apriori(dl, min_sup, min_conf)
    print("")

    end = time.time()
    print("Time Taken: " + str(end - start))


if __name__ == '__main__':
    main()
