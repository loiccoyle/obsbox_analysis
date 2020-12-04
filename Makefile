upload_metadata:
	cp metadata/*.h5 /eos/home-l/lcoyle/obsbox_metadata/

venv:
	python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

.PHONY: upload_metadata venv
