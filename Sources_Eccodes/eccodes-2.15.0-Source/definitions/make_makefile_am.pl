#!/usr/bin/perl
use strict;

my @sub;
push @sub , ".";
navigate(".");
foreach my $d ( sort @sub )
{
  process($d);
}
print "EXTRA_DIST=CMakeLists.txt\n\n";
print "include \$(DEVEL_RULES)\n";

sub navigate {
	my ($dir) = @_;

	opendir(DIR,$dir);
	foreach my $d ( readdir(DIR) )
	{
		next if($d =~ /^\./);

		if(-d "$dir/$d")
		{
			push @sub , "$dir/$d";
			navigate("$dir/$d");
		}
	}
	closedir(DIR);
}

sub process {
	my ($dir) = @_;
    my @files;

	opendir(DIR,$dir);
	foreach my $d ( readdir(DIR) )
	{
		next if($d =~ /^\./);

		unless (-d $d) {
			push @files, $d if($d =~ /\.(txt|list|table|def|grib|sh)$/);
		}

	}
	closedir(DIR);

	if(@files)
	{
		my $name;


		if($dir eq ".")
		{
			$name = "";
			print "#This file is generated by make_makefile_am.pl\n";
			print "#  DON'T EDIT!!!\n";
			print "definitionsdir = \@ECCODES_DEFINITION_PATH\@\n";
		}
		else
		{
			$dir  =~ s/^\.\///;
			$name = "$dir";
			$name =~ s/\W/_/g;
			print "definitions${name}dir = \@ECCODES_DEFINITION_PATH\@/$dir\n";
		}


		print "dist_definitions${name}_DATA = ";

		foreach my $f ( sort @files )
		{
			print "\\\n\t$dir/$f";
		}

		print "\n";
		print "\n";

	}


}
