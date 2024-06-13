#!/usr/bin/env python3
# coding=utf-8

import sys
import os
import xml.etree.ElementTree as ET

def fuckPath(path):
    path=path[path.rindex('\\')+1:]
    if ".cab" in path:
        path="cabs_"+path
    if ".wim" in path:
        path="Wim_"+path
    return path

print("UUP-Tools v2.2 - CompDBReader\nCopyright (C) 2012-2024 BetaWorld\n")
if len(sys.argv)==2:
    haveDotNet=False
elif len(sys.argv)==3:
    haveDotNet=True
else:
    print("Usage: CompDBReader <EditionCompDB> [DotNetCompDB]")
    exit()
editionTree=ET.parse(sys.argv[1])
editionRoot=editionTree.getroot()
featureSet=set()
warnings=0
for feature in editionRoot.findall("./{*}Features/{*}Feature/{*}Packages/{*}Package"):
    featureSet.add(feature.attrib["ID"])
for package in editionRoot.findall("./{*}Packages/{*}Package"):
    if package.attrib["ID"] not in featureSet:
        continue
    for payload in package.findall("./{*}Payload/{*}PayloadItem"):
        path=payload.attrib["Path"]
        path=path.replace("editionpackages", "editionPackages")
        fuckedPath=fuckPath(path)
        os.makedirs(os.path.dirname(path.replace('\\', os.sep)), exist_ok=True)
        if os.path.exists(fuckedPath):
            os.rename(fuckedPath, path.replace('\\', os.sep))
        else:
            warnings=warnings+1
            print(f"Warning: \'{path}\' does not exist.")
if haveDotNet:
    dotnetTree=ET.parse(sys.argv[2])
    dotnetRoot=dotnetTree.getroot()
    for payload in dotnetRoot.findall("./{*}Packages/{*}Package/{*}Payload/{*}PayloadItem"):
        path=payload.attrib["Path"]
        filename=path[path.rindex('\\')+1:]
        os.makedirs(os.path.dirname(path.replace('\\', os.sep)), exist_ok=True)
        if os.path.exists(filename):
            os.rename(filename, path.replace('\\', os.sep))
        else:
            warnings=warnings+1
            print(f"Warning: \'{path}\' does not exist.")
print(f"Operation successful with {warnings} warning(s).")
