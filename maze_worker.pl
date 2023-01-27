#!/bin/perl
# Author: Konrad Micek, Applied Computer Science, Bachelors degree 1st year

use strict;
use warnings;

# Hunt and Kill algorithm
# http://weblog.jamisbuck.org/2011/1/24/maze-generation-hunt-and-kill-algorithm

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

sub randomInt {

    # inclusive from both sides
    my $min = $_[0];
    my $max = $_[1] + 1;

    return $min + int( rand( $max - $min ) );
}

sub random_move {
    my @usedMoves = @{ $_[0] };
    if ( scalar @usedMoves >= 4 ) {
        return 0;
    }

    my $newDirection = 0;

    # grep checks if element exists on array
    while (( $newDirection == 0 )
        || ( grep( /^$newDirection$/, @usedMoves ) ) )
    {
        $newDirection = randomInt( 0, 3 );

        # get decimal from binary
        $newDirection = 2**$newDirection;
    }
    return $newDirection;
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

            my $move = $neighbors[ randomInt( 0, scalar @neighbors - 1 ) ];
            @direction = number_to_direction($move);
            $grid[$x][$y] += $move;
            $grid[ $x + $direction[0] ][ $y + $direction[1] ] +=
              opposite_move($move);

            return ( $x, $y );
        }
    }
    return (-1);
}

# @ARGV = ( 4, 5 );

my $x_size = $ARGV[0];
my $y_size = $ARGV[1];

# choose randomly start point - better randomization than start from (0, 0)
my @point = ( randomInt( 0, $x_size - 1 ), randomInt( 0, $y_size - 1 ) );

# create 2D array and init with 0
my @grid = ();
foreach ( 0 .. $y_size - 1 ) {
    foreach my $x ( 0 .. $x_size - 1 ) {
        push( @{ $grid[$x] }, 0 );
    }
}

while ( $point[0] > -1 ) {
    @point = walk( \@grid, $point[0], $point[1], $x_size, $y_size );
    if ( $point[0] < 0 ) {
        @point = hunt( \@grid, $x_size, $y_size );
    }
}

foreach my $y ( 0 .. $y_size - 1 ) {
    foreach my $x ( 0 .. $x_size - 1 ) {
        print( "$grid[$x][$y] " );
    }
}
