/*--------------------------------*- C++ -*----------------------------------*\
  Written by scripts/keyhole_cfd_laserbeamfoam.py (digital-alloy-lab, issue #235)
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    object      alpha.metal;
}
dimensions      [0 0 0 0 0 0 0];
internalField   uniform 0;
boundaryField
{
    lowerWall
    {
        type zeroGradient;
    }
    rightWall
    {
        type zeroGradient;
    }
    leftWall
    {
        type zeroGradient;
    }
    frontAndBack
    {
        type zeroGradient;
    }
    atmosphere
    {
        type inletOutlet;
        inletValue uniform 0;
        value uniform 0;
    }
}
