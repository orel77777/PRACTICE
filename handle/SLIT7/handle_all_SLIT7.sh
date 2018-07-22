#!/bin/bash
l=$(ls | grep fits)
atm="y"
for var in $l
do 
echo -e "$var\n500\n529\n$atm\n" | python ./main.py
if [[ ${var:9:1} == "K" ]]
then
rx0=0.00020453
rx1=0.000234503
ry0=0
ry1=0.015
elif [[ ${var:9:1} == "H" ]]
then
rx0=0.000149372
rx1=0.000177786
ry0=0
ry1=0.016
elif [[ ${var:9:1} == "J" ]]
then
rx0=0.00012055
rx1=0.00013320
ry0=0.002
ry1=0.013
elif [[ ${var:9:1} == "Y" ]]
then
rx0=0.000102730
rx1=0.000119465
ry0=0
ry1=0.009
fi
echo -e "set xrange [${rx0}:${rx1}]\nset yrange [${ry0}:${ry1}]\nset term eps\nunset key\nset format x '%f'\nset tics font ',8\nset mytics 10\nset mxtics 10\nset xlabel '{/Symbol l}, cm'\nset ylabel 'transmission'\nset grid ls 1 lc rgb 'black'\nset grid mxtics ls 1 lc rgb 'grey'\nset grid mytics ls 1 lc rgb 'grey'\nset output 'interpolated_teor_to_prac${var:9:1}.eps'\nplot 'interpolated_teor_to_prac${var:9:1}.txt' w p ls 7 ps 0.15 lc rgb 'black'\nsave 'interpolated_teor_to_prac${var:9:1}.eps'\nreset\nquit\n" | gnuplot
echo -e "set term eps\nunset key\nset format x '%f'\nset tics font ',8'\nset mytics 10\nset mxtics 10\nset xlabel '{/Symbol l}, cm'\nset ylabel 'Nph/{/Symbol D}{/Symbol l}, 1/cm'\nset grid ls 1 lc rgb 'black'\nset grid mxtics ls 1 lc rgb 'grey'\nset grid mytics ls 1 lc rgb 'grey'\nset output 'our_star_phot${var:9:1}.eps'\nplot 'our_star_phot${var:9:1}.txt' w p ls 7 ps 0.15 lc rgb 'black'\nsave 'our_star_phot${var:9:1}.eps'\nreset\nquit\n" | gnuplot
if [[ ${var:9:1} == "K" ]] || [[ ${var:9:1} == "H" ]]
then
echo -e "set term eps\nunset key\nset format x '%f'\nset tics font ',8'\nset mytics 10\nset mxtics 10\nset xlabel '{/Symbol l}, cm'\nset ylabel 'Nph/{/Symbol D}{/Symbol l}, 1/cm'\nset grid ls 1 lc rgb 'black'\nset grid mxtics ls 1 lc rgb 'grey'\nset grid mytics ls 1 lc rgb 'grey'\nset output '${atm:0:1}_${var:0:42}_spectr_abs.eps'\nplot '${atm:0:1}_${var:0:42}_spectr_abs.txt' w p ls 7 ps 0.15 lc rgb 'black'\nsave'${atm:0:1}_${var:0:42}_spectr_abs.eps'\nreset\nquit\n" | gnuplot
elif [[ ${var:9:1} == "J" ]] || [[ ${var:9:1} == "Y" ]]
then
echo -e "set term eps\nunset key\nset format x '%f'\nset tics font ',8'\nset mytics 10\nset mxtics 10\nset xlabel '{/Symbol l}, cm'\nset ylabel 'Nph/{/Symbol D}{/Symbol l}, 1/cm'\nset grid ls 1 lc rgb 'black'\nset grid mxtics ls 1 lc rgb 'grey'\nset grid mytics ls 1 lc rgb 'grey'\nset output '${atm:0:1}_${var:0:44}_spectr_abs.eps'\nplot '${atm:0:1}_${var:0:44}_spectr_abs.txt' w p ls 7 ps 0.15 lc rgb 'black'\nsave'${atm:0:1}_${var:0:44}_spectr_abs.eps'\nreset\nquit\n" | gnuplot
fi
done
echo -e "set term eps\nunset key\nset format x '%f'\nset tics font ',8'\nset mytics 10\nset mxtics 10\nset xlabel '{/Symbol l}, cm'\nset ylabel 'Nph/{/Symbol D}{/Symbol l}, 1/cm'\nset grid ls 1 lc rgb 'black'\nset grid mxtics ls 1 lc rgb 'grey'\nset grid mytics ls 1 lc rgb 'grey'\nset output 'our_star_phot.eps'\nplot 'our_star_phot.txt' w p ls 7 ps 0.15 lc rgb 'black'\nsave 'our_star_phot.eps'\nreset\nquit\n" | gnuplot
echo -e "set xrange [0.00010:0.00024]\nset yrange [0:0.0175]\nset term eps\nunset key\nset format x '%f'\nset tics font ',8'\nset mytics 10\nset mxtics 10\nset xlabel '{/Symbol l}, cm'\nset ylabel 'transmission'\nset grid ls 1 lc rgb 'black'\nset grid mxtics ls 1 lc rgb 'grey'\nset grid mytics ls 1 lc rgb 'grey'\nset output 'all_in_res.eps'\nplot 'interpolated_teor_to_pracJ.txt' w p ls 7 ps 0.15 lc rgb 'black', 'interpolated_teor_to_pracH.txt' w p ls 7 ps 0.15 lc rgb 'red', 'interpolated_teor_to_pracK.txt' w p ls 7 ps 0.15 lc rgb 0x006400, 'interpolated_teor_to_pracY.txt' w p ls 7 ps 0.15 lc rgb 'blue'\nsave 'all_in_res.eps'\nreset\nquit\n" | gnuplot
