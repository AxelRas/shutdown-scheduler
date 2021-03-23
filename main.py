from tkinter import *
import tkinter.ttk
import datetime as dt
import subprocess
from tkinter import messagebox
from PIL import ImageTk, Image

root= Tk()
root.title("Shutdown Scheduler v3")
root.geometry("390x300")
root.resizable(width=False, height=False)

subtitle= Label(root, text="Shutdown Scheduler")
subtitle.grid(row=0, column=0, pady=(5, 10), padx=(15, 0))

input_frame= LabelFrame(root)
input_frame.grid(row=1, column=0, padx=(15, 0), rowspan=2)


def set_delta():
    global delta_frame

    def set_time_delta():
        global response

        try:
            return_label.destroy()
        except:
            pass

        if hours.get() == '':
            hh= 0
        else:
            hh= int(hours.get())

        if minutes.get() == '':
            mm= 0
        else:
            mm= int(minutes.get())

        if seconds.get() == '':
            ss= 0
        else:
            ss= int(seconds.get())

        total_time= hh * 3600 + mm * 60 + ss

        if total_time == 0:
            try:
                response.destroy()
            except:
                pass

            response= Label(root, text="Delta needs to be\ngreater than 0.")
            response.grid(row=6, column=0, padx=(15, 0))

        else:
            try:
                response.destroy()
            except:
                pass

            if mm == 0 and ss == 0:
                response= Label(root, text="Shutdown scheduled in\n{}hs.".format(hh), fg="#06bf37")
                response.grid(row=6, column=0, padx=(15, 0))

            elif hh == 0 and mm == 0:
                response= Label(root, text="Shutdown scheduled in\n{}sec.".format(ss), fg="#06bf37")
                response.grid(row=6, column=0, padx=(15, 0))

            elif hh == 0 and ss == 0:
                response= Label(root, text="Shutdown scheduled in\n{}min.".format(mm), fg="#06bf37")
                response.grid(row=6, column=0, padx=(15, 0))

            elif hh == 0:
                response= Label(root, text="Shutdown scheduled in\n{}min and {}sec.".format(mm, ss), fg="#06bf37")
                response.grid(row=6, column=0, padx=(15, 0))

            elif mm == 0:
                response= Label(root, text="Shutdown scheduled in\n{}hs and {}sec.".format(hh, ss), fg="#06bf37")
                response.grid(row=6, column=0, padx=(15, 0))

            elif ss == 0:
                response= Label(root, text="Shutdown scheduled in\n{}hs and {}min.".format(hh, mm), fg="#06bf37")
                response.grid(row=6, column=0, padx=(15, 0))
            else:
                response= Label(root, text="Shutdown scheduled in\n{}hs {}min and {}sec.".format(hh, mm, ss), fg="#06bf37")
                response.grid(row=6, column=0, padx=(15, 0))

            command= "shutdown /s /t {}".format(str(total_time))
            subprocess.run(command)
            print(command)


    try:
        pending.destroy()
        specific_frame.grid_forget()
    except:
        pass

    delta_frame= LabelFrame(input_frame)
    delta_frame.grid(row=3, column=0, columnspan=3, pady=(5, 10))

    hours= Entry(delta_frame, width=2)
    hours.grid(row=4, column=0, padx=(5, 0), pady=(5, 5))

    hh_mm= Label(delta_frame, text=":").grid(row=4 , column=1, pady=(5, 5))

    minutes= Entry(delta_frame, width=2)
    minutes.grid(row=4, column=2, pady=(5, 5))

    mm_ss= Label(delta_frame, text=":").grid(row=4, column=3, pady=(5, 5))

    seconds= Entry(delta_frame, width=2)
    seconds.grid(row=4, column=4, pady=(5, 5), padx=(0, 5))

    set_button= Button(delta_frame, text="Set", command=set_time_delta, width=5)
    set_button.grid(row=5, column=0, columnspan=5, pady=(5, 10))


def set_specific():
    global specific_frame

    def set_time_specific():
        global response
        current_time = dt.datetime.now()
        try:
            response.destroy()
        except:
            pass

        if set_h.get() == '' or set_m.get() == '' or set_s.get() == '':
            response = Label(root, text="Specific time needs\nhs : min : sec format.")
            response.grid(row=6, column=0, padx=(15, 0))
        else:
            if len(str(set_h.get())) == 1:
                hh= "0" + str(set_h.get())
            else:
                hh= str(set_h.get())

            if len(str(set_m.get())) == 1:
                mm= "0" + str(set_m.get())
            else:
                mm= str(set_m.get())

            if len(str(set_s.get())) == 1:
                ss= "0" + str(set_s.get())
            else:
                ss= str(set_s.get())

            scheduled_time= dt.datetime.combine(dt.date.today(),
                                                 dt.time(int(set_h.get()), int(set_m.get()), int(set_s.get())))
            delta_obj= int(round((scheduled_time - current_time).total_seconds()))
            # print(delta_obj)

            if delta_obj < 0:
                scheduled_time= dt.datetime.combine(dt.date.today() + dt.timedelta(days=1),
                                                     dt.time(int(set_h.get()), int(set_m.get()), int(set_s.get())))
                delta_obj= int(round((scheduled_time - current_time).total_seconds()))

                try:
                    response.destroy()
                except:
                    pass

                response= Label(root, text="Shutdown scheduled for\ntomorrow at {}:{}:{}.".format(hh, mm, ss), fg="#06bf37")
                response.grid(row=6, column=0)

                command= "shutdown /s /t {}".format(delta_obj)
                print(command)

                subprocess.run("shutdown /a")
                subprocess.run(command)

            else:
                try:
                    response.destroy()
                except:
                    pass

                response= Label(root, text="Shutdown scheduled\nat {}:{}:{}.".format(hh, mm, ss), fg="#06bf37")
                response.grid(row=6, column=0)

                command= "shutdown /s /t {}".format(delta_obj)
                print(command)

                subprocess.run("shutdown /a")
                subprocess.run(command)


    try:
        pending.destroy()
        delta_frame.grid_forget()
    except:
        pass

    specific_frame= LabelFrame(input_frame)
    specific_frame.grid(row=3, column=0, columnspan=3, pady=(5, 10))

    h_list= []

    for i in range(24):
        h_list.append(i)

    set_h= IntVar()

    h_menu= tkinter.ttk.Combobox(specific_frame, textvariable=set_h, values=h_list, width=3)
    h_menu.grid(row=4, column=0, padx=(5, 1), pady=(5, 5))

    h_m= Label(specific_frame, text=":").grid(row=4, column=1)

    m_list= []

    for i in range(60):
        m_list.append(i)

    set_m= IntVar()

    m_menu= tkinter.ttk.Combobox(specific_frame, textvariable=set_m, values=m_list, width=3)
    m_menu.grid(row=4, column=2, padx=(1, 1), pady=(5, 5))

    m_s= Label(specific_frame, text=":").grid(row=4, column=3)

    s_list = []

    for i in range(60):
        s_list.append(i)

    set_s= IntVar()

    s_menu= tkinter.ttk.Combobox(specific_frame, textvariable=set_s, values=s_list, width=3)
    s_menu.grid(row=4, column=4, padx=(1, 5), pady=(5, 5))

    set_button = Button(specific_frame, text="Set", command=set_time_specific, width=5)
    set_button.grid(row=5, column=1, columnspan=3, pady=(5,10))


def cancel_shutdown():
    global return_label

    try:
        response.destroy()
        return_label.destroy()
    except:
        pass

    a= subprocess.run("shutdown /a")
    print(a)

    if a.returncode == 0:
        return_label= Label(cancel_frame, text="Shutdown cancelled.", fg="#06bf37", width=20)
        return_label.grid(row=2, column=1, padx=(5,0), pady=(0,5))

    else:
        return_label= Label(cancel_frame, text="No shutdown scheduled.")
        return_label.grid(row=2, column=1, padx=(5,0), pady=(0,5))


r= IntVar()

Radiobutton(input_frame, text="Delta", variable=r, value=1, command=set_delta).grid(row=2, column=0, padx=(15, 15), pady=(5, 5))
Radiobutton(input_frame, text="Specific", variable=r, value=2, command=set_specific).grid(row=2, column=1, padx=(15, 15), pady=(5, 5))

pending= Label(input_frame, text="Select \"Delta\" or \"Specific\"")
pending.grid(row=3, column=0, columnspan=2, pady=(5,10))

cancel_frame= LabelFrame(root)
cancel_frame.grid(row=1, column=1, padx=(10, 10), columnspan=4)

cancel_button= Button(cancel_frame, text="Cancel shutdown schedule", command=cancel_shutdown)
cancel_button.grid(row=1, column=1, padx=(5, 5), pady=(5, 5))

def help():
    messagebox.showinfo("Help", "When \"Delta\" is chosen, you need to input at least the amount of hours, minutes or seconds.\n\nWhen \"Specific\" is chosen, you just need to select a specific time from the determinated values.\n\nThe \"Cancel shutdown\" button cancels any scheduled shutdown, if there isn't one, it'll do nothing.")

help_button= Button(root, text="?", command=help, width=2)
help_button.grid(row=0, column=4, pady=(10,5))


root.mainloop()
