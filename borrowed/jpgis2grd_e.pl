#!/usr/bin/env perl -w

# Description: 国土地理院の10 mメッシュの標高データを，GMTで扱えるxyz形
# 式に変換し，grdファイルを作成する

# Input data: 基盤地図情報（数値標高モデル）10 mメッシュ（標高）
# Data format: JPGIS 2.0 (GML)
# Datum: 世界測地系（日本測地系2000）
# Source url: http://fgd.gsi.go.jp/download/

# Usage:
# 1つ以上のxmlファイルがあるディレクトリでjpgis2grd.plを実行すると，
# out.grdを生成しますので，適当な名称に変更して下さい．

# 数値地図データの使用にあたっては，国土地理院の指示に従って下さい．
# http://www.gsi.go.jp/LAW/2930-index.html

# Last updated: 2010/12/22 16:38:45.
# Noda, Atsushi

# 0.0.6 (2010/12/15): オプションにGetopt::Longを使い，helpにPod::Usageを使うようにした．
# 0.0.5 (2010/12/14): grdファイルにtitleとremarkを入れられるように修正
# 0.0.4 (2010/05/02): 不必要なエラー表示を消去
# 0.0.3 (2010/05/01): 日本測地系のオプションを消去
# 0.0.2 (2010/03/08): デフォルトで地形データのxyz fileを消すように修正
# 0.0.1 (2010/01/20): 作成

# Kanji code: UTF-8-UNIX

# Modified by H.OTK: サブディレクトリ内のファイルをグリッド化するために特化

use strict;
use Getopt::Long;
use Pod::Usage;

# global option
my $progname = "jpgis2grd.pl";		# プログラム名

# user option
my %opts = ();
GetOptions(\%opts, 'help', 'noremove', 'verbose', 'title=s', 'remark=s');

if ($opts{help}) { pod2usage(-verbose => 2); }
if ($opts{title}) { $opts{title} =~ s/ /_/g; } else { $opts{title} = "="; }
if ($opts{remark}) { $opts{remark} =~ s/ /_/g; } else { $opts{remark} = "="; }
if ($opts{verbose}) { print STDERR "Title = $opts{title}\nRemark=$opts{remark}\n"; }

my $dir = $ARGV[0];
chdir $dir or die "Cannot change working directory $dir: $!";
# from global option
my $outfile = "../${dir}.xyz";
if (-e $outfile) { unlink $outfile; }
my $grdfile = "../${dir}.grd";
if (-e $grdfile) { unlink $grdfile; }

my @file = glob("FG-GML*.xml");
unless (@file) { die "ERROR: there is no GML xml file.\n"; }

my @line = ();

my (@mesh, @lowerCorner, @upperCorner, @height) = ();
my (@xmin, @xmax, @ymin, @ymax, @xint, @yint) = ();
my ($lowerCorner, $upperCorner) = 0;
my ($ymin, $ymax, $xmin, $xmax) = 0;
my ($x_mesh, $y_mesh);		     # 縦と横のメッシュの数
my ($yint, $xint) = 0;		     # メッシュ間の幅
my ($lat, $lon, $height) = 0;	     # 緯度・経度・標高
my ($x, $y, $n) = 0;	   # データの座標位置 ($x, $y) とデータ数 ($n)
my $data_on = 0;

open (OUT, ">>$outfile") || die "ERROR: there is no $outfile.\n";
foreach my $file (@file) {
  open (F, $file) || die "ERROR: there is no GML xml file.\n";
  print STDERR "$file\n";
  while (<F>) {
    chomp;

    # 地図範囲の緯度・経度
    if (/lowerCorner>(.+)</) { 
      @lowerCorner = split(/\s+/, $1); 
      $ymin = sprintf("%.8f", $lowerCorner[0]);
      $xmin = sprintf("%.8f", $lowerCorner[1]);
      # 描画範囲を配列に保存しておく．
      push (@xmin, $xmin);
      push (@ymin, $ymin);
    } 
    if (/upperCorner>(.+)</) { 
      @upperCorner = split(/\s+/, $1);
      $ymax = sprintf("%.8f", $upperCorner[0]);
      $xmax = sprintf("%.8f", $upperCorner[1]);
      # 描画範囲を配列に保存しておく．
      push (@xmax, $xmax);
      push (@ymax, $ymax);
    }

    # 縦と横のメッシュの数
    if (/gml:high>(.+)</) { 
      @mesh = split(/\s+/, $1);
      $x_mesh = $mesh[0];
      $y_mesh = $mesh[1];
      # 縦と横のメッシュ間の幅
      $yint = ($ymax - $ymin)/($y_mesh+1);
      $xint = ($xmax - $xmin)/($x_mesh+1);
      $x = 0;
      $y = 0;
      push (@xint, $xint);
      push (@yint, $yint);
    }

    # データ開始位置の特定
    if (/<gml:tupleList>/) { $data_on = 1; $n = 0; } # $n=0 をリセット
    if (/^\s*$/) { $data_on = 0; $n = 0; } # 空行ならデータ行は終了

    # $n=1以上なら，データ処理の開始
    if ($data_on && $n) {

      @height = split(/,/);
      $height = $height[1];
      $lon = $xmin + $xint/2 + $xint * $x;
      $lat = $ymax - $yint/2 - $yint * $y;

      print OUT "$lon $lat $height\n";	# データを出力

      # xy座標の計算
      if ($x < $x_mesh) { ++$x; } else { $x = 0; ++$y; }
    }
    if ($data_on) { ++$n; }		# データ行のカウント
  }
  close F;
}
close OUT;
&grd();

#-------------------------------------
# Cleaning
unless ($opts{noremove}) {
  if ($opts{verbose}) { print STDERR "Remove $outfile\n"; }
  unlink ($outfile);
}

#-------------------------------------
sub grd {
  $xmin = (sort {$a <=> $b} @xmin)[0];
  $xmax = (sort {$a <=> $b} @xmax)[-1];
  $ymin = (sort {$a <=> $b} @ymin)[0];
  $ymax = (sort {$a <=> $b} @ymax)[-1];
  $xint = (sort {$a <=> $b} @xint)[-1];
  $yint = (sort {$a <=> $b} @yint)[-1];

  $xint = $xint * ($x_mesh+1)/$x_mesh;
  $yint = $yint * ($y_mesh+1)/$y_mesh;

  print STDOUT "Making a grd file.\n";
  my $command="awk '\$3!=NULL{print \$1, \$2, \$3}' out.xyz | xyz2grd -R$xmin/$xmax/$ymin/$ymax -I$xint/$yint -Gtmp.grd -di-9999 -Dlongitude/latitude/height/1/0/$opts{title}/$opts{remark} ";
  if ($opts{verbose}) { print STDERR "Running \"$command\"\n"; }
  system("$command");

  my $command2="grdmath tmp.grd -9999 NAN = ${grdfile}";
  if ($opts{verbose}) { print STDERR "Running \"$command2\"\n"; }
  system("$command2");

  system("grdinfo $grdfile");
}

#-------------------------------------
sub usage {
  print STDERR "Usage: $progname [-h] [-v] [-n] [-t...] [-r...]\n";
  print STDERR "\t-h: Show this message.\n";
  print STDERR "\t-v: Speak much.\n";
  print STDERR "\t-n: Do not remove xyz data file.\n";
  print STDERR "\t-t: Title for the grd file.\n";
  print STDERR "\t-r: Remark for the grd file.\n";
}



__END__

=head1 NAME

 jpgis2grd.pl - Making grd file for GMT from jpgis (gml) xml files

=head1 Usage

 jpgis2grd.pl [options]

=head1 Options

  -h (--help)            Show help message
  -v (--verbose)         Speak much in progress
  -n (--noremove)        Do not remove xyz data file
  -t (--title=string)    Title for grd file
  -r (--remark=string)   Remark for grd file

=cut
