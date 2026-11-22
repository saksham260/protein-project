#!/usr/bin/env bash
# Apply one migration from supabase/migrations to the database in SUPABASE_DB_URL.
#
#   supabase/apply_migration.sh <file.sql> dry-run   # run it, print row counts, ROLL BACK
#   supabase/apply_migration.sh <file.sql> apply     # run it and COMMIT
#   supabase/apply_migration.sh <file.sql> print     # print the SQL that would be sent (no database)
#
# The whole migration runs in ONE transaction: if any statement fails, nothing is kept.
# "-- PREVIEW" queries in the file's header comments are run first, so the log shows the
# state before the change. psql prints each statement's row count (e.g. "UPDATE 2800").
# Used by .github/workflows/apply-migration.yml.
set -euo pipefail

file="${1:-}"
mode="${2:-}"
here="$(cd "$(dirname "$0")" && pwd)"

if [[ ! "$file" =~ ^[0-9]{3}_[A-Za-z0-9_]+\.sql$ ]]; then
  echo "error: give a file name from supabase/migrations, e.g. 016_data_incident_repair.sql" >&2
  exit 2
fi
path="$here/migrations/$file"
[[ -f "$path" ]] || { echo "error: $path not found" >&2; exit 2; }
case "$mode" in dry-run|apply|print) ;; *) echo "error: mode must be dry-run, apply or print" >&2; exit 2 ;; esac

# Statements that cannot run inside one transaction, or that would end it early.
if grep -n -i -E '^[[:space:]]*(rollback|savepoint|vacuum)\b|\bconcurrently\b' "$path" >&2; then
  echo "error: $file has statements that can't run inside a single transaction (above); apply it by hand" >&2
  exit 2
fi

# The file's own top-level "BEGIN;" / "COMMIT;" lines are dropped: this script owns the transaction.
# (plpgsql bodies use "BEGIN" without a semicolon, so they are not touched.)
body="$(grep -v -i -E '^[[:space:]]*(begin|commit)[[:space:]]*;[[:space:]]*$' "$path")"

# "-- PREVIEW ..." header blocks: the commented lines after the heading, uncommented, up to the
# first line that isn't a "-- " comment.
previews="$(awk '
  /^--[[:space:]]*PREVIEW/ { inblk = 1; t = $0; sub(/^--[[:space:]]*/, "", t); gsub(/\047/, "\047\047", t); print "\\echo \047" t "\047"; next }
  inblk && /^-- / { sub(/^-- /, ""); print; next }
  inblk { inblk = 0; print "" }
' "$path")"

end="ROLLBACK;"
[[ "$mode" == "apply" ]] && end="COMMIT;"

sql="\\set ON_ERROR_STOP on
\\echo '== $file ($mode) =='
BEGIN;
\\echo '-- previews (before the change) --'
$previews
\\echo '-- migration --'
$body
\\echo '-- ending transaction: $end --'
$end
"

if [[ "$mode" == "print" ]]; then
  printf '%s\n' "$sql"
  exit 0
fi

: "${SUPABASE_DB_URL:?SUPABASE_DB_URL is not set}"
printf '%s\n' "$sql" | psql "$SUPABASE_DB_URL" --no-psqlrc --set=ON_ERROR_STOP=1 --echo-errors
if [[ "$mode" == "apply" ]]; then
  echo "Committed $file."
else
  echo "Dry run: everything above was rolled back. Nothing was changed."
fi
