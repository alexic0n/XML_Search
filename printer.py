MAX_RESULTS = 1000

def my_print_boolean(query_no, valid_files):
    count = 0
    with open("CW1_out/results.boolean.txt", "a+") as fout:
        for v in valid_files:
            fout.write(query_no.strip("q:") + " 0 " + str(v) + " 0 1 0\n")
            count += 1
            if count == MAX_RESULTS:
                break

def my_print_ranked(query_no,valid_files):
    count = 0
    with open("CW1_out/results.ranked.txt", "a+") as fout:
        for docid, rank in sorted(valid_files,key=lambda x: x[1],reverse=True):
            fout.write(str(query_no) + " 0 " + str(docid) + " 0 " + "{0:.4f}".format(rank) + " 0\n")
            count += 1
            if count == MAX_RESULTS:
                break
