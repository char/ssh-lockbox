#!/usr/bin/env sh
# AuthorizedKeysCommand check_keys.sh "%u"

KEYS_HOST="https://keys.hackery.site/"
KEYS_USER="$1"

fetched_keys=`curl -s "$KEYS_HOST/keys/$KEYS_USER"`
if [ $? == 0 ]; then
  echo $fetched_keys

  authorized_keys_file="~$KEYS_USER/.ssh/authorized_keys"
  if [ -f "$authorized_keys_file" ]; then
    regular_authorized_keys=`sed '/.*###### SSH-KEY-AUTHORITY SECTION ######.*/{s///;q;}' < "$authorized_keys_file"`

    (echo $regular_authorized_keys; echo '###### SSH-KEY-AUTHORITY SECTION ######
# PLEASE DO NOT EDIT UNDER THIS SECTION
# IT WILL BE WIPED BY SSH-KEY-AUTHORITY'; echo $fetched_keys) > authorized_keys_file
  fi
else
  >&2 echo "An error occurred while fetching $KEYS_USER's keys from $KEYS_HOST."
fi
