#!/usr/bin/env python3
import requests
import argparse
import os
import glob
import json
import yaml
import logging
import sys
import csv
import re
import jinja2

GPIO_VALID_RANGE = [8, 36]

def load_yaml(yaml_file):
    with open(yaml_file, "r") as stream:
        return (yaml.safe_load(stream))

def write_user_config(module_name, sources, io_ranges):
    env = jinja2.Environment(
        loader = jinja2.FileSystemLoader('verilog/rtl')
    )
    top_module_template = env.get_template('tiny_user_project.v.jinja2')
    with open('verilog/rtl/tiny_user_project.v', 'w') as fh:
        fh.write(top_module_template.render(
            module_name=module_name,
            io_in_range=io_ranges[0],
            io_out_range=io_ranges[1]
        ))
    user_defines_template = env.get_template('user_defines.v.jinja2')
    with open('verilog/rtl/user_defines.v', 'w') as fh:
        fh.write(user_defines_template.render(
            io_in_range=io_ranges[0],
            io_out_range=io_ranges[1]
        ))
    with open('openlane/tiny_user_project/config.json', 'r') as fh:
        config_json = json.load(fh)
    sources.append('verilog/rtl/defines.v')
    sources.append('verilog/rtl/tiny_user_project.v')
    config_json['VERILOG_FILES'] = [f'dir::../../{s}' for s in sources]
    with open('openlane/tiny_user_project/config.json', 'w') as fh:
        json.dump(config_json, fh, indent=4)

def get_project_source(yaml):
    # wokwi_id must be an int or 0
    try:
        wokwi_id = int(yaml['project']['wokwi_id'])
    except ValueError:
        logging.error("wokwi id must be an integer")
        exit(1)

    # it's a wokwi project
    if wokwi_id != 0:
        url = "https://wokwi.com/api/projects/{}/verilog".format(wokwi_id)
        logging.info("trying to download {}".format(url))
        r = requests.get(url)
        if r.status_code != 200:
            logging.warning("couldn't download {}".format(url))
            exit(1)

        filename = "user_module.v"
        with open(os.path.join('verilog/rtl', filename), 'wb') as fh:
            fh.write(r.content)

        # also fetch the wokwi diagram
        url = "https://wokwi.com/api/projects/{}/diagram.json".format(wokwi_id)
        logging.info("trying to download {}".format(url))
        r = requests.get(url)
        if r.status_code != 200:
            logging.warning("couldn't download {}".format(url))
            exit(1)

        with open(os.path.join('verilog/rtl', "wokwi_diagram.json"), 'wb') as fh:
            fh.write(r.content)

        return [f'verilog/rtl/{filename}', 'verilog/rtl/cells.v']

    # else it's HDL, so check source files
    else:
        if 'source_files' not in yaml['project']:
            logging.error("source files must be provided if wokwi_id is set to 0")
            exit(1)

        source_files = yaml['project']['source_files']
        if source_files is None:
            logging.error("must be more than 1 source file")
            exit(1)

        if len(source_files) == 0:
            logging.error("must be more than 1 source file")
            exit(1)

        if 'top_module' not in yaml['project']:
            logging.error("must provide a top module name")
            exit(1)

        return source_files


# documentation
def check_docs(yaml):
    for key in ['author', 'title', 'description', 'how_it_works', 'how_to_test', 'language']:
        if key not in yaml['documentation']:
            logging.error("missing key {} in documentation".format(key))
            exit(1)
        if yaml['documentation'][key] == "":
            logging.error("missing value for {} in documentation".format(key))
            exit(1)

    # if provided, check discord handle is valid
    if len(yaml['documentation']['discord']):
        parts = yaml['documentation']['discord'].split('#')
        if len(parts) != 2 or len(parts[0]) == 0 or not re.match('^[0-9]{4}$', parts[1]):
            logging.error(f'Invalid format for discord username')
            exit(1)


def get_top_module(yaml):
    wokwi_id = int(yaml['project']['wokwi_id'])
    if wokwi_id != 0:
        return "user_module_{}".format(wokwi_id)
    else:
        return yaml['project']['top_module']

def get_io_ranges(yaml):
    input_range = (GPIO_VALID_RANGE[0], GPIO_VALID_RANGE[0]+len(yaml['documentation']['inputs']))
    output_range = (input_range[1], input_range[1]+len(yaml['documentation']['outputs']))
    gpio_end = output_range[1]
    if gpio_end > GPIO_VALID_RANGE[1]:
        raise Exception('ETOOMANY IOs')
    return (input_range, output_range)

def get_stats():
    with open('runs/wokwi/reports/metrics.csv') as f:
        report = list(csv.DictReader(f))[0]

    print('# Routing stats')
    print()
    print('| Utilisation | Wire length (um) |')
    print('|-------------|------------------|')
    print('| {} | {} |'.format(report['OpenDP_Util'], report['wire_length']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="TT setup")

    parser.add_argument('--check-docs', help="check the documentation part of the yaml", action="store_const", const=True)
    parser.add_argument('--get-stats', help="print some stats from the run", action="store_const", const=True)
    parser.add_argument('--create-user-config', help="create the user_config.tcl file with top module and source files", action="store_const", const=True)
    parser.add_argument('--debug', help="debug logging", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('--yaml', help="yaml file to load", default='info.yaml')

    args = parser.parse_args()
    # setup log
    log_format = logging.Formatter('%(asctime)s - %(module)-10s - %(levelname)-8s - %(message)s')
    # configure the client logging
    log = logging.getLogger('')
    # has to be set to debug as is the root logger
    log.setLevel(args.loglevel)

    # create console handler and set level to info
    ch = logging.StreamHandler(sys.stdout)
    # create formatter for console
    ch.setFormatter(log_format)
    log.addHandler(ch)

    if args.get_stats:
        get_stats()

    elif args.check_docs:
        logging.info("checking docs")
        config = load_yaml(args.yaml)
        check_docs(config)

    elif args.create_user_config:
        logging.info("creating include file")
        config = load_yaml(args.yaml)
        source_files = get_project_source(config)
        top_module = get_top_module(config)
        assert top_module != 'top'
        io_ranges = get_io_ranges(config)
        write_user_config(top_module, source_files, io_ranges)
