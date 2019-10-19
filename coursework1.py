import xml_processor
import printer
import InvertedList

def run_search_boolean(search,my_list):
    try:
        with open(search,"r") as fin:
            for line in fin:
                query_no, query = line.split(" ",1)
                try:
                    valid_files = (my_list.boolean_search(query.strip()))
                    if valid_files == []:
                        lil_str = None
                except Exception as e:
                    valid_files = None
                if valid_files != None:
                    printer.my_print_boolean(query_no,valid_files)
            print("Operation completed successfully.")
            run_search(my_list)
    except Exception:
        print("Invalid file name or format.")
        run_search(my_list)

def run_search_ranked(search,my_list):
    try:
        with open(search,"r") as fin:
            for line in fin:
                q_no,query = line.split(" ",1)
                results = my_list.search_with_ranked(query.strip())
                #print(results)
                if results != []:
                    printer.my_print_ranked(q_no,results)
        print("Operation completed successfully.")
        run_search(my_list)
    except Exception:
        print("Invalid file name or format.")
        run_search(my_list)


def run_search(my_list):
    search = input("Please enter your search file name, or q to quit: ")
    if search == "q":
        return
    if input("Would you like to use ranked search? (y/n): ") == "y":
        run_search_ranked(search,my_list)
    else:
        run_search_boolean(search,my_list)

def excepthandler(my_list):
    success = my_list.build_from_file()
    if success == -1:
        x = input("You don't seem to have a previously compiled inverted list, would you like to build it now? (y/n): ")
        if x == "y":
            in_file = input("Please enter the name of the file you'd like to parse: ")
            to_stem = True
            try:
                xml_processor.parse_xml(in_file, to_stem, my_list)
            except Exception:
                print("Invalid file name.")
                return
            my_list.stemmer(to_stem)
            excepthandler(my_list)
            return
        else:
            return
    run_search(my_list)


if __name__=="__main__":
    my_list = InvertedList.InvList()
    excepthandler(my_list)
