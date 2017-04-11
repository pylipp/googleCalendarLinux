# googleCalendarLinux
A python script that enables users to manage Google Calendar directly from the Linux terminal!

Create a virtualenv

    mkvirtualenv --python=$(which python3) gcalendar

and activate it 

    workon gcalendar 

To install the package including dependencies, run the following command in terminal:

	pip install -r requirements.txt -e .

Execute the main script by typing

	gcalendar

## Gotchas

### Using ZSH

zsh has a feature called `AUTO_CD` that interfers with the execution of the above command. To solve this, put `unsetopt AUTO_CD` in your `.zshrc` ([stackexchange](http://unix.stackexchange.com/questions/126719/how-to-disable-auto-cd-in-zsh-with-oh-my-zsh)). 
