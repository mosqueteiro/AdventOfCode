#!/bin/env bash
# Creates and files for new AoC day.
# --day N : required
# --name filename : required

if [[ $# = 0 ]]; then
	echo "--day N and --name filename are required" >&2
	exit 1
fi
while [[ $# -gt 0 ]]; do
    case "$1" in
	--day)
		dayN=$((10#$2))
		day=$(printf "day%02d" $dayN)
		shift 2
		;;
	--name)
		name="$2"
		shift 2
		;;
	*)
		echo "Unknown option: $1" >&2
		exit 1
		;;
    esac
done

source .env

echo "Creating directory: $day"
mkdir "$day"
touch "$day/$name"
touch "$day/example.txt"
curl "https://adventofcode.com/2024/day/$dayN/input" -H "Cookie: $COOKIE_SECRET" -o "$day/input.txt"
echo "Input received."

PYPROJ="pyproject.toml"

shopt -s lastpipe
grep -no "^day[0-9]\{2\}" $PYPROJ | while IFS=: read line dayline; do
	if (( $((10#${dayline#day})) > $dayN )); then
		insert_line=$line
		break
	fi
	prev_day=$dayline
	prev_line=$line
done

if [ -z "$insert_line" ]; then
	if [ -z "$prev_day" ]; then
		TASK_HEAD=$(grep -n "tasks" $PYPROJ | cut -d: -f1)
		insert_line=$(( $TASK_HEAD + 1 ))
	else
		insert_line=$(( $prev_line + 1 ))
	fi
fi

sed -i "${insert_line}i ${day} = { cmd = \"ipython -i $name -- -f input.txt\", cwd = \"$day\" }" $PYPROJ
sed -i "${insert_line}i ${day}-test = { cmd = \"ipython -i $name -- --test\", cwd = \"$day\" }" $PYPROJ
echo "new pixi tasks for $day added"

