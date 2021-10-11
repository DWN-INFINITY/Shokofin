﻿import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--version', required=True)
parser.add_argument('--prerelease')
opts = parser.parse_args()

version = opts.version
prerelease = bool(opts.prerelease)

artifact_dir = os.path.join(os.getcwd(), 'artifacts')
os.mkdir(artifact_dir)

if prerelease:
  jellyfin_repo_file="./manifest-unstable.json"
  version_list = version.split('.')
  if len(version_list) == 3:
    version_list.append('1')
  else:
    version_list[3] = str(int(version_list[3]) + 1)
  version = '.'.join(version_list)
else:
  jellyfin_repo_file="./manifest.json"

jellyfin_repo_url="https://github.com/ShokoAnime/Shokofin/releases/download"

zipfile=os.popen('jprm --verbosity=debug plugin build "." --output="%s" --version="%s" --dotnet-framework="net5.0"' % (artifact_dir, version)).read().strip()

os.system('jprm repo add --url=%s %s %s' % (jellyfin_repo_url, jellyfin_repo_file, zipfile))

os.system('sed -i "s/shoko\//%s\//" %s' % (version, jellyfin_repo_file))

print(version)
