# greetings.py
#
# ICS 32 Spring 2017
# Code Example
#
# An implementation of the Greetings application, which demonstrates how to
# create and use modal dialog boxes in Tkinter applications.  There are two
# classes here:
#
# * GreetingsApplication, which is an application class in the same basic
#   form that we've been writing them all along.
# * NameDialog, which is a class that represents the modal dialog box that
#   asks the user to specify a first and last name.

import tkinter


# Since we use the same font in a few places, we'll specify a default here
# as a global constant and use the constant everywhere else.  We used a
# much larger font in lecture, so it could easily be read when projected
# in a large room; notice that all I needed to change was this one line
# when I wanted the posted code example to have a smaller font.
DEFAULT_FONT = ('Helvetica', 14)



# The NameDialog class allows us to create objects that represent a modal
# dialog box that asks the user "Who do you want to greet?" and allows them
# to fill in a first and last name.  After the user fills these values in
# and presses either OK or Cancel, we can ask the object which button was
# used to dismiss the dialog (because "OK" and "Cancel" ultimately mean
# different things) and what values were in the two Entry widgets in which
# the user could enter a first and last name.

class NameDialog:
    def __init__(self):
        # A Toplevel object is, to a dialog box, akin to the Tk object
        # of an application.  It's the window.  The difference is that
        # it's not the root window of an entire application; it's a
        # separate, additional window.
        self._dialog_window = tkinter.Toplevel()


        # We'll create and lay out widgets inside the Toplevel object,
        # using all of the same techniques we've used previously when
        # creating and laying out widgets in an application's root window.

        who_label = tkinter.Label(
            master = self._dialog_window, text = 'Who do you want to greet?',
            font = DEFAULT_FONT)

        who_label.grid(
            row = 0, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W)

        first_name_label = tkinter.Label(
            master = self._dialog_window, text = 'First Name:',
            font = DEFAULT_FONT)

        first_name_label.grid(
            row = 1, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._first_name_entry = tkinter.Entry(
            master = self._dialog_window, width = 20, font = DEFAULT_FONT)

        self._first_name_entry.grid(
            row = 1, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)

        last_name_label = tkinter.Label(
            master = self._dialog_window, text = 'Last Name:',
            font = DEFAULT_FONT)

        last_name_label.grid(
            row = 2, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._last_name_entry = tkinter.Entry(
            master = self._dialog_window, width = 20, font = DEFAULT_FONT)

        self._last_name_entry.grid(
            row = 2, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)

        button_frame = tkinter.Frame(master = self._dialog_window)

        button_frame.grid(
            row = 3, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.E + tkinter.S)

        ok_button = tkinter.Button(
            master = button_frame, text = 'OK', font = DEFAULT_FONT,
            command = self._on_ok_button)

        ok_button.grid(row = 0, column = 0, padx = 10, pady = 10)

        cancel_button = tkinter.Button(
            master = button_frame, text = 'Cancel', font = DEFAULT_FONT,
            command = self._on_cancel_button)

        cancel_button.grid(row = 0, column = 1, padx = 10, pady = 10)

        self._dialog_window.rowconfigure(3, weight = 1)
        self._dialog_window.columnconfigure(1, weight = 1)


        # Finally, we'll initialize some attributes that will carry information
        # about the outcome of this dialog box (i.e., whether the user clicked
        # "OK" to dismiss it, and what first and last name the user specified).

        self._ok_clicked = False
        self._first_name = ''
        self._last_name = ''


    def show(self) -> None:
        # This is how we turn control over to our dialog box and make that
        # dialog box modal.
        self._dialog_window.grab_set()
        self._dialog_window.wait_window()


    # The next three methods allow us to ask our dialog box, after it's
    # been dismissed, what happened.  (It's too late to ask the Entry
    # widgets themselves by then, because the window will already have
    # been destroyed.)

    def was_ok_clicked(self) -> bool:
        return self._ok_clicked


    def get_first_name(self) -> str:
        return self._first_name


    def get_last_name(self) -> str:
        return self._last_name


    # Finally, we attached command handlers to our two buttons; these are
    # the command handler methods we attached.  Note that they both call
    # a destroy() method on the Toplevel object, which is how we make the
    # window go away.  But _on_ok_button also explicitly sets that the
    # OK button was clicked and extracts the first and last name that the
    # user entered (by calling the get() method on the two Entry widgets),
    # so that afterward we can determine what happened.	

    def _on_ok_button(self) -> None:
        self._ok_clicked = True
        self._first_name = self._first_name_entry.get()
        self._last_name = self._last_name_entry.get()

        self._dialog_window.destroy()


    def _on_cancel_button(self) -> None:
        self._dialog_window.destroy()



# The GreetingsApplication class is a fairly straightforward Tkinter
# application, in the same style as the ones we've written previously.
# The only interesting thing going on here that we haven't seen before
# is the use of something called a "control variable", which allows us
# to associate a widget with a value that we expect to change; changing
# the value of the control variable has an immediate impact on the way
# the widget looks (and, in the case of widgets whose state can be changed,
# like Checkbuttons and Spinboxes, vice versa).  In our case, we use a
# tkinter.StringVar (a control variable whose value is a string) to
# represent the text in a Label widget, so that any change to the value
# of the StringVar will automatically and correspondingly make the Label's
# text change.  (This is an example of a general technique called "data
# binding".)

class GreetingsApplication:
    def __init__(self):
        self._root_window = tkinter.Tk()

        greet_button = tkinter.Button(
            master = self._root_window, text = 'Greet', font = DEFAULT_FONT,
            command = self._on_greet)

        greet_button.grid(
            row = 0, column = 0, padx = 10, pady = 10,
            sticky = tkinter.S)


        # A StringVar is a "control variable" that contains a string.  We
        # get its value by calling a get() method on it; we change its value
        # by calling a set() method on it.  We'll associate it with a Label
        # widget, in which case any subsequent change to the StringVar's
        # value will automatically cause the Label to be redrawn with its
        # new text.
        self._greeting_text = tkinter.StringVar()
        self._greeting_text.set('No greeting yet!')

        # Notice that we didn't set the Label's "text" option.  Instead,
        # we set its "textvariable" option and passed it a control variable
        # (in this case, a StringVar).  This is how we ask the Label to
        # automatically redraw itself when the StringVar changes; the
        # "textvariable" option implies that the text is, indeed,
        # variable (i.e., that we expect it to change, and that we want
        # the Label to handle that change for us automatically).
        greeting_label = tkinter.Label(
            master = self._root_window, textvariable = self._greeting_text,
            font = DEFAULT_FONT)

        greeting_label.grid(
            row = 1, column = 0, padx = 10, pady = 10,
            sticky = tkinter.N)

        self._root_window.rowconfigure(0, weight = 1)
        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)


    def start(self) -> None:
        self._root_window.mainloop()


    def _on_greet(self) -> None:
        # When the user clicks the Greet! button, we pop up a NameDialog.
        # Since we've already encapsulate all of that in the NameDialog
        # class, all we need to do is create a NameDialog object, ask it
        # to show itself, and then ask it afterward what happened.
        #
        # Note that the call to show() isn't going to return until the user
        # has dismissed the dialog box.
        dialog = NameDialog()
        dialog.show()

        # After the dialog box is dismissed, we'll check if it was the OK
        # or the Cancel button that got clicked.  If OK was clicked, we'll
        # change the greeting label's text by setting its control variable.
        if dialog.was_ok_clicked():
            first_name = dialog.get_first_name()
            last_name = dialog.get_last_name()
            self._greeting_text.set('Hello, {} {}!'.format(first_name, last_name))



if __name__ == '__main__':
    GreetingsApplication().start()
