import tkinter
import tkinter.filedialog
from tkinter import *
from tkinter import ttk, Tk
from tkinter.font import Font
import moviepy.editor as mpy
import random

currentQueue = {"output_directory": "", "files": []}


def createInterface():
    main: Tk = Tk()
    main.geometry("843x843")
    main.resizable(False, False)
    main.title("Batcher")
    main.iconbitmap("Batcher.ico")
    source_Font = Font(
        family="System",
        size=8,
    )
    small_sourceFont = Font(
        family="System",
        size=2
    )
    ttk_Style = ttk.Style()
    ttk_Style.configure('TNotebook.Tab', font=source_Font)

    notebook = ttk.Notebook(main)
    notebook.pack()

    gif_Frame = Frame(notebook, width=777, height=777, bg="#262626")
    thumbnail_Frame = Frame(notebook, width=777, height=777, bg="#262626")

    input_files_text = Text(gif_Frame, width=30, height=45, background="#f5f5f5", font=small_sourceFont, wrap="none")
    output_files_text = Text(gif_Frame, width=30, height=45, background="#f5f5f5", font=small_sourceFont, wrap="none")

    input_files_text.insert(END, "______________________________\nInputs\n______________________________\n")
    output_files_text.insert(END, "______________________________\nOutputs\n______________________________\n")

    def browseFiles():
        # rowNumber = 1
        input_files_text.config(state="normal")
        fileList = []
        gif_Frame.filename = tkinter.filedialog.askopenfilenames(initialdir="I:/", title="Select files")
        for x in range(len(gif_Frame.filename)):
            currentQueue["files"].append(gif_Frame.filename[x])
            splitString = gif_Frame.filename[x].split("/")
            fileList.append(splitString[-1])
        for file in fileList:
            input_files_text.insert(END, str(file) + "\n")
        input_files_text.config(state="disabled")

    def browseFilesThumbnail():
        print("This browses!")

    def clearBrowse():
        if input_files_text.get(4.0) != "":
            input_files_text.config(state="normal")
            output_files_text.config(state="normal")
            input_files_text.delete(1.0, END)
            input_files_text.insert(END, "______________________________\nInputs\n______________________________\n")
            output_files_text.delete(1.0, END)
            output_files_text.insert(END, "______________________________\nOutputs\n______________________________\n")
            currentQueue["output_directory"] = ""
            currentQueue["files"] = []
            input_files_text.config(state="disabled")
            output_files_text.config(state="disabled")

    def convertGIFFiles():
        for files in currentQueue["files"]:
            output = []
            currentVideo = mpy.VideoFileClip(files)
            randomTime = random.randint(0, int(currentVideo.duration))
            if (randomTime - 15) < 0:
                randomTime = 0
            elif randomTime + 15 > int(currentVideo.duration):
                randomTime = 0
            output.append(currentVideo.subclip(randomTime, (randomTime + 15)))
            final_clip = mpy.CompositeVideoClip(output)
            splitFiles = str(files).split("/")
            fileName = str(currentQueue["output_directory"] + "/" + splitFiles[-1].replace(".mp4", ".gif"))
            final_clip.write_gif(fileName, fps=23.976)
            output_files_text.config(state="normal")
            output_files_text.insert(END, fileName + "\n")
            output_files_text.config(state="disabled")

    def outputLocation():
        output_files_text.config(state="normal")
        output_location = tkinter.filedialog.askdirectory()
        currentQueue["output_directory"] = output_location
        splitString = output_location.split("/")
        output_files_text.insert(END, splitString[-1] + "\n")
        output_files_text.insert(END, "______________________________\n")
        output_files_text.config(state="disabled")

    browseButton = Button(gif_Frame, text="Browse", command=browseFiles, font=source_Font, width=6)
    clearButton = Button(gif_Frame, text="Clear", command=clearBrowse, font=source_Font, width=6)
    convertButton = Button(gif_Frame, text="Convert", command=convertGIFFiles, font=source_Font, width=6)
    outputFolderButton = Button(gif_Frame, text="Output", command=outputLocation, font=source_Font, width=6)

    browseButtonThumbnail = Button(thumbnail_Frame, text="Browse", command=browseFilesThumbnail, font=source_Font, width=6)

    gif_Frame.grid(row=0, column=0)
    thumbnail_Frame.grid(row=0, column=0)
    browseButton.grid(row=0, column=0, sticky="w")
    browseButtonThumbnail.grid(row=0, column=0, sticky="w")
    clearButton.grid(row=1, column=1, sticky="nw")
    convertButton.grid(row=1, column=0, sticky="nw")
    outputFolderButton.grid(row=0, column=1, sticky="w")
    input_files_text.grid(row=1, column=2, padx=30)
    output_files_text.grid(row=1, column=3, padx=30)
    notebook.add(gif_Frame, text="Gif")
    notebook.add(thumbnail_Frame, text="Thumbnail")

    input_files_text.config(state="disabled")
    output_files_text.config(state="disabled")

    main.mainloop()


createInterface()
