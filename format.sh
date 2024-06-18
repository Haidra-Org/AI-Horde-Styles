if # check syntax. If syntax invalid, node will say where.
    node "$1"
then # don't split up Loras, it's annoying
    jq . "$1" --indent 4|perl -0 -pe 's/\s*"(name.+|clip".+|model"\: [0-9].+|is_.+)\s*/ "\1/g'|sponge "$1"
fi
