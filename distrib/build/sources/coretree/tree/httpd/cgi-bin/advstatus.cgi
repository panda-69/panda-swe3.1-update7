#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use strict;
use warnings;

my $graphcriticalcolour = "#ff0000";
my $graphwarningcolour  = "#ff5d00";
my $graphnominalcolour  = "#ffa200";
my $graphblankcolour    = "#ffffff";
my $graphbgcolour;

my $graphalertcritical = 90;
my $graphalertwarning  = 70;
my $errormessage = '';

&showhttpheaders();

&openpage($tr{'advanced status information'}, 1, '', 'about your smoothie');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

&openbox($tr{'memory'});

my @echo = `/usr/bin/free -ot`;
shift(@echo);

print <<END
<br/>
<table style='width: 93%; margin-left: auto; margin-right: auto; border-collapse: collapse; border: solid 1px #c0c0c0;'>
<tr>
	<th>&nbsp;</th>
	<th style='text-align: right; width: 6em'>$tr{'adv total'}</th>
	<th style='text-align: right; width: 6em'>$tr{'adv used'}</th>
	<th style='text-align: right; width: 6em'>$tr{'adv free'}</th>
	<th>&nbsp;</th>
	<th style='text-align: center; width: 150px;'>$tr{'adv used%'}</th>
	<th style='text-align: right; width: 6em;' >$tr{'adv shared'}</th>
	<th style='text-align: right; width: 6em;' >$tr{'adv buffers'}</th>
	<th style='text-align: right; width: 6em;' >$tr{'adv cached'}</th>
</tr>
END
;

foreach my $mline (@echo) {
	chomp($mline);

	my ($mdev, $mtotal, $mused, $mfree, $mshared, $mbuffers, $mcached) = split(/\s+/, $mline);
	my $mperc = 0;

	if ($mtotal) {
		$mperc = int((($mused/$mtotal)*100));
	}

	if ($mperc > $graphalertcritical) {
		$graphbgcolour = $graphcriticalcolour;
	} 
	elsif ($mperc > $graphalertwarning) {
		$graphbgcolour = $graphwarningcolour;
	}
	elsif ($mperc > 0) {
		$graphbgcolour = $graphnominalcolour;
	}
	else {
		$graphbgcolour = $graphblankcolour;
	}

	if ( $mdev eq "Total:" ) {
		print '<tr><td colspan="9"><hr></td></tr>';
	}
	if ($mdev eq 'Mem:') {
		$graphbgcolour = $graphnominalcolour;
	}
	print <<END
<tr>
	<td style='text-align: right;'><code>$mdev</code></td>
	<td style='text-align: right;'><code>${mtotal}</code></td>
	<td style='text-align: right;'><code>${mused}K</code></td>
	<td style='text-align: right;'><code>${mfree}K</code></td>
	<td style='text-align: right;'><code>&nbsp;</code></td>
	<td style='text-align: right; width: 160px; white-space: nowrap;'>
		<table class='blank' style='width: 150px; border: 1px #505050 solid;'>
		<tr>
END
;

	if ($mperc < 1) {
		print "\t\t\t<td style='background-color: $graphbgcolour; width: 1%; text-align: center;'><code>$mperc%</code></td>\n";
	}
	else {
		print "\t\t\t<td style='background-color: $graphbgcolour; width: $mperc%; text-align: center;'><code>$mperc%</code></td>\n";
	}
	print <<END
			<td style='background-color: $graphblankcolour;'>&nbsp;</td>
		</tr>
		</table></td>
END
;

	if ( (($mbuffers) && $mbuffers ne "") || (($mcached) && $mcached ne "") ) {
		print <<END
	<td style='text-align: right;'><code>${mshared}K</code></td>
	<td style='text-align: right;'><code>${mbuffers}K</code></td>
	<td style='text-align: right;'><code>${mcached}K</code></td>
END
;
	}
	else {
		print <<END
	<td></td>
	<td></td>
	<td></td>
END
;
	}
	print <<END
</tr>
END
;
}

print <<END
</table><br/>
END
;

&closebox();

&openbox($tr{'disk usage'});

@echo = `df -h`;
shift(@echo);

print <<END
<br/>
<table style='width: 93%; margin-left: auto; margin-right: auto; border-collapse: collapse; border: solid 1px #c0c0c0;'>
<tr>
	<th style='text-align: left; width: 120px;'>$tr{ 'adv filesystem' }</th>
	<th style='text-align: left; width: 100px;'>$tr{ 'adv mount point' }</th>
	<th style='text-align: right; width: 80px;'>$tr{ 'adv size'}</th>
	<th style='text-align: right; width: 80px;'>$tr{ 'adv used'}</th>
	<th style='text-align: right; width: 100px;'>$tr{ 'adv available'}</th>
	<th>&nbsp;</th>
	<th style='text-align: center; width: 150px;'>$tr{ 'adv used%' }</th>
</tr>
END
;

foreach my $mount (@echo) {
	chomp($mount);
	my ($dev, $size, $size_used, $size_avail, $size_percentage, $mount_point) = split(/\s+/,$mount);

	$size_percentage =~ s/\%//;

	if (int($size_percentage) > $graphalertcritical) {
		$graphbgcolour = $graphcriticalcolour;
	}
	elsif (int($size_percentage) > $graphalertwarning) {
		$graphbgcolour = $graphwarningcolour;
	}
	elsif (int($size_percentage) > 0) {
		$graphbgcolour = $graphnominalcolour;
	}
	else {
		$graphbgcolour = $graphblankcolour;
	}

	print <<END
<tr>
	<td><code>$dev</code></td>
	<td><code>$mount_point</code></td>
	<td style='text-align: right;'><code>$size</code></td>
	<td style='text-align: right;'><code>$size_used</code></td>
	<td style='text-align: right;'><code>$size_avail</code></td>
	<td><code>&nbsp;</code></td>
	<td><table class='blank' style='width: 150px; border: 1px #505050 solid;'>
<tr>
END
;

	if (int($size_percentage) < 1) {
		print "\t<td style='background-color: $graphbgcolour; width: 1%; text-align: center;'><code>${size_percentage}%</code></td>\n";
	}
	else {
		print "\t<td style='background-color: $graphbgcolour; width: ${size_percentage}%; text-align: center;'><code>${size_percentage}%</code></td>\n";
	}

	print <<END
	<td style='background-color: $graphblankcolour;'>&nbsp;</td>
</tr>
</table></td>
</tr>
END
;
}

print <<END
</table><br/>
END
;

&closebox();

&openbox($tr{'inode usage'});
@echo = `df -i`;
shift(@echo);

print <<END
<br/>
<table style='width: 93%; margin-left: auto; margin-right: auto; border-collapse: collapse; border: solid 1px #c0c0c0;'>
<tr>
	<th style='text-align: left; width: 120px;'>$tr{ 'adv filesystem' }</th>
	<th style='text-align: left; width: 100px;'>$tr{ 'adv mount point' }</th>
	<th style='text-align: right; width: 80px;'>$tr{ 'adv inodes' }</th>
	<th style='text-align: right; width: 80px;'>$tr{ 'adv used' }</th>
	<th style='text-align: right; width: 100px;'>$tr{ 'adv free' }</th>
	<th>&nbsp;</th>
	<th style='text-align: center; width: 150px;'>$tr{ 'adv used%' }</th>
</tr>
END
;

foreach my $mount (@echo) {
	chomp($mount);
	my ($dev, $size, $size_used, $size_avail, $size_percentage, $mount_point) = split(/\s+/,$mount);

	$size_percentage =~ s/\%//g;

	if (int($size_percentage) > $graphalertcritical) {
		$graphbgcolour = $graphcriticalcolour;
	}
	elsif (int($size_percentage) > $graphalertwarning) {
		$graphbgcolour = $graphwarningcolour;
	}
	elsif (int($size_percentage) > 0) {
		$graphbgcolour = $graphnominalcolour;
	}
	else {
		$graphbgcolour = $graphblankcolour;
	}

	print <<END
<tr>
	<td ><code>$dev</code></td>
	<td ><code>$mount_point</code></td>
	<td style='text-align: right;'><code>$size</code></td>
	<td style='text-align: right;'><code>$size_used</code></td>
	<td style='text-align: right;'><code>$size_avail</code></td>
	<td><code>&nbsp;</code></td>
	<td><table class='blank' style='width: 150px; border: 1px #505050 solid;'>
<tr>
END
;

	if (int($size_percentage) < 1) {
		print "\t<td style='background-color: $graphbgcolour; width: 1%; text-align: center;'><code>${size_percentage}%</code></td>\n";
	}
	else {
		print "\t<td style='background-color: $graphbgcolour; width: ${size_percentage}%; text-align: center;'><code>${size_percentage}%</code></td>\n";
	}

	print <<END
	<td style='background-color: $graphblankcolour;'>&nbsp;</td>
</tr>
</table></td>
</tr>
END
;
}

print <<END
</table><br/>
END
;

&closebox();

&openbox($tr{'uptime and users'});

my @who = split /\n/, &pipeopen( '/usr/bin/w' );
my ( $time, $up, $users, $load ) = ( $who[0] =~/\s+([^\s]*)\s+up\s+([^,]*),\s+([^,]*),\s+(.*)/ );

print "<div style='text-align: center;'>$time,  up $up,  $users,  $load</div>";

print <<END
<br/>
<table style='width: 93%; margin-left: auto; margin-right: auto; border-collapse: collapse; border: solid 1px #c0c0c0;'>
<tr>
	<th style='text-align: left;'>$tr{'adv user'}</th>
	<th style='text-align: left;'>$tr{'adv tty'}</th>
	<th style='text-align: left;'>$tr{'adv login'}</th>
	<th style='text-align: left;'>$tr{'adv idle'}</th>
	<th style='text-align: left;'>$tr{'adv jcpu'}</th>
	<th style='text-align: left;'>$tr{'adv pcpu'}</th>
	<th style='text-align: left;'>$tr{'adv what'}</th>
</tr>
END
;

shift @who;  # remove the header information
shift @who;  # remove the header information

foreach my $whol (@who){
	my ( $user, $tty, $login, $idle, $jcpu, $pcpu, $what ) = split /\s+/, $whol;
	print <<END
<tr>
	<td>$user</td>
	<td>$tty</td>
	<td>$login</td>
	<td>$idle</td>
	<td>$jcpu</td>
	<td>$pcpu</td>
	<td>$what</td>
</tr>
END
;
}

print <<END
</table><br/>
END
;

&closebox();

my %ethersettings;
&readhash(  "${swroot}/ethernet/settings", \%ethersettings );
my %devices;
$devices{$ethersettings{'GREEN_DEV'}} = $tr{'green'};
$devices{$ethersettings{'ORANGE_DEV'}} = $tr{'orange'};
$devices{$ethersettings{'RED_DEV'}} = $tr{'red'};
$devices{$ethersettings{'PURPLE_DEV'}} = $tr{'purple'};

&openbox($tr{'interfaces'});

my @interfaces = split /\n\n/, &pipeopen( '/sbin/ifconfig', '-a' );

my ($devicename, $macaddress, $ipaddress, $mtu, $broadcast, $netmask, $status) = ('','', '', '', '', '', '');

foreach my $interface ( @interfaces ){
	$devicename	= $1 if ( $interface =~ /([^\s]+)/ );
	$macaddress	= $1 if ( $interface =~ /HWaddr\s+(([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2}))/ );
	$ipaddress	= $1 if ( $interface =~ /inet addr:(\d+\.\d+\.\d+\.\d+)/ );
	$mtu		= $1 if ( $interface =~ /MTU:(\d+)/ );
	$broadcast	= $1 if ( $interface =~ /Bcast:(\d+\.\d+\.\d+\.\d+)/ );
	$netmask	= $1 if ( $interface =~ /Mask:(\d+\.\d+\.\d+\.\d+)/ );
	$status	= $1 if ( $interface =~ /\s+(UP)\s+/ );
	my ( $rx, $rxk   ) = ( $interface =~ /RX bytes:(\d+) \((\d+\.\d+ [KMG]*b)\)/ );
	my ( $tx, $txk   ) = ( $interface =~ /TX bytes:(\d+) \((\d+\.\d+ [KMG]*b)\)/ );
	my ( $rxp, $rxe, $rxd, $rxo, $rxf) =
		( $interface =~ /RX packets:(\d+)\s+errors:(\d+)\s+dropped:(\d+)\s+overruns:(\d+)\s+frame:(\d+)/ );
	my ( $txp, $txe, $txd, $txo, $txc) =
		( $interface =~ /TX packets:(\d+)\s+errors:(\d+)\s+dropped:(\d+)\s+overruns:(\d+)\s+carrier:(\d+)/ );

	$devices{$devicename} = "Red" if ($devicename =~ /ppp/);
	$devicename = "$devicename ($devices{$devicename})" if ( $devices{$devicename} );

	print <<END
<br/>
<table style='width: 93%; margin-left: auto; margin-right: auto; border-collapse: collapse; border: solid 1px #c0c0c0;'>
<tr>
	<th colspan='5'>$devicename</th>
</tr>
<tr>
	<th style='width: 4%;' rowspan='8'>&nbsp;</th>
	<td style='width: 23%;'>IP Address:</td>
	<td style='width: 25%;'>$ipaddress</td>
	<td style='width: 23%;'>Broadcast</td>
	<td style='width: 25%;'>$broadcast</td>
</tr>
<tr>
	<td>Netmask</td>
	<td>$netmask</td>
	<td>MTU</td>
	<td>$mtu</td>
</tr>
<tr>
	<td>MAC Address</td>
	<td>$macaddress</td>
	<td>Status</td>
	<td>$status</td>
</tr>
<tr>
	<td>Sent packets</td>
	<td>$txp ($txk)</td>
	<td>Received packets</td>
	<td>$rxp ($rxk)</td>
</tr>
<tr>
	<td>Errors (sent)</td>
	<td>$txe</td>
	<td>Errors (received)</td>
	<td>$rxe</td>
</tr>
<tr>
	<td>Dropped (sent)</td>
	<td>$txd</td>
	<td>Dropped (received)</td>
	<td>$rxd</td>
</tr>
<tr>
	<td>Overruns (sent)</td>
	<td>$txo</td>
	<td>Overruns (received)</td>
	<td>$rxo</td>
</tr>
<tr>
	<td>Carrier (sent)</td>
	<td>$txc</td>
	<td>Frame (received)</td>
	<td>$rxf</td>
</tr>
</table>
<br/>
END
;
}

&closebox();

&openbox($tr{'routing'});

my @routes = split /\n/, &pipeopen( '/sbin/route', '-n' );

print <<END
<br/>
<table style='width: 93%; margin-left: auto; margin-right: auto; border-collapse: collapse; border: solid 1px #c0c0c0;'>
<tr>
	<th style='text-align:left;'>$tr{'adv destination'}</th>
	<th style='text-align:left;'>$tr{'adv gateway'}</th>
	<th style='text-align:left;'>$tr{'adv genmask'}</th>
	<th style='text-align:left;'>$tr{'adv flags'}</th>
	<th style='text-align:left;'>$tr{'adv metric'}</th>
	<th style='text-align:left;'>$tr{'adv ref'}</th>
	<th style='text-align:left;'>$tr{'adv use'}</th>
	<th style='text-align:left;'>$tr{'adv iface'}</th>
</tr>
END
;

shift @routes;  # remove the header information
shift @routes;  # remove the header information

foreach my $routel (@routes){
	my ( $destination, $gateway, $genmask, $flags, $metric, $ref, $use, $iface ) = split (/\s+/, $routel);
	$devices{$iface} = "Red" if ($iface =~ /ppp/);

	print <<END
<tr>
	<td>$destination</td>
	<td>$gateway</td>
	<td>$genmask</td>
	<td>$flags</td>
	<td>$metric</td>
	<td>$ref</td>
	<td>$use</td>
	<td>$devices{$iface} ($iface)</td>
</tr>
END
;
}

print <<END
</table><br/>
END
;

&closebox();
&openbox($tr{'adv hardware'});

my @lspci = split /\n/, &pipeopen( '/usr/sbin/lspci' );

print <<END
<br/>
<table style='width: 93%; margin-left: auto; margin-right: auto; border-collapse: collapse; border: solid 1px #c0c0c0;'>
<tr>
	<th style='text-align:left;'>$tr{'adv address'}&nbsp;</th>
	<th style='text-align:left;'>$tr{'adv type'}</th>
	<th style='text-align:left;'>$tr{'adv device'}</th>
</tr>
END
;

foreach my $devl (@lspci){
	my ( $address, $type, $device ) = ( $devl =~/([^\s]*)\s+([^:]*):\s+(.*)/ );
	print <<END
<tr>
	<td>$address</td>
	<td>$type</td>
	<td>$device</td>
</tr>
END
;
}

print <<END
</table><br/>
END
;

&closebox();

&openbox($tr{'loaded modules'});

my @lsmod = split /\n/, &pipeopen( '/bin/lsmod' );

print <<END
<br/>
<table style='width: 93%; margin-left: auto; margin-right: auto; border-collapse: collapse; border: solid 1px #c0c0c0;'>
<tr>
	<th style='text-align:left;'>$tr{'adv module'}</th>
	<th style='text-align:left;'>$tr{'adv size'}</th>
	<th style='text-align:left;'>$tr{'adv used by'}</th>
</tr>
END
;

shift @lsmod;  # remove the header information

foreach my $modl (@lsmod){
	my ( $module, $size, $usedby ) = split /\s+/, $modl;
	print <<END
<tr>
	<td>$module</td>
	<td>$size</td>
	<td>$usedby</td>
</tr>
END
;
}

print <<END
</table><br/>
END
;

&closebox();

&openbox($tr{'kernel version'});
print "<PRE>";
system ('/bin/uname', '-a');
print "</PRE>\n";
&closebox();

&alertbox('add', 'add');

&closebigbox();
&closepage();

