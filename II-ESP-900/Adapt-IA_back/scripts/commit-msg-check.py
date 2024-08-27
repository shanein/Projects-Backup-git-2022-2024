import sys
import re

commit_msg_filepath = sys.argv[1]
with open(commit_msg_filepath, "r") as file:
    commit_msg = file.read().strip()

pattern = r"^(feature|bugfix|improvement|refactor)\([a-z]+\): .+$"
if not re.match(pattern, commit_msg):
    print(
        "Commit message does not follow the format: typeDeModification(partieconcernée): details"
    )
    sys.exit(1)
