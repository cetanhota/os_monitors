#!/bin/bash

function comment_on_val {
    local the_reply="$1"
    local the_word="$2"

    if (( the_reply == 1 )); then
        echo "The value is one ($the_word)"
    else
        echo "The value isn't one ($the_word)"
    fi
}

echo "Menu:"
select word in "Yes" "No" "Exit"; do
    case "$REPLY" in
        3) break    ;;
        *) comment_on_val "$REPLY" "$word"   ;;
    esac
done
