#! /bin/csh -f

source include.csh

gmtset PS_MEDIA a4
gmtset PS_PAGE_ORIENTATION landscape #portrait
gmtset MAP_FRAME_TYPE inside #plain
gmtset FORMAT_GEO_MAP +ddd:mmF
gmtset FORMAT_FLOAT_OUT %g
gmtset FONT_ANNOT_PRIMARY 8
gmtset MAP_ANNOT_OFFSET_PRIMARY -0.2c
gmtset MAP_TICK_LENGTH_PRIMARY -0.2c

set light = 45/80
set intfile=${tmp_d}'Joetsu3D.int'

# Regional map

set lonw = 130
set lone = 143
set lats = 33
set latn = 42

set region = $lonw/$lone/$lats/$latn

set grdfile=${grd_d}'Joetsu250m.grd'
#set grdfile='/cygdrive/e/cygwork/Cygwork_AIST/grd/japan250m.kita.grd'
#set grdfile='/cygdrive/e/cygwork/Cygwork_PhD/Tokai_3D/JTOPO30.grd'

set psfile=${out_d}'Joetsu_map.ps'
set regcpt=${tmp_d}'regional.cpt'

rm $psfile

makecpt -Crelief -T-3000/3000/50 > $regcpt 
grdgradient $grdfile -A${light} -G${intfile} -Ne0.6 -V

psbasemap -JM10 -R$region -Ba5f5 -V -K > $psfile
#psbasemap -Jl138/37.5/33/45/1:10000000 -R$region -Ba5f5/a5f5 -V -K > $psfile
grdimage $grdfile -J -R -B -C$regcpt -I${intfile} -V -O -K >> $psfile
#grdcontour $grdfile -J -R -B -C1000 -A5000 -V -O -K >> $psfile
pscoast -J -R -W0.1p -G220 -Df -P -V -O -K >> $psfile

set lonw = 137
set lone = 138.5
set lats = 37
set latn = 38

psxy -J -R -B -Wred -L -O -V << END >> $psfile
${lonw} ${lats}
${lonw} ${latn}
${lone} ${latn}
${lone} ${lats}
END
#137.5 37

ps2pdf ${psfile}

#Closed map

set grdfile=${grd_d}'Joetsu250m.grd'
set region = $lonw/$lone/$lats/$latn
set psfile=${out_d}'Joetsu_zoom.ps'
set regcpt=${tmp_d}'regional.cpt'

rm $psfile

makecpt -Ctopo -T-2000/2000/50 > $regcpt 
psbasemap -JM10 -R$region -Ba.5f.5 -V -K > $psfile
grdimage $grdfile -J -R -B -C$regcpt -V -O -K >> $psfile
grdcontour $grdfile -J -R -B -C100 -A500 -V -O -K >> $psfile
pscoast -J -R -B -W2 -G220 -I1 -Dh -V -O -K >> $psfile

#--test-------------------------------------------
# maybe correct
#psxy -J -R -B -Wred -L -O -V -K << END >> $psfile
#137.878375534 37.4755976480
#137.878375534 37.6637543925
#138.047956635 37.6637543925
#138.047956635 37.4755976480
#END

#psxy -J -R -B -Wblack -L -O -V -K << END >> $psfile
#137.8881512180 37.52573202050
#137.8881512180 37.70628810050
#138.0446842100 37.70628810050
#138.0446842100 37.52573202050
#END
#-------------------------------------------------

set lonlat = ${data_d}'Joetsu3D_SB.lonlat'
set lonw = `awk '($1!="NaN"){print $1}' ${lonlat} | sort -n | head -1`
set lone = `awk '($1!="NaN"){print $1}' ${lonlat} | sort -n | tail -1`
set lats = `awk '($2!="NaN"){print $2}' ${lonlat} | sort -n | head -1`
set latn = `awk '($2!="NaN"){print $2}' ${lonlat} | sort -n | tail -1`

psxy -J -R -B -W1p,255/0/0 -L -O -V << END >> $psfile
${lonw} ${lats}
${lonw} ${latn}
${lone} ${latn}
${lone} ${lats}
END

ps2pdf ${psfile}

#3D seismic topo

set region = $lonw/$lone/$lats/$latn
echo ${region} > Joetsu3D_region.txt

set grdfile=${grd_d}'Joetsu3D_SB.grd'
set psfile=${out_d}'Joetsu_3D.ps'
set regcpt=${tmp_d}'regional.cpt'

rm $psfile

makecpt -Ctopo -T-1900/1900/10 -I > $regcpt
grdgradient $grdfile -A${light} -G${intfile} -Ne0.6 -V
 
psbasemap -JM10 -R$region -Ba.1f.1 -V -K > $psfile
grdimage $grdfile -J -R -B -C$regcpt -I${intfile} -V -O -K >> $psfile
grdcontour $grdfile -J -R -B -C10 -A50 -V -O >> $psfile
#pscoast -J -R -B -W1 -I1 -Dh -V -O >> $psfile

ps2pdf ${psfile}

mv *.pdf ${out_d}