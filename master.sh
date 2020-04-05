# TODO: Parameterize logs folder name

# Time between checking processes
SLEEP_TIME=1

# Make the logs directory if it doesn't exist
mkdir logs

while [ true ]
do
    # Run the broker
	if [[ !($(pgrep mosquitto)) ]]; then
        echo 'mosquitto dead, restarting' >> logs/master.log
		mosquitto -d -c mosquitto.conf
	fi

    # Run the webapp backend
	if [[ !($(pgrep flask)) ]]; then
        echo 'backend dead, restarting' >> logs/master.log
		cd ../ecp-webapp/flask-backend
		source my_venv/bin/activate
		FLASK_APP=api.py FLASK_ENV=development flask run &>> backend.log &
		cd ../../interaction-layer
	fi

    # Run the webapp frontend
	if [[ !($(pgrep npm)) ]]; then
        echo 'frontend dead, restarting' >> logs/master.log
		cd ../ecp-webapp/ecp-frontend
		npm start &>> frontend.log &
		cd ../../interaction-layer
	fi

	sleep SLEEP_TIME
done