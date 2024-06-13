#!/usr/bin/env python3
# coding=utf-8

import sys
import os
import xml.etree.ElementTree as ET
import hashlib
import base64

validateFlag=True
files_ok=0
files_error=0
files_total=0

def sha256base64hash(filename):
    blockSize=65536
    hasher=hashlib.sha256()
    with open(filename, "rb") as file:
        fileBuffer=file.read(blockSize)
        while len(fileBuffer)>0:
            hasher.update(fileBuffer)
            fileBuffer=file.read(blockSize)
    return base64.b64encode(hasher.digest()).decode('utf-8')

print("UUP-Tools v2.2 - File Validator\nCopyright (C) 2012-2024 BetaWorld\n")
if len(sys.argv)==2:
    haveApps=False
elif len(sys.argv)==3:
    haveApps=True
else:
    print("Usage: FileValidator <EditionCompDB> [AppCompDB]")
    exit()
editionTree=ET.parse(sys.argv[1])
editionRoot=editionTree.getroot()
featureSet=set()
for feature in editionRoot.findall("./{*}Features/{*}Feature/{*}Packages/{*}Package"):
    featureSet.add(feature.attrib["ID"])
for package in editionRoot.findall("./{*}Packages/{*}Package"):
    if(package.attrib["ID"] not in featureSet):
        continue
    for payload in package.findall("./{*}Payload/{*}PayloadItem"):
        path=payload.attrib["Path"]
        path=path.replace("editionpackages", "editionPackages")
        path=path.replace('\\', os.sep)
        fileHash=payload.attrib["PayloadHash"]
        files_total=files_total+1
        if os.path.exists(path):
            realHash=sha256base64hash(path)
            if realHash!=fileHash:
                files_error=files_error+1
                validateFlag=False
                print(f"Warning: checksum error on file \'{path}\'.")
            else:
                files_ok=files_ok+1
        else:
            files_error=files_error+1
            validateFlag=False
            print(f"Warning: \'{path}\' does not exist.")
if haveApps:
    for feature in editionRoot.findall("./{*}Features/{*}Feature/{*}Dependencies/{*}Feature"):
        featureSet.add(feature.attrib["FeatureID"])
    appTree=ET.parse(sys.argv[2])
    appRoot=appTree.getroot()
    for feature in appRoot.findall("./{*}Features/{*}Feature"):
        if feature.attrib["FeatureID"] not in featureSet:
            continue
        for dependency in feature.findall("./{*}Dependencies/{*}Feature"):
            featureSet.add(dependency.attrib["FeatureID"])
    packageSet=set()
    for feature in appRoot.findall("./{*}Features/{*}Feature"):
        if feature.attrib["FeatureID"] not in featureSet:
            continue
        for package in feature.findall("./{*}Packages/{*}Package"):
            packageSet.add(package.attrib["ID"])
    for package in appRoot.findall("./{*}Packages/{*}Package"):
        if package.attrib["ID"] not in packageSet:
            continue
        for payload in package.findall("./{*}Payload/{*}PayloadItem"):
            path=payload.attrib["Path"]
            path=path.replace('\\', os.sep)
            fileHash=payload.attrib["PayloadHash"]
            files_total=files_total+1
            if os.path.exists(path):
                realHash=sha256base64hash(path)
                if realHash!=fileHash:
                    files_error=files_error+1
                    validateFlag=False
                    print(f"Warning: checksum error on file \'{path}'\'.")
                else:
                    files_ok=files_ok+1
            else:
                files_error=files_error+1
                validateFlag=False
                print(f"Warning: \'{path}\' does not exist.")
print("Summary:", files_ok, "file(s) OK,", files_error, "file(s) error,", files_total, "file(s) in total.")
if validateFlag:
    print("Everything OK")
