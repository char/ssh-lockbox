#!/usr/bin/env sh
# AuthorizedKeysCommand check_keys.sh "%u"

KEYS_HOST="https://keys.hackery.site/"
KEYS_USER="$1"

fetched_keys=`curl -s "$KEYS_HOST/keys/$KEYS_USER"`
if [ $? == 0 ]; then
  echo $fetched_keys

  authorized_keys_file="~$KEYS_USER/.ssh/authorized_keys"
  if [ -f "$authorized_keys_file" ]; then
    regular_authorized_keys=`sed '/.*### LOCKBOX SECTION.*/{s///;q;}' < "$authorized_keys_file"`

    (echo $regular_authorized_keys; echo '### LOCKBOX SECTION
# Please do not edit under this section, it is
# automatically generated and may be wiped
# at any time.'; echo $fetched_keys) > authorized_keys_file
  fi
else
  >&2 echo "An error occurred while fetching $KEYS_USER's keys from $KEYS_HOST."
fi
