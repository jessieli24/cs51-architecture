#!/bin/bash
# 
# test_q4.sh - generates a test vector for HW2.Q4
# 
# usage: ./test_q4.sh
# 
# Jessie Li
# CS 51, Fall 2024
# 

RANDOM=12
TEXT_FILE="test_q4.txt"

cat > "$TEXT_FILE" <<EOF
# 
# test_q4.txt - test vector for Q4
# 
# Expect:
#   - NotBCD: 1 if the input does not consist of four BCD digits, 0 otherwise 
#   - SixMult: 1 if the input (as BCD) is a multiple of 6, 0 if not BCD or not a multiple of 6
# 
# Jessie Li
# CS 51, Fall 2024
# 
A[4] B[4] C[4] D[4] NotBCD SixMult
0x0 0x0 0x0 0x0 0 1
0x3 0x0 0x1 0x8 0 1
0x9 0x9 0x9 0x6 0 1
0x1 0x2 0x1 0x2 0 1
0x0 0x4 0x5 0x0 0 1
0x0 0x0 0x0 0x1 0 0
0x9 0x9 0x9 0x9 0 0
0x5 0x9 0x0 0x1 0 0
0x1 0x2 0x3 0x4 0 0
0x7 0x0 0x2 0x5 0 0
0x1 0x7 0x7 0xc 1 0
0xa 0x9 0x1 0xe 1 0
EOF

count=0
for ((i = 0; i < 256; i++)); do
    A=$(( RANDOM % 16 ))
    B=$(( RANDOM % 16 ))
    C=$(( RANDOM % 16 ))
    D=$(( RANDOM % 16 ))

    if [[ $A -le 9 && $B -le 9 && $C -le 9 && $D -le 9 ]]; then
        NotBCD=0
        num=$((10#${A}${B}${C}${D}))
        SixMult=$(( num % 6 == 0 ? 1 : 0 ))
    else
        NotBCD=1
        SixMult=0
    fi

    printf "0x%x 0x%x 0x%x 0x%x %d %d\n" $A $B $C $D $NotBCD $SixMult >> "$TEXT_FILE"
    ((count++))
done

echo "Created ${count} test cases."
exit 0