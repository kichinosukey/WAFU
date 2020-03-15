let setTools = (list) => {
    let tool_list_str = "";
    for (let index = 0; index < list.length; index++) {
        const item = list[index];
        if (index + 1 == list.length) {
            tool_list_str += item;
        } else {
            tool_list_str += item + ',';
        }
    }
    return tool_list_str
}

// Action
const TOOL_REDO = 'redo'
const TOOL_RESET = 'reset'
const TOOL_SAVE = 'save'
const TOOL_UNDO = 'undo'
const TOOL_ZOOM_IN = 'zoom_in'
const TOOL_XZOOM_IN = 'xzoom_in'
const TOOL_YZOOM_IN = 'yzoom_in'
const TOOL_ZOOM_OUT = 'zoom_out'
const TOOL_XZOOM_OUT = 'xzoom_out'
const TOOL_YZOOM_OUT = 'yzoom_out'

// Click/Tap
const TOOL_POLY_SELECT = 'poly_select'
const TOOL_TAP = 'tap'

// Inspectors
const TOOL_CROSS_HAIR = 'crosshair'
const TOOL_HOVER = 'hover'

// Pan/Drag
const TOOL_BOX_SELECT = 'box_select'
const TOOL_BOX_ZOOM = 'box_zoom'
const TOOL_LASSO_SELECT = 'lasso_select'
const TOOL_PAN = 'pan'
const TOOL_XPAN = 'xpan'
const TOOL_YPAN = 'ypan'

// Scroll/Pinch Tools
const TOOL_WHEEL_ZOOM = 'wheel_zoom'
const TOOL_XHEEL_PAN = 'xwheel_pan'
const TOOL_XHEEL_ZOOM = 'xwheel_zoom'
const TOOL_YWHEEL_PAN = 'ywheel_pan'
const TOOL_YWHEEL_ZOOM = 'ywheel_zoom'


// create a data source to hold data
var source = new Bokeh.ColumnDataSource({
    data: { x: [], y: [] }
});

// make a plot with some tools
tool_list_str = setTools([TOOL_WHEEL_ZOOM, TOOL_XHEEL_PAN]);
var plot = Bokeh.Plotting.figure({
    title:'Example of Random data',
    tools: tool_list_str,
    height: 300,
    width: 300
});

// add a line with data from the source
plot.line({ field: "x" }, { field: "y" }, {
    source: source,
    line_width: 2
});

// show the plot, appending it to the end of the current section
Bokeh.Plotting.show(plot);

function addPoint() {
    // add data --- all fields must be the same length.
    source.data.x.push(Math.random())
    source.data.y.push(Math.random())

    // notify the DataSource of "in-place" changes
    source.change.emit()
}

var addDataButton = document.createElement("Button");
addDataButton.appendChild(document.createTextNode("Add Some Data!!!"));
document.currentScript.parentElement.appendChild(addDataButton);
addDataButton.addEventListener("click", addPoint);

addPoint();
addPoint();