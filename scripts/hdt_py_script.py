from hdt_py import HDT, utils
import traceback
import re
import json
import logging
import os
import math

def get_fragment(uri):
    last_index = max(uri.rfind('/'), uri.rfind('#'))
    if last_index > -1:
        return uri[last_index + 1:]
    return uri


def get_label(hdt, uri):
    label = next(t.o for t in hdt.search(uri, "http://www.w3.org/2000/01/rdf-schema#label", "") if t.o.endswith("@en"))
    if label is None:
        label = get_fragment(uri)
    return label


def clean_label(dirty_label):
    pattern = re.compile('[\W_]+')
    labels = list(
        map(lambda x: pattern.sub('', x), dirty_label.split(' ')))
    return"_".join(labels)


def get_reified_statements_with_range(hdt):
    for triple in hdt.search("", "http://www.wikidata.org/prop/statement/P2302", "http://www.wikidata.org/entity/Q21510865"):
        yield triple.s


def get_reified_statements_with_domain(hdt):
    for triple in hdt.search("", "http://www.wikidata.org/prop/statement/P2302", "http://www.wikidata.org/entity/Q21503250"):
        yield triple.s


def get_reified_statement_classes(hdt, reified_statement):
    for triple in hdt.search(reified_statement, "http://www.wikidata.org/prop/qualifier/P2308", ""):
        yield triple.o


def get_reified_statement_fragment(reified_statement):
    dirty_fragment = get_fragment(reified_statement)
    first_index = dirty_fragment.find("-")
    if first_index > -1:
        return dirty_fragment[0:first_index]
    return dirty_fragment


def saving_to_json(file_path, instance_labels):
    # with open('propertiesTmp.json', 'w') as fp:
    with open(file_path, 'w') as fp:
        json.dump(instance_labels, fp)

def create_logger():
    # Create a custom logger
    logger = logging.getLogger(__name__)

    # Create handlers
    c_handler = logging.StreamHandler()
    log_dir = "/scripts"
    if not os.path.isdir(log_dir):
        log_dir = ""
    f_handler = logging.FileHandler(os.path.join(log_dir, 'app.log'))
    c_handler.setLevel(logging.DEBUG)
    f_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    logger.setLevel(logging.DEBUG)
    return logger

if __name__ == "__main__":
    logger = create_logger()
    logger.info("start")
    
    # logging.basicConfig(filename=os.path.join(log_dir, 'app.log'), filemode='w', format='%(name)s - %(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    # hdt_file = "/data/dbpedia/dbpedia2016-04en.hdt"
    # s = "http://dbpedia.org/resource/Paris"
    # p = "http://www.w3.org/2002/07/owl#sameAs"
    # print(get_reified_statement_fragment("http://www.wikidata.org/entity/statement/P868-6c07ec43-4961-4721-f52a-545b546f8b32"))

    # s = "http://www.wikidata.org/entity/Q90"
    # # s = "http://www.wikidata.org/entity/P868"
    # # s = "http://www.wikidata.org/entity/statement/P868-6c07ec43-4961-4721-f52a-545b546f8b32"
    # p = ""
    # s = "http://www.wikidata.org/prop/P868"
    hdt_file = "/data/wikidata/wikidata2018_09_11.hdt"
    wd_entity = "http://www.wikidata.org/entity/"
    owl_thing = "http://www.w3.org/2002/07/owl#Thing"

    # hdt_file = "/mnt/d/dev/hdt/dataset.hdt"
    # with HDT(hdt_file, "/mnt/d/dev/Python/hdt_py/libs/libhdt.so") as f:
    # count = 0
    try:
        global_dic = {}
        with HDT(hdt_file) as f:
            # for triple in f.search(s, p, ""):
            logger.info("creating global_dic...")
            count = 0
            for p in f.get_predicates():
                count += 1
                wiki_id = get_reified_statement_fragment(p)
                if wiki_id in global_dic:
                    tmp_dic = global_dic[wiki_id]
                    tmp_dic["urls"].append(p)
                else:
                    tmp_dic = {"urls": [p]}
                    global_dic[wiki_id] = tmp_dic
            logger.info("global_dic created: " + str(count))
            count = 0
            logger.info("getting statements for domains...")
            statements = {statement for statement in get_reified_statements_with_domain(f)}
            logger.info("{} statements for domain".format(len(statements)))
            logger.info("looping for domains...")
            perc = 0
            for statement in statements:
                wiki_id = get_reified_statement_fragment(statement)
                if wiki_id in global_dic:
                    tmp_dic = global_dic[wiki_id]
                else:
                    tmp_dic = {}
                    global_dic[wiki_id] = tmp_dic
                domains = {
                    domain for domain in get_reified_statement_classes(f, statement)}
                tmp_dic["domains"] = domains
                if "label" not in tmp_dic:
                    label = clean_label(get_label(f, wd_entity + wiki_id))
                    tmp_dic["label"] = label
                count += 1
                cur_perc = math.floor(count * 100 / len(statements))
                if cur_perc > perc:
                    perc = cur_perc
                    logger.debug("{}%".format(perc))
            logger.info("domains: " + str(count))
            count = 0
            logger.info("getting statements for ranges...")
            statements = {statement for statement in get_reified_statements_with_range(f)}
            logger.info("{} statements for range".format(len(statements)))
            logger.info("looping for ranges...")
            perc = 0
            for statement in statements:
                wiki_id = get_reified_statement_fragment(statement)
                if wiki_id in global_dic:
                    tmp_dic = global_dic[wiki_id]
                else:
                    tmp_dic = {}
                    global_dic[wiki_id] = tmp_dic
                ranges = {r for r in get_reified_statement_classes(f, statement)}
                tmp_dic["ranges"] = ranges
                if "label" not in tmp_dic:
                    label = clean_label(get_label(f, wd_entity + wiki_id))
                    tmp_dic["label"] = label
                count += 1
                cur_perc = math.floor(count * 100 / len(statements))
                if cur_perc > perc:
                    perc = cur_perc
                    logger.debug("{}%".format(perc))
            logger.info("ranges: " + str(count))
        logger.info("OWL Thing filling...")
        count = 0
        perc = 0
        for wiki_id in global_dic:
            tmp_dic = global_dic[wiki_id]
            if "domains" not in tmp_dic:
                tmp_dic["domains"] = {owl_thing}
            if "ranges" not in tmp_dic:
                tmp_dic["ranges"] = {owl_thing}
            count += 1                
            cur_perc = math.floor(count * 100 / len(global_dic))
            if cur_perc > perc:
                perc = cur_perc
                logger.debug("{}%".format(perc))
        logger.info("OWL fillings: " + str(count))
        logger.info("saving...")
        saving_to_json("/scripts/wiki_props.json", global_dic)
    except Exception as e:
        logger.error("Exception occurred", exc_info=True)
    logger.info("end.")

        # print("Finalizing instances labels...")
        # for wiki_id in global_dic:
        #     tmp_dic = global_dic[wiki_id]
        #     for uri in tmp_dic["urls"]:
        #         pass


        # c = 0
        # for p in f.get_predicates():
        #     print(p)
        #     c += 1
        #     if c == 10:
        #         raise Exception("yop")
        # for p in {t.p for t in f.search(s, p, "")}:
        #     if not p.startswith("http://www.wikidata.org/"):
        #         continue
        #     # print(triple)
        #     p_fragment = get_fragment(p)
        #     label = get_label(f, wd_entity + p_fragment)#next(t.o for t in f.search(wd_entity + p_fragment, "http://www.w3.org/2000/01/rdf-schema#label", "") if t.o.endswith("@en"))
        #     print("#############\n{} ({}):".format(p_fragment, label))
        #     for constraint in f.search(wd_entity + p_fragment, "http://www.wikidata.org/prop/P2302", ""):
        #         # if not constraint.o.startswith("http://www.wikidata.org/entity/statement/"):
        #         #     continue
        #         for triple in f.search(constraint.o, "", ""):
        #             print(triple)

    #         count += 1
    # print("count: " + str(count))

# docker run -it --rm -v D:/dev/hdt:/data-v D:/dev/cpp/hdt-cpp-ph/scripts:/scripts hdt_commands python3 hdt_py_script.py
# docker run -it --rm -v /data2/hamdif/doctorants/ph/linkeddatasets/hdt:/data  -v /etudiants/deptinfo/p/pari_p1/dev/python/scripts:/scripts hdt_commands python3 hdt_py_script.py
