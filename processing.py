import PictureBuilder.PictureBuilder as PB
import matplotlib.pylab as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.widgets import RectangleSelector
from skimage.feature import peak_local_max
from skimage import data, img_as_float
from scipy import ndimage as ndi

x_corner=0
y_corner=0
x_width= 1920
y_height= 1200

def onselect(eclick, erelease):
    "eclick and erelease are matplotlib events at press and release."
    print('startposition: (%f, %f)' % (eclick.xdata, eclick.ydata))
    print('endposition  : (%f, %f)' % (erelease.xdata, erelease.ydata))
    print('used button  : ', eclick.button)

def toggle_selector(event):
    print('Key pressed.')
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        print('RectangleSelector deactivated.')
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        print('RectangleSelector activated.')
        toggle_selector.RS.set_active(True)

def do_processing_plot(self, mode):
    def default():
        print("Fine")

    def draw_rectangle():
        global x_corner, x_width, y_corner, y_height
        rect = patches.Rectangle((x_corner,y_corner),x_width,y_height,linewidth=1,edgecolor='r',facecolor='none')
        PB.plot.add_patch(rect)

    def save_cropped_image():
        global x_corner, x_width, y_corner, y_height
        freq_array=PB.get_freq(rounded=0)
        subarray=PB.array[y_corner:y_corner+y_height,x_corner:x_corner+x_width]
        mean_subarray= subarray.mean(axis=0)
        print (PB.global_basename[:PB.global_basename.find("_")], mean_subarray.max(), freq_array[mean_subarray.argmax()+x_corner])
        #plt.imsave(address_of_save_fig+'/'+global_basename.replace('dat','jpg'),  subarray)
        plt.imsave(PB.address_of_save_fig+'/'+PB.global_basename.replace('dat','png'),  PB.array)

        ###Вывод среза в файл
        f= open(PB.address_of_save_fig+'/'+PB.global_basename.replace('dat','txt'), "a")
        #np.savetxt(f, mean_subarray, fmt='%1.4f')
        f.close()

    def draw_a_rectangle_with_a_mouse():
        toggle_selector.RS = RectangleSelector(PB.plot, onselect, drawtype='line')

    def set_parameters():
        global x_corner, x_width, y_corner, y_height
        def set_single_par(X, name_of_X):
            print (name_of_X, '= ', X)
            buffer=input()
            if (buffer):
                X= int(buffer)
            return X

        x_corner= set_single_par(x_corner, 'x_corner')
        y_corner= set_single_par(y_corner, 'y_corner')
        x_width= set_single_par(x_width, 'x_width')
        y_height= set_single_par(y_height, 'y_height')

    def finding_local_maxima():
        im = PB.array[y_corner:y_corner+y_height,x_corner:x_corner+x_width]
        # image_max is the dilation of im with a 20*20 structuring element
        # It is used within peak_local_max function
        image_max = ndi.maximum_filter(im, size=20, mode='constant')

        # Comparison between image_max and im to find the coordinates of local maxima
        coordinates = peak_local_max(im, min_distance=20)

        # display results
        fig, axes = plt.subplots(3, 1, sharex=True, sharey=True)
        ax = axes.ravel()

        ax[0].imshow(im, cmap=plt.cm.gray)
        ax[0].axis('off')
        ax[0].set_title('Original')

        ax[1].imshow(image_max, cmap=plt.cm.gray)
        ax[1].axis('off')
        ax[1].set_title('Maximum filter')

        ax[2].imshow(im, cmap=plt.cm.gray)
        ax[2].autoscale(False)
        ax[2].plot(coordinates[:, 1], coordinates[:, 0], 'r.')
        ax[2].axis('off')
        ax[2].set_title('Peak local max')

        fig.tight_layout()
        plt.show()


    functions = {
                    'prob': draw_a_rectangle_with_a_mouse,
                    'draw': draw_rectangle,
                    'set_par': set_parameters,
                    'save_crop': save_cropped_image,
                    'find_max': finding_local_maxima,
                    'default': default
                }
    selected_function = functions.get(mode)
    if (selected_function):
        selected_function()
    else:
        print ("You can call function using argument: ", functions)