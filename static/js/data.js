/* Percept-V project page — data extracted verbatim from the camera-ready paper. */

const SKILLS = {
  D:  { name: "Visual Discrimination",        blurb: "Telling objects apart by size, colour or shape." },
  M:  { name: "Visual Memory",                blurb: "Recalling the visual traits of a form or object." },
  SM: { name: "Visual Sequential Memory",     blurb: "Recalling a sequence of objects in the correct order." },
  FG: { name: "Visual Figure Ground",         blurb: "Locating a target inside a busy background." },
  FC: { name: "Visual Form Constancy",        blurb: "Recognising a shape after scaling or rotation." },
  C:  { name: "Visual Closure",               blurb: "Recognising a form when part of it is missing." },
  SR: { name: "Visual Spatial Relationship",  blurb: "Understanding how objects sit relative to each other." }
};

const ANSWER_TYPES = {
  single: { label: "Single",       desc: "Boolean or numeric",              count: 11 },
  fixed:  { label: "Fixed length", desc: "A fixed-length list or tuple",    count: 6  },
  list:   { label: "List",         desc: "An ordered list",                 count: 8  },
  set:    { label: "Set",          desc: "An unordered set",                count: 5  }
};

/* Skill -> domains, exactly as Table 1 of the paper. */
const SKILL_DOMAINS = {
  D:  ["change_colour", "vanishing_objects", "comparing_size", "counting_shapes", "sort_lines", "sort_circles", "locate_circles_colour", "locate_circles_shape", "match_shadow", "match_outline"],
  M:  ["list_colours", "list_shapes", "circle_boxes", "colours_present", "count_coloured_circles", "numbered_shapes", "graph_counting", "sort_circles", "sort_lines", "counting_shapes", "identifying_shapes"],
  SM: ["grid_path", "layered_colours", "layered_shapes", "comparing_size", "match_outline", "match_shadow"],
  FG: ["list_colours", "list_shapes", "locate_circles_colour", "locate_circles_shape", "layered_shapes", "layered_colours"],
  FC: ["mirror_image", "water_image", "counting_circles", "counting_shapes", "numbered_shapes"],
  C:  ["match_outline", "match_shadow", "layered_shapes", "layered_colours"],
  SR: ["comparing_size", "circle_location", "circle_right_triangle", "counting_locations", "cross_and_knots", "inside_circles", "maze_solving"]
};

const IMG = "static/images/domains/";

/* The 30 domains: prompts are the input prompts listed in Appendix A.1. */
const DOMAINS = [
  {
    id: "change_colour", name: "Change Colour", answer: "single",
    images: [IMG + "change_colour_first91.png", IMG + "change_colour_second91.png"],
    prompt: [
      "These are two identical images with circles of different colours.",
      "The colours of the circles at the same position in the two images may be different.",
      "Count the number of differently coloured circles between the two images.",
      "The output must be given in a single line in the form of COUNT:x"
    ]
  },
  {
    id: "circle_boxes", name: "Circle Boxes", answer: "single",
    images: [IMG + "circle_boxes_91.png"],
    prompt: [
      "This is an image with some red circles divided and a blue partition that divides the image into two sides.",
      "Some circles are on the left side of the partition whereas some are on the right. Note that, a side of the image may be completely empty as well.",
      "Determine the number of circles to be moved from the side with more number of circles to the side with less number of circles so that each side has equal number of circles.",
      "In case of both the sides having equal number of circles, return zero.",
      "The output must be given in a single line in the form of COUNT:x where x is the number of circles to be transferred"
    ]
  },
  {
    id: "circle_location", name: "Circle Location", answer: "fixed",
    images: [IMG + "circle_location_91.png"],
    prompt: [
      "This is an image with some black circles drawn in the four quadrants.",
      "The quadrants are numbered in the default way i.e. quadrant 1 is the rightmost and topmost quadrant, quadrant 2 is the leftmost and topmost, quadrant 3 is the leftmost and lowest and quadrant 4 is the rightmost and lowest.",
      "Determine the quadrant with the most number of black circles and the count of black circles in that quadrant.",
      "In case of a tie, return the lesser quadrant number.",
      "The output must be given in a single line in the form of QUADRANT:x COUNT:y where x is the quadrant number and y is the count of circles."
    ]
  },
  {
    id: "circle_right_triangle", name: "Circle Right Triangle", answer: "single",
    images: [IMG + "circle_right_triangle_91.png"],
    prompt: [
      "This is a grid which contains some circles and triangles.",
      "Check if any triangle cell has a circle cell to its immediate right.",
      "The last line of output should be “NO” if no such cell exists and “YES” otherwise."
    ]
  },
  {
    id: "colours_present", name: "Colours Present", answer: "fixed",
    images: [IMG + "colours_present_91.png"],
    prompt: [
      "This image contains some shapes in different colours.",
      "The colours belong to the following list — [black, gray, brown, maroon, red, coral, tan, orange, ivory, goldenrod, yellow, green, olive, turquoise, skyblue, blue, lavender, purple, pink, fuchsia]",
      "No colour is repeated.",
      "Produce a list of yes or no; write yes in the list if the colour at the corresponding index of the above list is present and no if it is absent.",
      "The output should be written in a single line as a comma-separated list of yes or no, written in order of the given list of colours.",
      "For example, the output should be of the form ANSWER: yes, no, no, yes and so on."
    ]
  },
  {
    id: "comparing_size", name: "Comparing Size", answer: "list",
    images: [IMG + "comparing_size_21.png"],
    prompt: [
      "This is an image with several rows of circles where each row is above a horizontal line.",
      "The image may also contain a single row with a blue and a green circle.",
      "Each row contains two colored circles (one blue and one green) of different sizes.",
      "Analyse which circle is bigger between the two in each row.",
      "The last line of the output should be of form “ANSWER:” followed by the space separated color answers for all the rows in the image.",
      "For example ANSWER: Blue Green Blue"
    ]
  },
  {
    id: "count_coloured_circles", name: "Count Coloured Circles", answer: "single",
    images: [IMG + "count_coloured_circles_91.png"],
    prompt: [
      "This is an image containing some colored circles.",
      "Count the total number of red circles in the image.",
      "Last line of the output must be of the form COUNT:x"
    ]
  },
  {
    id: "counting_circles", name: "Counting Circles", answer: "single",
    images: [IMG + "counting_circles_91.png"],
    prompt: [
      "This is an image containing some black circles.",
      "Count the total number of circles in the image.",
      "The last line of the output should be of form COUNT:x."
    ]
  },
  {
    id: "counting_locations", name: "Counting Locations", answer: "fixed",
    images: [IMG + "counting_locations_91.png"],
    prompt: [
      "There will be an image containing a rectangle and some circles above and below it.",
      "Count the number of circles above the rectangle and below the rectangle.",
      "The output must be of form in a single line ABOVE:x BELOW:y"
    ]
  },
  {
    id: "counting_shapes", name: "Counting Shapes", answer: "fixed",
    images: [IMG + "counting_shapes_91.png"],
    prompt: [
      "This is an image containing shapes such as circles, triangles and squares.",
      "Count the number of circles, triangles and squares in the image.",
      "The last line of the output must be of the form CIRCLES:x TRIANGLES:y SQUARES:z"
    ]
  },
  {
    id: "cross_and_knots", name: "Cross and Knots", answer: "fixed",
    images: [IMG + "cross_and_knots_91.png"],
    prompt: [
      "This is a grid containing some black X.",
      "Each cell is given a coordinate (x,y) which is (row,column) with 0 based indexing.",
      "An adjacent cell to a cell A is any cell sharing an edge with A.",
      "A safe cell is a cell that is not adjacent to any black X.",
      "Output the coordinates of any one safe cell as labelled in the grid.",
      "If no such cell exists output None.",
      "The last line of the output should just contain the cell coordinates (x,y) or None and nothing else."
    ]
  },
  {
    id: "graph_counting", name: "Graph Counting", answer: "fixed",
    images: [IMG + "graph_counting_91.png"],
    prompt: [
      "This is a graph where the blue colored circles are nodes and the lines joining them are edges.",
      "The graph may contain a single blue node with no edges.",
      "The graph may be disconnected.",
      "Count the number of nodes and edges in the graph.",
      "Last line of the output must be of the form NODES:x EDGES:y."
    ]
  },
  {
    id: "grid_path", name: "Grid Path", answer: "list",
    images: [IMG + "grid_path_91.png"],
    prompt: [
      "This is a grid which contains some circles, triangles and squares.",
      "Travel from cell labelled S to cell labelled E.",
      "Follow the path marked by the black line and arrows.",
      "Write down the sequence of shapes seen while moving along this path.",
      "The shapes present in the S and E cells should also be included in the sequence.",
      "The last line of the output should be a comma-separated list of shapes without colors, written in order of visiting of form SHAPES : Shape 1 , Shape 2 and so on."
    ]
  },
  {
    id: "identifying_shapes", name: "Identifying Shapes", answer: "list",
    images: [IMG + "identifying_shapes_21.png"],
    prompt: [
      "This is an image with several rows of different shapes where each row is above a horizontal line.",
      "Each row contains a coloured shape.",
      "The image may also contain a single shape.",
      "Identify the shape present in each row.",
      "In case there is a single shape, treat it as a single row.",
      "The output should have only a single line containing the answer.",
      "The output format should be “ANSWER:” followed by the space separated shape names.",
      "For example, ANSWER: Circle Triangle Circle"
    ]
  },
  {
    id: "inside_circles", name: "Inside Circles", answer: "single",
    images: [IMG + "inside_circles_91.png"],
    prompt: [
      "This is an image containing some black circles and a single red dot.",
      "Determine if the red dot is contained inside any circle in the image.",
      "Note that a circle containing the red dot means the centre of the dot is present inside the circumference of the circle.",
      "The last line of the output should be of form ANSWER: x where x is Yes if the dot is contained in any circle and No otherwise."
    ]
  },
  {
    id: "layered_colours", name: "Layered Colours", answer: "list",
    images: [IMG + "layered_colours_91.png"],
    prompt: [
      "This image contains some concentric circles in different colours.",
      "The image may also contain a single circle.",
      "Write down the sequence of colours seen from inside to outside.",
      "In case of a single circle in the image, write down the colour of that circle.",
      "The colours belong to the following list — [black, gray, brown, maroon, red, coral, tan, orange, ivory, goldenrod, yellow, green, olive, turquoise, skyblue, blue, lavender, purple, pink, fuchsia]",
      "No colour is repeated.",
      "The output should be written in a single line as a comma-separated list of colours, written in order from the innermost colour to the outermost colour.",
      "For example, the output should be of the form COLOURS: Colour 1 , Colour 2 and so on."
    ]
  },
  {
    id: "layered_shapes", name: "Layered Shapes", answer: "list",
    images: [IMG + "layered_shapes_91.png"],
    prompt: [
      "This image contains some shapes that are layered on top of each other in a white background.",
      "The shapes could be of the following types — [circle, diamond, hexagon, octagon]",
      "The image could also contain a single shape with no other shapes layered on top of it.",
      "Write down the sequence of shapes from the inside layer to the outside layer.",
      "If there is a single shape then identify it.",
      "The last line of the output should be a comma-separated list of shapes without colors, written in order from top to bottom of form SHAPES : Shape 1 , Shape 2 and so on.",
      "If there is a single shape then write SHAPES : shape-name where shape-name is the name of the shape seen."
    ]
  },
  {
    id: "list_colours", name: "List Colours", answer: "set",
    images: [IMG + "list_colours_91.png"],
    prompt: [
      "This is an image with some multi-coloured shapes drawn on top of it.",
      "The colours belong to the following list — [black, gray, brown, maroon, red, coral, tan, orange, ivory, goldenrod, yellow, green, olive, turquoise, skyblue, blue, lavender, purple, pink, fuchsia]",
      "No colour is repeated.",
      "Identify the colour of the shapes drawn over the background image.",
      "Form a list of all the colours of the shapes.",
      "The output must be given in a single line in the form of a list of all the colours found."
    ]
  },
  {
    id: "list_shapes", name: "List Shapes", answer: "set",
    images: [IMG + "list_shapes_91.png"],
    prompt: [
      "This is an image with some multi-coloured shapes drawn on top of it.",
      "The shapes belong to the following list — [circle, triangle, square, pentagon]",
      "Identify the shapes drawn over the background image.",
      "Form a set of all the unique shapes seen in the image.",
      "The output must be given in a single line in the form of a set of unique shapes found."
    ]
  },
  {
    id: "locate_circles_colour", name: "Locate Circles Colour", answer: "set",
    images: [IMG + "locate_circles_colour_91.png"],
    prompt: [
      "This is a grid which contains some coloured circles.",
      "The rows and columns are numbered in the grid.",
      "The coordinate of a cell is given by the row number followed by the column number.",
      "Write down all the coordinates of the cells which contain a green circle.",
      "The last line of the output should be a space-separated list of the coordinates of the cells which contain a green circle.",
      "The coordinates should be in the format (row,column) with the comma and bracket."
    ]
  },
  {
    id: "locate_circles_shape", name: "Locate Circles Shape", answer: "set",
    images: [IMG + "locate_circles_shape_91.png"],
    prompt: [
      "This is a grid which contains some coloured circles, rectangles and triangles.",
      "The rows and columns are numbered in the grid.",
      "The coordinate of a cell is given by the row number followed by the column number.",
      "Write down all the coordinates of the cells which contain a green circle.",
      "The last line of the output should be a space-separated list of the coordinates of the cells which contain a green circle.",
      "The coordinates should be in the format (row,column) with the comma and bracket."
    ]
  },
  {
    id: "match_outline", name: "Match Outline", answer: "single",
    images: [IMG + "match_outline_first91.png", IMG + "match_outline_second91.png"],
    prompt: [
      "These are two images of some sequence of shapes separated by black horizontal lines.",
      "The two images may also contain a single shape each.",
      "The first image consists of rows of shapes and the second image consists of rows of outlines of shapes.",
      "Determine the number of shapes in the first image that match the outlines in the corresponding row in the second image.",
      "In case each of the two images contain only a single shape, treat the single shape in each image as a row.",
      "The output must be given in a single line in the form of ANSWER:x where x is the number of matching shapes."
    ]
  },
  {
    id: "match_shadow", name: "Match Shadow", answer: "single",
    images: [IMG + "match_shadow_first91.png", IMG + "match_shadow_second91.png"],
    prompt: [
      "These are two images of some sequence of shapes separated by black horizontal lines.",
      "The two images may also contain a single shape each.",
      "The first image consists of rows of shapes and the second image consists of rows of shadows of those shapes.",
      "Determine the number of shapes in the first image that match the shadows in the corresponding row in the second image.",
      "In case each of the two images contain only a single shape, treat the single shape in each image as a row.",
      "The output must be given in a single line in the form of ANSWER:x where x is the number of matching shadows."
    ]
  },
  {
    id: "maze_solving", name: "Maze Solving", answer: "list",
    images: [IMG + "maze_solving_91.png"],
    prompt: [
      "This is a maze.",
      "You start from the cell labelled S.",
      "Your goal is to reach cell labelled E through the shortest path possible.",
      "You can move up, down, left or right.",
      "You cannot move through the black walls.",
      "You can only move through white cells.",
      "Give the sequence of cells taken to go from S to E.",
      "Last line of output should be a comma separated line with cell numbers starting with S and ending at E and nothing else."
    ]
  },
  {
    id: "mirror_image", name: "Mirror Image", answer: "single",
    images: [IMG + "mirror_image_first91.png", IMG + "mirror_image_second91.png"],
    prompt: [
      "These are two images containing different shapes in different colours.",
      "The image consists of a vertical blue line at the centre.",
      "Some objects of the first image are mirrored along the given vertical line in the second image.",
      "Other objects in the second image maintain the same positions as in the first image.",
      "Determine the number of objects that are mirrored in the second image.",
      "The output must be given in a single line in the form of COUNT: x, where x is the number being mirrored."
    ]
  },
  {
    id: "numbered_shapes", name: "Numbered Shapes", answer: "set",
    images: [IMG + "numbered_shapes_91.png"],
    prompt: [
      "This is an image with some shapes drawn and numbers written on top of the shapes.",
      "Determine the list of numbers written on top of the circles.",
      "The output must be given in a single line in the form of CIRCLES:x where x is the list of numbers seen on top of the circles."
    ]
  },
  {
    id: "sort_circles", name: "Sort Circles", answer: "list",
    images: [IMG + "sort_circles_91.png"],
    prompt: [
      "There are several black circles with different sizes.",
      "The image may also have a single black circle.",
      "Sort these circles by size, from smallest to largest.",
      "If there is only a single circle, give the number written on that circle.",
      "Output must only contain the space separated labels of circles in their sorted order by size."
    ]
  },
  {
    id: "sort_lines", name: "Sort Lines", answer: "list",
    images: [IMG + "sort_lines_91.png"],
    prompt: [
      "The image has several parallel lines of varying lengths.",
      "The image may also contain only a single line.",
      "Sort these lines by length, from shortest to longest.",
      "If there is only a single line, give the number of that line.",
      "Last line of the output must only contain the space separated labels of the lines in their sorted order by length and nothing else."
    ]
  },
  {
    id: "vanishing_objects", name: "Vanishing Objects", answer: "single",
    images: [IMG + "vanishing_objects_first91.png", IMG + "vanishing_objects_second91.png"],
    prompt: [
      "These are two images containing shapes such as circles, triangles and squares.",
      "The images are identical except for the fact that the second image has a few objects missing.",
      "Count the number of missing objects in the second image.",
      "The output must be given in a single line in the form of COUNT:x"
    ]
  },
  {
    id: "water_image", name: "Water Image", answer: "single",
    images: [IMG + "water_image_first91.png", IMG + "water_image_second91.png"],
    prompt: [
      "These are two images containing different shapes in different colours.",
      "The image consists of a horizontal blue line at the centre.",
      "Some objects of the first image are mirrored along the given horizontal line in the second image.",
      "Other objects in the second image maintain the same positions as in the first image.",
      "Determine the number of objects that are mirrored along the horizontal line in the second image.",
      "The output must be given in a single line in the form of COUNT: x, where x is the number being mirrored."
    ]
  }
];

/* Attach the skills of each domain by inverting SKILL_DOMAINS. */
DOMAINS.forEach(d => {
  d.skills = Object.keys(SKILL_DOMAINS).filter(k => SKILL_DOMAINS[k].includes(d.id));
});

/* Table 2: zero-shot accuracy (%). */
const MODELS = [
  { key: "gpt5mini",  label: "GPT-5-mini", family: "proprietary" },
  { key: "gpt4o",     label: "GPT-4o",     family: "proprietary" },
  { key: "o4mini",    label: "o4-mini",    family: "proprietary" },
  { key: "gemini",    label: "Gemini",     family: "proprietary" },
  { key: "gemma4",    label: "Gemma-4",    family: "open" },
  { key: "qwen3vl",   label: "Qwen3-VL",   family: "open" },
  { key: "qwen",      label: "Qwen2.5-VL", family: "open" },
  { key: "deepseek",  label: "DeepSeek",   family: "open" }
];

const RESULTS_SKILL = [
  ["Visual Discrimination",       55.0,  23.7,  55.3,  51.25, 68.75, 34.74, 11.5,  4.1,   38.04],
  ["Visual Memory",               49.95, 33.55, 47.55, 46.55, 64.0,  30.12, 19.59, 1.32,  36.58],
  ["Visual Sequential Memory",    43.5,  21.5,  47.5,  41.92, 52.58, 15.75, 4.67,  5.25,  29.08],
  ["Visual Figure Ground",        64.75, 25.42, 63.25, 62.83, 59.5,  40.0,  7.58,  0.08,  40.43],
  ["Visual Form Constancy",       58.7,  27.3,  48.9,  50.3,  71.0,  34.67, 25.6,  3.0,   39.93],
  ["Visual Closure",              44.88, 23.0,  50.25, 43.25, 43.5,  13.12, 5.75,  7.88,  28.96],
  ["Visual Spatial Relationship", 66.64, 50.36, 62.64, 69.79, 84.5,  54.36, 27.79, 17.64, 54.22]
];
const RESULTS_SKILL_AVG = ["Average of skills", 54.77, 29.26, 53.63, 52.27, 63.4, 31.82, 14.64, 5.61, 38.18];

const RESULTS_DOMAIN = [
  ["change_colour", 32, 18.5, 32, 23.5, 58.5, 8.5, 8, 4.5, 23.19],
  ["circle_boxes", 30, 33, 34, 28, 64.5, 15, 12.5, 10.5, 28.44],
  ["circle_location", 56.5, 41.5, 46, 57.5, 81.5, 22.5, 14.5, 5.5, 40.69],
  ["circle_right_triangle", 100, 82, 99.5, 99, 98.5, 94.5, 25, 50, 81.06],
  ["colours_present", 3.5, 1.5, 4.5, 4.5, 5.5, 1.5, 0, 0, 2.62],
  ["comparing_size", 27, 36.5, 31, 55, 81, 31.5, 5, 0, 33.38],
  ["count_coloured_circles", 51, 44, 37.5, 44.5, 99, 38, 39, 2.5, 44.44],
  ["counting_circles", 68, 57.5, 55, 55.5, 100, 54.5, 42.5, 5.5, 54.81],
  ["counting_locations", 44.5, 20.5, 36.5, 33.5, 98.5, 37, 15.5, 0, 35.75],
  ["counting_shapes", 72.5, 44, 58.5, 61, 100, 62.37, 41, 0, 54.92],
  ["cross_and_knots", 99.5, 57.5, 100, 96, 81.5, 89.5, 23.5, 0, 68.44],
  ["graph_counting", 39, 31, 33.5, 36, 51.5, 25.5, 26, 0, 30.31],
  ["grid_path", 54.5, 0.5, 53, 23.5, 60.5, 10.5, 0, 0, 25.31],
  ["identifying_shapes", 79.5, 69, 92.5, 47, 100, 80, 41.5, 0, 63.69],
  ["inside_circles", 96, 87.5, 95.5, 93, 97, 94.5, 96.5, 68, 91],
  ["layered_colours", 35, 25, 33.5, 34, 29.5, 10, 0.5, 0, 20.94],
  ["layered_shapes", 24, 11.5, 20, 18.5, 16.5, 11.5, 9.5, 0, 13.94],
  ["list_colours", 41, 18, 35.5, 58, 37, 3.5, 1.5, 0.5, 24.38],
  ["list_shapes", 88.5, 70.5, 90.5, 92, 90.5, 31.5, 21, 0, 60.56],
  ["locate_circles_colour", 100, 11.5, 100, 82, 92, 95, 6, 0, 60.81],
  ["locate_circles_shape", 100, 16, 100, 92.5, 91.5, 88.5, 7, 0, 61.94],
  ["match_outline", 66, 23, 84.5, 72.5, 82, 19, 7.5, 17, 46.44],
  ["match_shadow", 54.5, 32.5, 63, 48, 46, 12, 5.5, 14.5, 34.5],
  ["maze_solving", 43, 27, 30, 54.5, 53.5, 11, 14.5, 0, 29.19],
  ["mirror_image", 33.5, 12.5, 29, 24, 32.5, 3.5, 21.5, 5, 20.19],
  ["numbered_shapes", 81.5, 12, 75.5, 88.5, 84, 49.5, 8, 1, 50],
  ["sort_circles", 36.5, 24, 34, 30, 31.5, 0, 20, 0, 22],
  ["sort_lines", 26.5, 22, 27, 22.5, 40.5, 24.5, 5, 0, 21],
  ["vanishing_objects", 35, 9, 23, 25.5, 64.5, 6, 10, 5, 22.25],
  ["water_image", 38, 10.5, 26.5, 22.5, 38.5, 3.5, 15, 3.5, 19.75]
];
const RESULTS_DOMAIN_AVG = ["Full Percept-V", 55.22, 31.65, 52.7, 50.75, 66.92, 34.48, 18.1, 6.43, 39.53];

/* Table 6: human study (same samples, same protocol). */
const HUMAN_STUDY = [
  ["Human",       95.43, true],
  ["Gemma-4-31B", 68.71, false],
  ["o4-mini",     56.83, false],
  ["GPT-5-mini",  56.81, false],
  ["Gemini",      55.58, false],
  ["Qwen3-VL",    36.14, false],
  ["GPT-4o",      31.94, false],
  ["Qwen2.5-VL",  14.69, false],
  ["DeepSeek",     7.08, false]
];

/* Table 4: fine-tuning Qwen2.5-VL-7B on Percept-V_train (60K samples). */
const FINETUNE = {
  baseline: ["—", "—", "—", 18.10, 29.81, 6.35, 73.92, 46.28],
  lora: [
    [0, 0, 1, 49.15, 65.05, 33.28, 74.02, 47.43],
    [0, 1, 0, 68.67, 80.76, 56.60, 68.49, 46.49],
    [1, 0, 0, 75.18, 84.33, 66.05, 76.70, 47.54],
    [0, 1, 1, 70.20, 82.49, 57.91, 74.02, 47.43],
    [1, 0, 1, 74.63, 83.80, 65.49, 78.06, 42.72],
    [1, 1, 0, 83.42, 89.47, 77.38, 74.77, 44.71],
    [1, 1, 1, 80.30, 87.56, 73.06, 75.62, 47.02]
  ],
  full: [
    [0, 0, 1, 25.25, 38.71, 11.78, 74.46, 46.28],
    [0, 1, 0, 75.80, 87.50, 64.09, 72.53, 42.61],
    [1, 0, 0, 82.60, 92.60, 72.57, 58.91, 44.60],
    [0, 1, 1, 76.35, 87.32, 65.36, 73.46, 44.08],
    [1, 0, 1, 78.83, 90.93, 66.69, 63.38, 44.71],
    [1, 1, 0, 84.18, 93.55, 74.79, 69.54, 46.28],
    [1, 1, 1, 84.30, 93.33, 75.27, 77.56, 45.97]
  ]
};

/* Table 5 (one-shot), Table 7 (resolution), Table 8 (prompt style), Table 9 (3D). */
const ONE_SHOT = [
  ["Visual Discrimination",       51.46, 11.17, 52.51, 43.57],
  ["Visual Memory",               46.55, 20.93, 45.96, 39.38],
  ["Visual Sequential Memory",    38.61, 12.33, 45.48, 33.42],
  ["Visual Figure Ground",        63.90, 20.00, 63.90, 48.83],
  ["Visual Form Constancy",       53.06, 16.64, 45.63, 40.70],
  ["Visual Closure",              40.58, 17.75, 50.76, 40.96],
  ["Visual Spatial Relationship", 64.61, 24.50, 61.59, 64.11],
  ["Average of skills",           51.25, 17.62, 52.26, 44.42]
];
const ZERO_SHOT_REF = { "GPT-5-mini": 54.77, "GPT-4o": 29.26, "o4-mini": 53.63, "Gemini": 52.27 };

const RESOLUTION = [
  ["Visual Discrimination",       55.00, 54.80, 45.83, 11.50, 11.70, 10.20],
  ["Visual Memory",               49.95, 49.94, 32.92, 19.59, 22.83, 17.22],
  ["Visual Sequential Memory",    43.50, 42.17, 29.42,  4.67,  4.83,  4.33],
  ["Visual Figure Ground",        64.75, 63.12, 52.00,  7.58,  4.88,  4.62],
  ["Visual Form Constancy",       58.70, 61.90, 38.15, 25.60, 25.20, 21.50],
  ["Visual Closure",              44.88, 45.75, 32.75,  5.75,  5.25,  5.75],
  ["Visual Spatial Relationship", 66.64, 71.64, 57.07, 27.79, 30.36, 24.07],
  ["Average of skills",           54.77, 55.62, 41.16, 14.64, 15.01, 12.53]
];

const THREE_D = [
  ["change_colour",          64.0, 58.0, 16.0, 15.0],
  ["colours_present",         1.0,  9.0,  0.0,  0.0],
  ["count_coloured_circles", 90.0, 78.0, 62.0, 62.0],
  ["counting_circles",       93.0, 74.0, 78.0, 92.0],
  ["counting_shapes",        95.0, 94.0, 67.0, 81.0],
  ["numbered_shapes",        98.0, 19.0, 16.0, 17.0],
  ["Average (6 domains)",    73.50, 55.33, 39.8, 44.5]
];

const PROMPT_STYLE = [
  ["Visual Discrimination",       55.30, 53.55, 13.91, 13.45],
  ["Visual Memory",               47.55, 49.27, 21.87, 18.77],
  ["Visual Sequential Memory",    47.50, 39.83,  5.50,  7.25],
  ["Visual Figure Ground",        63.25, 63.42,  4.33,  5.08],
  ["Visual Form Constancy",       48.90, 58.50, 24.31, 30.10],
  ["Visual Closure",              50.25, 39.62,  5.38, 10.62],
  ["Visual Spatial Relationship", 62.64, 66.29, 18.07, 15.50],
  ["Average of skills",           53.63, 52.93, 13.34, 14.40]
];

/* Table 3: format-error rate (%) by answer type. */
const FORMAT_ERRORS = [
  ["single", 0.14, 0.00, 0.00, 0.00, 11.95, 15.09, 0.00, 3.68],
  ["fixed",  0.00, 0.00, 0.17, 0.83,  4.08, 13.00, 5.18, 61.58],
  ["list",   2.19, 0.00, 0.00, 0.00,  5.94, 14.19, 0.00, 22.44],
  ["set",    0.00, 0.00, 0.10, 0.20,  6.40,  2.40, 19.10, 60.00]
];

/* Figure 1 of the paper, rebuilt for the web. */
const TEASER = [
  {
    skill: "Visual Closure",
    prompt: "Determine the number of shapes in the rows of the first column that match the outlines in the corresponding rows in the second column.",
    img: "static/images/teaser/combined.png", tall: true,
    gold: "5", pred: "“ANSWER: 3”", correct: false
  },
  {
    skill: "Visual Sequential Memory",
    prompt: "This image contains some concentric circles in different colors. Write down the sequence of colors seen from inside to outside.",
    img: "static/images/teaser/layered_colours1.png",
    gold: "orange, yellow, green, tan, purple, gray", pred: "orange, yellow, green, tan, purple, gray", correct: true
  },
  {
    skill: "Visual Discrimination",
    prompt: "The images are identical except for the fact that the lower image has a few objects missing. Count the number of missing objects in the lower image.",
    img: "static/images/teaser/combined_with_line.png",
    gold: "10", pred: "“COUNT: 5”", correct: false
  },
  {
    skill: "Visual Figure Ground",
    prompt: "Identify the shapes drawn over the background image. Form a set of all the unique shapes seen in the image.",
    img: "static/images/teaser/list_shapes1.png",
    gold: "circle, pentagon, rectangle, triangle", pred: "“{circle, triangle}”", correct: false
  },
  {
    skill: "Visual Memory",
    prompt: "This is an image with some shapes drawn and numbers written on top of the shapes. Determine the list of numbers written on top of the circles.",
    img: "static/images/teaser/numbered_shapes1.png",
    gold: "1,3,6,7,9,10,14,15,16,20", pred: "“CIRCLES:1,3,7,10,14,15”", correct: false
  },
  {
    skill: "Visual Spatial Relationship",
    prompt: "Count the number of circles above the rectangle and below the rectangle.",
    img: "static/images/teaser/counting_locations1.png",
    gold: "ABOVE:10, BELOW:10", pred: "“ABOVE:8, BELOW:10”", correct: false
  },
  {
    skill: "Visual Form Constancy",
    prompt: "Count the total number of circles in the image.",
    img: "static/images/teaser/counting_circles1.png",
    gold: "10", pred: "“CIRCLES:10”", correct: true
  }
];
