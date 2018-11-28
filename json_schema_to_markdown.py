# encoding: utf-8
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Author: Kyle Lahnakoski (kyle@lahnakoski.com)
#

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from mo_files import File
from mo_logs import Log, startup
from pyLibrary import convert


def _convert(file_):
    if file_.is_directory():
        for f in file_.children:
            _convert(f)
    elif file_.extension == "json":
        try:
            json = file_.read_json()
            if not json["$schema"]:
                return
            Log.note("{{json|json}}", json=json)
            md = convert.json_schema_to_markdown(json)
            file_.set_extension("md").write(md)
        except Exception as e:
            Log.warning("Can not convert {{filename}}", filename=file_.name, cause=e)


def main():
    try:
        args = startup.argparse(
            {
                "name": ["--file", "--source"],
                "help": "directory or file with *.json schema files",
                "type": str,
                "dest": "source",
                "required": True,
            }
        )
        _convert(File(args.source))

    except Exception as e:
        Log.error(
            "Serious problem with ActiveData service!  Shutdown completed!", cause=e
        )
    finally:
        Log.stop()


if __name__ == "__main__":
    main()
