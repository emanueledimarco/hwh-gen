#!/usr/bin/perl -w

################################################################################
#                                                                             ##
#                    MadGraph/MadEvent                                        ##
#                                                                             ##
# FILE : split.pl                                                             ##
# VERSION : 1.0                                                               ##
# DATE : 23 December 2007                                                     ##
# AUTHOR : Michel Herquet (UCL-CP3)                                           ##
#                                                                             ##
# DESCRIPTION : script to split LHE events files                              ##
# USAGE :                                                                     ##
# ./split.pl numeventschunk events1.lhe.gz events2.lhe.gz events.lhe.gz            ##                                                   ##
################################################################################

use POSIX qw(ceil);

if ( $#ARGV < 3 ) {
     die "This script must be called with at least four arguments!\n";
}

my $nevents_chunk=$ARGV[0];
my $outfile1=$ARGV[1];
my $outfile2=$ARGV[2];
my $infile=$ARGV[3];

if ( $nevents_chunk<0) {
     die "The first argument should range from 0 to the total number of events in the LHE file\n";
}

#print "Unzipping input file...\n";

#system("gunzip $infile")==0 || die "Error while unzipping $infile, stopping\n";
#$infile=~ s/\.gz//;

print "Reading input file...\n";

open(INFILE,"$infile") || die "Cannot open input file called $infile, stopping\n";

while(<INFILE>)
{
    $fulltext .= $_;
} 

close(INFILE);

#print "Rezipping input file...\n";

#system("gzip $infile")==0 || die "Error while rezipping $infile, stopping\n";

my $begin_tag='<!--'."\n";
my $end_tag='-->';
if ($fulltext =~ m/<header>/) {
 $begin_tag='<header>'."\n";
 $end_tag='</header>';
}

my $begin_init='<init>'."\n";
my $end_init='</init>';
my $begin_events='</init>'."\n";
my $end_events='</LesHouchesEvents>';

($banner)= $fulltext=~ m/$begin_tag(.*)$end_tag/s;
($init)= $fulltext=~ m/$begin_init(.*)$end_init/s;
($events)= $fulltext=~ m/$begin_events(.*)$end_events/s;

($num_events)= $banner=~ m/#  Number of Events\s*:(.*)\n/;
($xsec)= $banner=~ m/#  Integrated weight \(pb\)\s*:(.*)\n/;
$num_events =~ s/^\s*(\S*(?:\s+\S+)*)\s*$/$1/;
$xsec =~ s/^\s*(\S*(?:\s+\S+)*)\s*$/$1/;
$disp_xsec=sprintf('%0.5E',$xsec);

print "File $infile read with $num_events events and $xsec xsec\n";

$num_events1=$nevents_chunk;
$num_events2=$num_events-$num_events1;

print "Now outputting $outfile1 with $num_events1 events and $outfile2 with $num_events2 events\n";
$outfile1=~ s/\.gz//;
$outfile2=~ s/\.gz//;
open(OUTFILE1,">$outfile1") || die "Cannot open output file called $outfile1, stopping\n";
open(OUTFILE2,">$outfile2") || die "Cannot open output file called $outfile2, stopping\n";


$banner1=$banner;

$uwgt1=sprintf('%0.5E',$xsec/$num_events1);

$banner1=~ s/#  Integrated weight \(pb\)\s*:(.*)\n/#  Integrated weight (pb)  :  $disp_xsec\n/;
$banner1=~ s/#  Number of Events\s*:(.*)\n/#  Number of Events        :  $num_events1\n/;
$banner1=~ s/#  Unit wgt\s*:(.*)\n/#  Unit wgt                :  $uwgt1\n/;

$banner2=$banner;

$uwgt2=sprintf('%0.5E',$xsec/$num_events2);

$banner2=~ s/#  Integrated weight \(pb\)\s*:(.*)\n/#  Integrated weight (pb)  :  $disp_xsec\n/;
$banner2=~ s/#  Number of Events\s*:(.*)\n/#  Number of Events        :  $num_events2\n/;
$banner2=~ s/#  Unit wgt\s*:(.*)\n/#  Unit wgt                :  $uwgt2\n/;

print OUTFILE1 "<LesHouchesEvents version=\"1.0\">\n";
print OUTFILE1 $begin_tag;
print OUTFILE1 $banner1;
print OUTFILE1 $end_tag."\n";
print OUTFILE1 "<init>\n";
print OUTFILE1 $init;
print OUTFILE1 "</init>\n";

print OUTFILE2 "<LesHouchesEvents version=\"1.0\">\n";
print OUTFILE2 $begin_tag;
print OUTFILE2 $banner2;
print OUTFILE2 $end_tag."\n";
print OUTFILE2 "<init>\n";
print OUTFILE2 $init;
print OUTFILE2 "</init>\n";

@events = split('\n',$events);

$newblock = 0;
$i=0;

foreach (@events) {

	$curr=$_;
	
	if($newblock==1) {
		$curr =~ s/^\s+//;
		@param=split(/\s+/,$curr);
		if ($#param != 5) { die "Not right number of param in first line of event"; }
		if ($i<=$num_events1) {
			$curr=" $param[0] $param[1] $uwgt1 $param[3] $param[4] $param[5]";
		} else {
			$curr=" $param[0] $param[1] $uwgt2 $param[3] $param[4] $param[5]";
		}
		$newblock=0;
	}
	
	if($curr =~ m/<event>/) {$newblock=1;$i++;}
	
	if ($i<=$num_events1) {
		print OUTFILE1 $curr."\n";
	} else {
		print OUTFILE2 $curr."\n";
	}

}

print OUTFILE1 "</LesHouchesEvents>\n";
print OUTFILE2 "</LesHouchesEvents>\n";

close(OUTFILE1);
close(OUTFILE2);

#print "Zipping output files...\n";

#system("gzip -f $outfile1")==0 || die "Error while zipping $outfile1, stopping\n";
#system("gzip -f $outfile2")==0 || die "Error while zipping $outfile2, stopping\n";
