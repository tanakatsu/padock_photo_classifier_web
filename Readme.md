## padock\_photo\_classifier\_web

### What's this?

This service takes horse's padock photos and tells their distance aptitude (sprint / mile / middle / long).

#### Implemented API

- GET /predict.json	 
	- required params
		- url or data (base64 encoded)
- POST /predict.json
	- required params
		- file
			
- POST /netkeiba/search.json 
	- required params
		- name: horse name
		 	
#### API test page

- /upload


#### Run on local

```
$ python main.py
```

Navigate to http://127.0.0.1:5000/