#!/bin/bash
cd $pyduino
inotifywait -q -m -e close_write data/gelita_borehole |
while read -r filename event; do
      #./myfile.py         # or "./$filename"
      #  date >> b.txt
      #aDATE=$(date +"%Y_%m_%d_%H_%M_%S")_gelita
      #cp data/gelita_borehole data/tmp
      #mv data/tmp data/$aDATE
      python python/gelita_pizo_update_mango.py
done

