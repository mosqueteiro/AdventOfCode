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
		dayN="$2"
		day="day$dayN"
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

mkdir "$day"
touch "$day/$name"
touch "$day/example.txt"
curl "https://adventofcode.com/2024/day/$dayN/input" -H "Cookie: $COOKIE_SECRET" -o "$day/input.txt"
# TODO: insert pixi tasks for day

