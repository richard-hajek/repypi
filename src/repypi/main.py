import xml.etree.ElementTree as ET
import requests
import xmltodict
from pprint import pprint
from datetime import datetime
from typing import List, Tuple
import sys
import dateutil.parser
import argparse
import os.path as osp
import os
import requirements

def get_history(project: str):
    url = f"https://pypi.org/rss/project/{project}/releases.xml"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = xmltodict.parse(response.content)
    return data

def find_version_at(d: datetime.date, history: dict) -> str:
    
    latest_valid_ver = None

    if type(history) == dict:
        history = [history]

    for version in reversed(history):
        version_uploaded_at = datetime.strptime(version["pubDate"], "%a, %d %b %Y %X %Z")

        if d > version_uploaded_at:
            latest_valid_ver = version["title"]

    return latest_valid_ver


def find_versions_at(d: datetime.date, packages: List[str]) -> List[Tuple[str, str]]:

    results = []

    for package in packages:
        history = get_history(package)

        if history is None:
            results.append((package, None))
            print(f"Could not find package '{package}' on PyPI", file=sys.stderr)
            continue
        
        history = history["rss"]["channel"]["item"]
        
        newest_version_at_d = find_version_at(d, history)

        if newest_version_at_d is None:
            results.append((package, None))
            print(f"Package '{package}' has not been created yet on {d}", file=sys.stderr)
            continue
        
        results.append((package, newest_version_at_d))

    return results

def print_pkgver(package, version, f=sys.stdout):
    if version is None:
        print(package, file=f)
    else:
        print(f"{package}=={version}", file=f)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--now", action="store_true", help="Use now as date (default)")
    parser.add_argument("-d", "--date", type=str, help="Used date")
    parser.add_argument("-f", "--format", type=str, help="Used date format")

    parser.add_argument("-r", "--requirements", type=str, help="Path to requirements file, will replace req file")
    parser.add_argument("-p", "--packages", type=str, nargs="+", help="Packages to find, will print to stdout")
    parser.add_argument("--dry", action="store_true", help="Do not modify requirements.txt, instead print it")
    args = parser.parse_args() 

    date = None

    if args.date:

        if args.format:
            date = datetime.strptime(args.date, args.format)
        else:
            date = dateutil.parser.parse(args.date)
    
    if args.now or date is None:
        date = datetime.now()

    if args.packages:
        results = find_versions_at(date, args.packages)

        for (package, ver) in results:
            print_pkgver(package, ver)
    
    if args.requirements:
        
        reqs = []

        with open(args.requirements, "r") as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            try:
                req = requirements.requirement.Requirement.parse(line)
                reqs.append(req)
            except (AssertionError, ValueError):
                reqs.append(line)

        new_content = []

        for req in reqs:
            if type(req) == str:
                new_content.append(req)
                continue
            
            if len(req.specs) == 0:
                result = find_versions_at(date, [req.name])
                result = result[0]
                name, ver = result
                if ver is None:
                    new_content.append(req.line)
                else:
                    new_content.append(req.line+"=="+ver)
            else:
                new_content.append(req.line)
        
        new_content='\n'.join(new_content)
        
        if args.dry:
            print(new_content)
        else:
            with open(args.requirements, "w") as f:
                f.write(new_content)
            



if __name__ == "__main__":
    main()
