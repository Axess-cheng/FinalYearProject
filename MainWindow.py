import tkinter as tk;
import tkinter.messagebox as tkMB;
from tkinter.filedialog import askopenfilenames;
import processingPart1 as p1;

# Main Window
window = tk.Tk();
window.title('my window');
window.geometry('500x400');

# Labels
label1 = tk.Label(window, text='WOW! here\'s TKInter! ', bg='blue', font=('Arial', 12), width=15, height=2);
label1.pack();


# Buttons
def hit_me():
    open_file_path = tk.filedialog.askopenfilename(title = 'Choose the files',filetypes = [("images", "*.png")]);
    # TODO: delete the comma and show image when open multiple images
    print(open_file_path);
    p1.readImage(open_file_path);

btn1 = tk.Button(window, text='input', width=15, height=2, command=hit_me)
btn1.pack()

window.mainloop();