#!/usr/bin/python
# -*- coding: utf-8 -*-

from clevertap import CleverTap
import argparse
import datetime
import json
import csv

MAX_BATCH_SIZE = 5000


def _flatten(structure, key="", flattened=None):
    if flattened is None:
        flattened = {}
    if type(structure) not in (dict, list):
        if isinstance(structure, basestring):
            flattened[key] = "\"" + str(structure.encode("UTF-8")) + "\""
        else:
            flattened[key] = str(structure)
    elif isinstance(structure, list):
        for i, item in enumerate(structure):
            _flatten(item, "%d" % i, flattened)
    else:
        for new_key, value in structure.items():
            _flatten(value, new_key, flattened)
    return flattened


def _add_to_field_names(field_names, main_list_of_fields):
    for field in field_names:
        if field not in main_list_of_fields:
            main_list_of_fields.append(field)


def _convert_to_csv(result, pathcsv):
    result_list = []
    main_list_of_fields = []

    print "Received %s results" % len(result)
    if len(result) == 0:
        print "No .csv file created"
        return

    print "Converting to .csv format..."

    for row in result:
        try:
            res = _flatten(row)
            _add_to_field_names(res.keys(), main_list_of_fields)
            # res = {k: unicode(v).encode("utf-8") for k,v in res.iteritems()}
            res = {k: str(v) for k,v in res.iteritems()}

            result_list.append(res)
        except Exception, e:
            print e
            print "ERROR: Failed to process record: %s" % row

    with open(pathcsv, "wb") as csvfile:
        writer = csv.DictWriter(csvfile, main_list_of_fields)
        writer.writeheader()

        for row in result_list:
            try:
                writer.writerow(row)
            except Exception, e:
                print e
                print "ERROR: Failed to write this record to CSV file: %s" % row

    print "Download Complete!"


def main(account_id, passcode, path_json, path_csv, type_of_download, dryrun):

    clevertap = CleverTap(account_id, passcode)
    result = []

    if type_of_download not in ["event", "profile"]:
        raise Exception("unknown record type %s" % type)
        return

    start_time = datetime.datetime.now()
    print "Downloading..."
    try:
        with open(path_json) as data_file:
            data = json.load(data_file)
        if type_of_download == "profile":
            result = clevertap.profiles(data, MAX_BATCH_SIZE)
        elif type_of_download == "event":
            result = clevertap.events(data, MAX_BATCH_SIZE)
        _convert_to_csv(result, path_csv)

    except Exception, e:
        print e

    finally:
        end_time = datetime.datetime.now()
        processing_time = end_time - start_time
        print "Processing Time: %s" % processing_time


if __name__ == "__main__":
    def str2bool(v):
        return v.lower() in ("yes", "true", "t", "1")


    parser = argparse.ArgumentParser(description='CleverTap CSV downloader')
    parser.register('type', 'bool', str2bool)
    parser.add_argument('-a', '--id', help='CleverTap Account ID', required=True)
    parser.add_argument('-c', '--passcode', help='CleverTap Account Passcode', required=True)
    parser.add_argument('-pjson', '--pathjson', help='Absolute path to the json file', required=True)
    parser.add_argument('-pcsv', '--pathcsv', help='Absolute path to the csv file', required=True)
    parser.add_argument('-t', '--t', help='The type of data, either profile or event, defaults to profile',
                        default="profile")
    parser.add_argument('-d', '--dryrun', help='Do a dry run, process records but do not upload', default=False,
                        type='bool')

    args = parser.parse_args()

    main(args.id, args.passcode, args.pathjson, args.pathcsv, args.t, args.dryrun)
