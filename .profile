# all variables
set t_Co=256
export HOME=/d/jiten/home/jitendra
export PATH=$PATH:/d/jiten/mongodb-win32-x86_64-2008plus-ssl-3.6.6/bin

# all aliases
alias python3='/usr/bin/python3'
alias python='winpty python2'

# commands for mongodb
alias mongoimport='winpty mongoimport'
alias mongo='winpty mongo'
alias mondod='winpty mongod'
alias startdb="mongod --dbpath /d/jiten/mongodb-win32-x86_64-2008plus-ssl-3.6.6/data/ --bind_ip 127.0.0.1"

# shorter commands
alias watchjsx='npx babel --watch jsxsrc/ --out-dir static/ --presets react-app/prod'
alias software_list="pacman -Qe | awk '{print $1}' > package_list.txt && pip list >> package_list.txt"

# python envs
alias workon_jobapp="cd /d/jiten/home/jitendra/projects/py2_proj1/ && pipenv shell"
alias workon_pandas="cd /d/jiten/home/jitendra/projects/newenv/ && pipenv shell"

#tmux do not lose your colors
alias tmux="TERM=screen-256color-bce tmux"
