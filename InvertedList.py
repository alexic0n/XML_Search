import pickle
import preprocessor
import math

class InvList:

    def __init__(self):
        self.dict = {}
        self.max_id = []
        self.is_stemmed = False

    def ret_string(self, tolis):
        return ",".join(map(str,tolis))

    def stemmer(self,yorn):
        self.is_stemmed = yorn

    def write_to_file(self):
        fout = open("./file_store/inverted_list.txt","w+")
        for word_dict in sorted(self.dict, key=str.lower):
            fout.write(word_dict + ":\n")
            for docno in self.dict[word_dict]:
                fout.write("   " + str(docno) + ": " + self.ret_string(self.dict[word_dict][docno]) + "\n")
        fout.close()
        with open('./file_store/inverted_list.pickle','wb+') as handle:
            pickle.dump(self.dict,handle)
        with open('./file_store/inverted_list_max_id.pickle','wb+') as handle:
            pickle.dump(self.max_id,handle)
        with open('./file_store/inverted_list_stemmed.pickle','wb+') as handle:
            pickle.dump(self.is_stemmed,handle)


    def build_from_file(self):
        try:
            with open('./file_store/inverted_list.pickle','rb') as handle:
                self.dict = pickle.load(handle)
        except Exception as e:
            return -1
        try:
            with open('./file_store/inverted_list_max_id.pickle','rb') as handle:
                self.max_id = pickle.load(handle)
        except Exception as e:
            return -1
        try:
            with open('./file_store/inverted_list_stemmed.pickle','rb') as handle:
                self.is_stemmed = pickle.load(handle)
        except Exception as e:
            return -1
        print("Inverted List Loaded Successfully")
        return 1

    def sanitise_input(self,string):
        stop_list = preprocessor.make_stop()
        proc_list = preprocessor.process_line(string,stop_list, self.is_stemmed)
        return proc_list

    def boolean_search(self,term):
        t_list = term.split(" OR ")
        if len(t_list) == 1:
            return self.and_search(t_list[0])
        holder = self.and_search(t_list[0])
        for a in range(1,len(t_list)):
            holder = holder + [out for out in self.and_search(t_list[a]) if out not in holder]
        return sorted(holder)

    def and_search(self,term):
        t_list = term.split(" AND ")
        if len(t_list) == 1:
            temp = t_list[0].split("NOT ")
            if len(temp) == 1:
                if temp[0][0] == "\"":
                    return self.quote_search(t_list[0])
                if temp[0][0] == "#":
                    return self.proximity_search(t_list[0])
                return self.single_search(t_list[0])
            else:
                if temp[1][0] == "\"":
                    return self.quote_search(t_list[0])
                if temp[1][0] == "#":
                    return self.proximity_search(t_list[0])
                return self.single_search(t_list[0])
        holder = self.and_search(t_list[0])
        for a in t_list:
            holder = [out for out in holder for b in self.and_search(a) if out == b ]
        return holder


    def single_search(self, term):
        try:
            not_check = term.split("NOT ")
            has_not = False
            if len(not_check) == 2:
                term = not_check[1]
                has_not = True
            else:
                term = not_check[0]
            t_list = self.sanitise_input(term)
            holder = list(self.dict[t_list[0]].keys())
            for a in range(1,len(t_list)):
                holder = holder + [out for out in list(self.dict[t_list[a]].keys()) if out not in holder]
            if has_not:
                return [a for a in self.max_id if a not in holder]
            return sorted(holder)
        except Exception as e:
            return []

    def search_with_ranked(self, terms):
        terms = self.sanitise_input(terms)
        #print(terms)
        q_len = len(terms)
        results = []
        for x in range(0,q_len):
            results += [a for a in self.single_search(terms[x]) if a not in results]
        tuple_list = []
        col_size = len(self.max_id)
        for r in results:
            score = 0
            for t in terms:
                try:
                    tf = len(self.dict[t][r])
                    df = len(self.dict[t])
                    score += (1+math.log10(tf))*math.log10(col_size/df)
                except:
                    pass
            tuple_list.append((r,score))
        return tuple_list


    def get_valid_files(self, t_list):
        locations = []
        for t in t_list:
            locations.append(self.dict[t])
        valid_files = []
        for ds in list(locations[0].keys()):
            tripped = False
            for a in range(1,len(locations)):
                if ds not in locations[a]:
                    tripped = True
                    break
            if not tripped:
                valid_files.append(ds)
        return valid_files

    def get_files_subsequent_pos(self, valid_files,words):
        for_ret = []
        for vf in valid_files:
            curindlist = self.dict[words[0]][vf]
            for curind in curindlist:
                subseq = True
                for x in range(1,len(words)):
                    if curind+x not in self.dict[words[x]][vf]:
                        subseq = False
                        break
                if subseq:
                    for_ret.append(vf)
                    break
        return for_ret

    def quote_search(self, term):
        try:
            not_check = term.split("NOT ")
            has_not = False
            if len(not_check) == 2:
                term = not_check[1]
                has_not = True
            else:
                term = not_check[0]
            t_list = self.sanitise_input(term)
            valid_files = self.get_valid_files(t_list)
            if has_not:
                return [a for a in self.max_id if a not in self.get_files_subsequent_pos(valid_files,t_list)]
            return self.get_files_subsequent_pos(valid_files,t_list)
        except Exception as e:
            return []

    def get_files_prox_pos(self, valid_files, words, prox):
        for_ret = []
        for vf in valid_files:
            curindlist = self.dict[words[0]][vf]
            for curind in curindlist:
                has_hit = False
                for x in range(-prox,prox+1):
                    if curind+x in self.dict[words[1]][vf]:
                        has_hit = True
                        break
                if has_hit:
                    for_ret.append(vf)
                    break
        return for_ret


    def proximity_search(self, term):
        try:
            not_check = term.split("NOT ")
            has_not = False
            if len(not_check) == 2:
                term = not_check[1]
                has_not = True
            else:
                term = not_check[0]
            term = term[1:]
            t_list = term.split("(")
            prox = int(t_list[0])
            t_list = self.sanitise_input(t_list[1])
            valid_files = self.get_valid_files(t_list)
            #holder = self.get_files_prox_pos(valid_files, t_list, prox)
            if has_not:
                return [a for a in self.max_id if a not in self.get_files_prox_pos(valid_files,t_list,prox)]
            return self.get_files_prox_pos(valid_files,t_list,prox)
        except Exception as e:
            return []
