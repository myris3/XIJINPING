#!/bin/bash
echo Starting transfer
sudo rm /var/www/html/*
sudo cp ./HTML/* /var/www/html/
echo transfer done
