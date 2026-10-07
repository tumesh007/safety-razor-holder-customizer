/* [=================== SHAVING BRUSH KNOT ===================] */

// Shaving brush knot opening diameter (mm)
knot_diameter = 26.0; // [22.0:0.5:34.0]

// Entrance slot length extension (mm)
slot_length = 35.0; // [20.0:1.0:50.0]


/* [=================== BOTTOM BRANDING / TEXT ===================] */

// Primary Text (e.g. Owner Name)
text_line_1 = "     Tumesh";

// Font size for Line 1 (mm)
text_size_1 = 8.0; // [4.0:0.5:14.0]

// Secondary Text (e.g. Brush Model, Knot Size, Hair Type)
text_line_2 = "       30mm Silvertip";

// Font size for Line 2 (mm)
text_size_2 = 4.8; // [3.0:0.5:10.0]

// Vertical spacing between line 1 and line 2 (mm)
line_spacing = 7.5; // [4.0:0.5:16.0]

// Text Rotation (degrees: 0 = along length, 90 = across width)
text_rotation = 180; // [0, 90, 180, 270]

// Font Family & Style
font_name = "Arial:style=Bold"; // ["Arial:style=Bold", "Arial", "Liberation Sans:style=Bold", "Trebuchet MS:style=Bold", "Impact", "Georgia:style=Bold"]

// Deboss engraving depth into bottom plate (mm)
deboss_depth = 0.8; // [0.4:0.1:1.5]

// Text X Position (0 = under knot hole, 20 = center of base, 45 = under soap bowl)
text_pos_x = 20.0; // [-15.0:1.0:55.0]

// Text Y Position (0 = centered across width)
text_pos_y = 0.0; // [-20.0:1.0:20.0]


/* [=================== BOTTOM LOGO / EMBLEM ===================] */

// Choose a bottom emblem / icon
logo_type = "Brush"; // ["None", "Brush", "Razor", "Crown", "Star", "Custom_SVG"]

// Logo Placement relative to text
logo_position = "Left_Of_Text"; // ["Above_Text", "Below_Text", "Left_Of_Text", "Right_Of_Text", "Custom_Offset", "Logo_Only"]

// Logo scale multiplier
logo_scale = 0.85; // [0.3:0.05:2.5]

// Custom Logo X Position (only used if logo_position is Custom_Offset)
custom_logo_x = 48.0; // [-20.0:1.0:60.0]

// Custom Logo Y Position (only used if logo_position is Custom_Offset)
custom_logo_y = 0.0; // [-25.0:1.0:25.0]

// Filename of custom SVG file in the same folder (if logo_type = "Custom_SVG")
custom_svg_file = "my_logo.svg";


/* [=================== PRINT ORIENTATION ===================] */

// Slicing and Print Orientation
print_orientation = "Flat-Side (Fast 2.5h)"; // ["Flat-Side (Fast 2.5h)", "Upright (Standard 4.2h)"]


/* [=================== ADVANCED / TEMPLATE ===================] */

// Path to blank template STL (keep in same folder)
template_file = "holder_template_upright.stl";

$fn = 60;


/* [=================== GEOMETRY MODULES ===================] */

module icon_brush(s = 1.0) {
    scale([s, s, 1]) {
        hull() {
            translate([0, 1]) circle(r = 2.2);
            translate([-5.0, 6.0]) circle(r = 1.6);
            translate([5.0, 6.0]) circle(r = 1.6);
            translate([0, 8.5]) circle(r = 2.8);
        }
        hull() {
            translate([0, 0]) circle(r = 2.2);
            translate([0, -2.5]) circle(r = 1.6);
        }
        hull() {
            translate([0, -2.5]) circle(r = 1.6);
            translate([0, -5.5]) circle(r = 3.0);
        }
    }
}

module icon_razor(s = 1.0) {
    scale([s, s, 1]) {
        hull() {
            translate([-5.5, 4.5]) circle(r = 0.8);
            translate([5.5, 4.5]) circle(r = 0.8);
            translate([-5.0, 6.5]) circle(r = 0.8);
            translate([5.0, 6.5]) circle(r = 0.8);
        }
        translate([-1.0, 2.8]) square([2.0, 1.8]);
        hull() {
            translate([-1.2, -5.5]) circle(r = 0.6);
            translate([1.2, -5.5]) circle(r = 0.6);
            translate([-1.3, 2.8]) circle(r = 0.6);
            translate([1.3, 2.8]) circle(r = 0.6);
        }
        translate([0, -5.5]) circle(r = 1.5);
    }
}

module icon_crown(s = 1.0) {
    scale([s, s, 1]) {
        polygon([
            [-6.5, -3], [6.5, -3],
            [7.5, 3.5], [3, 0], [0, 4.5], [-3, 0], [-7.5, 3.5]
        ]);
        translate([-7.5, 3.5]) circle(r = 0.8);
        translate([0, 4.5]) circle(r = 1.0);
        translate([7.5, 3.5]) circle(r = 0.8);
    }
}

module icon_star(s = 1.0) {
    scale([s, s, 1]) {
        points = [
            for (i = [0:9]) 
                let (r = i % 2 == 0 ? 6.0 : 2.6, a = i * 36 + 90)
                [r * cos(a), r * sin(a)]
        ];
        polygon(points);
    }
}

module render_logo() {
    if (logo_type == "Brush") {
        icon_brush(logo_scale);
    } else if (logo_type == "Razor") {
        icon_razor(logo_scale);
    } else if (logo_type == "Crown") {
        icon_crown(logo_scale);
    } else if (logo_type == "Star") {
        icon_star(logo_scale);
    } else if (logo_type == "Custom_SVG") {
        scale([logo_scale, logo_scale, 1])
            import(custom_svg_file, center = true);
    }
}

module bottom_branding_2d() {
    // Translate in model coordinates first
    translate([text_pos_x, text_pos_y]) {
        // Mirror horizontally so it reads normally left-to-right when looking directly at the base plate
        mirror([1, 0, 0]) {
            rotate([0, 0, text_rotation]) {
                if (logo_position == "Logo_Only") {
                    render_logo();
                } else {
                    // Text
                    if (text_line_2 == "") {
                        text(text = text_line_1, size = text_size_1, font = font_name, halign = "center", valign = "center");
                    } else {
                        translate([0, line_spacing / 2])
                            text(text = text_line_1, size = text_size_1, font = font_name, halign = "center", valign = "center");
                        translate([0, -line_spacing / 2])
                            text(text = text_line_2, size = text_size_2, font = font_name, halign = "center", valign = "center");
                    }
                    
                    // Logo Placement
                    if (logo_type != "None") {
                        if (logo_position == "Left_Of_Text") {
                            translate([-24.0 * logo_scale, 0])
                                render_logo();
                        } else if (logo_position == "Right_Of_Text") {
                            translate([24.0 * logo_scale, 0])
                                render_logo();
                        } else if (logo_position == "Above_Text") {
                            translate([0, (text_line_2 == "" ? 8.0 : line_spacing + 5.0)])
                                render_logo();
                        } else if (logo_position == "Below_Text") {
                            translate([0, -(text_line_2 == "" ? 8.0 : line_spacing + 5.0)])
                                render_logo();
                        } else if (logo_position == "Custom_Offset") {
                            translate([custom_logo_x - text_pos_x, custom_logo_y - text_pos_y])
                                render_logo();
                        }
                    }
                }
            }
        }
    }
}

module knot_cutter(d) {
    if (d > 22.0) {
        translate([0, 0, 115])
            cylinder(r = d / 2, h = 30, $fn = 80);
        translate([-slot_length, -d / 2, 115])
            cube([slot_length, d, 30]);
    }
}

module custom_razor_holder() {
    difference() {
        import(template_file);
        
        // Knot expansion cutter
        knot_cutter(knot_diameter);
        
        // Bottom debossed engraving (Z from -0.1 to deboss_depth)
        translate([0, 0, -0.1])
            linear_extrude(height = deboss_depth + 0.1)
                bottom_branding_2d();
    }
}

/* [=================== OUTPUT RENDERING ===================] */

if (print_orientation == "Flat-Side (Fast 2.5h)") {
    // Mathematical rotation to cancel 4.2° draft angle and seat flat at Z = 0
    multmatrix([
      [0.994385, -0.075946, 0.073695, 0],
      [-0.075946, -0.027196, 0.996741, 0],
      [-0.073695, -0.996741, -0.032811, 34.229908],
      [0, 0, 0, 1]
    ])
    custom_razor_holder();
} else {
    // Upright on base at Z = 0
    custom_razor_holder();
}
