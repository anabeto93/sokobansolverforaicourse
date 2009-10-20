Storage 
{
	{ Format 1.33 }
	{ GeneratedFrom TSCD-version-2.20 }
	{ WrittenBy morten }
	{ WrittenOn "" }
}

Document 
{
	{ Type "Statechart Diagram" }
	{ Name TopLevel.scd }
	{ Author morten }
	{ CreatedOn "" }
	{ Annotation "" }
	{ Hierarchy True }
}

Page 
{
	{ PageOrientation Landscape }
	{ PageSize A4 }
	{ ShowHeaders False }
	{ ShowFooters False }
	{ ShowNumbers False }
}

Scale 
{
	{ ScaleValue 1 }
}

# GRAPH NODES

SDCDefaultState 1
{
	{ Name "" }
	{ Annotation "" }
	{ Parent 0 }
	{ Index "" }
}

SCDOrState 2
{
	{ Name "Read File" }
	{ Annotation "" }
	{ Parent 0 }
	{ Index "" }
}

SCDOrState 3
{
	{ Name "Next Command" }
	{ Annotation "" }
	{ Parent 0 }
	{ Index "" }
}

SCDOrState 4
{
	{ Name "Follow Line" }
	{ Annotation "" }
	{ Parent 0 }
	{ Index "" }
}

SCDOrState 5
{
	{ Name "Turn Around" }
	{ Annotation "" }
	{ Parent 0 }
	{ Index "" }
}

SCDOrState 6
{
	{ Name "Turn Right" }
	{ Annotation "" }
	{ Parent 0 }
	{ Index "" }
}

SCDOrState 7
{
	{ Name "Turn Left" }
	{ Annotation "" }
	{ Parent 0 }
	{ Index "" }
}

# GRAPH EDGES

SCDTransitionEdge 8
{
	{ Name "" }
	{ Annotation "" }
	{ Parent 0 }
	{ Subject1 1 }
	{ Subject2 2 }
}

SCDTransitionEdge 9
{
	{ Name "" }
	{ Annotation "" }
	{ Parent 0 }
	{ Subject1 2 }
	{ Subject2 3 }
}

SCDTransitionEdge 10
{
	{ Name "val='a'" }
	{ Annotation "" }
	{ Parent 0 }
	{ Subject1 3 }
	{ Subject2 5 }
}

SCDTransitionEdge 11
{
	{ Name "val='f'" }
	{ Annotation "" }
	{ Parent 0 }
	{ Subject1 3 }
	{ Subject2 4 }
}

SCDTransitionEdge 12
{
	{ Name "!Finished" }
	{ Annotation "" }
	{ Parent 0 }
	{ Subject1 5 }
	{ Subject2 5 }
}

SCDTransitionEdge 13
{
	{ Name "!Detect crossing" }
	{ Annotation "" }
	{ Parent 0 }
	{ Subject1 4 }
	{ Subject2 4 }
}

SCDTransitionEdge 14
{
	{ Name "Finished" }
	{ Annotation "" }
	{ Parent 0 }
	{ Subject1 5 }
	{ Subject2 2 }
}

SCDTransitionEdge 16
{
	{ Name "(val='u' && heading='left')||\r(val='r' && heading='up')||\r(val='d' && heading='right')||\r(val='l' && heading='down')" }
	{ Annotation "" }
	{ Parent 0 }
	{ Subject1 3 }
	{ Subject2 6 }
}

SCDTransitionEdge 17
{
	{ Name "(va='u' && heading='right')||\r(val='r' && heading='down')||\r(val='d' && heading='left')||\r(val='l' && heading='up')" }
	{ Annotation "" }
	{ Parent 0 }
	{ Subject1 3 }
	{ Subject2 7 }
}

SCDTransitionEdge 18
{
	{ Name "" }
	{ Annotation "" }
	{ Parent 0 }
	{ Subject1 6 }
	{ Subject2 3 }
}

SCDTransitionEdge 20
{
	{ Name "" }
	{ Annotation "" }
	{ Parent 0 }
	{ Subject1 7 }
	{ Subject2 3 }
}

SCDTransitionEdge 21
{
	{ Name "(Val='u' && heading='up')||\r(val='r' && heading='right')||\r(val='d' && heading='down')||\r(val='l' && heading='left)" }
	{ Annotation "" }
	{ Parent 0 }
	{ Subject1 3 }
	{ Subject2 4 }
}

SCDTransitionEdge 15
{
	{ Name "Detect crossing" }
	{ Annotation "" }
	{ Parent 0 }
	{ Subject1 4 }
	{ Subject2 2 }
}

# VIEWS AND GRAPHICAL SHAPES

View 22
{
	{ Index "0" }
	{ Parent 0 }
}

BlackDot 23
{
	{ View 22 }
	{ Subject 1 }
	{ Position 210 230 }
	{ Size 8 8 }
	{ Color "black" }
	{ LineWidth 1 }
	{ LineStyle Solid }
	{ FillStyle Unfilled }
	{ FillColor "white" }
	{ FixedName True }
	{ Font "-*-courier-medium-r-normal--10*" }
	{ TextAlignment Center }
	{ TextColor "black" }
	{ NameUnderlined False }
}

RoundedBox 24
{
	{ View 22 }
	{ Subject 2 }
	{ Position 290 260 }
	{ Size 138 40 }
	{ Color "black" }
	{ LineWidth 1 }
	{ LineStyle Solid }
	{ FillStyle Unfilled }
	{ FillColor "white" }
	{ FixedName False }
	{ Font "-*-courier-medium-r-normal--10*" }
	{ TextAlignment Center }
	{ TextColor "black" }
	{ NameUnderlined False }
}

Line 25
{
	{ View 22 }
	{ Subject 8 }
	{ FromShape 23 }
	{ ToShape 24 }
	{ Curved False }
	{ End1 Empty }
	{ End2 FilledArrow }
	{ Points 2 }
	{ Point 214 231 }
	{ Point 237 240 }
	{ NamePosition 230 226 }
	{ Color "black" }
	{ LineWidth 1 }
	{ LineStyle Solid }
	{ FixedName False }
	{ Font "-*-courier-medium-r-normal--10*" }
	{ TextAlignment Center }
	{ TextColor "black" }
	{ NameUnderlined False }
}

RoundedBox 26
{
	{ View 22 }
	{ Subject 3 }
	{ Position 480 260 }
	{ Size 138 40 }
	{ Color "black" }
	{ LineWidth 1 }
	{ LineStyle Solid }
	{ FillStyle Unfilled }
	{ FillColor "white" }
	{ FixedName False }
	{ Font "-*-courier-medium-r-normal--10*" }
	{ TextAlignment Center }
	{ TextColor "black" }
	{ NameUnderlined False }
}

Line 27
{
	{ View 22 }
	{ Subject 9 }
	{ FromShape 24 }
	{ ToShape 26 }
	{ Curved False }
	{ End1 Empty }
	{ End2 FilledArrow }
	{ Points 2 }
	{ Point 359 260 }
	{ Point 411 260 }
	{ NamePosition 385 250 }
	{ Color "black" }
	{ LineWidth 1 }
	{ LineStyle Solid }
	{ FixedName False }
	{ Font "-*-courier-medium-r-normal--10*" }
	{ TextAlignment Center }
	{ TextColor "black" }
	{ NameUnderlined False }
}

RoundedBox 28
{
	{ View 22 }
	{ Subject 4 }
	{ Position 290 340 }
	{ Size 124 40 }
	{ Color "black" }
	{ LineWidth 1 }
	{ LineStyle Solid }
	{ FillStyle Unfilled }
	{ FillColor "white" }
	{ FixedName False }
	{ Font "-*-courier-medium-r-normal--10*" }
	{ TextAlignment Center }
	{ TextColor "black" }
	{ NameUnderlined False }
}

RoundedBox 29
{
	{ View 22 }
	{ Subject 5 }
	{ Position 510 340 }
	{ Size 118 40 }
	{ Color "black" }
	{ LineWidth 1 }
	{ LineStyle Solid }
	{ FillStyle Unfilled }
	{ FillColor "white" }
	{ FixedName False }
	{ Font "-*-courier-medium-r-normal--10*" }
	{ TextAlignment Center }
	{ TextColor "black" }
	{ NameUnderlined False }
}

Line 30
{
	{ View 22 }
	{ Subject 10 }
	{ FromShape 26 }
	{ ToShape 29 }
	{ Curved False }
	{ End1 Empty }
	{ End2 FilledArrow }
	{ Points 2 }
	{ Point 488 280 }
	{ Point 503 320 }
	{ NamePosition 508 297 }
	{ Color "black" }
	{ LineWidth 1 }
	{ LineStyle Solid }
	{ FixedName False }
	{ Font "-*-courier-medium-r-normal--10*" }
	{ TextAlignment Center }
	{ TextColor "black" }
	{ NameUnderlined False }
}

Line 31
{
	{ View 22 }
	{ Subject 11 }
	{ FromShape 26 }
	{ ToShape 28 }
	{ Curved False }
	{ End1 Empty }
	{ End2 FilledArrow }
	{ Points 2 }
	{ Point 433 280 }
	{ Point 338 320 }
	{ NamePosition 380 291 }
	{ Color "black" }
	{ LineWidth 1 }
	{ LineStyle Solid }
	{ FixedName False }
	{ Font "-*-courier-medium-r-normal--10*" }
	{ TextAlignment Center }
	{ TextColor "black" }
	{ NameUnderlined False }
}

Line 32
{
	{ View 22 }
	{ Subject 12 }
	{ FromShape 29 }
	{ ToShape 29 }
	{ Curved True }
	{ End1 Empty }
	{ End2 FilledArrow }
	{ Points 4 }
	{ Point 470 360 }
	{ Point 410 390 }
	{ Point 500 390 }
	{ Point 500 360 }
	{ NamePosition 455 390 }
	{ Color "black" }
	{ LineWidth 1 }
	{ LineStyle Solid }
	{ FixedName False }
	{ Font "-*-courier-medium-r-normal--10*" }
	{ TextAlignment Center }
	{ TextColor "black" }
	{ NameUnderlined False }
}

Line 33
{
	{ View 22 }
	{ Subject 13 }
	{ FromShape 28 }
	{ ToShape 28 }
	{ Curved True }
	{ End1 Empty }
	{ End2 FilledArrow }
	{ Points 4 }
	{ Point 290 360 }
	{ Point 290 400 }
	{ Point 230 400 }
	{ Point 270 360 }
	{ NamePosition 260 400 }
	{ Color "black" }
	{ LineWidth 1 }
	{ LineStyle Solid }
	{ FixedName False }
	{ Font "-*-courier-medium-r-normal--10*" }
	{ TextAlignment Center }
	{ TextColor "black" }
	{ NameUnderlined False }
}

Line 34
{
	{ View 22 }
	{ Subject 14 }
	{ FromShape 29 }
	{ ToShape 24 }
	{ Curved True }
	{ End1 Empty }
	{ End2 FilledArrow }
	{ Points 4 }
	{ Point 451 348 }
	{ Point 370 360 }
	{ Point 410 320 }
	{ Point 330 280 }
	{ NamePosition 390 340 }
	{ Color "black" }
	{ LineWidth 1 }
	{ LineStyle Solid }
	{ FixedName False }
	{ Font "-*-courier-medium-r-normal--10*" }
	{ TextAlignment Center }
	{ TextColor "black" }
	{ NameUnderlined False }
}

RoundedBox 36
{
	{ View 22 }
	{ Subject 6 }
	{ Position 280 460 }
	{ Size 122 40 }
	{ Color "black" }
	{ LineWidth 1 }
	{ LineStyle Solid }
	{ FillStyle Unfilled }
	{ FillColor "white" }
	{ FixedName False }
	{ Font "-*-courier-medium-r-normal--10*" }
	{ TextAlignment Center }
	{ TextColor "black" }
	{ NameUnderlined False }
}

RoundedBox 37
{
	{ View 22 }
	{ Subject 7 }
	{ Position 280 520 }
	{ Size 114 40 }
	{ Color "black" }
	{ LineWidth 1 }
	{ LineStyle Solid }
	{ FillStyle Unfilled }
	{ FillColor "white" }
	{ FixedName False }
	{ Font "-*-courier-medium-r-normal--10*" }
	{ TextAlignment Center }
	{ TextColor "black" }
	{ NameUnderlined False }
}

Line 38
{
	{ View 22 }
	{ Subject 16 }
	{ FromShape 26 }
	{ ToShape 36 }
	{ Curved True }
	{ End1 Empty }
	{ End2 FilledArrow }
	{ Points 4 }
	{ Point 523 280 }
	{ Point 760 390 }
	{ Point 620 540 }
	{ Point 341 474 }
	{ NamePosition 494 523 }
	{ Color "black" }
	{ LineWidth 1 }
	{ LineStyle Solid }
	{ FixedName False }
	{ Font "-*-courier-medium-r-normal--10*" }
	{ TextAlignment Center }
	{ TextColor "black" }
	{ NameUnderlined False }
}

Line 39
{
	{ View 22 }
	{ Subject 17 }
	{ FromShape 26 }
	{ ToShape 37 }
	{ Curved True }
	{ End1 Empty }
	{ End2 FilledArrow }
	{ Points 4 }
	{ Point 549 250 }
	{ Point 920 410 }
	{ Point 770 640 }
	{ Point 300 540 }
	{ NamePosition 487 601 }
	{ Color "black" }
	{ LineWidth 1 }
	{ LineStyle Solid }
	{ FixedName False }
	{ Font "-*-courier-medium-r-normal--10*" }
	{ TextAlignment Center }
	{ TextColor "black" }
	{ NameUnderlined False }
}

Line 40
{
	{ View 22 }
	{ Subject 18 }
	{ FromShape 36 }
	{ ToShape 26 }
	{ Curved True }
	{ End1 Empty }
	{ End2 FilledArrow }
	{ Points 4 }
	{ Point 235 440 }
	{ Point 30 350 }
	{ Point 100 60 }
	{ Point 442 240 }
	{ NamePosition 65 205 }
	{ Color "black" }
	{ LineWidth 1 }
	{ LineStyle Solid }
	{ FixedName False }
	{ Font "-*-courier-medium-r-normal--10*" }
	{ TextAlignment Center }
	{ TextColor "black" }
	{ NameUnderlined False }
}

Line 42
{
	{ View 22 }
	{ Subject 20 }
	{ FromShape 37 }
	{ ToShape 26 }
	{ Curved True }
	{ End1 Empty }
	{ End2 FilledArrow }
	{ Points 4 }
	{ Point 235 500 }
	{ Point 11 400 }
	{ Point 40 1 }
	{ Point 446 240 }
	{ NamePosition 25 200 }
	{ Color "black" }
	{ LineWidth 1 }
	{ LineStyle Solid }
	{ FixedName False }
	{ Font "-*-courier-medium-r-normal--10*" }
	{ TextAlignment Center }
	{ TextColor "black" }
	{ NameUnderlined False }
}

Line 43
{
	{ View 22 }
	{ Subject 21 }
	{ FromShape 26 }
	{ ToShape 28 }
	{ Curved True }
	{ End1 Empty }
	{ End2 FilledArrow }
	{ Points 4 }
	{ Point 546 277 }
	{ Point 670 310 }
	{ Point 510 500 }
	{ Point 318 360 }
	{ NamePosition 475 438 }
	{ Color "black" }
	{ LineWidth 1 }
	{ LineStyle Solid }
	{ FixedName False }
	{ Font "-*-courier-medium-r-normal--10*" }
	{ TextAlignment Center }
	{ TextColor "black" }
	{ NameUnderlined False }
}

Line 35
{
	{ View 22 }
	{ Subject 15 }
	{ FromShape 28 }
	{ ToShape 24 }
	{ Curved True }
	{ End1 Empty }
	{ End2 FilledArrow }
	{ Points 4 }
	{ Point 228 330 }
	{ Point 190 330 }
	{ Point 200 280 }
	{ Point 222 275 }
	{ NamePosition 195 305 }
	{ Color "black" }
	{ LineWidth 1 }
	{ LineStyle Solid }
	{ FixedName False }
	{ Font "-*-courier-medium-r-normal--10*" }
	{ TextAlignment Center }
	{ TextColor "black" }
	{ NameUnderlined False }
}

