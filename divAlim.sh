#!/bin/bash
launch_dir=$(realpath .)
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd $script_dir

if [ $# == 0 ];then
    # display program help
    cat help
else
    if [ $1 == "-f" ] || [ $1 == "-u" ]; then
        echo -e "## check pipenv installation"
        if which pipenv >/dev/null; then
            :
        else
            echo -e "## installing pipenv"
            sudo apt-get install -y pipenv
        fi

        echo -e "## check venv installation"

        if [ -d $HOME/.local/share/virtualenvs/diversite-phylogenetique-de-l-assiette-au--QHx-bX7s ]; then
            echo -e "## virtual environment already exist"
        else
            echo -e "## installing venv from requirements.txt"
            pipenv install -r requirements.txt
            echo -e "## diversite-phylogenetique-de-l-assiette-au--QHx-bX7s venv installed"
        fi

        if [ $# == 2 ]; then

            if [ $1 == "-f" ]; then
                # take as entry a txt file

                cd $launch_dir
                if [ -e $(realpath $2) ]; then
                    # test if the file exist
                    cd $script_dir
                else
                    echo "err: $2 doesn't exist or it is an invalid file"
                fi

                echo -e "## Launching subshell in virtual environment..."
                pipenv run python cli/divAlim.py -f $2 $launch_dir $script_dir

            cd $script_dir
            elif [ $1 == "-u" ]; then
                # take as entry a URL
                echo -e "## Launching subshell in virtual environment..."
                pipenv run python cli/divAlim.py -u $2 $launch_dir $script_dir
            fi
        else
            echo -e "err: invalid file or URL"
        fi
    
    elif [ $1 == "--help" ]; then
        cat help
    else
        echo -e "err: unrecognized command \'$1\'"
    fi
fi