#!/bin/bash
# for use in local dev only.

set -e

echo 'Migrating database...'
flask db upgrade
echo 'Seeding database...'
python3 seed.py
echo 'Done.'
