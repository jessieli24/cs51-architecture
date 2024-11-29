#!/bin/bash
# 
# q1_test.sh - generates a test vector for HW4.Q1
# 
# usage: ./q1_test.sh
#
# Jessie Li CS 51 Fall 2024
# 

TEXT_FILE="q1_test.txt"

cat > "$TEXT_FILE" <<EOF
# 
# q1_test.txt - test vector for HW4.Q1
# 
# 
# Q = Cnd(CC, ifun)
# 
# Jessie Li, CS 51 Fall 2024
# 
ifun[4] CC[3] Q 
EOF

D2B=({0..1}{0..1}{0..1}{0..1})
count=0

# ifun from 0 to 6
for ifun in {0..6}; do
    # CC: Z / S / O
    for Z in {0..1}; do
        for S in {0..1}; do
            for O in {0..1}; do
    
            case $ifun in
                0)
                Cnd=1                       # always
                ;;
                1)
                Cnd=$(( $S ^ $O | $Z ))     # le
                ;;
                2)
                Cnd=$(( $S ^ $O ))          # l
                ;;
                3)
                Cnd=$(( $Z ))               # e
                ;;
                4)
                Cnd=$(( ~$Z ))              # ne
                ;;
                5)
                Cnd=$(( ~($S ^ $O) ))       # ge
                ;;
                6)
                Cnd=$(( ~($S ^ $O) & ~$Z )) # g
                ;;
                *)
                Cnd=0  # default case (unknown ifun)
                ;;
            esac

            # printf "%04d %d%d%d %d\n" $(bc <<< "ibase=10;obase=2;$ifun") $Z$S$O $Cnd >> "$TEXT_FILE"
            # just the last bit of Cnd
            echo "${D2B[$ifun]} $Z$S$O $(( Cnd & 1 ))" >> "$TEXT_FILE"
            ((count++))
            done
        done
    done
done

# invalid ifun
echo "0111 000 0" >> "$TEXT_FILE"
echo "1000 000 0" >> "$TEXT_FILE"

echo "Created ${count} valid + 2 invalid test cases."
exit 0