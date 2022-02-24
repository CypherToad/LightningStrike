#!/bin/bash

if [[ "$ENABLE_TOR" == "true" ]] ; then
  echo "Starting Tor"
  service tor start

  echo "Start Tor Hidden Service"
  python utils/tor.py
fi

echo "Starting Flask"
TOKEN=$TOKEN python app.py
