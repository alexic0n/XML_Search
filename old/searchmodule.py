import xml_processor
import InvertedList

def run_search(search,my_list):
    if search == "q":
        return
    if search == "":
        run_search(input("Please enter a search term, or q to quit: "), my_list)
    else:
        try:
            lil_str = str((my_list.boolean_search(search)))
            if lil_str == "[]":
                lil_str = "Error...no matches for your term!"
        except Exception as e:
            lil_str = "Error...no matches for your term!"
        print("Documents that match \"{}\": ".format(search) + lil_str)
        run_search(input("Please enter a search term, or q to quit: "), my_list)

def excepthandler(my_list):
    success = my_list.build_from_file()
    if success == -1:
        x = input("You don't seem to have a previously compiled inverted list, would you like to build it now? (y/n): ")
        if x == "y":
            in_file = input("Please enter the name of the file you'd like to parse: ")
            to_stem = input("Would you like to stop and stem when constructing this list? (y/n): ")
            if to_stem == "y":
                to_stem = True
            else:
                to_stem = False
            Lab_2.parse_xml(in_file, to_stem)
            #print(to_stem)
            my_list.stemmer(to_stem)
            excepthandler(my_list)
            return
        else:
            return
    search = input("Please enter your search file name, or q to quit: ")
    run_search(search, my_list)


if __name__=="__main__":
    my_list = InvertedList.InvList()
    excepthandler(my_list)
