#!/bin/perl
# Author: Konrad Micek, Applied Computer Science, Bachelors degree 1st year
# generating maze using Hunt and Kill algorithm

use strict;
use warnings;

# 1 -> left, 2 -> right, 4 -> down, 8 -> up
sub number_to_direction {
    my $numb = $_[0];

    if ( $numb == 1 ) {
        return ( -1, 0 );
    }
    elsif ( $numb == 2 ) {
        return ( 1, 0 );
    }
    elsif ( $numb == 4 ) {
        return ( 0, 1 );
    }
    elsif ( $numb == 8 ) {
        return ( 0, -1 );
    }
}

sub opposite_move {
    my $numb = $_[0];

    if ( $numb == 1 ) {
        return 2;
    }
    elsif ( $numb == 2 ) {
        return 1;
    }
    elsif ( $numb == 4 ) {
        return 8;
    }
    elsif ( $numb == 8 ) {
        return 4;
    }
}

sub random_int {

    # inclusive from both sides
    my $min = $_[0];
    my $max = $_[1] + 1;

    return $min + int( rand( $max - $min ) );
}

sub random_move {
    my @used_moves = @{ $_[0] };
    if ( scalar @used_moves >= 4 ) {
        return 0;
    }

    my $new_direction = 0;

    # grep checks if element exists on array
    while (( $new_direction == 0 )
        || ( grep( /^$new_direction$/, @used_moves ) ) )
    {
        $new_direction = random_int( 0, 3 );

        # get decimal from binary
        $new_direction = 2**$new_direction;
    }
    return $new_direction;
}

sub walk {
    my @grid        = @{ $_[0] };
    my $current_x   = $_[1];
    my $current_y   = $_[2];
    my $x_grid_size = $_[3];
    my $y_grid_size = $_[4];
    my @used_moves  = ();

    while ( scalar @used_moves < 4 ) {
        my $move = random_move( \@used_moves );
        push( @used_moves, $move );
        my @direction = number_to_direction($move);
        my $new_x     = $current_x + $direction[0];
        my $new_y     = $current_y + $direction[1];
        if (   ( $new_x < 0 )
            || ( $new_y < 0 )
            || ( $new_x >= $x_grid_size )
            || ( $new_y >= $y_grid_size )
            || ( $grid[$new_x][$new_y] != 0 ) )
        {
            next;
        }
        $grid[$current_x][$current_y] += $move;
        $grid[$new_x][$new_y]         += opposite_move($move);

        return ( $new_x, $new_y );
    }

    return (-1);
}

sub hunt {
    my @grid        = @{ $_[0] };
    my $x_grid_size = $_[1];
    my $y_grid_size = $_[2];

    for ( my $x = 0 ; $x < $x_grid_size ; $x += 1 ) {
        for ( my $y = 0 ; $y < $y_grid_size ; $y += 1 ) {
            if ( $grid[$x][$y] != 0 ) {
                next;
            }

            my @neighbors = ();
            my @direction;

            for ( my $move_pow = 0 ; $move_pow < 4 ; $move_pow += 1 ) {
                my $move = 2**$move_pow;
                @direction = number_to_direction($move);
                my $x_new = $x + $direction[0];
                my $y_new = $y + $direction[1];
                if (   ( $x_new >= 0 )
                    && ( $x_new < $x_grid_size )
                    && ( $y_new >= 0 )
                    && ( $y_new < $y_grid_size )
                    && ( $grid[$x_new][$y_new] != 0 ) )
                {
                    push( @neighbors, $move );
                }
            }

            if ( scalar @neighbors == 0 ) {
                next;
            }

            my $move = $neighbors[ random_int( 0, scalar @neighbors - 1 ) ];
            @direction = number_to_direction($move);
            $grid[$x][$y] += $move;
            $grid[ $x + $direction[0] ][ $y + $direction[1] ] +=
              opposite_move($move);

            return ( $x, $y );
        }
    }
    return (-1);
}

foreach (@ARGV) {
    if ( ( $_ eq "-h" ) || ( $_ eq "--help" ) ) {
        print
"Application goal is to generate mazes with size specified by user and allow him to resolve it programmatically.\n";
        print
"Different application parts are built in Python (GUI/languages connector), Perl (generator) and Bash (resolver).\n";
        print
"Bash solving takes some time - it is Bash, so it obviously have right to be slow :-)\n";
        print "After generation, picture is saved as file MazeUnresolved.jpeg.\n";
        print "After resolving, picture is saved as file MazeResolved.jpeg.\n";
        print "Picture is also shown in GUI.\n";
        print "Requirements:\n";
        print "For proper working, user should have installed packages PIL (Pillow) and Tkinter.\n";
        print "User should run application on Linux capable of running GUI.\n";
        print "For guaranted experience use the newest version of Python.\n";
        exit;
    }
}
if ( scalar @ARGV != 2 ) {
    print
"That script won't run separately from Python GUI. Starting Python GUI script instead...";
    system "./python_gui.py &";
    exit;
}

my $x_size = $ARGV[0];
my $y_size = $ARGV[1];

# choose randomly start point - better randomization than start from (0, 0)
my @point = ( random_int( 0, $x_size - 1 ), random_int( 0, $y_size - 1 ) );

# create 2D array and init with 0
my @grid = ();
foreach ( 0 .. $y_size - 1 ) {
    foreach my $x ( 0 .. $x_size - 1 ) {
        push( @{ $grid[$x] }, 0 );
    }
}

# Hunt and Kill - walk/hunt
while ( $point[0] > -1 ) {
    @point = walk( \@grid, $point[0], $point[1], $x_size, $y_size );
    if ( $point[0] < 0 ) {
        @point = hunt( \@grid, $x_size, $y_size );
    }
}

# return result as string separated by whitespaces
foreach my $y ( 0 .. $y_size - 1 ) {
    foreach my $x ( 0 .. $x_size - 1 ) {
        print("$grid[$x][$y] ");
    }
}
