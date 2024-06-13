#!/usr/bin/env python3
# coding=utf-8

import sys
import os
import xml.etree.ElementTree as ET

print("UUP-Tools v2.2 - AppXMLParser\nCopyright (C) 2012-2024 BetaWorld\n")
if len(sys.argv)!=3:
    print("Usage: AppXMLParser <EditionCompDB> <AppCompDB>")
    exit()
editionTree=ET.parse(sys.argv[1])
editionRoot=editionTree.getroot()
featureSet=set()
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
warnings=0
for feature in appRoot.findall("./{*}Features/{*}Feature"):
    if feature.attrib["FeatureID"] not in featureSet:
        continue
    for package in feature.findall("./{*}Packages/{*}Package"):
        packageSet.add(package.attrib["ID"])
for package in appRoot.findall("./{*}Packages/{*}Package"):
    if(package.attrib["ID"] not in packageSet):
        continue
    for payload in package.findall("./{*}Payload/{*}PayloadItem"):
        path=payload.attrib["Path"]
        fuckedPath=path[17:].replace('\\', '_')
        os.makedirs(os.path.dirname(path.replace('\\', os.sep)), exist_ok=True)
        if os.path.exists(fuckedPath):
            os.rename(fuckedPath, path.replace('\\', os.sep))
        else:
            print(f"Warning: \'{path}\' does not exist.")
print(f"Operation successful with {warnings} warning(s).")
