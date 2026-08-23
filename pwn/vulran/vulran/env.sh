#!/bin/sh

alias vulran_build="docker build -t vulran ."
alias vulran_run="docker run -d -p 6767:6767 vulran"
alias vulran_conn="nc localhost 6767:6767"
alias vulran_kill="docker kill $(docker ps -q)"
