import control as ctrl
import numpy as np
from manim import *

def CreateBodeMagnitudeDiagram(w, dB, scale = 1, **kwargs):
    x_len = 6
    y_len = 3

    # Default axis configuration
    axis_config = {
        "include_numbers": True,
        "include_tip": False,
        "stroke_width": 2.5,
        "font_size": 20}
    
    # Update axis_config with any additional keyword arguments
    axis_config.update(kwargs)

    # Create Axes object with given parameters
    axes = Axes(
        x_range = w,
        y_range = dB,
        x_length = x_len,
        y_length = y_len,
        axis_config = axis_config,
        x_axis_config = {"scaling": LogBase(custom_labels=True),
                         "label_direction": 0.5 * RIGHT + 0.2 * DOWN})
    
    # Get and position the x-axis label
    xlabel = axes.get_x_axis_label(r"\omega\ [rad/s]", edge = DR, buff = 0).scale(0.50).shift(1.6*LEFT + 0.5*DOWN)

    # Get and position the y-axis label
    ylabel = axes.get_y_axis_label(r"\text{Mag}\ [dB]", edge = UR, buff = 0).scale(0.50).shift(1.0*LEFT)

    # Create the group of objects
    magnitudediagram = VGroup(axes, xlabel, ylabel)
    magnitudediagram.scale(scale)

    # Return the Axes object and the x-axis and y-axis labels
    return magnitudediagram

def CreateNyquistDiagram(Re, Im, scale = 1, **kwargs):
    x_len = 5
    y_len = 5

    # Default axis configuration
    axis_config = {
        "include_numbers": True,
        "include_tip": False,
        "stroke_width": 2.5,
        "font_size": 20}

    # Create Axes object with given parameters
    axes = Axes(
        x_range = Re,
        y_range = Im,
        x_length = x_len,
        y_length = y_len,
        axis_config = axis_config)
    
    # Get and position the x-axis label
    xlabel = axes.get_x_axis_label(r"Re", edge = DR, buff = 0).scale(0.50)

    # Get and position the y-axis label
    ylabel = axes.get_y_axis_label(r"Im", edge = UR, buff = 0).scale(0.50)

    # Create the group of objects
    nyquistdiagram = VGroup(axes, xlabel, ylabel)
    nyquistdiagram.scale(scale)

    # Return the Axes object and the x-axis and y-axis labels
    return nyquistdiagram

def ObtainNyquistPlots(nyquistdiagram = None, freqrespdata = None, **kwargs):
    line_color = kwargs.get("line_color", ORANGE)
    add_vertex_dots = kwargs.get("add_vertex_dots", False)
    stroke_width = kwargs.get("stroke_width", 2)

    nyquistline = None

    if (nyquistdiagram != None) and (freqrespdata != None):
        nyquistline = nyquistdiagram[0].plot_line_graph(
            x_values = freqrespdata["real"],
            y_values = freqrespdata["imag"],
            line_color = line_color,
            add_vertex_dots = add_vertex_dots,
            stroke_width = stroke_width)

    return nyquistline

def CreateBodePhaseDiagram(w, phase, scale = 1, magnitudediagram = None, **kwargs):
    # Set default x_len and y_len values if not provided in kwargs
    x_len = 6
    y_len = 3

    # Default axis configuration
    axis_config = {
        "include_numbers": True,
        "include_tip": False,
        "stroke_width": 2.5,
        "font_size": 20}
    
    # Update axis_config with any additional keyword arguments
    axis_config.update(kwargs)

    # Create Axes object with given parameters
    axes = Axes(
        x_range = w,
        y_range = phase,
        x_length = x_len,
        y_length = y_len,
        axis_config = axis_config,
        x_axis_config = {"scaling": LogBase(custom_labels=True),
                         "label_direction": 0.5 * RIGHT + 0.2 * DOWN})
    
    # Get and position the x-axis label
    xlabel = axes.get_x_axis_label(r"\omega\ [rad/s]", edge = DR, buff = 0).scale(0.50).shift(1.6*LEFT + 0.5*DOWN)

    # Get and position the y-axis label
    ylabel = axes.get_y_axis_label(r"\angle \ [^{o}]", edge = UR, buff = 0).scale(0.50).shift(1.0*LEFT)

    # Create the group of objects
    phasediagram = VGroup(axes, xlabel, ylabel)
    phasediagram.scale(scale)

    # Align magnitude and phase plots
    if magnitudediagram != None:
        phasediagram.next_to(magnitudediagram, DOWN, 0.4*scale)
        offset = phasediagram.get_edge_center(RIGHT)[0] - magnitudediagram.get_edge_center(RIGHT)[0]
        phasediagram.shift(-offset)

    # Return the Axes object and the x-axis and y-axis labels
    return phasediagram

def ObtainFrequencyResponse(sys, wlimits = [0.01, 1000], wnum = 100):
    log_vector = np.linspace(np.log10(wlimits[0]), np.log10(wlimits[1]), wnum)
    mag, phase, w = ctrl.freqresp(sys, np.power(10, log_vector))

    freqrespdata = {
        "w_rad": w,
        "w_Hz": w/(2*np.pi),
        "mag_abs": mag,
        "mag_dB": 20*np.log10(mag),
        "phase_rad": phase,
        "phase_deg": 180*phase/np.pi,
        "real": mag*np.cos(phase),
        "imag": mag*np.sin(phase)}

    return freqrespdata

def ObtainBodePlots(magnitudediagram = None, phasediagram = None, freqrespdata = None, **kwargs):
    line_color = kwargs.get("line_color", ORANGE)
    add_vertex_dots = kwargs.get("add_vertex_dots", False)
    stroke_width = kwargs.get("stroke_width", 2)

    magnitudeline = None
    phaseline = None

    if (magnitudediagram != None) and (freqrespdata != None):
        magnitudeline = magnitudediagram[0].plot_line_graph(
            x_values = freqrespdata["w_rad"],
            y_values = freqrespdata["mag_dB"],
            line_color = line_color,
            add_vertex_dots = add_vertex_dots,
            stroke_width = stroke_width)

    if (phasediagram != None) and (freqrespdata != None):
        phaseline = phasediagram[0].plot_line_graph(
            x_values = freqrespdata["w_rad"],
            y_values = freqrespdata["phase_deg"],
            line_color = line_color,
            add_vertex_dots = add_vertex_dots,
            stroke_width = stroke_width)

    return magnitudeline, phaseline

def StepResponsePlot(sys, timediagram, color, Tf = 10, Dt = 0.1):
    [time, output] = ctrl.step_response(sys, np.arange(0, Tf, Dt))
    plot = timediagram.plot_line_graph(x_values = time, y_values = output, line_color = color, add_vertex_dots = False)
    return plot

def GainMargin(sys, magnitudediagram = None, phasediagram = None, **kwargs):
    gm, pm, sm, wpc, wgc, wms = ctrl.stability_margins(sys)
    gmline = VMobject()
    pmline = VMobject()
    gmdashed = VMobject()
    pmdashed = VMobject()
    if (magnitudediagram != None):
        gmline = magnitudediagram[0].plot_line_graph(
            x_values = [wpc, wpc],
            y_values = [-20*np.log10(gm), 0],
            line_color = YELLOW,
            add_vertex_dots = False)
    if (phasediagram != None):
        pmline = phasediagram[0].plot_line_graph(
            x_values = [wgc, wgc],
            y_values = [-180+pm, -180],
            line_color = YELLOW,
            add_vertex_dots = False)
    if ((magnitudediagram != None) and (phasediagram != None)):
        gmdashed = DashedLine(start = phasediagram[0].coords_to_point(wpc, 0), end = magnitudediagram[0].coords_to_point(wpc, 0), buff = 0, dash_length = 0.05)
        pmdashed = DashedLine(start = magnitudediagram[0].coords_to_point(wgc, 0), end = phasediagram[0].coords_to_point(wgc, -180), buff = 0, dash_length = 0.05)
    return gmline, pmline, gmdashed, pmdashed
