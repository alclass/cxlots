#!/usr/bin/env python3
"""
fs/dbfs/sqlfs/sqlitefs/show_dbtable_fields_documentation.py

1) nconsecutivos => counts the number of dozens that are consecutive (eg (1, 2)) among themselves:
    2 is consecutive of 1 and viceversa
  1-1 notice that the pair (20, 21) is not graphically consecutive, just as a number
  1-2 notice also that pair (1, 60) is consecutive as modulo 60

2) adjacente1 => counts all dozens that have a neighbour that is arrived at from "one jump"
    it's like 'consecutivos' but with the following differences:
  2-1 the pair (20, 21) is not adjacent-1, though it's a consecutive
  2-2 up-and-down is also adjacent-1, for example, (10, 20) is adjacent-1

2) n_immed_repeat => when a dozen drawn also happened in the previous conc

3) idxshapearea
  this metric started as the radius-metric but, as it was later seen, the latter is reduced to the former,
  ie, the radius-metric is equivalent to figshare and figshape is a variant of
    row_pattern (rowpatt) and column_pattern (colpatt)
  The difference between figshape and row/column patterns is that the former has zeroes grafted
    in between its counting numbers. Example:
  A rowpatt might be: 321 meaning 3 dozens in a row, 2 in another row, 1 in another (6 altogether)
  321 becomes a figshape if it tells whether there are empty rows in between the ones occurring.
  Example:
     321 may be a figshare of 321, 3021, 3201, 30021, ..., 320001 (maximum of 6 digits for rows)
     it is also simmetrical, ie: 321 may be 123, 1023, ..., 100023
     notice that figshare 321 is graphically different than 123, but its area is the same.
  Because of this, integer indices are mapped into the area/figshare values
    and this index value is the one recorded.
    The implement will calculate either area or figshare (one corresponds to the other) and then
    fetch its correspondent index from a pre-processed dict-table.

  (derived-metric) immg_rad_n_cnt_commasep
   => an immaginary circle is abstracted here, the 2D-tuple is composed
     of the circle's radius and center rounded-off integers;
     the radius is multiplied by 100 before being rounded-off to integer

  Example (the former radius-metric):
    (200, 23) 200 is the radius and 23 is the dozen that centers it
    the algorithm centers rows and then columns finding the integer middle;
    the radius is the avg of the squared x, y distances from each dozen to
    its integer middle, where x is row and y is column
    Obs: if dozens form a line or a triangle, None should be returned

Updates:

1) resto6 & resto10 is derived from rowpatt and colpatt,
   rethink them (maybe change them to resto5 & resto12)

2) concs_histogram_json should become (or be renamed to) drawn_dzs_hstgrm_semicoloncommasep

3) coinc_w_prev_count should become (or be renamed to) morethan_1repeat_semicoloncommasep
  Example:
    e1 '10:2,27:3' means
      dozen 10 had two repeats in-depth (3 altogether with current conc)
      dozen 27 had three repeats in-depth (4 altogether with current conc)
    e2 '5:1,33:5' means
      dozen 5 had one immediate reccurrence  (2 altogether with current conc)
      dozen 33 has five immediate reccurrences (6 altogether with current conc)
  formerly: repeat_depth_commasep => the number of concs down history until
   a specified dozen had a repeat (ie happened previously)
   (this method is related to histogram, though not it)
   its former metric-name was concs_dist_array_json

4) n_simmetrical became triplesimmetrics
  The triplesimmetrics is an INT that contains 3 numbers
    n1 the first, if it exists, is the row simmetric
    n2 the second, if it exists, is the column simmetric
    n3 the third, if it exists, is the arithmetic simmetric
      (which is not 'totally' simmetric because, for instance,
       19 should have 91 as simmetrical which does not exist in MS)
    Examples:
        if 01 & 10 happened, it counts 1 row simmetric
        if 01 & 51 happened, it counts 1 column simmetric
        pair 01 & 10 is also an arithmetic simmetric
    Now, suppose a drawn game is (01, 02, 09, 10, 51, 56)
      There are, in the order of summation:
        (1, 51) counts a row simmetric
        (1, 10) counts a column simmetric
        (2, 9) counts another column simmetric
        (1, 10) counts an arithmetic simmetric
      Altogether, the triplesimmetrics is '121' (or 1*10**2+2*10**1+1*10**0)

"""
print(__doc__)
