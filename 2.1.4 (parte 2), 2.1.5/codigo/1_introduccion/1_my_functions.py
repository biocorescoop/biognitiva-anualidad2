                            # -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 13:14:13 2022

@author: migue
"""

# %% Preliminaries

# =============================================================================
# Import modules
# =============================================================================

import os
import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy import interpolate

# %% Directory change

def dir_change(directory):
    
    """
    
    Changes the current working directory and prints it.
    
    :param directory:  str, target directory to change to 
    
    :return: prints the current working directory
    
    """
    
    os.chdir(directory)
    work_dir = os.getcwd()
    
    return print('Current working directory is {}.'.format(work_dir))

#%% Plot parameters

def plot_parameters():
    
    """
    
    Sets plotting parameters.
    
    """

    # General style
    
    plt.style.use(['dark_background'])
    plt.rcParams['figure.figsize'] = [33, 22]
    plt.rcParams.update({'font.size': 32})
    
    # Use scientific notation on axes
    
    plt.rcParams['axes.formatter.limits'] = -3, 3 # sets range outside which notation is used
    plt.rcParams['axes.formatter.use_mathtext'] = True # use x10^n instead of 1en

# %% Data pre-processing

# =============================================================================
# Create array from text file
# =============================================================================

def create_array(filename, delimiter = None, skip_rows = 0, maxrows = None):
    
    """
    
    Creates a numpy array from a text file.
    
    :param filename: str, name of the text file 
    :param delimiter: str, default None, delimiter used to separate values
    :param skip_rows: int, default 0, number of rows to be skipped from start
    :param maxsrows: int, default None
    
    :return: creates variables with the header and content of the array
    
    """
    
    with open(filename) as file:
        
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames # generates a list with the headers
        
        array = np.genfromtxt(file, delimiter = delimiter, skip_header = skip_rows, max_rows = maxrows) # cambiar parámetros dependiendo de archivo

    return (fieldnames, array)

# =============================================================================
# Sort array by specified value
# =============================================================================

def sort_array(array_content, array_header, column_index):
    
    """
    
    Sorts the contents of the array by the specified column.
    
    :param array_content: numpy array, contents of the array
    :param array_header: list, header of the array
    :param column_index: str, element for which we want to sort the array
        
    :return: numpy array, sorted array by the specified element
    
    """
    
    sorted_array = array_content[array_content[:, array_header.index(column_index)].argsort()]
    
    return sorted_array

# =============================================================================
# Does the rest of the pre-processing using previous functions
# =============================================================================

def primes_preprocessing(filename, sorts = None):
    
    """
    
    Does all the necessary pre-processing for our data of primes.
    
    :param filename: str, name of the file to be processed
    :param sorts: str, what attribute to sort the data by, default None
    
    :return: creates a new header and its sorted content in variables
    
    """
    
    print('\n' + 'Pre-processing the data...')
    
    header, content = create_array(filename, delimiter = ',', skip_rows = 0)

    # =============================================================================
    # Clean up the header
    # =============================================================================
    
    new_header = []
    
    for attribute in header:
        
        if attribute.endswith(']'): # change only n, i, j, k
        
            attribute = attribute[0]
            
        attribute = attribute
        
        new_header.append(attribute)
        
        del attribute
    
    # =============================================================================
    # Sort by the required column, if required
    # =============================================================================
    
    if sorts != None:
    
        content = sort_array(content, new_header, sorts) # rewrite
  
        print('\n' + 'Data was sorted by {}.'.format(sorts))
        
    else:
        
        print('\n' + 'Data was not sorted.')   
    
    return new_header, content

# %% Create plots

def create_subplots(x, rows = 1, columns = 1, sharex = False, 
                    sharey = False, plot_type = 'plot', colour = 'firebrick', marker = '.'):
    
    """
    
    Creates subplots using matplotlib.
        
    :param x: name of the variable to be plotted on the x-axsis
    # :param y: name of the variable to be plotted on the y-axsis
    :param title: str, title for the plot
    :param xlabel: str, label for the x-axsis
    :param ylabel: str, label for the y-axsis
    # :param filename: str, name of the file under which the image will be saved
    :param colour: str, colour of our plot
    :param rows: int, number of rows to be plotted, default 1
    :param columns: int, number of columns to be plotted, default 1
    :param sharex: bool, whether the plots share the x-axis, default False
    :param sharey: bool, whether the plots share the y-axis, default False
    :param plot_type: str, type of the plot to be, default 'plot'
    :param linestyle: str, linestyle of the plot, default '-' (solid)
    :param marker: str, marker of the scatter, default 'o'
    
    """

    plt.style.use(['dark_background'])
    plt.rcParams['figure.figsize'] = [33, 22]
    plt.rcParams.update({'font.size': 42})

    fig, axs = plt.subplots(rows, columns, sharex = sharex, sharey = sharey)

# =============================================================================
#     Plot the data
# =============================================================================

    for i in range(rows):
        
        for j in range(columns):

            if plot_type == 'plot':
        
                axs[i, j].plot(x[j][i, :], marker, c = colour, markersize = 1)

            # elif plot_type == 'scatter':
        
                # axs[i, j].scatter(x, y, c = colours[colour], marker = marker)

# =============================================================================
#     Set labels
# =============================================================================
    
            # axs[i, j].set_title(title, pad = 35) # pad increases spacing between text and plot
            # axs[i, j].set_xlabel(xlabel, labelpad = 35)
            # axs[i, j].set_ylabel(ylabel, labelpad = 35)
    
# =============================================================================
#     Set axes
# =============================================================================
    
            # axs[i, j].tick_params(which = 'major', direction = 'in', length = 15, width = 5, pad = 35, top = True, right = True, grid_alpha = .3) # check documentation for all parameters!
            # axs[i, j].tick_params(which = 'minor', direction = 'in', length = 12.5, width = 2, top = True, right = True)

# =============================================================================
#     Last touches
# =============================================================================
    
            axs[i, j].margins(0) # make it so the plots have no margins and fit the box
            axs[i, j].grid(True, alpha = .3)

    # plt.savefig(filename)

# =============================================================================
# Create grid of 4 plots
# =============================================================================

def grid_4Plots(x, y, labels, colours, title, xlabel, ylabel, filename,
                marker = None, markersize = 1, plot_type = 'plot'):
    
    """
    
    Create a grid of 4 subplots using matplotlib.
    
    :param x: var, variable to plot on the x-axis
    :param y: var, variable to plot on the y-axis
    :param labels: list of strings to be used as labels for the plots
    :param colours: list of strings to be used as colours for the plots
    :param title: str, title of the grid
    :param xlabel: str, overarching label on the x-axis
    :param ylabel: str, overarching label on the y-axis
    :param filename: str, path and name of the file to which we save the plot
    :param marker: str or None, marker to use on the plot, default None
    :param markersize: int, size of the marker in pixels, default 1
    :param plot_type: str, defines what type of plot to use (scatter, plot...), default 'plot'
    
    """
    
    print('\n' + 'Plotting the data (4 subplots)...')
    
    # =============================================================================
    # Preliminaries for the figure
    # =============================================================================

    rows, cols = 2, 2 # number of rows and columns

    fig = plt.figure()
    gs = fig.add_gridspec(rows, cols, hspace = 0, wspace = 0) # no space between plots

    (ax1, ax2), (ax3, ax4) = gs.subplots() # change depending on rows and cols
    axes = [ax1, ax2, ax3, ax4] # change depending on number of plots

    # =============================================================================
    # And plot
    # =============================================================================

    for ax in range(len(axes)):
        
        if plot_type == 'plot':
        
            axes[ax].plot(x[ax], y[ax], marker = marker, label = labels[ax], 
                          c = colours[ax])
        
        elif plot_type == 'scatter':
            
            axes[ax].scatter(x, y[ax], marker = marker, s = markersize,  
                             label = labels[ax], c = colours[ax])

        elif plot_type == 'bar':
            
            axes[ax].bar(x, y[ax], label = labels[ax],
                         color = colours[ax])
        
    # =============================================================================
    # Labels and axes
    # =============================================================================

        # axes[ax].set_title('{}'.format(elements[ax]), pad = 35) # pad increases spacing between text and plot
        # axes[ax].set_xlabel('Valor', labelpad = 35)
        # axes[ax].set_ylabel('Frecuencia', labelpad = 35)
        
        axes[ax].tick_params(which = 'major', direction = 'in', length = 15, 
                             width = 5, pad = 35, top = True, right = True, 
                             grid_alpha = .3,  labelsize = 26) # check documentation for all parameters!
       
        axes[ax].tick_params(which = 'minor', direction = 'in', length = 12.5, 
                             width = 2, top = True, right = True)        
        
    # =============================================================================
    # ...y ajustamos posiciones y últimos parámetros.
    # =============================================================================

        # axes[ax].margins(0) # make it so the plots have no margins and fit the box
        axes[ax].grid(True)
        axes[ax].legend()
        # axes[ax].set_xticklabels([])
        # axes[ax].set_yticklabels([])

    axes[0].tick_params(bottom = False, right = False, labeltop = True,
                        labelbottom = False, labelsize = 26)

    axes[1].tick_params(bottom = False, left = False, labeltop = True, 
                        labelbottom = False, labelleft = False, labelright = True, 
                        labelsize = 26)

    axes[2].tick_params(top = False, right = False, labelsize = 26)

    axes[3].tick_params(top = False, left = False, labeltop = False,
                        labelbottom = True, labelleft = False, labelright = True,
                        labelsize = 26)

    fig.suptitle(title)
    fig.supxlabel(xlabel) # estas dos líneas ponen etiquetas generalizadas a todos los subplots
    fig.supylabel(ylabel) # Frecuencia absoluta de cuántas veces aparece cada valor en la tabla

    fig.tight_layout() # sirve para ajustar bien los gráficos

    plt.savefig(filename)

    print('\n' + 'Data was plotted.')    

# =============================================================================
# Create grid of 16 plots
# =============================================================================

def grid_16Plots(x, y, labels, colours, title, xlabel, ylabel, filename,
                marker = None, markersize = 1, plot_type = 'plot'):
    
    """
    
    Create a grid of 16 subplots using matplotlib.
    
    :param x: var, variable to plot on the x-axis
    :param y: var, variable to plot on the y-axis
    :param labels: list of strings to be used as labels for the plots
    :param colours: list of strings to be used as colours for the plots
    :param title: str, title of the grid
    :param xlabel: str, overarching label on the x-axis
    :param ylabel: str, overarching label on the y-axis
    :param filename: str, path and name of the file to which we save the plot
    :param marker: str or None, marker to use on the plot, default None
    :param markersize: int, size of the marker in pixels, default 1
    :param plot_type: str, defines what type of plot to use (scatter, plot...), default 'plot'
    
    """

    print('\n' + 'Plotting the data (16 plots)...')
    
    # =============================================================================
    # Preliminaries for the figure
    # =============================================================================

    rows, cols = 4, 4 # number of rows and columns

    fig = plt.figure()
    gs = fig.add_gridspec(rows, cols, hspace = 0, wspace = 0) # no space between plots

    (ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8), (ax9, ax10, ax11, ax12), (ax13, ax14, ax15, ax16),  = gs.subplots() # change depending on rows and cols
    axes = [ax1, ax2, ax3, ax4,
            ax5, ax6, ax7, ax8,
            ax9, ax10, ax11, ax12, 
            ax13, ax14, ax15, ax16] # change depending on number of plots

    # =============================================================================
    # And plot
    # =============================================================================

    for ax in range(len(axes)):
        
        if plot_type == 'plot':
        
            axes[ax].plot(x, y[ax], marker = marker, label = labels[ax], 
                          c = colours[ax])
        
        elif plot_type == 'scatter':
            
            axes[ax].scatter(x, y[ax], marker = marker, s = markersize,  
                             label = labels[ax], c = colours[ax])

        elif plot_type == 'bar':
            
            axes[ax].bar(x, y[ax], label = labels[ax],
                         color = colours[ax])
        
    # =============================================================================
    # Labels and axes
    # =============================================================================

        # axes[ax].set_title('{}'.format(elements[ax]), pad = 35) # pad increases spacing between text and plot
        # axes[ax].set_xlabel('Valor', labelpad = 35)
        # axes[ax].set_ylabel('Frecuencia', labelpad = 35)
                
        
        axes[ax].tick_params(which = 'major', direction = 'in', length = 10, 
                             width = 3, pad = 35, top = True, right = True, 
                             grid_alpha = .3,  labelsize = 26) # check documentation for all parameters!
       
        axes[ax].tick_params(which = 'minor', direction = 'in', length = 12.5, 
                             width = 2, top = True, right = True)        
        
    # =============================================================================
    # ...y ajustamos posiciones y últimos parámetros.
    # =============================================================================

        # axes[ax].margins(0) # make it so the plots have no margins and fit the box
        axes[ax].grid(True)
        axes[ax].legend()
        axes[ax].set_xticklabels([])
        axes[ax].set_yticklabels([])

# =============================================================================
# Set titles, last labels...
# =============================================================================

    fig.suptitle(title)
    fig.supxlabel(xlabel) # estas dos líneas ponen etiquetas generalizadas a todos los subplots
    fig.supylabel(ylabel) # Frecuencia absoluta de cuántas veces aparece cada valor en la tabla

    fig.tight_layout() # sirve para ajustar bien los gráficos

    plt.savefig(filename)
    
    print('\n' + 'Data was plotted.')


# =============================================================================
# Create grid of 3 plots
# =============================================================================

def grid_3Plots(x, y, labels, colours, title, xlabel, ylabel, filename,
                marker = None, markersize = 1, plot_type = 'plot'):
    
    """
    
    Create a grid of 4 subplots using matplotlib.
    
    :param x: var, variable to plot on the x-axis
    :param y: var, variable to plot on the y-axis
    :param labels: list of strings to be used as labels for the plots
    :param colours: list of strings to be used as colours for the plots
    :param title: str, title of the grid
    :param xlabel: str, overarching label on the x-axis
    :param ylabel: str, overarching label on the y-axis
    :param filename: str, path and name of the file to which we save the plot
    :param marker: str or None, marker to use on the plot, default None
    :param markersize: int, size of the marker in pixels, default 1
    :param plot_type: str, defines what type of plot to use (scatter, plot...), default 'plot'
    
    """
    
    print('\n' + 'Plotting the data (3 subplots)...')
    
    # =============================================================================
    # Preliminaries for the figure
    # =============================================================================

    rows, cols = 3, 1 # number of rows and columns

    fig = plt.figure()
    gs = fig.add_gridspec(rows, cols, hspace = 0, wspace = 0) # no space between plots

    (ax1, ax2, ax3) = gs.subplots() # change depending on rows and cols
    axes = [ax1, ax2, ax3] # change depending on number of plots

    # =============================================================================
    # And plot
    # =============================================================================

    for ax in range(len(axes)):
        
        if plot_type == 'plot':
        
            axes[ax].plot(x, y[ax], marker = marker, label = labels[ax], 
                          c = colours[ax])
        
        elif plot_type == 'scatter':
            
            axes[ax].scatter(x, y[ax], marker = marker, s = markersize,  
                             label = labels[ax], c = colours[ax])

        elif plot_type == 'bar':
            
            axes[ax].bar(x, y[ax], label = labels[ax],
                         color = colours[ax])
        
    # =============================================================================
    # Labels
    # =============================================================================

        # axes[ax].set_title('{}'.format(elements[ax]), pad = 35) # pad increases spacing between text and plot
        # axes[ax].set_xlabel('Valor', labelpad = 35)
        # axes[ax].set_ylabel('Frecuencia', labelpad = 35)
        
        axes[ax].tick_params(which = 'major', direction = 'in', length = 15, 
                             width = 5, pad = 35, top = True, right = True, 
                             grid_alpha = .3,  labelsize = 26) # check documentation for all parameters!
       
        axes[ax].tick_params(which = 'minor', direction = 'in', length = 12.5, 
                             width = 2, top = True, right = True)        
        
    # =============================================================================
    # ...y ajustamos posiciones y últimos parámetros.
    # =============================================================================

        # axes[ax].margins(0) # make it so the plots have no margins and fit the box
        axes[ax].grid(True)
        axes[ax].legend()
        # axes[ax].set_xticklabels([])
        # axes[ax].set_yticklabels([])


    axes[0].tick_params(
                        
                        labelbottom = False,
                        labeltop = True, 
                        labelleft = True,
                        labelright = True,
                        labelsize = 26
                        
                        )

    axes[1].tick_params(
                        
                        labelbottom = False,
                        labeltop = False, 
                        labelleft = True,
                        labelright = True,
                        labelsize = 26
                        
                        )
    
    axes[2].tick_params(
                        
                        labelbottom = True,
                        labeltop = False, 
                        labelleft = True,
                        labelright = True,
                        labelsize = 26
                        
                        )
    

    fig.suptitle(title)
    fig.supxlabel(xlabel) # estas dos líneas ponen etiquetas generalizadas a todos los subplots
    fig.supylabel(ylabel) # Frecuencia absoluta de cuántas veces aparece cada valor en la tabla

    fig.tight_layout() # sirve para ajustar bien los gráficos

    plt.savefig(filename)

    print('\n' + 'Data was plotted.')    

# %% Count the frequency of values

def count_frequency(list):
    
    """
    
    Counts the number of times an element appears within a given list.
    
    :param list: list of elements to be counted
    
    :return: creates variable with the number of counts
    
    """
    
    # Create empty dictionary
    
    count = {}
    
    # And fill it up
    
    for i in list:
        
        count[i] = count.get(i, 0) + 1
        
    return count

#%% Interpolation

# =============================================================================
# Cubic Spline Interpolation
# =============================================================================

def cubic_spline_interpolation(x, y, fs, bc_type = 'not-a-knot'):
    
    """
    
    Perform a cubic spline interpolation. Needs 'interpolate' package from scipy.
    
    :param x: list or arr, independent variable
    :param y: list or arr, dependent variable
    :param fs: int, new sampling rate for the independent variable after interpolation
    :param bc_type: str, boundary condition type, default is 'not-a-knot' (can also try 'clamped')
    
    :return: dict, gives the new independent variable and the interpolated series
    
    """
        
    # =============================================================================
    # Calculate the cubic spline polynomials    
    # =============================================================================

    cubic_spline = interpolate.CubicSpline(x, y, bc_type = bc_type) # the bc type tells me what happens at boundaries

    # =============================================================================
    # And interpolate    
    # =============================================================================

    new_x = np.arange(0, len(x), fs) # add time steps
    
    interpolated_series = cubic_spline(new_x) # use the new x axis with more time steps to perform the spline

    
    return {'new_x': new_x, 'interpolated_series': interpolated_series}


#%% Fast Fourier Transform (FFT)

# =============================================================================
# Perform the FFT
# =============================================================================

def fastFourierTransform(series, attribute):
    
    """
    
    Calculates the Fast Fourier Transform (FFT) of the chosen attribute and the power spectral density (PSD)
    
    :param series: list or arr, series on which we perform the transform
    :param attribute: str, attribute to use

    :return: dict, gives the frequency axis, the transform and the power spectrum of the series

    """    
        
    # =============================================================================2
    # Define the parameters to use    
    # =============================================================================
            
    n = len(series) # length of the series on which to perform the fft 
    
    # L = np.arange(0, np.floor(n / 2), dtype = 'int') # only plot first half
    
    freq = (((1 / n) * np.arange(n))) # Creates an x-axis of all frequencies for the plot
            
    # =============================================================================
    # Perform the FFT    
    # =============================================================================
            
    yhat = (np.fft.fft(series, n)) # Compute the transform
    
    PSD = (yhat * np.conj(yhat) / n) # power spectrum - complex * its conj. gives magnitude squared
    
    return {'freq': freq, 'yhat': yhat, 'PSD': PSD}

# =============================================================================
# Inverse FFT
# =============================================================================

def cleanSignal(yhat, PSD, peak_indices):
    
    """
    
    Performs the inverse transformation of the FFT and gives us the resulting signal to plot after setting a threshold,
    effectively cleaning our original signal.
    
    :param yhat: list or arr, the FFT to invert
    :param PSD: list or arr, the Power Spectral Density from which we filter the signal
    :param peak_indices: int, indices for the desired peaks above which we set the treshold
    
    :return: dict, gives back the filtered PSD and the clean signal
    
    """
        
    # =============================================================================
    # Use threshold to clean the signal
    # =============================================================================
                
    PSD_clean = PSD * peak_indices # zeroes out all indices with smaller Fourier coefficients, keeps only with power greater than specified
    
    yhat_clean = peak_indices * 2 * yhat
    
    ffilt = np.fft.ifft(yhat_clean) # Inverse FFT for filtered time signal
    
    
    return {'PSD_clean': PSD_clean, 'ffilt': ffilt}
