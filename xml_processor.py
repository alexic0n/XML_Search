import xml.etree.ElementTree as ET
import preprocessor
import InvertedList

def parse_xml(in_file,stem_or, my_list):
    stop_list = preprocessor.make_stop()
    tree = ET.parse(in_file)
    root = tree.getroot()
    max_docid = -1
    for child in root:
        DOC_ID = int(child.find("DOCNO").text)
        DOC_TEXT = child.find("HEADLINE").text + " " + child.find("TEXT").text
        proc_list = preprocessor.process_line(DOC_TEXT,stop_list, stem_or)
        for index,word in enumerate(proc_list):
            if word in my_list.dict:
                if DOC_ID in my_list.dict[word]:
                    my_list.dict[word][DOC_ID].append(index)
                else:
                    my_list.dict[word][DOC_ID] = [index]
            else:
                my_list.dict[word] = {DOC_ID:[index]}
        my_list.max_id.append(int(DOC_ID))
    my_list.stemmer(stem_or)
    my_list.write_to_file()
