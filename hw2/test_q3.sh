#!/bin/bash
# 
# test_q3.sh - generates a test vector for HW2.Q3
# 
# usage: ./test_q3.sh
#
# Jessie Li
# CS 51, Fall 2024
# 

TEXT_FILE="test_q3.txt"

cat > "$TEXT_FILE" <<EOF
# 
# test_q3.txt - test vector for Q3
# 
# Expect output 1 if A > B.
# 
# Jessie Li
# CS 51, Fall 2024
# 
A[4] B[4] Q 
EOF

count=0
for A in {0..15}; do
    for B in {0..15}; do
        C=$(( A > B ? 1 : 0 ))
        printf "0x%x 0x%x %d\n" $A $B $C >> "$TEXT_FILE"
        ((count++))
    done
done

echo "Created ${count} test cases."
exit 0
