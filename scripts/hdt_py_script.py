from hdt_py import HDT, utils
import logging
import os
import sys

def create_logger(script_name):
    # Create a custom logger
    logger = logging.getLogger(__name__)

    # Create handlers
    c_handler = logging.StreamHandler()
    log_dir = "/scripts"
    if not os.path.isdir(log_dir):
        log_dir = ""
    f_handler = logging.FileHandler(os.path.join(log_dir, 'app_' + script_name + '.log'))
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
    logger = create_logger(sys.argv[0])
    logger.info("start")

    hdt_file = "/data/wikidata/wikidata2018_09_11.hdt"
    s = "http://www.wikidata.org/entity/Q90"
    p = ""
    o = ""
    count = 0
    try:
        with HDT(hdt_file) as f:
            for triple in f.search(s, p, o):
                print(triple)
                count +=1
    except Exception as e:
        logger.error("Exception occurred", exc_info=True)
    logger.info("end.")

# docker run -it --rm -v D:/dev/hdt:/data-v D:/dev/cpp/hdt-cpp-ph/scripts:/scripts hdt_commands python3 hdt_py_script.py
# docker run -it --rm -v /data2/hamdif/doctorants/ph/linkeddatasets/hdt:/data  -v /etudiants/deptinfo/p/pari_p1/dev/python/scripts:/scripts hdt_commands python3 hdt_py_script.py
