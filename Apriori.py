import pandas as pd
import itertools
import time


def load_csv(filename):
    """
    Load a csv file and represent it as a list of transactions also appending the column name to each value.
    :param filename: The name of the file which is placed in the DATA folder
    :return: The data as a list of transactions with the column name appended to each value in the column
    """
    df = pd.read_csv("DATA\\" + filename)
    names = list(df.columns.values)[1:]
    dl = list(df.values.tolist())
    for idx, t in enumerate(dl):
        dl[idx] = t[1:]
    for t in dl:
        for i, v in enumerate(t):
            t[i] = names[i] + "_" + str(v)  # append column names to the values
    return dl


def apriori(data, min_sup, min_conf):
    """
    apriori runs all the parts needed to generate the association rules and passes the values between them.
    :param data: The data as a list of transactions
    :param min_sup: The minimum support
    :param min_conf: The minimum confidence
    :return: A list of tuples containing the information for each association rule.
             (left hand side, right hand side, support, confidence)
    """
    set_supports = find_freq(data, min_sup)
    print_itemsets(set_supports)
    assoc_rules = apriori_gen(set_supports, min_conf)
    print_rules(assoc_rules)
    return assoc_rules


def apriori_gen(set_supports, min_conf):
    """
    Generate the association rules.
    :param set_supports: A dictionary where the key is the itemset and the value is its support.
    :param min_conf: The minimum confidence
    :return: A list of tuples containing the information for each association rule.
             (left hand side, right hand side, support, confidence)
    """
    max_len = 0
    assoc_itemsets = {}
    # Find the longest itemset
    for key in set_supports:
        max_len = len(key)
    # Make a list of only frequent itemsets shorter than the longest itemsets
    for key in set_supports:
        if len(key) != max_len:
            assoc_itemsets[key] = set_supports[key]

    assoc_rules = []
    for lhs in assoc_itemsets:
        for rhs in assoc_itemsets:
            # no item in the left side is also in the right side
            if not any(item in lhs for item in rhs):
                superset = lhs.union(rhs)
                # the set of the left and right hand sides is shorter than the longest frequent itemsets and both the
                # superset and the left side exist in the list of frequent itemsets.
                if len(superset) <= max_len and superset in set_supports and lhs in set_supports:
                    confidence = set_supports[superset]/set_supports[lhs]
                    if confidence > min_conf:
                        assoc_rules.append((lhs, rhs, set_supports[superset], confidence))
    return assoc_rules


def find_freq(data, min_sup):
    """
    Find all frequent itemsets using initial_freq to first find all frequent one item itemsets.
    :param data: The data as a list of transactions
    :param min_sup: The minimum support
    :return: A dictionary where the key is the itemset and the value is its support
    """
    # Find the one item itemsets
    initial_items = initial_freq(data, min_sup)

    set_supports = {}
    # generate all combinations of the frequent one item itemsets and check if they meet min_sup
    for i in range(1, len(initial_items)):
        combinations = itertools.combinations(list(initial_items), i)
        for c in combinations:
            c = frozenset(c)
            count = 0
            for tran in data:
                if c.issubset(set(tran)):
                    count += 1
            support = float(count) / float(len(data))
            if support >= min_sup:
                set_supports[c] = support
    return set_supports


def initial_freq(data, min_sup):
    """
    Find the one item itemsets.
    :param data: The data as a list of transactions
    :param min_sup: The minimum support
    :return: A dictionary where with key is the single item itemset and the value is its support
    """
    i_s = {}
    for tran in data:
        for item in tran:
            if item in i_s:
                i_s[item] = i_s[item] + 1
            else:
                i_s[item] = 1
    to_del = []
    for key in i_s:
        sup = float(i_s[key]) / float(len(data))
        if sup < min_sup:
            to_del.append(key)
    for key in to_del:
        del i_s[key]
    return set(i_s.keys())


def print_itemsets(set_supports):
    """
    Prints out the frequent itemsets to make them look pretty.
    :param set_supports: A dictionary where the key is the itemset and the value is its support
    :return: None
    """
    print("The following " + str(len(set_supports)) + " frequent itemsets were found:")
    for itemset in set_supports:
        print(str(itemset) + ": support = " + str(set_supports[itemset]))
    print("")


def print_rules(assoc_rules):
    """
    Prints out the association rules to make them look pretty.
    :param assoc_rules: A list of tuples containing the information for each association rule.
                        (left hand side, right hand side, support, confidence)
    :return: None
    """
    print("The following " + str(len(assoc_rules)) + " rules that satisfy min_sup and min_conf are generated: ")
    for rule in assoc_rules:
        print(str(rule[0]) + " -> " + str(rule[1]) + " | support: " +
              str(rule[2]) + " | confidence: " + str(rule[3]))
    print("")


def main():
    start = time.time()

    dl = load_csv("stock_prices_2018.csv")

    min_sup = 0.1
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
