@import 'lib/flexmaster.cps';

glyph, point > center, contour > p, component  {
    sidebearingLeftSummand: 0.5 * master:SpacingS + 0.5 * glyph:SpacingS;
    sidebearingRightSummand: 0.5 * master:SpacingS + 0.5 * glyph:SpacingS;
    widthFactor: master:WidthF * glyph:WidthF;
    heightFactor: master:HeightF * glyph:HeightF;
}

point > left, point > right, contour > p {
    weightFactor: master:WeightF * glyph:WeightF * WeightF;
}

master {
    SpacingS: 0;
    WidthF: 1;
    HeightF: 1;
    WeightF: 1;
}

glyph {
    SpacingS: 0;
    WidthF: 1;
    HeightF: 1;
    WeightF: 1;
}

point > left, point > right, contour > p {
    WeightF: 1;
}