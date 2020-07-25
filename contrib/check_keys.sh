#!/usr/bin/env sh
# AuthorizedKeysCommand check_keys.sh "%u"

LOCKBOX_CONFIG_FILE="~$1/.config/lockbox.conf"
eval LOCKBOX_CONFIG_FILE="$LOCKBOX_CONFIG_FILE"

# If the user doesn't have a lockbox configuration, we shouldn't do anything
if [ -f "$LOCKBOX_CONFIG_FILE" ]; then
  read -d "\n" keys_host keys_user keys_access < "$LOCKBOX_CONFIG_FILE"

  curl_command="-s"
  if [ -z "$keys_access" ]; then
    fetched_keys=$(curl -s "$keys_host/keys/$keys_user")
  else
    fetched_keys=$(curl -s -H "Authorization: Bearer $keys_access" "$keys_host/keys/$keys_user")
  fi

  if [ $? == 0 ]; then
    echo "$fetched_keys"

    authorized_keys_file="~$keys_user/.ssh/authorized_keys"
    eval authorized_keys_file="$authorized_keys_file"
    if [ -f "$authorized_keys_file" ]; then
      regular_authorized_keys=$(sed '/.*### LOCKBOX SECTION.*/{s///;q;}' < "$authorized_keys_file")

      (echo "$regular_authorized_keys"; echo '### LOCKBOX SECTION
# Please do not edit under this section, it is
# automatically generated and may be wiped
# at any time.'; echo "$fetched_keys") > $authorized_keys_file
    fi
  else
    >&2 echo "An error occurred while fetching $1's keys from $keys_host."
  fi
fi
