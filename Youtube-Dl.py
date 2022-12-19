from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from tkinter.messagebox import showinfo , showerror
import threading
from pytube import YouTube

def searchResolution():
    
    video_link = url_entry.get()
    
    if video_link == '':
        showerror(title='Error', message='Provide the video link please!')
     
    else:
        try:
            
            video = YouTube(video_link)
            
            resolutions = []
        
            for i in video.streams.filter(file_extension='mp4'):
                
                resolutions.append(i.resolution)
            
            video_resolution['values'] = resolutions
            
            showinfo(title='Search Complete', message='Check the Combobox for the available video resolutions')
    
        except:
            
            showerror(title='Error', message='An error occurred while searching for video resolutions!\n'\
                'Below might be the causes\n->Unstable internet connection\n->Invalid link')

def searchThread():
    t1 = threading.Thread(target=searchResolution)
    t1.start()
    
def download_video():
    
    try:
        
        video_link = url_entry.get()
    
        resolution = video_resolution.get()
    
        if resolution == '' and video_link == '':
            
            showerror(title='Error', message='Please enter both the video URL and resolution!!')
        
        elif resolution == '':
        
            showerror(title='Error', message='Please select a video resolution!!')
        
        elif resolution == 'None':
        
            showerror(title='Error', message='None is an invalid video resolution!!\n'\
                    'Please select a valid video resolution')    
        #
        else:
        
            try:
            
                def on_progress(stream, chunk, bytes_remaining):
                    
                    total_size = stream.filesize
                    
                    def get_formatted_size(total_size, factor=1024, suffix='B'):
                        
                        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
                            if total_size < factor:
                                return f"{total_size:.2f}{unit}{suffix}"
                            total_size /= factor
                        
                        return f"{total_size:.2f}Y{suffix}"
                    
                    formatted_size = get_formatted_size(total_size)
                    
                    bytes_downloaded = total_size - bytes_remaining
                    
                    percentage_completed = round(bytes_downloaded / total_size * 100)
                
                    progress_bar['value'] = percentage_completed
                
                    progress_label.config(text=str(percentage_completed) + '%, File size:' + formatted_size)
                    
                    window.update()
        
                video = YouTube(video_link, on_progress_callback=on_progress)
            
                video.streams.filter(res=resolution).first().download()
            
                showinfo(title='Download Complete', message='Video has been downloaded successfully.')
    
                progress_label.config(text='')
                progress_bar['value'] = 0
            
            except:
                showerror(title='Download Error', message='Failed to download video for this resolution')
                
                progress_label.config(text='')
                progress_bar['value'] = 0
    
    except:
        
        showerror(title='Download Error', message='An error occurred while trying to ' \
                    'download the video\nThe following could ' \
                    'be the causes:\n->Invalid link\n->No internet connection\n'\
                     'Make sure you have stable internet connection and the video link is valid')

        progress_label.config(text='')
        progress_bar['value'] = 0
        

def downloadThread():
    t2 = threading.Thread(target=download_video)
    t2.start()
    
window = Tk()

info_img  = PhotoImage(file= 'photo/info.png')
window.iconphoto(False , info_img)

window.title('YouTube Video  Downloader')
window.geometry('500x460+430+180')
window.resizable(height=False, width=False)
canvas = Canvas(window , width=500 , height=400)
canvas.pack()

logo = PhotoImage(file= "photo/logo.png")
logo = logo.subsample(1 , 1)
canvas.create_image(250 , 80, image=logo)

label_style = ttk.Style()
label_style.configure('TEntry' , font=('Dotum' , 15))

button_style = ttk.Style()
button_style.configure('TButton' , foreground = '#000000' , font='DotumChe')

url_lable = ttk.Label(window , text= 'Enter Video URL:' , style= 'TLabel')
url_entry = ttk.Entry(window , width=76 , style= 'TEntry')

canvas.create_window(114 , 200 , window=url_lable)
canvas.create_window(250 , 230 , window=url_entry)

resolution_label = Label(window , text='Resolution:')
canvas.create_window(50 , 260 , window=resolution_label)
video_resolution = ttk.Combobox(window , width=10)
canvas.create_window(60 , 280, window=video_resolution)

search_resolution = ttk.Button(window , text='Search Resolution' , command=searchThread)
canvas.create_window(85 , 315 , window=search_resolution)

progress_label = Label(window , text='')
canvas.create_window(240,360 , window=progress_label)
progress_bar = ttk.Progressbar(window, orient=HORIZONTAL , length=450 , mode='determinate')
canvas.create_window(250 , 380 , window=progress_bar)

download_button = ttk.Button(window , text='Downlaod Video' , style='TButton' , command=downloadThread)
canvas.create_window(240, 410, window=download_button)

window.mainloop()


